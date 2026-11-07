"""ConceptLens: a local-model assessment prototype."""
from __future__ import annotations

import csv
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import streamlit as st
from evaluator import evaluate_answer

ROOT = Path(__file__).parent
DB_PATH = ROOT / "conceptlens.db"
QUESTIONS_PATH = ROOT / "questions2.csv"

TYPE_LABELS = {
    "recall": "Recall",
    "explain": "Explanation",
    "transfer": "Apply in a new situation",
}


def load_questions() -> dict[str, dict[str, dict[str, str]]]:
    """Load question prompts and rubrics from questions2.csv."""
    if not QUESTIONS_PATH.exists():
        raise FileNotFoundError("questions2.csv must be beside app.py")

    grouped: dict[str, dict[str, dict[str, str]]] = {}
    required_columns = {
        "concept",
        "question_type",
        "prompt",
        "maximum_score",
        "criteria",
        "reference_answer",
        "feedback_guidance",
    }

    with QUESTIONS_PATH.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames or not required_columns.issubset(reader.fieldnames):
            raise ValueError(
                "questions2.csv must include these columns: "
                + ", ".join(sorted(required_columns))
            )

        for row in reader:
            concept_name = row["concept"].strip()
            question_type = row["question_type"].strip().lower()

            if question_type not in TYPE_LABELS:
                raise ValueError(f"Unknown question_type: {question_type}")
            if not concept_name or not row["prompt"].strip():
                raise ValueError("Every row needs a concept and prompt.")

            try:
                maximum_score = int(row["maximum_score"])
            except ValueError as error:
                raise ValueError(
                    f"Invalid maximum_score for {concept_name}/{question_type}"
                ) from error

            if maximum_score < 1:
                raise ValueError("maximum_score must be at least 1.")

            grouped.setdefault(concept_name, {})[question_type] = row

    required_types = set(TYPE_LABELS)
    for concept_name, questions in grouped.items():
        if set(questions) != required_types:
            raise ValueError(
                f"{concept_name} must have one recall, explain, and transfer question."
            )

    if not grouped:
        raise ValueError("questions2.csv contains no questions.")

    return grouped


def init_db() -> None:
    """Create the local assessment history table if it does not exist."""
    with sqlite3.connect(DB_PATH) as db:
        db.execute(
            """CREATE TABLE IF NOT EXISTS assessments (
                id INTEGER PRIMARY KEY,
                created_at TEXT NOT NULL,
                concept TEXT NOT NULL,
                answers_json TEXT NOT NULL,
                scores_json TEXT NOT NULL,
                total INTEGER NOT NULL
            )"""
        )


def main() -> None:
    st.set_page_config(
        page_title="ConceptLens",
        page_icon="🔎",
        layout="centered",
    )
    init_db()

    try:
        concepts = load_questions()
    except (FileNotFoundError, KeyError, ValueError) as error:
        st.error(f"Question data problem: {error}")
        st.stop()

    st.markdown("### HACKCARTEL · LEARNING PROTOTYPE")
    st.title("ConceptLens")
    st.caption("Understanding beyond memorization")
    st.write(
        "Choose a Python concept, then show what you remember, "
        "how you explain it, and how you apply it in a new situation."
    )
    st.info(
        "Answers are evaluated by Gemini. Scores are estimates "
        "of the evidence in each response, not proof of a learner's understanding.",
        icon="ℹ️",
    )

    concept_name = st.selectbox("Choose a concept", list(concepts))
    concept = concepts[concept_name]

    with st.expander("View the rubric and reference answers"):
        for question_type in ("recall", "explain", "transfer"):
            question = concept[question_type]
            st.markdown(
                f"**{TYPE_LABELS[question_type]} · "
                f"up to {question['maximum_score']} points**"
            )
            st.write(f"Rubric: {question['criteria']}")
            st.caption(question["feedback_guidance"])
            st.write(f"Reference answer: {question['reference_answer']}")

    with st.form("assessment"):
        answers: dict[str, str] = {}

        for number, question_type in enumerate(
            ("recall", "explain", "transfer"),
            start=1,
        ):
            st.subheader(f"{number} · {TYPE_LABELS[question_type]}")
            answers[question_type] = st.text_area(
                concept[question_type]["prompt"],
                key=f"{question_type}_{concept_name}",
                height=100 if question_type != "transfer" else 130,
            )

        submitted = st.form_submit_button(
            "Review my answers",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        results: dict[str, dict] = {}

        with st.spinner("Reviewing your answers with Gemini..."):
            try:
                for question_type, answer in answers.items():
                    results[question_type] = evaluate_answer(
                        question=concept[question_type],
                        answer=answer,
                        question_type=question_type,
                    )
            except Exception as error:
                st.error(
                    "Could not evaluate the answers. Check your Gemini API key, "
                    "internet connection, model access, and API usage limits."
                )
                st.code(str(error))
                st.stop()

        total = sum(
            result["total_score"] for result in results.values()
        )
        maximum_total = sum(
            int(concept[question_type]["maximum_score"])
            for question_type in answers
        )

        with sqlite3.connect(DB_PATH) as db:
            db.execute(
                """INSERT INTO assessments
                (created_at, concept, answers_json, scores_json, total)
                VALUES (?, ?, ?, ?, ?)""",
                (
                    datetime.now(timezone.utc).isoformat(),
                    concept_name,
                    json.dumps(answers, ensure_ascii=False),
                    json.dumps(
                        {
                            question_type: result["total_score"]
                            for question_type, result in results.items()
                        }
                    ),
                    total,
                ),
            )

        st.divider()
        st.header("Your learning snapshot")
        st.metric("Rubric score", f"{total} / {maximum_total}")

        if any(
            result["needs_human_review"] for result in results.values()
        ):
            st.warning(
                "The model marked one or more answers for human review. "
                "Check the rubric evidence and reference answers."
            )

        all_gaps: list[str] = []

        for question_type, answer in answers.items():
            result = results[question_type]
            maximum = int(concept[question_type]["maximum_score"])

            st.subheader(
                f"{TYPE_LABELS[question_type]} · "
                f"{result['total_score']}/{maximum}"
            )
            st.markdown(f"> {answer.strip() or 'No response provided.'}")

            for criterion in result["criteria_results"]:
                st.markdown(
                    f"**{criterion['score']}/{criterion['maximum_score']} · "
                    f"{criterion['criterion']}**"
                )
                st.caption(f"Evidence: {criterion['evidence']}")
                if criterion["feedback"]:
                    st.write(criterion["feedback"])

            st.write(result["overall_feedback"])

            for gap in result["conceptual_gaps"]:
                if gap not in all_gaps:
                    all_gaps.append(gap)

            with st.expander(
                f"Reference answer · {TYPE_LABELS[question_type]}"
            ):
                st.write(concept[question_type]["reference_answer"])

        st.subheader("Possible conceptual gaps")
        if all_gaps:
            for gap in all_gaps:
                st.write(f"- {gap}")
        else:
            st.write(
                "The model did not identify a specific conceptual gap. "
                "Review the criterion evidence above."
            )

        st.caption(
            "Answers are evaluated by AI. Scores are estimates and should be reviewed."
        )

    st.divider()
    st.caption(
        "ConceptLens · Research prototype · Estimates observable answer evidence"
    )


if __name__ == "__main__":
    main()

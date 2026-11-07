<div align="center">

# ConceptLens
### Understanding Beyond Memorization

**HackCartel · Education · Group 1 · 5 Members**

*Research ambition. Focused prototype. Evidence-based learning.*

</div>

---

## Overview

ConceptLens is a HackCartel education research prototype that explores the difference between recalling an answer and applying a concept. It uses varied questions and evidence-based feedback to help students and teachers identify conceptual gaps.

**Status:** Working research prototype. The app provides topic selection, three question types, Gemini-assisted rubric evaluation, evidence-linked feedback, possible conceptual gaps, and local SQLite history.

## Problem statement

> Develop an assessment system that estimates whether a student understands a concept and can apply it in unfamiliar situations, rather than merely recalling answers.

Selected research challenge: **Measuring Understanding Beyond Memorization**.

## Initial prototype scope

Focus on **one subject and three concepts**. Start with Python fundamentals: variables and data types, conditionals, and loops. The team can agree on a different subject before implementation.

| Planned capability | Scope |
| --- | --- |
| Topic selection | Choose one of three concepts in a single subject. |
| Three question types | Assess direct recall, explanation in the learner's own words, and application to an unfamiliar example. |
| Rubric-based evaluation | Evaluate correctness, reasoning, and application separately using a defined rubric. |
| Evidence-linked feedback | Connect each assessment to the learner's answer and the expected reasoning. |
| Concept report | Summarize demonstrated strengths, possible misconceptions, and a suggested next exercise. |

## User workflow

Select a concept → Answer varied questions → Evaluate against a rubric → Review evidence and gaps → Practice again

## Five-member ownership

Replace the member labels with names and GitHub handles once responsibilities are assigned. Each owner should document interfaces needed by the other members.

| Owner | Responsibility | Initial deliverable |
| --- | --- | --- |
| Member 1 | Frontend and experience | Topic selection, question screens, and feedback views. |
| Member 2 | Backend and APIs | Assessment sessions, answer submission, and report endpoints. |
| Member 3 | Question and rubric design | Three concepts, reference answers, scoring criteria, and transfer questions. |
| Member 4 | Evaluation logic | Gemini-assisted rubric scoring, evidence extraction, and uncertainty flagging. |
| Member 5 | Integration and quality | End-to-end checks, sample responses, documentation, and demonstration. |

## Current technical implementation

- **UI:** Streamlit for the first working demonstration.
- **Logic:** Python modules with clear inputs and outputs.
- **Data:** SQLite for prototype persistence; JSON or CSV for authored sample records.
- **Evaluation:** Gemini API through the Google GenAI Python SDK with structured JSON output. Scores are estimates and should be reviewed against independently scored examples.
- **Optional later architecture:** React frontend and FastAPI backend if the team needs separate services.

## Run locally

Requires Python 3.10 or newer, a Gemini API key, and internet access.

```bash
python3 -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```

Create `.streamlit/secrets.toml` locally (this file is ignored by Git) and add:

```toml
GEMINI_API_KEY = "your-key-here"
```

Never commit API keys or real student data. Gemini API usage is subject to the account's current limits and billing terms.

## Data plan

Store concept definitions, question type, reference rubric, submitted response, criterion scores, and supporting feedback. Start with fictional learner profiles and authored sample answers.

Use synthetic or consented data. Do not commit real student identities, private records, API keys, or credentials.

## Demonstration target

Show two sample learners with the same recall score but different explanation and application responses. Demonstrate how the report reflects the difference, while allowing uncertain cases to be reviewed.

## Evaluation and limitations

Compare system assessments with independently scored reference responses. Inspect agreement with the rubric, unsupported feedback, and sensitivity to paraphrasing. Do not use fluent writing as a substitute for conceptual correctness.

The system estimates understanding from observable responses; it cannot prove a learner's internal understanding. Language proficiency, accessibility needs, and test anxiety can affect answers. Uncertain assessments should be marked for review.

## Initial milestones

- [ ] Assign five owners and agree on the three concepts.
- [ ] Define the data schema and interfaces.
- [ ] Prepare sample records and expected outcomes.
- [ ] Implement the core workflow and persistence.
- [ ] Connect the interface to the core logic.
- [ ] Review outputs against expected outcomes.
- [ ] Record a short demo and document remaining limitations.

## Repository contents

| File | Purpose |
| --- | --- |
| `README.md` | Project brief, scope, responsibilities, and milestones |
| `CONTRIBUTING.md` | Branching, review, and contribution conventions |
| `GITHUB_SETUP.md` | Windows PowerShell instructions for the first upload |
| `.gitignore` | Excludes credentials, local environments, and generated files |

`app.py` is the Streamlit interface and local SQLite workflow. `evaluator.py` calls Gemini. `questions2.csv` contains questions, scoring criteria, reference answers, and feedback guidance. `sample_responses.csv` contains synthetic examples for evaluation checks; it is not real student data.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md), choose a scoped task, and open a pull request describing the change and how it was checked. Coordinate shared interfaces before implementation.

## About HackCartel

HackCartel is a community building products around problem statements and real-world problems. Members share ownership across research, development, testing, and documentation.

## License

No license has been selected yet. Add a `LICENSE` file after the repository owners agree on reuse terms.

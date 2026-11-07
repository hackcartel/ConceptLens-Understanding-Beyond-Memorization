# Contributing

1. Agree on task ownership with the group. Use an issue to state the expected outcome.
2. Update your local `main`, then create a branch such as `feat/quiz-flow`, `fix/profile-update`, or `docs/setup`.
3. Keep changes focused. Document inputs and outputs before changing shared interfaces.
4. Check the affected workflow using representative sample data. Record what was checked and any limitations.
5. Open a pull request into `main` with a short summary, checks performed, and screenshots when useful.
6. Ask another group member to review before merging. Never commit secrets or private student data.

## Suggested commands after cloning

```bash
git switch main
git pull --ff-only
git switch -c feat/your-task
# Make and check your changes.
git add .
git commit -m "feat: describe your change"
git push -u origin feat/your-task
```

Create the pull request on GitHub after pushing. Keep incomplete features clearly marked and update the README when setup or behavior changes.

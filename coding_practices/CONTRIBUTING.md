# Team Coding Practices & Git Workflow
### CSCB 3308 — Team 2 | Spring 2026

This document defines the shared standards every team member follows when contributing to this project.

---

## Essential Rules

These are the non-negotiables.

> **1. Always pull before you start working.**
> **2. Never commit directly to `main`.**
> **3. Never push broken code.**

---

## Git Workflow

Follow this exact sequence every time you go to push to GitHub:

```
1. git checkout main
2. git pull
3. git checkout -b "your-branch"
4. work in your environment
5. git add .
6. git commit -m "Explanation of what has been changed and added"
7. git push origin "your-branch"
8. Open a Pull Request at https://github.com/PeytonCunningham720/3308-TEAM-2-SPRING-2026-PROJECT
    request a review
```

---

## Commit Message Standards

Every commit message follows this format:

```
type: short description
```

### Types

| Type | When to use |
|------|-------------|
| `feat` | Adding new functionality |
| `fix` | Fixing a bug |
| `refactor` | Restructuring code without changing behavior |
| `test` | Adding or updating tests |
| `docs` | Updating documentation or comments |
| `chore` | Dependency updates, file moves, cleanup |
| `wip` | Work in progress — not ready for review yet |

### Examples

```bash
git commit -m "feat: add cross-correlation scoring to similarity ranker"
git commit -m "fix: handle mismatched spectrogram shapes before comparison"
git commit -m "test: add unit tests for normalize_spectrogram edge cases"
git commit -m "docs: update README with integration instructions"
git commit -m "refactor: extract scoring logic into separate helper functions"
```
---

## Branching

Branch names follow the same convention as commits:

```
type/short-description
```

```bash
git checkout -b feat/similarity-ranking-model
git checkout -b fix/spectrogram-shape-mismatch
git checkout -b test/librosa-conversion-tests
git checkout -b docs/update-contributing-guide
```

---

## Repository Structure

```
3308-TEAM-2-SPRING-2026-PROJECT/
├── data/                  audio datasets (Jake)
├── spectrogram/           librosa + matplotlib modules (Brie)
├── similarity_model/      scoring and ranking (Peyton)
├── ui/                    input/output interface (Stephen)
├── coding_practices/      this document and team standards
└── README.md              project overview
```

- Each person works in their assigned folder. Don't modify another team member's files.
- Test files live in the same folder as the code they test, named `test_<module_name>.py`

---

## Standup Protocol

At each standup, every team member answers three questions:

1. **What did I complete since last standup?**
2. **What am I working on next?**
3. **Is there anything blocking me?**

Standups are 5-10 minutes.

---
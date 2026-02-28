# Team Coding Practices & Git Workflow
### CSCI 3308 — Team 2 | Spring 2026

This document defines the shared standards every team member follows when contributing to this project. Consistency here keeps merge conflicts minimal and the codebase readable for everyone.

---

## Table of Contents
1. [The Golden Rules](#the-golden-rules)
2. [Git Workflow](#git-workflow)
3. [Commit Message Standards](#commit-message-standards)
4. [Branching](#branching)
5. [Pull Requests](#pull-requests)
6. [Code Style](#code-style)
7. [File & Folder Conventions](#file--folder-conventions)
8. [Standup Protocol](#standup-protocol)

---

## The Golden Rules

These are non-negotiable. Everything else is guidance — these are rules.

> **1. Always pull before you start working.**
> **2. Never commit directly to `main`.**
> **3. Never push broken code.**
> **4. If you're stuck for more than 30 minutes, ask for help.**

---

## Git Workflow

Follow this exact sequence every time you go to push to GitHub:

```
1. git checkout main
2. git pull
3. git checkout -b your-branch
4. ... do your work ...
5. git add .
6. git commit -m "Explanation of what has been changed and added"
7. git push origin your-branch
8. Open a Pull Request at https://github.com/PeytonCunningham720/3308-TEAM-2-SPRING-2026-PROJECT → request a review
```

**Why pull first?** If you start working on stale code and someone else pushed changes, you'll have conflicts when you try to merge. Pulling first keeps your local copy current and saves everyone headaches.

---

## Commit Message Standards

Every commit message follows this format:

```
type: short description in present tense (50 chars max)
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
# Good
git commit -m "feat: add cross-correlation scoring to similarity ranker"
git commit -m "fix: handle mismatched spectrogram shapes before comparison"
git commit -m "test: add unit tests for normalize_spectrogram edge cases"
git commit -m "docs: update README with integration instructions"
git commit -m "refactor: extract scoring logic into separate helper functions"

# Bad — don't do these
git commit -m "stuff"
git commit -m "fixed it"
git commit -m "asdfgh"
git commit -m "WIP"
git commit -m "changes"
```

The goal is that anyone reading the commit history can understand what changed and why without opening the diff.

---

## Branching

Branch names follow the same convention as commits:

```
type/short-description
```

```bash
# Good
git checkout -b feat/similarity-ranking-model
git checkout -b fix/spectrogram-shape-mismatch
git checkout -b test/librosa-conversion-tests
git checkout -b docs/update-contributing-guide

# Bad
git checkout -b peyton-branch
git checkout -b newstuff
git checkout -b branch1
```

One branch per feature or fix. Don't pile multiple unrelated changes onto one branch — it makes pull requests much harder to review.

---

## Pull Requests

- **Never merge your own PR.** At least one other teammate must review and approve it first.
- Keep PRs small and focused. A PR that changes 10 files is hard to review. A PR that changes 2 is easy.
- Write a short description in the PR body explaining *what* changed and *why*.
- If your PR is not ready for review yet, prefix the title with `[WIP]` or open it as a Draft PR.
- Resolve all reviewer comments before merging.

### PR Description Template

```
## What does this do?
Brief description of the change.

## Why?
Context or motivation — what problem does this solve?

## How to test it?
Steps a reviewer can take to verify the change works.

## Notes
Anything else reviewers should know (edge cases, open questions, etc.)
```

---

## Code Style

We use Python. Follow these standards:

**Formatting**
- Indent with 4 spaces (no tabs)
- Max line length: 100 characters
- Two blank lines between top-level functions and classes
- One blank line between methods inside a class

**Naming**
- Variables and functions: `snake_case`
- Constants: `ALL_CAPS`
- Classes: `PascalCase`
- Files: `snake_case.py`

**Documentation**
- Every function needs a docstring explaining what it does, its parameters, and what it returns
- Use inline comments to explain *why*, not *what* — the code should speak for itself on what it's doing
- Don't leave commented-out dead code in commits

**Example of a well-documented function:**

```python
def normalize_spectrogram(spec: np.ndarray) -> np.ndarray:
    """
    Normalize a spectrogram array to [0, 1] range.

    Without normalization, louder recordings score higher regardless
    of call similarity, which breaks the comparison algorithm.

    Args:
        spec: 2D numpy array (frequency bins x time frames)

    Returns:
        Normalized 2D numpy array
    """
    min_val = spec.min()
    max_val = spec.max()

    if max_val == min_val:
        return np.zeros_like(spec, dtype=float)  # handle flat/silent input

    return (spec - min_val) / (max_val - min_val)
```

---

## File & Folder Conventions

```
3308-TEAM-2-SPRING-2026-PROJECT/
├── data/                  ← audio datasets (Jake)
├── spectrogram/           ← librosa + matplotlib modules (Brie)
├── similarity_model/      ← scoring and ranking (Peyton)
├── ui/                    ← input/output interface (Stephen)
├── coding_practices/      ← this document and team standards
└── README.md              ← project overview
```

- Each person works in their assigned folder. Don't modify another team member's files without talking to them first.
- Test files live in the same folder as the code they test, named `test_<module_name>.py`
- No files named `final`, `final2`, `new`, `fixed`, or anything ambiguous. Use Git for version history — that's what it's for.

---

## Standup Protocol

At each standup, every team member answers three questions:

1. **What did I complete since last standup?**
2. **What am I working on next?**
3. **Is there anything blocking me?**

Keep it brief — standups are 5-10 minutes max. Longer conversations get taken offline.

If a task turns out to be harder than estimated: **say so at standup, ask for help**. Don't silently fall behind.
If a task turns out to be easier than estimated: **say so at standup, offer to help**. Don't sit idle.

---

*Last updated: Sprint 1 — Questions or changes? Bring it up at standup or open a PR against this file.*

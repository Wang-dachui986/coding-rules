# Contributing

Thanks for helping improve `coding-rules`. This repository is a Codex skill:
governance instructions, blank templates, and a validator. It does not contain
a sample application.

By participating you agree to the [Code of Conduct](CODE_OF_CONDUCT.md).

## What belongs here

- Behavior changes belong in [`coding-rules/SKILL.md`](coding-rules/SKILL.md), [`coding-rules/references/`](coding-rules/references/), and the templates under [`coding-rules/assets/project-governance/`](coding-rules/assets/project-governance/).
- Checks for those files belong in [`coding-rules/scripts/validate_skill.py`](coding-rules/scripts/validate_skill.py) and [`coding-rules/scripts/test_validate_skill.py`](coding-rules/scripts/test_validate_skill.py).
- User-facing description belongs in [README.md](README.md) and [CHANGELOG.md](CHANGELOG.md).

Please describe only behavior the skill actually implements. A sentence in the
README is not a feature unless `SKILL.md`, a reference, or a template says the
same thing.

Project-specific rules stay in that project's own `AGENTS.md`. This skill is
the shared baseline.

## Language

The skill instructions, role prompts, and project templates are written in
Chinese. Please keep them in Chinese unless a change is specifically about
translation. Repository health files (this file, the README's English half,
issue templates, and the changelog) are written in English.

## Setup

You need Python 3.11 or newer. [uv](https://docs.astral.sh/uv/) is optional and
is what CI uses. From a checkout:

```bash
cd coding-rules
uv run scripts/validate_skill.py
uv run scripts/test_validate_skill.py
```

Without uv:

```bash
cd coding-rules
python3 scripts/validate_skill.py
python3 -m pip install "pytest>=8,<10"
python3 -m pytest -q scripts/test_validate_skill.py
```

From the repository root, this builds the same zip the release workflow
publishes:

```bash
python3 scripts/package_skill.py dev
```

The validator checks the skill tree. It does not start Codex, and it does not
test whatever project you later apply the skill to.

## Pull requests

1. Open an issue first for a behavior change, so the maintainer can confirm it
   belongs in the shared skill.
2. Use a focused branch. Keep the diff limited to that change.
3. Run the validator and the tests above.
4. Update `CHANGELOG.md` under `Unreleased` when behavior or user-facing docs
   change. Do not add a version heading or tag. The maintainer cuts versions.
5. Fill in the pull request template. Do not include secrets, tokens, private
   URLs, or customer data.

GitHub Actions runs the same validator, tests, and zip packaging on push and
on pull requests. See [`.github/workflows/ci.yml`](.github/workflows/ci.yml).

## Reporting issues

Use the bug or feature templates. Security reports follow
[SECURITY.md](SECURITY.md) and should stay private.

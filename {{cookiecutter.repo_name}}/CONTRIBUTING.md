# Contributing to {{ cookiecutter.repo_name }}

Thank you for considering contributing!

## Resources

- Issue tracker: https://github.com/{{ cookiecutter.github_org }}/{{ cookiecutter.repo_name }}/issues
- Source code: https://github.com/{{ cookiecutter.github_org }}/{{ cookiecutter.repo_name }}

## Reporting Bugs

Please file issues at the GitHub issue tracker.

## Development Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/{{ cookiecutter.github_org }}/{{ cookiecutter.repo_name }}.git
   cd {{ cookiecutter.repo_name }}
   ```

2. Install dependencies with [uv](https://docs.astral.sh/uv/):

   ```bash
   uv sync --group docs
   ```

3. Run the tests:

   ```bash
   uv run pytest
   ```

4. Run linters:

   ```bash
   uv run ruff check --no-fix src/ tests/
   uv run ty check
   ```

## Pull Requests

1. Fork and create a feature branch.
2. Add tests for any new functionality.
3. Ensure all tests pass and linters are clean.
4. Submit a pull request.

"""Post-generation hook: initialize the generated project."""

import subprocess
import sys


def init_git():
    """Initialize a git repository in the generated project."""
    try:
        subprocess.run(
            ["git", "init"],
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "add", "."],
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from cookiecutter"],
            check=True,
            capture_output=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Warning: could not initialize git repository.", file=sys.stderr)


init_git()

print(
    "\nProject '{{ cookiecutter.repo_name }}' created successfully!\n"
    "\n"
    "Next steps:\n"
    "  cd {{ cookiecutter.repo_name }}\n"
    "  uv sync\n"
    "  uv run pytest\n"
)

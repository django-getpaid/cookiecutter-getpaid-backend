"""Bake tests for the cookiecutter-getpaid-backend template.

These tests use pytest-cookies to bake the cookiecutter template
and verify the generated project has the expected structure, content,
and configuration.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest


# -- Default bake context for convenience --

DEFAULT_CONTEXT = {
    "full_name": "Test Author",
    "email": "test@example.com",
    "github_org": "django-getpaid",
    "gateway_name": "MyGateway",
}


def _bake(cookies, extra_context=None):
    """Bake the template and assert success."""
    ctx = {**DEFAULT_CONTEXT, **(extra_context or {})}
    result = cookies.bake(extra_context=ctx)
    assert result.exit_code == 0, result.exception
    assert result.exception is None
    assert result.project_path.is_dir()
    return result


# ---------------------------------------------------------------
# Project structure
# ---------------------------------------------------------------


class TestProjectStructure:
    """Verify the generated project has the expected files."""

    def test_bake_with_defaults(self, cookies):
        result = _bake(cookies)
        project = result.project_path
        assert project.name == "python-getpaid-mygateway"

    def test_top_level_files(self, cookies):
        project = _bake(cookies).project_path
        expected = [
            "pyproject.toml",
            "README.md",
            "LICENSE",
            "CONTRIBUTING.md",
            "CODE_OF_CONDUCT.md",
            ".gitignore",
            ".readthedocs.yml",
        ]
        for name in expected:
            assert (project / name).is_file(), f"Missing {name}"

    def test_source_layout(self, cookies):
        project = _bake(cookies).project_path
        pkg = project / "src" / "getpaid_mygateway"
        expected = [
            "__init__.py",
            "processor.py",
            "client.py",
            "types.py",
            "py.typed",
        ]
        for name in expected:
            assert (pkg / name).is_file(), (
                f"Missing src/getpaid_mygateway/{name}"
            )

    def test_tests_layout(self, cookies):
        project = _bake(cookies).project_path
        tests = project / "tests"
        expected = ["__init__.py", "conftest.py", "test_processor.py"]
        for name in expected:
            assert (tests / name).is_file(), f"Missing tests/{name}"

    def test_docs_layout(self, cookies):
        project = _bake(cookies).project_path
        docs = project / "docs"
        expected = [
            "conf.py",
            "requirements.txt",
            "index.md",
            "getting-started.md",
            "configuration.md",
            "concepts.md",
            "reference.md",
            "changelog.md",
            "contributing.md",
            "codeofconduct.md",
            "license.md",
        ]
        for name in expected:
            assert (docs / name).is_file(), f"Missing docs/{name}"

    def test_github_issue_template(self, cookies):
        project = _bake(cookies).project_path
        tmpl = project / ".github" / "ISSUE_TEMPLATE.md"
        assert tmpl.is_file()


# ---------------------------------------------------------------
# Variable substitution
# ---------------------------------------------------------------


class TestVariableSubstitution:
    """Verify cookiecutter variables are correctly substituted."""

    def test_custom_gateway_name(self, cookies):
        result = _bake(
            cookies,
            extra_context={"gateway_name": "StripeConnect"},
        )
        project = result.project_path
        assert project.name == "python-getpaid-stripeconnect"
        pkg = project / "src" / "getpaid_stripeconnect"
        assert pkg.is_dir()

    def test_processor_class_name(self, cookies):
        result = _bake(cookies)
        processor = (
            result.project_path / "src" / "getpaid_mygateway" / "processor.py"
        )
        content = processor.read_text()
        assert "class MyGatewayProcessor(BaseProcessor):" in content

    def test_client_class_name(self, cookies):
        result = _bake(cookies)
        client = result.project_path / "src" / "getpaid_mygateway" / "client.py"
        content = client.read_text()
        assert "class MyGatewayClient:" in content

    def test_slug_in_processor(self, cookies):
        result = _bake(cookies)
        processor = (
            result.project_path / "src" / "getpaid_mygateway" / "processor.py"
        )
        content = processor.read_text()
        assert 'slug: ClassVar[str] = "mygateway"' in content
        assert 'display_name: ClassVar[str] = "MyGateway"' in content

    def test_init_exports(self, cookies):
        result = _bake(cookies)
        init = result.project_path / "src" / "getpaid_mygateway" / "__init__.py"
        content = init.read_text()
        assert "MyGatewayClient" in content
        assert "MyGatewayProcessor" in content
        assert '__version__ = "0.1.0"' in content

    def test_author_in_pyproject(self, cookies):
        result = _bake(
            cookies,
            extra_context={
                "full_name": "Jan Kowalski",
                "email": "jan@example.com",
            },
        )
        content = (result.project_path / "pyproject.toml").read_text()
        assert "Jan Kowalski" in content
        assert "jan@example.com" in content

    def test_urls_use_github_org(self, cookies):
        result = _bake(
            cookies,
            extra_context={"github_org": "my-org"},
        )
        content = (result.project_path / "pyproject.toml").read_text()
        assert "my-org/python-getpaid-mygateway" in content

    def test_gateway_with_underscores(self, cookies):
        """Gateway name with spaces produces underscored slug."""
        result = _bake(
            cookies,
            extra_context={"gateway_name": "Pay Now"},
        )
        project = result.project_path
        assert project.name == "python-getpaid-pay-now"
        pkg = project / "src" / "getpaid_pay_now"
        assert pkg.is_dir()
        processor = (pkg / "processor.py").read_text()
        assert "class PayNowProcessor(BaseProcessor):" in processor
        assert 'slug: ClassVar[str] = "pay_now"' in processor


# ---------------------------------------------------------------
# pyproject.toml content
# ---------------------------------------------------------------


class TestPyprojectToml:
    """Verify generated pyproject.toml has correct configuration."""

    def _read_pyproject(self, cookies, extra_context=None):
        result = _bake(cookies, extra_context=extra_context)
        return (result.project_path / "pyproject.toml").read_text()

    def test_project_name(self, cookies):
        content = self._read_pyproject(cookies)
        assert "name = 'python-getpaid-mygateway'" in content

    def test_build_system(self, cookies):
        content = self._read_pyproject(cookies)
        assert "hatchling" in content
        assert "build-backend = 'hatchling.build'" in content

    def test_python_requires(self, cookies):
        content = self._read_pyproject(cookies)
        assert "requires-python = '>=3.12'" in content

    def test_dependencies(self, cookies):
        content = self._read_pyproject(cookies)
        assert "'python-getpaid-core>=0.1.0'" in content
        assert "'httpx>=0.27.0'" in content

    def test_entry_point(self, cookies):
        content = self._read_pyproject(cookies)
        assert '[project.entry-points."getpaid.backends"]' in content
        assert (
            "mygateway = 'getpaid_mygateway.processor:MyGatewayProcessor'"
            in content
        )

    def test_hatch_wheel_packages(self, cookies):
        content = self._read_pyproject(cookies)
        assert "packages = ['src/getpaid_mygateway']" in content

    def test_pytest_config(self, cookies):
        content = self._read_pyproject(cookies)
        assert "asyncio_mode = 'auto'" in content

    def test_ruff_config(self, cookies):
        content = self._read_pyproject(cookies)
        assert "target-version = 'py312'" in content

    def test_ty_config(self, cookies):
        content = self._read_pyproject(cookies)
        assert "python-version = '3.12'" in content
        assert "error-on-warning = true" in content

    def test_dev_dependencies(self, cookies):
        content = self._read_pyproject(cookies)
        for dep in ["pytest", "pytest-asyncio", "ruff", "ty", "respx"]:
            assert dep in content, f"Missing dev dependency: {dep}"

    def test_docs_dependencies(self, cookies):
        content = self._read_pyproject(cookies)
        for dep in ["furo", "sphinx", "myst-parser"]:
            assert dep in content, f"Missing docs dependency: {dep}"


# ---------------------------------------------------------------
# License selection
# ---------------------------------------------------------------


class TestLicenseSelection:
    """Verify LICENSE file content for each license choice."""

    @pytest.mark.parametrize(
        ("license_choice", "expected_text", "expected_classifier"),
        [
            ("MIT", "MIT License", "MIT License"),
            (
                "BSD-3-Clause",
                "BSD 3-Clause License",
                "BSD License",
            ),
            (
                "Apache-2.0",
                "Apache License 2.0",
                "Apache Software License",
            ),
        ],
    )
    def test_license_file(
        self, cookies, license_choice, expected_text, expected_classifier
    ):
        result = _bake(
            cookies,
            extra_context={"open_source_license": license_choice},
        )
        license_content = (result.project_path / "LICENSE").read_text()
        assert expected_text in license_content

        pyproject = (result.project_path / "pyproject.toml").read_text()
        assert expected_classifier in pyproject

    def test_license_has_author_name(self, cookies):
        result = _bake(
            cookies,
            extra_context={"full_name": "Jan Kowalski"},
        )
        license_content = (result.project_path / "LICENSE").read_text()
        assert "Jan Kowalski" in license_content

    def test_license_in_pyproject(self, cookies):
        result = _bake(cookies)
        content = (result.project_path / "pyproject.toml").read_text()
        assert "license = {text = 'MIT'}" in content


# ---------------------------------------------------------------
# Source file content
# ---------------------------------------------------------------


class TestSourceContent:
    """Verify the generated source files have correct content."""

    def test_processor_inherits_base_processor(self, cookies):
        result = _bake(cookies)
        content = (
            result.project_path / "src" / "getpaid_mygateway" / "processor.py"
        ).read_text()
        assert "from getpaid_core.processor import BaseProcessor" in content
        assert "class MyGatewayProcessor(BaseProcessor):" in content

    def test_processor_has_required_methods(self, cookies):
        result = _bake(cookies)
        content = (
            result.project_path / "src" / "getpaid_mygateway" / "processor.py"
        ).read_text()
        for method in [
            "prepare_transaction",
            "verify_callback",
            "handle_callback",
            "fetch_payment_status",
        ]:
            assert f"async def {method}" in content

    def test_processor_has_sandbox_and_production_urls(self, cookies):
        result = _bake(
            cookies,
            extra_context={
                "sandbox_url": "https://sandbox.test.com/",
                "production_url": "https://api.test.com/",
            },
        )
        content = (
            result.project_path / "src" / "getpaid_mygateway" / "processor.py"
        ).read_text()
        assert "https://sandbox.test.com/" in content
        assert "https://api.test.com/" in content

    def test_client_uses_httpx(self, cookies):
        result = _bake(cookies)
        content = (
            result.project_path / "src" / "getpaid_mygateway" / "client.py"
        ).read_text()
        assert "import httpx" in content
        assert "httpx.AsyncClient" in content

    def test_client_is_async_context_manager(self, cookies):
        result = _bake(cookies)
        content = (
            result.project_path / "src" / "getpaid_mygateway" / "client.py"
        ).read_text()
        assert "async def __aenter__" in content
        assert "async def __aexit__" in content

    def test_types_has_auto_name_enum(self, cookies):
        result = _bake(cookies)
        content = (
            result.project_path / "src" / "getpaid_mygateway" / "types.py"
        ).read_text()
        assert "class AutoName(StrEnum):" in content

    def test_py_typed_marker(self, cookies):
        result = _bake(cookies)
        py_typed = (
            result.project_path / "src" / "getpaid_mygateway" / "py.typed"
        )
        assert py_typed.is_file()


# ---------------------------------------------------------------
# Tests layout content
# ---------------------------------------------------------------


class TestGeneratedTests:
    """Verify the generated test files are reasonable."""

    def test_conftest_has_mock_order(self, cookies):
        result = _bake(cookies)
        content = (result.project_path / "tests" / "conftest.py").read_text()
        assert "class MockOrder" in content

    def test_conftest_has_mock_payment(self, cookies):
        result = _bake(cookies)
        content = (result.project_path / "tests" / "conftest.py").read_text()
        assert "class MockPayment" in content

    def test_conftest_has_processor_fixture(self, cookies):
        result = _bake(cookies)
        content = (result.project_path / "tests" / "conftest.py").read_text()
        assert "def processor" in content

    def test_test_processor_has_attribute_tests(self, cookies):
        result = _bake(cookies)
        content = (
            result.project_path / "tests" / "test_processor.py"
        ).read_text()
        assert "MyGatewayProcessor" in content
        assert "BaseProcessor" in content


# ---------------------------------------------------------------
# Docs layout content
# ---------------------------------------------------------------


class TestDocsContent:
    """Verify docs files reference the correct project."""

    def test_docs_conf_project_name(self, cookies):
        result = _bake(cookies)
        content = (result.project_path / "docs" / "conf.py").read_text()
        assert "python-getpaid-mygateway" in content
        assert "furo" in content

    def test_docs_index_includes_readme(self, cookies):
        result = _bake(cookies)
        content = (result.project_path / "docs" / "index.md").read_text()
        assert "include" in content
        assert "README.md" in content


# ---------------------------------------------------------------
# README content
# ---------------------------------------------------------------


class TestReadme:
    """Verify the generated README has expected content."""

    def test_readme_has_project_name(self, cookies):
        result = _bake(cookies)
        content = (result.project_path / "README.md").read_text()
        assert "python-getpaid-mygateway" in content

    def test_readme_has_disclaimer(self, cookies):
        result = _bake(cookies)
        content = (result.project_path / "README.md").read_text()
        assert "nothing in common" in content.lower()

    def test_readme_has_install_instructions(self, cookies):
        result = _bake(cookies)
        content = (result.project_path / "README.md").read_text()
        assert "pip install" in content
        assert "python-getpaid-mygateway" in content

    def test_readme_has_entry_point_example(self, cookies):
        result = _bake(cookies)
        content = (result.project_path / "README.md").read_text()
        assert "getpaid.backends" in content


# ---------------------------------------------------------------
# Hook validation
# ---------------------------------------------------------------


class TestHookValidation:
    """Verify that pre-generation hooks reject invalid inputs."""

    def test_invalid_slug_rejected(self, cookies):
        """Slug with uppercase or special chars should fail."""
        result = cookies.bake(
            extra_context={
                **DEFAULT_CONTEXT,
                "gateway_name": "MyGateway",
                "gateway_slug": "INVALID-Slug!",
            }
        )
        assert result.exit_code != 0

    def test_slug_starting_with_digit_rejected(self, cookies):
        result = cookies.bake(
            extra_context={
                **DEFAULT_CONTEXT,
                "gateway_name": "MyGateway",
                "gateway_slug": "2checkout",
            }
        )
        assert result.exit_code != 0

    def test_invalid_package_name_rejected(self, cookies):
        """Package name not starting with getpaid_ should fail."""
        result = cookies.bake(
            extra_context={
                **DEFAULT_CONTEXT,
                "gateway_name": "MyGateway",
                "package_name": "not_getpaid_foo",
            }
        )
        assert result.exit_code != 0


# ---------------------------------------------------------------
# Ruff compliance
# ---------------------------------------------------------------


class TestRuffCompliance:
    """Verify generated Python files pass ruff linting."""

    def test_generated_python_passes_ruff_check(self, cookies):
        """All generated .py files should pass ruff check."""
        import subprocess

        result = _bake(cookies)
        project = result.project_path

        py_files = list(project.rglob("*.py"))
        assert len(py_files) > 0, "No Python files found"

        proc = subprocess.run(
            ["ruff", "check", "--no-fix", str(project)],
            capture_output=True,
            text=True,
        )
        assert proc.returncode == 0, (
            f"ruff check failed:\n{proc.stdout}\n{proc.stderr}"
        )

    def test_generated_python_passes_ruff_format(self, cookies):
        """All generated .py files should pass ruff format check."""
        import subprocess

        result = _bake(cookies)
        project = result.project_path

        proc = subprocess.run(
            ["ruff", "format", "--check", str(project)],
            capture_output=True,
            text=True,
        )
        assert proc.returncode == 0, (
            f"ruff format check failed:\n{proc.stdout}\n{proc.stderr}"
        )


# ---------------------------------------------------------------
# No leftover template variables
# ---------------------------------------------------------------


class TestNoTemplateLeaks:
    """Verify no raw cookiecutter variables remain in output."""

    TEMPLATE_PATTERN = re.compile(r"\{\{\s*cookiecutter\.")

    def test_no_template_variables_in_files(self, cookies):
        """No generated file should contain raw {{ cookiecutter. }}."""
        result = _bake(cookies)
        project = result.project_path

        for path in project.rglob("*"):
            if not path.is_file():
                continue
            try:
                content = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, ValueError):
                continue
            matches = self.TEMPLATE_PATTERN.findall(content)
            assert not matches, (
                f"Template variable leak in {path.relative_to(project)}: "
                f"{matches}"
            )

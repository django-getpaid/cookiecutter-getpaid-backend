# {{ cookiecutter.repo_name }}

[![PyPI version](https://badge.fury.io/py/{{ cookiecutter.pypi_name }}.svg)](https://pypi.org/project/{{ cookiecutter.pypi_name }}/)
[![License: {{ cookiecutter.open_source_license }}](https://img.shields.io/badge/license-{{ cookiecutter.open_source_license }}-blue.svg)](LICENSE)

{{ cookiecutter.project_description }}

## Overview

This is a [python-getpaid-core](https://github.com/django-getpaid/python-getpaid-core)
payment processor plugin for the **{{ cookiecutter.gateway_name }}** payment gateway.

> **Note:** This project has nothing in common with `getpaid` — a payment
> processing framework for the Plone CMS. It is a completely independent
> project.

## Installation

```bash
pip install {{ cookiecutter.pypi_name }}
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv add {{ cookiecutter.pypi_name }}
```

## Quick Start

The plugin auto-registers via the `getpaid.backends` entry point:

```python
from getpaid_core.registry import registry

# The processor is discovered automatically
processor_cls = registry.get_by_slug("{{ cookiecutter.gateway_slug }}")
```

## Configuration

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `sandbox` | `bool` | `True` | Use sandbox environment |

TODO: Add gateway-specific configuration keys.

## Release checklist

The generated scaffold includes contract tests that fail until processor
logic is implemented. Before publishing, make sure all items below are done:

- [ ] `accepted_currencies` contains supported ISO currency codes
- [ ] `prepare_transaction()` is implemented
- [ ] `verify_callback()` validates callback authenticity
- [ ] `handle_callback()` applies explicit FSM transitions
- [ ] `fetch_payment_status()` is implemented

## Requirements

- Python >= 3.12
- [python-getpaid-core](https://pypi.org/project/python-getpaid-core/) >= 0.1.0
- [httpx](https://pypi.org/project/httpx/) >= 0.27.0

## Related Projects

| Package | Description |
|---------|-------------|
| [python-getpaid-core](https://github.com/django-getpaid/python-getpaid-core) | Framework-agnostic payment processing core |
| [django-getpaid](https://github.com/django-getpaid/django-getpaid) | Django integration layer |

## License

{{ cookiecutter.open_source_license }} — see [LICENSE](LICENSE) for details.

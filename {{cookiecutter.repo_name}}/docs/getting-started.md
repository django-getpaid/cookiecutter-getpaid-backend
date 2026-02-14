# Getting Started

## Installation

```bash
pip install {{ cookiecutter.pypi_name }}
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv add {{ cookiecutter.pypi_name }}
```

## Basic Usage

```python
from {{ cookiecutter.package_name }} import {{ cookiecutter.processor_class_name }}
```

TODO: Add usage examples for your gateway.

## Plugin Registration

The processor is auto-discovered via the `getpaid.backends` entry point.
No manual registration is needed when installed.

To verify it is available:

```python
from getpaid_core.registry import registry

processor_cls = registry.get_by_slug("{{ cookiecutter.gateway_slug }}")
```

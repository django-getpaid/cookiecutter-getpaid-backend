# cookiecutter-getpaid-backend

A [Cookiecutter](https://github.com/cookiecutter/cookiecutter) template for
creating payment gateway plugins for the
[python-getpaid](https://github.com/django-getpaid) ecosystem.

The generated project follows the same structure and conventions as the
official plugins
([python-getpaid-payu](https://github.com/django-getpaid/python-getpaid-payu),
[python-getpaid-przelewy24](https://github.com/django-getpaid/python-getpaid-przelewy24)):
src layout, Hatchling build, async processor/client pattern, full
documentation skeleton, and comprehensive test scaffolding.

> **Note:** This project has nothing in common with `getpaid` — a payment
> processing framework for the Plone CMS. It is a completely independent
> project.

## Prerequisites

- Python >= 3.12
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- [Cookiecutter](https://github.com/cookiecutter/cookiecutter) >= 2.6

Install Cookiecutter if you don't have it:

```bash
uv tool install cookiecutter
# or
pip install cookiecutter
```

## Usage

Generate a new plugin project:

```bash
cookiecutter gh:django-getpaid/cookiecutter-getpaid-backend
```

Or from a local clone:

```bash
cookiecutter path/to/cookiecutter-getpaid-backend
```

You will be prompted for the following values:

| Variable | Default | Description |
|----------|---------|-------------|
| `full_name` | `Your Name` | Author name for pyproject.toml and LICENSE |
| `email` | `you@example.com` | Author email |
| `github_org` | `django-getpaid` | GitHub organization or username |
| `gateway_name` | `MyGateway` | Human-readable gateway name (e.g. `PayU`, `Stripe`, `Przelewy24`) |
| `gateway_slug` | *auto* | Lowercase underscore slug derived from `gateway_name` |
| `package_name` | *auto* | Python package name (`getpaid_<slug>`) |
| `repo_name` | *auto* | Repository name (`python-getpaid-<slug>`) |
| `pypi_name` | *auto* | PyPI package name (same as `repo_name`) |
| `project_description` | *auto* | One-line project description |
| `processor_class_name` | *auto* | Processor class name (`<Name>Processor`) |
| `client_class_name` | *auto* | Client class name (`<Name>Client`) |
| `sandbox_url` | `https://sandbox.example.com/` | Gateway sandbox API URL |
| `production_url` | `https://api.example.com/` | Gateway production API URL |
| `version` | `0.1.0` | Initial version |
| `open_source_license` | `MIT` | License choice: MIT, BSD-3-Clause, or Apache-2.0 |

Most values are derived automatically from `gateway_name`. For example,
entering `Przelewy24` generates:

- `gateway_slug` = `przelewy24`
- `package_name` = `getpaid_przelewy24`
- `repo_name` = `python-getpaid-przelewy24`
- `processor_class_name` = `Przelewy24Processor`
- `client_class_name` = `Przelewy24Client`

## Generated Project Structure

```
python-getpaid-<slug>/
├── pyproject.toml              # Hatchling build, entry points, tool config
├── README.md                   # Project README with badges and disclaimer
├── LICENSE                     # Selected license
├── CONTRIBUTING.md             # Contribution guidelines
├── CODE_OF_CONDUCT.md          # Contributor Covenant v2.1
├── .gitignore
├── .readthedocs.yml            # Read the Docs configuration
├── .github/
│   └── ISSUE_TEMPLATE.md
├── src/
│   └── getpaid_<slug>/
│       ├── __init__.py         # Package exports and __version__
│       ├── processor.py        # BaseProcessor subclass skeleton
│       ├── client.py           # Async httpx API client skeleton
│       ├── types.py            # StrEnum base class, TypedDict stubs
│       └── py.typed            # PEP 561 typing marker
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # MockOrder, MockPayment with FSM, fixtures
│   └── test_processor.py       # Attribute and initialization tests
└── docs/
    ├── conf.py                 # Sphinx + Furo + MyST config
    ├── requirements.txt        # Docs build dependencies
    ├── index.md
    ├── getting-started.md
    ├── configuration.md
    ├── concepts.md
    ├── reference.md            # Autodoc stubs
    ├── changelog.md
    ├── contributing.md
    ├── codeofconduct.md
    └── license.md
```

## Getting Started with the Generated Project

After generating the project:

```bash
cd python-getpaid-<slug>
uv sync
uv run pytest
```

The generated tests pass out of the box — they verify processor class
attributes and initialization without requiring network access.

### Key Files to Implement

#### 1. `processor.py` — Payment Processor

The processor is the main entry point. It subclasses `BaseProcessor` from
`getpaid-core` and must implement these methods:

```python
class MyGatewayProcessor(BaseProcessor):
    slug = "mygateway"
    display_name = "MyGateway"
    accepted_currencies = ["PLN", "EUR", "USD"]

    async def prepare_transaction(self, **kwargs) -> TransactionResult:
        """Register a payment with the gateway and return redirect info."""
        async with self._get_client() as client:
            result = await client.create_payment(
                amount=self.payment.amount_required,
                currency=self.payment.currency,
                description=self.payment.description,
            )
            return TransactionResult(
                redirect_url=result["redirect_url"],
                external_id=result["id"],
            )

    async def handle_callback(self, data, headers, **kwargs) -> None:
        """Process a payment status callback from the gateway."""
        if data["status"] == "COMPLETED":
            self.payment.confirm_payment()

    async def verify_callback(self, data, headers, **kwargs) -> None:
        """Verify callback signature (raise InvalidCallbackError if invalid)."""
        ...

    async def fetch_payment_status(self, **kwargs) -> PaymentStatusResponse:
        """Poll the gateway for current payment status (PULL flow)."""
        ...
```

**Required methods:**
- `prepare_transaction()` — communicates with the gateway API to register a
  transaction and returns a `TransactionResult` (redirect URL, method, etc.)
- `fetch_payment_status()` — polls the gateway for current status

**Optional methods:**
- `verify_callback()` — verifies callback authenticity (signature, etc.)
- `handle_callback()` — processes status updates, triggers FSM transitions
- `charge()` — captures a previously authorized payment
- `release_lock()` — releases a payment lock/hold
- `refund()` — issues a refund

#### 2. `client.py` — Async HTTP Client

The client wraps the gateway's REST API using `httpx.AsyncClient`. Use it as
an async context manager:

```python
class MyGatewayClient:
    def __init__(self, api_url: str, *, api_key: str):
        self.api_url = api_url.rstrip("/")
        self.api_key = api_key
        ...

    async def create_payment(self, **kwargs) -> dict:
        response = await self.client.post(
            f"{self.api_url}/payments",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json=kwargs,
        )
        self.last_response = response
        response.raise_for_status()
        return response.json()
```

#### 3. `types.py` — Type Definitions

Define gateway-specific enums and TypedDicts:

```python
from enum import auto

class TransactionStatus(AutoName):
    PENDING = auto()
    COMPLETED = auto()
    FAILED = auto()
    CANCELLED = auto()

class PaymentResponse(TypedDict, total=False):
    id: str
    status: str
    amount: int
    currency: str
```

### Plugin Registration

The generated `pyproject.toml` includes an entry point that registers your
processor with `getpaid-core` automatically:

```toml
[project.entry-points."getpaid.backends"]
mygateway = "getpaid_mygateway.processor:MyGatewayProcessor"
```

After installation, the processor is discoverable:

```python
from getpaid_core.registry import registry

processor_cls = registry.get_by_slug("mygateway")
```

### Payment Lifecycle

A typical payment flow:

1. **Create payment** — your framework adapter creates a `Payment` object
2. **Prepare transaction** — `prepare_transaction()` is called, which
   communicates with the gateway and returns a redirect URL
3. **Buyer redirected** — the buyer is sent to the gateway's payment page
4. **Callback received** — the gateway sends a status update to your callback
   endpoint
5. **Verify & handle** — `verify_callback()` checks authenticity, then
   `handle_callback()` triggers FSM transitions on the payment object
6. **Status polling** (optional) — `fetch_payment_status()` can be used for
   PULL-based status updates

### Testing Your Plugin

The generated test suite includes:

- **`conftest.py`** — `MockOrder` and `MockPayment` classes satisfying the
  getpaid-core protocols, with FSM state machines attached. Ready-to-use
  `processor`, `mock_order`, `mock_payment`, and `processor_config` fixtures.
- **`test_processor.py`** — Tests verifying processor attributes (slug,
  display_name, currencies, URLs) and initialization (config access, sandbox
  vs. production URL selection).

For testing API calls, use [respx](https://lundberg.github.io/respx/) to mock
`httpx` requests:

```python
import respx
import httpx

@respx.mock
async def test_create_payment(processor):
    respx.post("https://sandbox.example.com/payments").mock(
        return_value=httpx.Response(200, json={"id": "123", "redirect_url": "..."})
    )
    result = await processor.prepare_transaction()
    assert result.redirect_url == "..."
```

Run tests:

```bash
uv run pytest
uv run pytest --cov
```

### Linting and Type Checking

The generated project includes ruff and ty configuration:

```bash
uv run ruff check src/ tests/
uv run ruff format --check src/ tests/
uv run ty check src/
```

### Building Documentation

```bash
uv sync --group docs
uv run sphinx-build docs docs/_build
```

Documentation uses [Sphinx](https://www.sphinx-doc.org/) with the
[Furo](https://pradyunsg.me/furo/) theme and
[MyST](https://myst-parser.readthedocs.io/) Markdown parser.

### Publishing to PyPI

```bash
uv build
uv publish
```

## Development (of this cookiecutter)

### Running Bake Tests

The bake tests verify that the template generates a valid project:

```bash
uv sync
uv run pytest tests/ -v
```

The test suite (53 tests) covers:
- Project structure (files, directories, layouts)
- Variable substitution (gateway name, slug, class names)
- pyproject.toml content (build system, entry points, dependencies)
- License selection (MIT, BSD-3-Clause, Apache-2.0)
- Source file content (processor, client, types)
- Generated test fixtures and assertions
- Hook validation (invalid slugs, package names)
- Ruff compliance (lint + format)
- No template variable leaks

## Related Projects

| Package | Description |
|---------|-------------|
| [python-getpaid-core](https://github.com/django-getpaid/python-getpaid-core) | Framework-agnostic payment processing core |
| [django-getpaid](https://github.com/django-getpaid/django-getpaid) | Django integration layer |
| [python-getpaid-payu](https://github.com/django-getpaid/python-getpaid-payu) | PayU payment gateway plugin |
| [python-getpaid-przelewy24](https://github.com/django-getpaid/python-getpaid-przelewy24) | Przelewy24 payment gateway plugin |

## License

MIT

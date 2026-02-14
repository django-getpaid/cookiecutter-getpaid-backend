"""Test fixtures for {{ cookiecutter.package_name }}."""

from decimal import Decimal

import pytest
from getpaid_core.enums import FraudStatus
from getpaid_core.enums import PaymentStatus
from getpaid_core.fsm import create_fraud_machine
from getpaid_core.fsm import create_payment_machine

from {{ cookiecutter.package_name }} import {{ cookiecutter.processor_class_name }}


class MockOrder:
    """Mock order satisfying the getpaid_core Order protocol."""

    def __init__(
        self,
        total: Decimal = Decimal("100.00"),
        currency: str = "PLN",
        description: str = "Test order",
    ) -> None:
        self.total = total
        self.currency = currency
        self.description = description

    def get_total_amount(self) -> Decimal:
        return self.total

    def get_buyer_info(self) -> dict:
        return {
            "email": "buyer@example.com",
            "first_name": "Jan",
            "last_name": "Kowalski",
        }

    def get_description(self) -> str:
        return self.description

    def get_currency(self) -> str:
        return self.currency

    def get_items(self) -> list[dict]:
        return [
            {
                "name": "Test Product",
                "quantity": 1,
                "unit_price": self.total,
            },
        ]

    def get_return_url(self, success: bool | None = None) -> str:
        if success:
            return "https://example.com/success"
        return "https://example.com/failure"


class MockPayment:
    """Mock payment satisfying the getpaid_core Payment protocol."""

    def __init__(
        self,
        order: MockOrder | None = None,
        amount: Decimal = Decimal("100.00"),
        currency: str = "PLN",
    ) -> None:
        self.id = "test-payment-001"
        self.order = order or MockOrder(total=amount, currency=currency)
        self.amount_required = amount
        self.currency = currency
        self.status = PaymentStatus.NEW
        self.backend = "{{ cookiecutter.gateway_slug }}"
        self.external_id = ""
        self.description = self.order.get_description()
        self.amount_paid = Decimal("0")
        self.amount_locked = Decimal("0")
        self.amount_refunded = Decimal("0")
        self.fraud_status = FraudStatus.UNKNOWN
        self.fraud_message = ""

        create_payment_machine(self)
        create_fraud_machine(self)

    def is_fully_paid(self) -> bool:
        return self.amount_paid >= self.amount_required

    def is_fully_refunded(self) -> bool:
        return self.amount_refunded >= self.amount_paid


@pytest.fixture
def mock_order() -> MockOrder:
    """Provide a mock order."""
    return MockOrder()


@pytest.fixture
def mock_payment(mock_order: MockOrder) -> MockPayment:
    """Provide a mock payment with FSM attached."""
    return MockPayment(order=mock_order)


@pytest.fixture
def processor_config() -> dict:
    """Provide default processor configuration."""
    return {
        "sandbox": True,
        # TODO: add gateway-specific config keys
    }


@pytest.fixture
def processor(
    mock_payment: MockPayment,
    processor_config: dict,
) -> {{ cookiecutter.processor_class_name }}:
    """Provide a configured processor instance."""
    return {{ cookiecutter.processor_class_name }}(
        payment=mock_payment,
        config=processor_config,
    )

"""{{ cookiecutter.gateway_name }} payment processor."""

import logging
from typing import ClassVar

from getpaid_core.processor import BaseProcessor
from getpaid_core.types import PaymentUpdate
from getpaid_core.types import RefundResult
from getpaid_core.types import TransactionResult

from .client import {{ cookiecutter.client_class_name }}


logger = logging.getLogger(__name__)


class {{ cookiecutter.processor_class_name }}(BaseProcessor):
    """{{ cookiecutter.gateway_name }} payment gateway processor."""

    slug: ClassVar[str] = "{{ cookiecutter.gateway_slug }}"
    display_name: ClassVar[str] = "{{ cookiecutter.gateway_name }}"
    accepted_currencies: ClassVar[list[str]] = {{ cookiecutter.accepted_currencies | replace("'", '"') }}
    sandbox_url: ClassVar[str] = "{{ cookiecutter.sandbox_url }}"
    production_url: ClassVar[str] = "{{ cookiecutter.production_url }}"

    def _get_client(self) -> {{ cookiecutter.client_class_name }}:
        """Create a client instance from processor config."""
        return {{ cookiecutter.client_class_name }}(
            api_url=self.get_paywall_baseurl(),
            # TODO: pass credentials from self.get_setting(...)
        )

    async def prepare_transaction(self, **kwargs) -> TransactionResult:
        """Prepare a payment transaction with the gateway.

        This is the only REQUIRED method. It must communicate with
        the payment gateway API to register a new transaction and
        return a ``TransactionResult`` indicating where to redirect
        the buyer.

        Returns:
            TransactionResult with redirect_url, method, etc.
        """
        # TODO: implement gateway-specific transaction registration
        raise NotImplementedError

    async def verify_callback(
        self, data: dict, headers: dict, **kwargs
    ) -> None:
        """Verify the authenticity of a gateway callback.

        Called before ``handle_callback``. Should raise
        ``InvalidCallbackError`` if the signature or data is invalid.
        """
        # TODO: implement signature verification

    async def handle_callback(
        self, data: dict, headers: dict, **kwargs
    ) -> PaymentUpdate | None:
        """Handle a payment status callback from the gateway.

        Return a semantic ``PaymentUpdate`` describing what changed.
        Example:

        - ``PaymentUpdate(payment_event="payment_captured", paid_amount=...)``
        - ``PaymentUpdate(payment_event="failed")``
        - ``PaymentUpdate(payment_event="refund_confirmed", refunded_amount=...)``
        """
        # TODO: implement callback handling

    async def fetch_payment_status(self, **kwargs) -> PaymentUpdate | None:
        """Fetch current payment status from the gateway (PULL flow).

        Returns:
            PaymentUpdate describing the current semantic status.
        """
        # TODO: implement status polling
        raise NotImplementedError

    async def start_refund(self, amount=None, **kwargs) -> RefundResult:
        """Start a refund and return refund metadata."""
        # TODO: implement refund creation
        raise NotImplementedError

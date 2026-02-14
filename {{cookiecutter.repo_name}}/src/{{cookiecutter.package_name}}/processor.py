"""{{ cookiecutter.gateway_name }} payment processor."""

import logging
from typing import ClassVar

from getpaid_core.processor import BaseProcessor
from getpaid_core.types import PaymentStatusResponse
from getpaid_core.types import TransactionResult

from .client import {{ cookiecutter.client_class_name }}


logger = logging.getLogger(__name__)


class {{ cookiecutter.processor_class_name }}(BaseProcessor):
    """{{ cookiecutter.gateway_name }} payment gateway processor."""

    slug: ClassVar[str] = "{{ cookiecutter.gateway_slug }}"
    display_name: ClassVar[str] = "{{ cookiecutter.gateway_name }}"
    accepted_currencies: ClassVar[list[str]] = []  # TODO: add ISO codes
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
    ) -> None:
        """Handle a payment status callback from the gateway.

        Use FSM trigger methods on ``self.payment`` to transition
        payment state:
        - ``self.payment.confirm_payment()`` — mark as paid
        - ``self.payment.mark_as_paid()`` — finalize
        - ``self.payment.fail()`` — mark as failed
        """
        # TODO: implement callback handling

    async def fetch_payment_status(self, **kwargs) -> PaymentStatusResponse:
        """Fetch current payment status from the gateway (PULL flow).

        Returns:
            PaymentStatusResponse with status trigger name.
        """
        # TODO: implement status polling
        raise NotImplementedError

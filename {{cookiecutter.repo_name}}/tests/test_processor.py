"""Tests for {{ cookiecutter.processor_class_name }}."""

import pytest
from getpaid_core.exceptions import InvalidCallbackError
from getpaid_core.processor import BaseProcessor

from {{ cookiecutter.package_name }} import {{ cookiecutter.processor_class_name }}


class TestProcessorAttributes:
    """Test processor class attributes."""

    def test_is_base_processor_subclass(self) -> None:
        assert issubclass({{ cookiecutter.processor_class_name }}, BaseProcessor)

    def test_slug(self) -> None:
        assert {{ cookiecutter.processor_class_name }}.slug == "{{ cookiecutter.gateway_slug }}"

    def test_display_name(self) -> None:
        assert {{ cookiecutter.processor_class_name }}.display_name == "{{ cookiecutter.gateway_name }}"

    def test_accepted_currencies_is_list(self) -> None:
        assert isinstance({{ cookiecutter.processor_class_name }}.accepted_currencies, list)

    def test_sandbox_url(self) -> None:
        assert {{ cookiecutter.processor_class_name }}.sandbox_url

    def test_production_url(self) -> None:
        assert {{ cookiecutter.processor_class_name }}.production_url


class TestProcessorInit:
    """Test processor initialization."""

    def test_init(self, processor) -> None:
        assert processor.payment is not None
        assert processor.config is not None

    def test_get_setting(self, processor) -> None:
        assert processor.get_setting("sandbox") is True

    def test_get_setting_default(self, processor) -> None:
        assert processor.get_setting("nonexistent", "default") == "default"

    def test_paywall_baseurl_sandbox(self, processor) -> None:
        url = processor.get_paywall_baseurl()
        assert url == {{ cookiecutter.processor_class_name }}.sandbox_url

    def test_paywall_baseurl_production(
        self, mock_payment, processor_config
    ) -> None:
        processor_config["sandbox"] = False
        proc = {{ cookiecutter.processor_class_name }}(
            payment=mock_payment,
            config=processor_config,
        )
        assert proc.get_paywall_baseurl() == {{ cookiecutter.processor_class_name }}.production_url


class TestImplementationContract:
    """Release gate: these tests must pass before shipping."""

    @pytest.mark.asyncio
    async def test_prepare_transaction_implemented(self, processor) -> None:
        try:
            await processor.prepare_transaction()
        except NotImplementedError:
            pytest.fail("Implement prepare_transaction() before release.")

    @pytest.mark.asyncio
    async def test_verify_callback_rejects_invalid_payload(
        self, processor
    ) -> None:
        with pytest.raises(InvalidCallbackError):
            await processor.verify_callback(data={}, headers={})

    @pytest.mark.asyncio
    async def test_handle_callback_changes_or_validates_state(
        self, processor
    ) -> None:
        initial_status = processor.payment.status
        await processor.handle_callback(
            data={"status": "confirm_payment"},
            headers={},
        )
        assert processor.payment.status != initial_status, (
            "Implement handle_callback() with explicit state handling "
            "before release."
        )

    @pytest.mark.asyncio
    async def test_fetch_payment_status_implemented(self, processor) -> None:
        try:
            response = await processor.fetch_payment_status()
        except NotImplementedError:
            pytest.fail("Implement fetch_payment_status() before release.")
        assert "status" in response

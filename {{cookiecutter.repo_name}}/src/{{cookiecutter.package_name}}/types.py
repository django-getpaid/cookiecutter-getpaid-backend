"""{{ cookiecutter.gateway_name }} type definitions."""

from enum import StrEnum


class AutoName(StrEnum):
    """StrEnum that uses the member name as its value."""

    @staticmethod
    def _generate_next_value_(
        name: str,
        start: int,
        count: int,
        last_values: list[str],
    ) -> str:
        return name


# TODO: Define gateway-specific enums.
# Example:
#
# class Currency(AutoName):
#     CZK = auto()
#     EUR = auto()
#     PLN = auto()
#     USD = auto()
#
# class TransactionStatus(AutoName):
#     PENDING = auto()
#     COMPLETED = auto()
#     FAILED = auto()


# TODO: Define gateway-specific TypedDicts.
# Example:
#
# class PaymentResponse(TypedDict, total=False):
#     id: str
#     status: str
#     amount: int
#     currency: str

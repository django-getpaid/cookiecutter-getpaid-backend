"""Pre-generation hook: validate cookiecutter inputs."""

import ast
import logging
import re
import sys


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("pre_gen_project")

SLUG_REGEX = r"^[a-z][a-z0-9_]*$"

gateway_slug = "{{ cookiecutter.gateway_slug }}"
package_name = "{{ cookiecutter.package_name }}"
accepted_currencies_raw = "{{ cookiecutter.accepted_currencies }}"

if not re.match(SLUG_REGEX, gateway_slug):
    logger.error(
        "Invalid gateway_slug '%s'. "
        "Must be lowercase, start with a letter, "
        "and contain only letters, digits, and underscores.",
        gateway_slug,
    )
    sys.exit(1)

if not package_name.startswith("getpaid_"):
    logger.error(
        "Invalid package_name '%s': must start with 'getpaid_'.",
        package_name,
    )
    sys.exit(1)

try:
    accepted_currencies = ast.literal_eval(accepted_currencies_raw)
except (SyntaxError, ValueError):
    logger.error(
        "Invalid accepted_currencies '%s'. "
        "Provide a Python list literal, e.g. ['PLN', 'EUR'].",
        accepted_currencies_raw,
    )
    sys.exit(1)

if (
    not isinstance(accepted_currencies, list)
    or not accepted_currencies
    or not all(
        isinstance(code, str) and code.strip() for code in accepted_currencies
    )
):
    logger.error(
        "accepted_currencies must be a non-empty list of currency codes, "
        "e.g. ['PLN', 'EUR']."
    )
    sys.exit(1)

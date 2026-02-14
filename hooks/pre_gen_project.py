"""Pre-generation hook: validate cookiecutter inputs."""

import logging
import re
import sys


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("pre_gen_project")

SLUG_REGEX = r"^[a-z][a-z0-9_]*$"

gateway_slug = "{{ cookiecutter.gateway_slug }}"
package_name = "{{ cookiecutter.package_name }}"

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

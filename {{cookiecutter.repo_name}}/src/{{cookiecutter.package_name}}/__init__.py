"""{{ cookiecutter.project_description }}"""

from {{ cookiecutter.package_name }}.client import {{ cookiecutter.client_class_name }}
from {{ cookiecutter.package_name }}.processor import {{ cookiecutter.processor_class_name }}


__all__ = [
    "{{ cookiecutter.client_class_name }}",
    "{{ cookiecutter.processor_class_name }}",
]

__version__ = "{{ cookiecutter.version }}"

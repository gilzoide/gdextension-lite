"""
Generates bindings for Godot's builtin classes (a.k.a. Variants)
"""

from typing import Tuple

from json_types import BuiltinClass
from function_pointers import generate_variant_function_pointers


def generate_builtin_class(builtin_class: BuiltinClass) -> Tuple[str, str]:
    header_content = [
        '#include "../../gdextension/gdextension_interface.h"',
        "",
    ]

    function_pointers = generate_variant_function_pointers(builtin_class)
    header_content.extend(f"extern {line}" for line in function_pointers if line)

    implementation = [line for line in function_pointers if line]

    return ('\n'.join(header_content), '\n'.join(implementation))

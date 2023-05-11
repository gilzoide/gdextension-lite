"""
Generates bindings for Godot's builtin classes (a.k.a. Variants)
"""

from json_types import BuiltinClass
from function_pointers import generate_variant_function_pointers


def generate_builtin_class(builtin_class: BuiltinClass) -> str:
    lines = [
        '#include "../../gdextension/gdextension_interface.h"',
        "",
    ]

    function_pointers = generate_variant_function_pointers(builtin_class)
    lines.extend(f"extern {line}" for line in function_pointers if line)

    lines.append("")
    lines.append("#ifdef GDEXTENSION_LITE_IMPLEMENTATION")
    lines.extend(line for line in function_pointers if line)
    lines.append("#endif")

    return '\n'.join(lines)

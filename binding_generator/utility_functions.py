"""
Generates bindings for Godot's utility functions
"""

from typing import Tuple

from format_utils import (BindingCode,
                          format_utility_function)
from json_types import UtilityFunction

def generate_utility_functions(
    utility_functions: list[UtilityFunction],
) -> Tuple[str, str]:
    definitions = [format_utility_function(f) for f in utility_functions]
    merged = BindingCode.merge(definitions)
    includes = [
        '#include <string.h>',
        '',
        '#include "../gdextension/gdextension_interface.h"',
        '#include "../variant/all.h"',
    ]
    return (
        "\n".join(includes) + "\n\n" + merged.prototype,
        merged.implementation,
    )

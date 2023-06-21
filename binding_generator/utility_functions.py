"""
Generates bindings for Godot's utility functions
"""

from typing import Tuple

from format_utils import (BindingCode,
                          format_binders,
                          format_utility_function)
from json_types import UtilityFunction

def generate_utility_functions(
    utility_functions: list[UtilityFunction],
) -> Tuple[str, str]:
    definitions = [format_utility_function(f) for f in utility_functions]
    merged = BindingCode.merge(definitions)
    binders = format_binders("utility_functions", merged.bind)
    includes = [
        '#include <string.h>',
        '',
        '#include "../gdextension/gdextension_interface.h"',
        '#include "../variant/all.h"',
    ]
    return (
        "\n".join(includes) + "\n\n" + binders.prototype + "\n\n" + merged.prototype,
        merged.implementation + "\n\n" + binders.implementation,
    )

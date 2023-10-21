"""
Generates bindings for Godot's utility functions
"""

from common.binding_code import BindingCode
from misc.utility_function import UtilityFunctionCode
from json_types import UtilityFunction


def generate_utility_functions(
    utility_functions: list[UtilityFunction],
) -> BindingCode:
    definitions = [UtilityFunctionCode(f).get_c_code() for f in utility_functions]
    includes = [
        "../gdextension/gdextension_interface.h",
        "../implementation-macros.h",
        "../variant/all.h",
    ]
    return BindingCode.merge(definitions, includes=includes)

"""
Generate the cached bindings' function pointers
"""

from format_utils import (format_constructor_pointer,
                          format_destructor_pointer,
                          format_method_pointer,
                          format_operator_pointer,
                          should_generate_constructor,
                          should_generate_operator)
from json_types import BuiltinClass


def generate_operators(builtin_class: BuiltinClass) -> list[str]:
    type_name = builtin_class["name"]
    return [
        format_operator_pointer(type_name=type_name,
                                operator_name=op["name"],
                                right_type=op.get("right_type"))
        for op in builtin_class["operators"]
        if should_generate_operator(type_name, op.get("right_type"))
    ]


def generate_constructors(builtin_class: BuiltinClass) -> list[str]:
    return [
        format_constructor_pointer(builtin_class["name"], ctor)
        for ctor in builtin_class["constructors"]
        if should_generate_constructor(builtin_class["name"], ctor)
    ]


def generate_destructor(builtin_class: BuiltinClass) -> list[str]:
    return ([format_destructor_pointer(builtin_class["name"])]
            if builtin_class["has_destructor"]
            else [])


def generate_methods(builtin_class: BuiltinClass) -> list[str]:
    methods = builtin_class.get("methods")
    if methods:
        return [format_method_pointer(builtin_class["name"], method)
                for method in methods]
    else:
        return []


def generate_variant_function_pointers(builtin_class: BuiltinClass) -> list[str]:
    return (generate_constructors(builtin_class)
            + generate_destructor(builtin_class)
            + generate_operators(builtin_class)
            + generate_methods(builtin_class))

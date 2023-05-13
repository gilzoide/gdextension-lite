"""
Generates bindings for Godot's builtin classes (a.k.a. Variants)
"""

from typing import Tuple

from format_utils import (format_constructor_pointer,
                          format_destructor_pointer,
                          format_indexing_pointers,
                          format_member_pointers,
                          format_method_pointer,
                          format_operator_pointer,
                          format_type_from_to_variant,
                          should_generate_constructor,
                          should_generate_operator)
from json_types import BuiltinClass


def generate_operators(builtin_class: BuiltinClass) -> list[Tuple[str, str]]:
    type_name = builtin_class["name"]
    return [
        format_operator_pointer(type_name=type_name,
                                operator_name=op["name"],
                                right_type=op.get("right_type"))
        for op in builtin_class["operators"]
        if should_generate_operator(type_name, op.get("right_type"))
    ]


def generate_constructors(builtin_class: BuiltinClass) -> list[Tuple[str, str]]:
    return [
        format_constructor_pointer(builtin_class["name"], ctor)
        for ctor in builtin_class["constructors"]
        if should_generate_constructor(builtin_class["name"], ctor)
    ]


def generate_variant_from_to(builtin_class: BuiltinClass) -> list[Tuple[str, str]]:
    return [format_type_from_to_variant(builtin_class["name"])]


def generate_destructor(builtin_class: BuiltinClass) -> list[Tuple[str, str]]:
    if builtin_class["has_destructor"]:
        return [format_destructor_pointer(builtin_class["name"])]
    else:
        return []


def generate_members(builtin_class: BuiltinClass) -> list[Tuple[str, str]]:
    members = builtin_class.get("members")
    if members:
        return [format_member_pointers(builtin_class["name"], member)
                for member in members]
    else:
        return []


def generate_indexing(builtin_class: BuiltinClass) -> list[Tuple[str, str]]:
    indexing_return_type = builtin_class.get("indexing_return_type")
    if indexing_return_type:
        return [format_indexing_pointers(builtin_class["name"],
                                         builtin_class["is_keyed"],
                                         indexing_return_type)]
    else:
        return []



def generate_methods(builtin_class: BuiltinClass) -> list[Tuple[str, str]]:
    methods = builtin_class.get("methods")
    if methods:
        return [format_method_pointer(builtin_class["name"], method)
                for method in methods]
    else:
        return []


def generate_builtin_class(builtin_class: BuiltinClass) -> Tuple[str, str]:
    header_content = [
        '#include "../../gdextension/gdextension_interface.h"',
        '#include "../../variant/all.h"',
        "",
    ]

    definitions = (generate_constructors(builtin_class)
                   + generate_destructor(builtin_class)
                   + generate_variant_from_to(builtin_class)
                   + generate_members(builtin_class)
                   + generate_indexing(builtin_class)
                   + generate_operators(builtin_class)
                   + generate_methods(builtin_class))

    prototypes, implementation = zip(*definitions)
    
    header_content.extend(prototypes)

    return ('\n'.join(header_content), '\n'.join(implementation))

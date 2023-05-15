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


def prepend_section_comment(
    value: Tuple[str, str],
    comment: str,
) -> Tuple[str, str]:
    return (
        f"// {comment}\n{value[0]}",
        f"// {comment}\n{value[1]}",
    )


def generate_operators(
    builtin_class: BuiltinClass,
) -> list[Tuple[str, str]]:
    type_name = builtin_class["name"]
    operators = [
        format_operator_pointer(type_name, op)
        for op in builtin_class["operators"]
        if should_generate_operator(type_name, op.get("right_type"))
    ]
    if operators:
        operators[0] = prepend_section_comment(operators[0], "Operators")
    return operators


def generate_constructors(
    builtin_class: BuiltinClass,
) -> list[Tuple[str, str]]:
    ctors = [
        format_constructor_pointer(builtin_class["name"], ctor)
        for ctor in builtin_class["constructors"]
        if should_generate_constructor(builtin_class["name"], ctor)
    ]
    if ctors:
        ctors[0] = prepend_section_comment(ctors[0], "Constructors")
    return ctors


def generate_variant_from_to(
    builtin_class: BuiltinClass,
) -> list[Tuple[str, str]]:
    return [format_type_from_to_variant(builtin_class["name"])]


def generate_destructor(
    builtin_class: BuiltinClass,
) -> list[Tuple[str, str]]:
    if builtin_class["has_destructor"]:
        dtor = format_destructor_pointer(builtin_class["name"])
        dtor = prepend_section_comment(dtor, "Destructor")
        return [dtor]
    else:
        return []


def generate_members(
    builtin_class: BuiltinClass,
) -> list[Tuple[str, str]]:
    members = [format_member_pointers(builtin_class["name"], member)
               for member in builtin_class.get("members", [])]
    if members:
        members[0] = prepend_section_comment(members[0], "Members")
    return members


def generate_indexing(
    builtin_class: BuiltinClass,
) -> list[Tuple[str, str]]:
    indexing_return_type = builtin_class.get("indexing_return_type")
    if indexing_return_type:
        indexers = format_indexing_pointers(builtin_class["name"],
                                            builtin_class["is_keyed"],
                                            indexing_return_type)
        indexers = prepend_section_comment(indexers, "Indexing")
        return [indexers]
    else:
        return []


def generate_methods(
    builtin_class: BuiltinClass,
) -> list[Tuple[str, str]]:
    methods = [format_method_pointer(builtin_class["name"], method)
               for method in builtin_class.get("methods", [])]
    if methods:
        methods[0] = prepend_section_comment(methods[0], "Methods")
    return methods


def generate_builtin_class(
    builtin_class: BuiltinClass,
) -> Tuple[str, str]:
    definitions = (generate_constructors(builtin_class)
                   + generate_variant_from_to(builtin_class)
                   + generate_destructor(builtin_class)
                   + generate_members(builtin_class)
                   + generate_indexing(builtin_class)
                   + generate_operators(builtin_class)
                   + generate_methods(builtin_class))

    prototypes, implementation = zip(*definitions)
    imports = ('#include "../../gdextension/gdextension_interface.h"\n'
               '#include "../../variant/all.h"')
    return (
        "\n\n".join([imports] + list(prototypes)),
        "\n\n".join(implementation),
    )

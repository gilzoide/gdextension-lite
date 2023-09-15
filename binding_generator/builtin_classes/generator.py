"""
Generates bindings for Godot's builtin classes (a.k.a. Variants)
"""

from typing import Tuple

from .constructor import BuiltinClassConstructor
from .destructor import BuiltinClassDestructor
from .indexing import BuiltinClassIndexing
from .members import BuiltinClassMember
from .method import BuiltinClassMethod
from .operator import BuiltinClassOperator
from .variant_conversion import (BuiltinClassFromVariantConversion,
                                 BuiltinClassToVariantConversion)
from format_utils import (BindingCode,
                          format_class_enum,
                          format_constant,
                          format_type_snake_case)
from json_types import BuiltinClass


def generate_constants(
    builtin_class: BuiltinClass,
) -> list[BindingCode]:
    enum_names = {
        value["name"]
        for enum in builtin_class.get("enums", [])
        for value in enum["values"]
    }
    constants = [format_constant(builtin_class["name"], constant)
                 for constant in builtin_class.get("constants", [])
                 if constant["name"] not in enum_names]
    if constants:
        constants[0].prepend_section_comment("Constants")
    return constants


def generate_enums(
    builtin_class: BuiltinClass,
) -> list[BindingCode]:
    enums = [format_class_enum(builtin_class["name"], enum)
             for enum in builtin_class.get("enums", [])]
    if enums:
        enums[0].prepend_section_comment("Enums")
    return enums


def generate_operators(
    builtin_class: BuiltinClass,
) -> list[BindingCode]:
    operators = [
        op.get_c_code()
        for op in BuiltinClassOperator.get_all_operators(builtin_class)
    ]
    if operators:
        operators[0].prepend_section_comment("Operators")
    return operators


def generate_constructors(
    builtin_class: BuiltinClass,
) -> list[BindingCode]:
    ctors = [
        ctor.get_c_code()
        for ctor in BuiltinClassConstructor.get_all_constructors(builtin_class)
    ]
    if ctors:
        ctors[0].prepend_section_comment("Constructors")
    return ctors


def generate_variant_from_to(
    builtin_class: BuiltinClass,
) -> list[BindingCode]:
    return [
        BuiltinClassToVariantConversion(builtin_class["name"]).get_c_code(),
        BuiltinClassFromVariantConversion(builtin_class["name"]).get_c_code(),
    ]


def generate_destructor(
    builtin_class: BuiltinClass,
) -> list[BindingCode]:
    if builtin_class["has_destructor"]:
        dtor = BuiltinClassDestructor(builtin_class["name"]).get_c_code()
        dtor.prepend_section_comment("Destructor")
        return [dtor]
    else:
        return []


def generate_members(
    builtin_class: BuiltinClass,
) -> list[BindingCode]:
    members = [member.get_c_code()
               for member in BuiltinClassMember.get_all_members(builtin_class)]
    if members:
        members[0].prepend_section_comment("Members")
    return members


def generate_indexing(
    builtin_class: BuiltinClass,
) -> list[BindingCode]:
    indexers = [indexer.get_c_code()
                for indexer
                in BuiltinClassIndexing.get_all_indexers(builtin_class)]
    if indexers:
        indexers[0].prepend_section_comment("Indexing")
    return indexers


def generate_methods(
    builtin_class: BuiltinClass,
) -> list[BindingCode]:
    methods = [
        method.get_c_code()
        for method in BuiltinClassMethod.get_all_methods(builtin_class)
    ]
    if methods:
        methods[0].prepend_section_comment("Methods")
    return methods


def generate_builtin_class(
    builtin_class: BuiltinClass,
) -> Tuple[str, str]:
    definitions = (generate_constants(builtin_class)
                   + generate_enums(builtin_class)
                   + generate_constructors(builtin_class)
                   + generate_variant_from_to(builtin_class)
                   + generate_destructor(builtin_class)
                   + generate_members(builtin_class)
                   + generate_indexing(builtin_class)
                   + generate_operators(builtin_class)
                   + generate_methods(builtin_class))

    merged = BindingCode.merge(definitions)
    includes = [
        '#include "../../gdextension/gdextension_interface.h"',
        '#include "../../variant/all.h"',
    ]
    return (
        "\n".join(includes) + "\n\n" +  merged.prototype,
        merged.implementation,
    )


def generate_initialize_all_builtin_classes(
    builtin_classes: list[BuiltinClass],
) -> Tuple[str, str]:
    class_names = [cls["name"] for cls in builtin_classes]
    includes = "\n".join(f'#include "{format_type_snake_case(name)}.h"'
                         for name in class_names)
    return (
        includes,
        "",
    )

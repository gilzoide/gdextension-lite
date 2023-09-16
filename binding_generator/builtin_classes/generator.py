"""
Generates bindings for Godot's builtin classes (a.k.a. Variants)
"""

from .constructor import BuiltinClassConstructor
from .destructor import BuiltinClassDestructor
from .indexing import BuiltinClassIndexing
from .members import BuiltinClassMember
from .method import BuiltinClassMethod
from .operator import BuiltinClassOperator
from .variant_conversion import (BuiltinClassFromVariantConversion,
                                 BuiltinClassToVariantConversion)
from common.binding_code import BindingCode
from common.constant import Constant
from common.scoped_enum import ScopedEnum
from format_utils import NON_STRUCT_TYPES, format_type_snake_case
from json_types import BuiltinClass


def generate_constants(
    builtin_class: BuiltinClass,
    is_cpp: bool,
) -> list[BindingCode]:
    constants = [
        constant.get_code(is_cpp)
        for constant in Constant.get_all_constants(builtin_class)
    ]
    if constants:
        constants[0].prepend_section_comment("Constants")
    return constants


def generate_enums(
    builtin_class: BuiltinClass,
    is_cpp: bool,
) -> list[BindingCode]:
    enums = [
        enum.get_code(is_cpp)
        for enum in ScopedEnum.get_all_scoped_enums(builtin_class)
    ]
    if enums:
        enums[0].prepend_section_comment("Enums")
    return enums


def generate_operators(
    builtin_class: BuiltinClass,
    is_cpp: bool,
) -> list[BindingCode]:
    operators = [
        op.get_code(is_cpp)
        for op in BuiltinClassOperator.get_all_operators(builtin_class)
    ]
    if operators:
        operators[0].prepend_section_comment("Operators")
    return operators


def generate_constructors(
    builtin_class: BuiltinClass,
    is_cpp: bool,
) -> list[BindingCode]:
    ctors = [
        ctor.get_code(is_cpp)
        for ctor in BuiltinClassConstructor.get_all_constructors(builtin_class)
    ]
    if ctors:
        ctors[0].prepend_section_comment("Constructors")
    return ctors


def generate_variant_from_to(
    builtin_class: BuiltinClass,
    is_cpp: bool,
) -> list[BindingCode]:
    return [
        BuiltinClassToVariantConversion(builtin_class["name"]).get_code(is_cpp),
        BuiltinClassFromVariantConversion(builtin_class["name"]).get_code(is_cpp),
    ]


def generate_destructor(
    builtin_class: BuiltinClass,
    is_cpp: bool,
) -> list[BindingCode]:
    if builtin_class["has_destructor"]:
        dtor = BuiltinClassDestructor(builtin_class["name"]).get_code(is_cpp)
        dtor.prepend_section_comment("Destructor")
        return [dtor]
    else:
        return []


def generate_members(
    builtin_class: BuiltinClass,
    is_cpp: bool,
) -> list[BindingCode]:
    members = [member.get_code(is_cpp)
               for member in BuiltinClassMember.get_all_members(builtin_class)]
    if members:
        members[0].prepend_section_comment("Members")
    return members


def generate_indexing(
    builtin_class: BuiltinClass,
    is_cpp: bool,
) -> list[BindingCode]:
    indexers = [
        indexer.get_code(is_cpp)
        for indexer
        in BuiltinClassIndexing.get_all_indexers(builtin_class)
    ]
    if indexers:
        indexers[0].prepend_section_comment("Indexing")
    return indexers


def generate_methods(
    builtin_class: BuiltinClass,
    is_cpp: bool,
) -> list[BindingCode]:
    methods = [
        method.get_code(is_cpp)
        for method in BuiltinClassMethod.get_all_methods(builtin_class)
    ]
    if methods:
        methods[0].prepend_section_comment("Methods")
    return methods


def generate_builtin_class(
    builtin_class: BuiltinClass,
    is_cpp: bool = False,
) -> BindingCode:
    definitions = (generate_constants(builtin_class, is_cpp)
                   + generate_enums(builtin_class, is_cpp)
                   + generate_constructors(builtin_class, is_cpp)
                   + generate_variant_from_to(builtin_class, is_cpp)
                   + generate_destructor(builtin_class, is_cpp)
                   + generate_members(builtin_class, is_cpp)
                   + generate_indexing(builtin_class, is_cpp)
                   + generate_operators(builtin_class, is_cpp)
                   + generate_methods(builtin_class, is_cpp))

    includes = [
        '#include "../../gdextension/gdextension_interface.h"',
        '#include "../../variant/all.h"',
    ]
    merged = BindingCode.merge(definitions, includes=includes)
    if is_cpp and builtin_class['name'] not in NON_STRUCT_TYPES:
        merged.surround_prototype(
            f"struct {builtin_class['name']} : public godot_{builtin_class['name']} {{",
            "};",
        )
    return merged


def generate_initialize_all_builtin_classes(
    builtin_classes: list[BuiltinClass],
) -> BindingCode:
    class_names = [cls["name"] for cls in builtin_classes]
    includes = [
        f'#include "{format_type_snake_case(name)}.h"'
        for name in class_names
    ]
    return BindingCode(
        "",
        "",
        includes=includes,
    )

"""
Generates bindings for Godot's builtin classes (a.k.a. Variants)
"""

from .constructor import BuiltinClassConstructor
from .destructor import BuiltinClassDestructor
from .indexing import BuiltinClassIndexing
from .members import BuiltinClassMember
from .method import BuiltinClassMethod
from .operator import BuiltinClassOperator
from .variant import VariantCode
from .variant_size import VariantSizeCode
from common.binding_code import BindingCode
from common.constant import Constant
from common.scoped_enum import ScopedEnum
from format_utils import NON_STRUCT_TYPES, format_type_snake_case
from json_types import BuiltinClass, BuiltinClassSize


def generate_constants(
    builtin_class: BuiltinClass,
) -> BindingCode:
    constants = BindingCode.merge([
        constant.get_code()
        for constant in Constant.get_all_constants(builtin_class)
    ])
    if constants:
        constants.format_as_section("Constants")
    return constants


def generate_enums(
    builtin_class: BuiltinClass,
) -> BindingCode:
    enums = BindingCode.merge([
        enum.get_code()
        for enum in ScopedEnum.get_all_scoped_enums(builtin_class)
    ])
    if enums:
        enums.format_as_section("Enums")
    return enums


def generate_operators(
    builtin_class: BuiltinClass,
) -> BindingCode:
    operators = BindingCode.merge([
        op.get_code()
        for op in BuiltinClassOperator.get_all_operators(builtin_class)
    ])
    if operators:
        operators.format_as_section("Operators")
    return operators


def generate_constructors(
    builtin_class: BuiltinClass,
) -> BindingCode:
    ctors = BindingCode.merge([
        ctor.get_code()
        for ctor in BuiltinClassConstructor.get_all_constructors(builtin_class)
    ])
    if ctors:
        ctors.format_as_section("Constructors")
    return ctors


def generate_destructor(
    builtin_class: BuiltinClass,
) -> BindingCode:
    if builtin_class["has_destructor"]:
        dtor = BuiltinClassDestructor(builtin_class["name"]).get_code()
        dtor.format_as_section("Destructor")
        return dtor
    else:
        return BindingCode()


def generate_members(
    builtin_class: BuiltinClass,
) -> BindingCode:
    members = BindingCode.merge([
        member.get_code()
        for member in BuiltinClassMember.get_all_members(builtin_class)
    ])
    if members:
        members.format_as_section("Members")
    return members


def generate_indexing(
    builtin_class: BuiltinClass,
) -> BindingCode:
    indexers = BindingCode.merge([
        indexer.get_code()
        for indexer
        in BuiltinClassIndexing.get_all_indexers(builtin_class)
    ])
    if indexers:
        indexers.format_as_section("Indexing")
    return indexers


def generate_methods(
    builtin_class: BuiltinClass,
) -> BindingCode:
    methods = BindingCode.merge([
        method.get_code()
        for method in BuiltinClassMethod.get_all_methods(builtin_class)
    ])
    if methods:
        methods.format_as_section("Methods")
    return methods


def generate_builtin_class(
    builtin_class: BuiltinClass,
) -> BindingCode:
    definitions = [
        generate_constants(builtin_class),
        generate_enums(builtin_class),
        generate_constructors(builtin_class),
        generate_destructor(builtin_class),
        generate_members(builtin_class),
        generate_indexing(builtin_class),
        generate_operators(builtin_class),
        generate_methods(builtin_class),
    ]

    includes = [
        "../gdextension/gdextension_interface.h",
        "../variant/all.h",
    ]
    return BindingCode.merge(definitions, includes=includes)


def generate_variant(
    builtin_classes: list[BuiltinClass],
) -> BindingCode:
    return VariantCode(builtin_classes).get_code()


def generate_variant_sizes(
    sizes: list[BuiltinClassSize],
) -> BindingCode:
    return VariantSizeCode.get_all_sizes(sizes)


def generate_initialize_all_builtin_classes(
    builtin_classes: list[BuiltinClass],
) -> BindingCode:
    class_names = [cls["name"] for cls in builtin_classes] + ["Variant"]
    includes = [
        f'#include "{format_type_snake_case(name)}.h"'
        for name in class_names
    ]
    return BindingCode(
        "",
        "",
        includes=includes,
        implementation_includes=[line.replace(".h", ".c") for line in includes],
    )

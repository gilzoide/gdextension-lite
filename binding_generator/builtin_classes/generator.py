"""
Generates bindings for Godot's builtin classes (a.k.a. Variants)
"""

from sys import implementation
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
) -> BindingCode:
    constants = BindingCode.merge([
        constant.get_code(is_cpp)
        for constant in Constant.get_all_constants(builtin_class)
    ])
    if constants:
        constants.format_as_section("Constants")
    return constants


def generate_enums(
    builtin_class: BuiltinClass,
    is_cpp: bool,
) -> BindingCode:
    enums = BindingCode.merge([
        enum.get_code(is_cpp)
        for enum in ScopedEnum.get_all_scoped_enums(builtin_class)
    ])
    if enums:
        enums.format_as_section("Enums")
    return enums


def generate_operators(
    builtin_class: BuiltinClass,
    is_cpp: bool,
) -> BindingCode:
    operators = BindingCode.merge([
        op.get_code(is_cpp)
        for op in BuiltinClassOperator.get_all_operators(builtin_class)
    ])
    if operators:
        operators.format_as_section("Operators")
    return operators


def generate_constructors(
    builtin_class: BuiltinClass,
    is_cpp: bool,
) -> BindingCode:
    ctors = BindingCode.merge([
        ctor.get_code(is_cpp)
        for ctor in BuiltinClassConstructor.get_all_constructors(builtin_class)
    ])
    if ctors:
        ctors.format_as_section("Constructors")
    return ctors


def generate_variant_from_to(
    builtin_class: BuiltinClass,
    is_cpp: bool,
) -> BindingCode:
    return BindingCode.merge([
        BuiltinClassToVariantConversion(builtin_class["name"]).get_code(is_cpp),
        BuiltinClassFromVariantConversion(builtin_class["name"]).get_code(is_cpp),
    ])


def generate_destructor(
    builtin_class: BuiltinClass,
    is_cpp: bool,
) -> BindingCode:
    if builtin_class["has_destructor"]:
        dtor = BuiltinClassDestructor(builtin_class["name"]).get_code(is_cpp)
        dtor.format_as_section("Destructor")
        return dtor
    else:
        return BindingCode()


def generate_members(
    builtin_class: BuiltinClass,
    is_cpp: bool,
) -> BindingCode:
    members = BindingCode.merge([
        member.get_code(is_cpp)
        for member in BuiltinClassMember.get_all_members(builtin_class)
    ])
    if members:
        members.format_as_section("Members")
    return members


def generate_indexing(
    builtin_class: BuiltinClass,
    is_cpp: bool,
) -> BindingCode:
    indexers = BindingCode.merge([
        indexer.get_code(is_cpp)
        for indexer
        in BuiltinClassIndexing.get_all_indexers(builtin_class)
    ])
    if indexers:
        indexers.format_as_section("Indexing")
    return indexers


def generate_methods(
    builtin_class: BuiltinClass,
    is_cpp: bool,
) -> BindingCode:
    methods = BindingCode.merge([
        method.get_code(is_cpp)
        for method in BuiltinClassMethod.get_all_methods(builtin_class)
    ])
    if methods:
        methods.format_as_section("Methods")
    return methods


def generate_builtin_class(
    builtin_class: BuiltinClass,
    is_cpp: bool = False,
) -> BindingCode:
    definitions = [
        generate_constants(builtin_class, is_cpp),
        generate_enums(builtin_class, is_cpp),
        generate_constructors(builtin_class, is_cpp),
        generate_variant_from_to(builtin_class, is_cpp),
        generate_destructor(builtin_class, is_cpp),
        generate_members(builtin_class, is_cpp),
        generate_indexing(builtin_class, is_cpp),
        generate_operators(builtin_class, is_cpp),
        generate_methods(builtin_class, is_cpp),
    ]

    includes = [
        "../gdextension/gdextension_interface.h",
        "../variant/all.h",
    ]
    merged = BindingCode.merge(definitions, includes=includes)
    type_name = builtin_class['name']
    if is_cpp:
        merged.add_extras(implementation_includes=[f"variant/{format_type_snake_case(type_name)}.h", "cpp/variant/all.hpp"],
                          includes=["cpp/variant/all-stubs.hpp"])
        if type_name not in NON_STRUCT_TYPES:
            merged.surround_prototype(
                f"struct {type_name} : public godot_{type_name} {{",
                "};",
            )
    return merged


def generate_initialize_all_builtin_classes(
    builtin_classes: list[BuiltinClass],
    is_cpp: bool = False,
) -> BindingCode:
    class_names = [cls["name"] for cls in builtin_classes]
    h_or_hpp = "hpp" if is_cpp else "h"
    includes = [
        f'#include "{format_type_snake_case(name)}.{h_or_hpp}"'
        for name in class_names
    ]
    c_or_cpp = "cpp" if is_cpp else "c"
    return BindingCode(
        "",
        "",
        includes=includes,
        implementation_includes=[line.replace(f".{h_or_hpp}", f".{c_or_cpp}") for line in includes],
    )


def generate_initialize_all_builtin_classes_cpp_stub(
    builtin_classes: list[BuiltinClass],
) -> BindingCode:
    forward_declarations = [
        f"struct {cls['name']};"
        for cls in builtin_classes
        if cls['name'] not in NON_STRUCT_TYPES
    ] + ["struct Object;", "struct Variant;"]
    return BindingCode(
        "\n".join(forward_declarations),
    )

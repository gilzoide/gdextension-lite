"""
Generates bindings for Godot classes
"""

from .method import ClassMethod
from common.binding_code import BindingCode
from common.constant import Constant
from common.opaque_struct import OpaqueStruct
from common.scoped_enum import ScopedEnum
from format_utils import format_type_snake_case
from json_types import Class


def generate_class_constants(
    cls: Class,
) -> BindingCode:
    constants = BindingCode.merge([
        constant.get_c_code()
        for constant in Constant.get_all_constants(cls)
    ])
    if constants:
        constants.format_as_section("Constants")
    return constants


def generate_class_enums(
    cls: Class,
) -> BindingCode:
    enums = BindingCode.merge([
        enum.get_c_code()
        for enum in ScopedEnum.get_all_scoped_enums(cls)
    ])
    if enums:
        enums.format_as_section("Enums")
    return enums


def generate_class_stub(
    cls: Class,
) -> BindingCode:
    return BindingCode.merge([
        OpaqueStruct(cls['name']).get_c_code(),
        generate_class_constants(cls),
        generate_class_enums(cls),
    ])


def generate_class_stub_header(
    cls: Class,
) -> BindingCode:
    includes = (
        ["../variant/int.h"]
        if cls.get('constants')
        else []
    )
    stub = generate_class_stub(cls)
    stub.add_extras(includes=includes)
    return stub


def generate_all_class_stubs(
    classes: list[Class],
) -> BindingCode:
    includes = [
        f'#include "{format_type_snake_case(cls["name"])}.h"'
        for cls in classes
    ]
    return BindingCode(
        "",
        "",
        includes=includes,
    )


def generate_class_methods(
    cls: Class,
    is_cpp: bool,
) -> BindingCode:
    methods = BindingCode.merge([
        method.get_code(is_cpp)
        for method in ClassMethod.get_all_methods(cls)
    ])
    if methods:
        methods.format_as_section("Methods")
    return methods


def generate_class_method_header(
    cls: Class,
    is_cpp: bool = False,
) -> BindingCode:
    includes = [
        "class-stubs/all.h",
        "global_enums.h",
        "native_structures.h",
        "variant/all.h",
        "../gdextension/gdextension_interface.h",
        "../variant/all.h",
    ]
    implementation_includes = (
        ["<string.h>"]
        if any(method.get('is_vararg') for method in cls.get('methods', []))
        else []
    )
    definitions = generate_class_methods(cls, is_cpp=is_cpp)
    definitions.add_extras(includes=includes,
                           implementation_includes=implementation_includes)
    return definitions


def generate_initialize_all_classes(
    classes: list[Class],
) -> BindingCode:
    class_names = [cls["name"] for cls in classes]
    includes = [
        f'#include "{format_type_snake_case(name)}.h"'
        for name in class_names
    ]
    return BindingCode(
        "",
        "",
        includes=includes,
    )

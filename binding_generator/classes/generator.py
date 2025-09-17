"""
Generates bindings for Godot classes
"""

from .constructor import ClassConstructor
from .method import ClassMethod
from .singleton_getter import SingletonGetterCode
from common.binding_code import BindingCode
from common.constant import Constant
from common.opaque_struct import OpaqueStruct
from common.scoped_enum import ScopedEnum
from format_utils import format_type_snake_case
from json_types import ArgumentOrSingletonOrMember, Class


def generate_class_constants(
    cls: Class,
) -> BindingCode:
    constants = BindingCode.merge([
        constant.get_c_code()
        for constant in Constant.get_all_constants(cls)
    ], extra_newline=True)
    if constants:
        constants.format_as_section("Constants")
    return constants


def generate_class_enums(
    cls: Class,
) -> BindingCode:
    enums = BindingCode.merge([
        enum.get_c_code()
        for enum in ScopedEnum.get_all_scoped_enums(cls)
    ], extra_newline=True)
    if enums:
        enums.format_as_section("Enums")
    return enums


def generate_class_stub(
    cls: Class,
) -> BindingCode:
    structdef = OpaqueStruct(cls['name'], cls.get('inherits')).get_c_code()
    return BindingCode.merge([
        structdef,
        generate_class_constants(cls),
        generate_class_enums(cls),
    ], extra_newline=True)


def generate_class_stub_header(
    cls: Class,
) -> BindingCode:
    includes = ["../definition-macros.h"]
    if cls.get('constants'):
        includes.append("../variant/int.h")
    return generate_class_stub(cls).add_extras(includes=includes)


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
        implementation_includes=[line.replace(".h", ".c") for line in includes],
    )


def generate_class_constructor(
    cls: Class,
    singleton: ArgumentOrSingletonOrMember | None,
) -> BindingCode:
    if singleton:
        return SingletonGetterCode(singleton).get_c_code().format_as_section("Singleton")
    elif cls.get("is_instantiable", True):
        return ClassConstructor(cls["name"]).get_c_code().format_as_section("Constructor")
    else:
        return BindingCode()


def generate_class_methods(
    cls: Class,
) -> BindingCode:
    methods = BindingCode.merge([
        method.get_code()
        for method in ClassMethod.get_all_methods(cls)
    ])
    if methods:
        methods.format_as_section("Methods")
    return methods


def generate_class_method_header(
    cls: Class,
    singleton: ArgumentOrSingletonOrMember | None,
) -> BindingCode:
    includes = [
        "class-stubs/all.h",
        "global_enums.h",
        "native_structures.h",
        "variant/all.h",
        "../gdextension/gdextension_interface.h",
        "../variant/all.h",
    ]
    return BindingCode.merge([
        generate_class_constructor(cls, singleton),
        generate_class_methods(cls),
    ], includes=includes)


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
        implementation_includes=[line.replace(".h", ".c") for line in includes],
    )

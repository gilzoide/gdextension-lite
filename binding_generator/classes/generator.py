"""
Generates bindings for Godot classes
"""

from .method import ClassMethod
from common.constant import Constant
from common.opaque_struct import OpaqueStruct
from common.scoped_enum import ScopedEnum
from format_utils import BindingCode, format_type_snake_case
from json_types import Class


def generate_class_constants(
    cls: Class,
) -> list[BindingCode]:
    constants = [
        constant.get_c_code()
        for constant in Constant.get_all_constants(cls)
    ]
    if constants:
        constants[0].prepend_section_comment("Constants")
    return constants


def generate_class_enums(
    cls: Class,
) -> list[BindingCode]:
    enums = [
        enum.get_c_code()
        for enum in ScopedEnum.get_all_scoped_enums(cls)
    ]
    if enums:
        enums[0].prepend_section_comment("Enums")
    return enums


def generate_class_stub(
    cls: Class,
) -> list[BindingCode]:
    return ([OpaqueStruct(cls['name']).get_c_code()]
            + generate_class_constants(cls)
            + generate_class_enums(cls))


def generate_class_stub_header(
    cls: Class,
) -> BindingCode:
    return BindingCode.merge(generate_class_stub(cls))


def generate_all_class_stubs(
    classes: list[Class],
) -> BindingCode:
    includes = (
        f'#include "{format_type_snake_case(cls["name"])}.h"'
        for cls in classes
    )
    return BindingCode(
        "",
        "",
        includes="\n".join(includes),
    )

def generate_class_methods(
    cls: Class,
) -> list[BindingCode]:
    methods = [
        method.get_c_code()
        for method in ClassMethod.get_all_methods(cls)
    ]
    if methods:
        methods[0].prepend_section_comment("Methods")
    return methods


def generate_class_method_header(
    cls: Class,
) -> BindingCode:
    definitions = (generate_class_methods(cls))
    includes = [
        '#include "../class-stubs/all.h"',
        '#include "../global_enums.h"',
        '#include "../native_structures.h"',
        '#include "../variant/all.h"',
        '#include "../../gdextension/gdextension_interface.h"',
        '#include "../../variant/all.h"',
    ]
    return BindingCode.merge(definitions, includes=includes)


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
        includes="\n".join(includes),
    )

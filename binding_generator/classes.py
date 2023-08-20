"""
Generates bindings for Godot classes
"""

from typing import Tuple
from textwrap import indent

from format_utils import (BindingCode,
                          code_block,
                          format_binders,
                          format_class_enum,
                          format_class_method_pointer,
                          format_class_struct,
                          format_type_snake_case)
from json_types import Class


def generate_class_enums(
    cls: Class,
) -> list[BindingCode]:
    enums = [format_class_enum(cls["name"], enum)
             for enum in cls.get("enums", [])]
    if enums:
        enums[0].prepend_section_comment("Enums")
    return enums


def generate_class_stub(
    cls: Class,
) -> list[BindingCode]:
    return ([format_class_struct(cls["name"])]
            + generate_class_enums(cls))


def generate_class_stub_header(
    cls: Class,
) -> Tuple[str, str]:
    merged = BindingCode.merge(generate_class_stub(cls))
    return (
        merged.prototype,
        "",
    )


def generate_all_class_stubs(
    classes: list[Class],
) -> Tuple[str, str]:
    includes = (f'#include "{format_type_snake_case(cls["name"])}.h"'
                for cls in classes)
    return (
        "\n".join(includes),
        ""
    )

def generate_class_methods(
    cls: Class,
) -> list[BindingCode]:
    methods = [format_class_method_pointer(cls["name"], method)
               for method in cls.get("methods", [])]
    if methods:
        methods[0].prepend_section_comment("Methods")
    return methods


def generate_class_method_header(
    cls: Class,
) -> Tuple[str, str]:
    definitions = (generate_class_methods(cls))
    merged = BindingCode.merge(definitions)
    binders = format_binders(cls["name"], merged.bind, type_stringname_var=True)
    includes = [
        '#include "../global_enums.h"',
        '#include "../class-stubs/all.h"',
        '#include "../../gdextension/gdextension_interface.h"',
        '#include "../../variant/all.h"',
    ]
    return (
        "\n".join(includes) + "\n\n" + binders.prototype + "\n\n" + merged.prototype,
        merged.implementation + "\n\n" + binders.implementation,
    )


def generate_initialize_all_classes(
    classes: list[Class],
) -> Tuple[str, str]:
    class_names = [cls["name"] for cls in classes]
    includes = "\n".join(f'#include "{format_type_snake_case(name)}.h"'
                         for name in class_names)
    prototype = ("void gdextension_lite_initialize_generated_classes()")
    calls = "\n".join(f"gdextension_lite_initialize_{name}();"
                      for name in class_names)
    return (
        code_block(f"""
{indent(includes, "            ")}

            {prototype};
        """),
        code_block(f"""
            {prototype} {{
{indent(calls, "            	")}
            }}
        """),
    )

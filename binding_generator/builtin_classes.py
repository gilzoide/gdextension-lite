"""
Generates bindings for Godot's builtin classes (a.k.a. Variants)
"""

from typing import Tuple
from textwrap import indent

from format_utils import (BindingCode,
                          code_block,
                          format_binders,
                          format_constructor_pointer,
                          format_destructor_pointer,
                          format_indexing_pointers,
                          format_member_pointers,
                          format_method_pointer,
                          format_operator_pointer,
                          format_type_from_to_variant,
                          format_type_snake_case,
                          should_generate_constructor,
                          should_generate_method,
                          should_generate_operator)
from json_types import BuiltinClass


def generate_operators(
    builtin_class: BuiltinClass,
) -> list[BindingCode]:
    type_name = builtin_class["name"]
    operators = [
        format_operator_pointer(type_name, op)
        for op in builtin_class["operators"]
        if should_generate_operator(type_name, op.get("right_type"))
    ]
    if operators:
        operators[0].prepend_section_comment("Operators")
    return operators


def generate_constructors(
    builtin_class: BuiltinClass,
) -> list[BindingCode]:
    ctors = [
        format_constructor_pointer(builtin_class["name"], ctor)
        for ctor in builtin_class["constructors"]
        if should_generate_constructor(builtin_class["name"], ctor)
    ]
    if ctors:
        ctors[0].prepend_section_comment("Constructors")
    return ctors


def generate_variant_from_to(
    builtin_class: BuiltinClass,
) -> list[BindingCode]:
    return [format_type_from_to_variant(builtin_class["name"])]


def generate_destructor(
    builtin_class: BuiltinClass,
) -> list[BindingCode]:
    if builtin_class["has_destructor"]:
        dtor = format_destructor_pointer(builtin_class["name"])
        dtor.prepend_section_comment("Destructor")
        return [dtor]
    else:
        return []


def generate_members(
    builtin_class: BuiltinClass,
) -> list[BindingCode]:
    members = [format_member_pointers(builtin_class["name"], member)
               for member in builtin_class.get("members", [])]
    if members:
        members[0].prepend_section_comment("Members")
    return members


def generate_indexing(
    builtin_class: BuiltinClass,
) -> list[BindingCode]:
    indexing_return_type = builtin_class.get("indexing_return_type")
    if indexing_return_type:
        indexers = format_indexing_pointers(builtin_class["name"],
                                            builtin_class["is_keyed"],
                                            indexing_return_type)
        indexers.prepend_section_comment("Indexing")
        return [indexers]
    else:
        return []


def generate_methods(
    builtin_class: BuiltinClass,
) -> list[BindingCode]:
    members = builtin_class.get("members", [])
    methods = [format_method_pointer(builtin_class["name"], method)
               for method in builtin_class.get("methods", [])
               if should_generate_method(method, members)]
    if methods:
        methods[0].prepend_section_comment("Methods")
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

    merged = BindingCode.merge(definitions)
    binders = format_binders(builtin_class["name"], merged.bind)
    includes = [
        '#include "../../gdextension/gdextension_interface.h"',
        '#include "../../variant/all.h"',
    ]
    return (
        "\n".join(includes) + "\n\n" + binders.prototype + "\n\n" + merged.prototype,
        merged.implementation + "\n\n" + binders.implementation,
    )


def generate_initialize_all(
    builtin_classes: list[BuiltinClass],
) -> Tuple[str, str]:
    class_names = [cls["name"] for cls in builtin_classes]
    includes = "\n".join(f'#include "{format_type_snake_case(name)}.h"'
                         for name in class_names)
    prototype = ("void gdextension_lite_initialize_generated("
                 "const GDExtensionInterface *interface)")
    calls = "\n".join(f"gdextension_lite_initialize_{name}(interface);"
                      for name in class_names
                      if name != "StringName")
    return (
        code_block(f"""
            #include "../../gdextension/gdextension_interface.h"

{indent(includes, "            ")}

            {prototype};
        """),
        code_block(f"""
            {prototype} {{
{indent(calls, "            	")}
            }}
        """),
    )

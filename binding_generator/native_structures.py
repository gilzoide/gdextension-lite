"""
Generates bindings for Godot's native structures
"""

from common.binding_code import BindingCode
from format_utils import format_native_struct_field
from json_types import NativeStructure


def generate_native_structure(
    struct: NativeStructure,
) -> BindingCode:
    name = struct["name"]
    fields = [
        format_native_struct_field(field)
        for field in struct["format"].split(";")
    ]
    return BindingCode(
        '\n'.join([
            f"typedef struct godot_{name} {{",
            *(f"\t{f};" for f in fields),
            f"}} godot_{name};",
        ]),
        "",
    )



def generate_all_native_structures(
    structs: list[NativeStructure],
) -> BindingCode:
    includes = [
        "class-stubs/all.h",
        "../definition-macros.h",
        "../variant/all.h",
    ]
    return BindingCode.merge(
        (generate_native_structure(struct) for struct in structs),
        extra_newline=True,
        includes=includes,
    )

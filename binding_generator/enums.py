"""
Generates C enum bindings for GDExtension
"""

from json_types import GlobalEnumOrEnum
from format_utils import BindingCode


def generate_enum(enum: GlobalEnumOrEnum) -> BindingCode:
    lines = [
        "typedef enum {",
        *[f"\t{value['name']} = {value['value']}," for value in enum['values']],
        f"}} godot_{enum['name'].replace('.', '_')};",
    ]
    return BindingCode("\n".join(lines), "")


def generate_all_enums(enums: list[GlobalEnumOrEnum]) -> BindingCode:
    return BindingCode.merge([generate_enum(e) for e in enums])

"""
Generates C enum bindings for GDExtension
"""

from common.binding_code import BindingCode
from json_types import GlobalEnumOrEnum


def generate_enum(enum: GlobalEnumOrEnum) -> BindingCode:
    lines = [
        "typedef enum {",
        *(f"\t{value['name']} = {value['value']}," for value in enum['values']),
        f"}} godot_{enum['name'].replace('.', '_')};",
    ]
    return BindingCode("\n".join(lines), "")


def generate_all_enums(enums: list[GlobalEnumOrEnum]) -> BindingCode:
    return BindingCode.merge(generate_enum(e) for e in enums)

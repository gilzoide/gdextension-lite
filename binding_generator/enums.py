"""
Generates C enum bindings for GDExtension
"""

from typing import TypedDict


class EnumValue(TypedDict):
    name: str
    value: int


class EnumType(TypedDict):
    name: str
    values: list[EnumValue]


def generate_enum(enum: EnumType) -> str:
    lines = ["typedef enum {"]
    for value in enum['values']:
        lines.append(f"\t{value['name']} = {value['value']},")
    lines.append(f"}} godot_{enum['name'].replace('.', '')};")
    return '\n'.join(lines)


def generate_all_enums(enums: list[EnumType]) -> str:
    return '\n\n'.join(generate_enum(e) for e in enums)

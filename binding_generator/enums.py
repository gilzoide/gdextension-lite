"""
Generates C enum bindings for GDExtension
"""

from json_types import GlobalEnumOrEnum


def generate_enum(enum: GlobalEnumOrEnum) -> str:
    lines = ["typedef enum {"]
    for value in enum['values']:
        lines.append(f"\t{value['name']} = {value['value']},")
    lines.append(f"}} godot_{enum['name'].replace('.', '_')};")
    return '\n'.join(lines)


def generate_all_enums(enums: list[GlobalEnumOrEnum]) -> str:
    return '\n\n'.join(generate_enum(e) for e in enums)

"""
Generates bindings for Godot's native structures
"""

from format_utils import format_native_struct_field
from json_types import NativeStructure


def generate_native_structure(
    struct: NativeStructure,
) -> str:
    name = struct["name"]
    fields = [format_native_struct_field(field) for field in struct["format"].split(";")]
    return '\n'.join([
        f"typedef struct godot_{name} {{",
        *[f"\t{f};" for f in fields],
        f"}} godot_{name};",
    ])


def generate_all_native_structures(
    structs: list[NativeStructure],
) -> str:
    lines = [
        '#include "class-stubs/all.h"\n#include "../variant/all.h"',
    ]
    lines.extend(generate_native_structure(struct) for struct in structs)
    return "\n\n".join(lines)

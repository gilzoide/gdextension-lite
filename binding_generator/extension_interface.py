"""
Generate bindings for Godot extension interface
"""

import re
from textwrap import indent

from format_utils import BindingCode

SYMBOL_RE = re.compile(r"@name\s+(\w+)")
TYPE_RE = re.compile(r"typedef [^(]*\(\*(\w+)")


def generate_extension_binding(
    symbol: str,
    type_name: str,
) -> BindingCode:
    return BindingCode(
        f"extern {type_name} godot_{symbol};",
        f"{type_name} godot_{symbol};",
        bind=f'godot_{symbol} = ({type_name}) get_proc_address("{symbol}");',
    )


def generate_all_extension_bindings() -> BindingCode:
    with open("gdextension-lite/gdextension/gdextension_interface.h") as header_file:
        lines = header_file.readlines()

    bindings = [
        BindingCode(
            "void gdextension_lite_initialize_interface(const GDExtensionInterfaceGetProcAddress get_proc_address);",
            "",
            includes='#include "../gdextension/gdextension_interface.h"',
        ),
    ]
    symbol = None
    for line in lines:
        line = line.rstrip()
        if symbol is None:
            _, _, n = line.partition("@name ")
            if n:
                symbol = n
        else:
            match = TYPE_RE.match(line)
            if match:
                bindings.append(generate_extension_binding(symbol, match.group(1)))
                symbol = None

    merged = BindingCode.merge(bindings)
    merged.implementation += "\n".join([
        "void gdextension_lite_initialize_interface(const GDExtensionInterfaceGetProcAddress get_proc_address) {",
        indent(merged['bind'], "\t"),
        "}",
    ])
    return merged

"""
Generate bindings for Godot extension interface
"""

import re

from common.binding_code import BindingCode
from misc.extension_interface_function import ExtensionInterfaceFunction

SYMBOL_RE = re.compile(r"@name\s+(\w+)")
FUNCTION_POINTER_TYPE_RE = re.compile(r"""
    typedef\s+   # 'typedef '
        ([^(]*)  # return type, may contain trailing whitespace
    \(\s*\*\s*   # '(*'
        (\w+)    # the defined name for the function pointer type
    \s*\)\s*\(   # ')('
        (.*)     # all arguments text
    \);          # ');'
""", re.VERBOSE)


def generate_all_extension_bindings(
    is_cpp: bool = False,
) -> BindingCode:
    with open("gdextension-lite/gdextension/gdextension_interface.h") as header_file:
        lines = header_file.readlines()

    functions: list[ExtensionInterfaceFunction] = []
    symbol = None
    for line in lines:
        line = line.rstrip()
        if symbol is None:
            _, _, n = line.partition("@name ")
            if n:
                symbol = n
        else:
            match = FUNCTION_POINTER_TYPE_RE.match(line)
            if match:
                functions.append(ExtensionInterfaceFunction(symbol, match.group(2), match.group(1), match.group(3)))
                symbol = None

    return BindingCode.merge([
        BindingCode(
            "extern GDExtensionInterfaceGetProcAddress gdextension_lite_get_proc_address;",
            "GDExtensionInterfaceGetProcAddress gdextension_lite_get_proc_address;\n",
        ),
        *(f.get_code(is_cpp) for f in functions),
        BindingCode(
            "\nvoid gdextension_lite_initialize_interface(const GDExtensionInterfaceGetProcAddress get_proc_address);",
            "\n".join([
                "",
                "void gdextension_lite_initialize_interface(const GDExtensionInterfaceGetProcAddress get_proc_address) {",
                "\tgdextension_lite_get_proc_address = get_proc_address;",
                "}",
            ]),
            includes=["../gdextension/gdextension_interface.h", "../implementation-macros.h"],
        )
    ])

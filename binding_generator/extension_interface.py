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


def generate_all_extension_bindings() -> BindingCode:
    with open("gdextension-lite/gdextension/gdextension_interface.h") as header_file:
        lines = header_file.readlines()

    functions: list[ExtensionInterfaceFunction] = []
    symbol = None
    since = None
    for line in lines:
        line = line.rstrip()
        if symbol is None:
            _, _, n = line.partition("@name ")
            if n:
                symbol = n
        if since is None:
            _, _, s = line.partition("@since ")
            if s:
                since = s
        else:
            match = FUNCTION_POINTER_TYPE_RE.match(line)
            if match:
                functions.append(ExtensionInterfaceFunction(symbol, match.group(2), match.group(1), match.group(3), since))
                symbol = None
                since = None

    return BindingCode.merge(
        [
            BindingCode(
                "",
                "GDExtensionInterfaceGetProcAddress gdextension_lite_get_proc_address;",
            ),
            BindingCode.merge(f.get_code() for f in functions),
            BindingCode(
                "GDEXTENSION_LITE_DECL void gdextension_lite_initialize_interface(const GDExtensionInterfaceGetProcAddress get_proc_address);",
                "\n".join([
                    "void gdextension_lite_initialize_interface(const GDExtensionInterfaceGetProcAddress get_proc_address) {",
                        "\tgdextension_lite_get_proc_address = get_proc_address;",
                    "}",
                ]),
            )
        ],
        extra_newline=True,
        includes=[
            "../gdextension/gdextension_interface.h",
            "../definition-macros.h",
        ],
    )

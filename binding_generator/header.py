"""
C header file generator
"""

from pathlib import Path
import re

from common.binding_code import BindingCode


class HeaderWriter:
    """C/C++ header file writer class"""
    def __init__(self, *pathsegments):
        self.base_dir = Path(*pathsegments)

    def write_header(self,
                     contents: BindingCode,
                     *pathsegments: str,
                     is_cpp: bool = False):
        header_name = Path(*pathsegments)
        h_or_hpp = "hpp" if is_cpp else "h"
        guard_name = re.sub("[^a-zA-Z0-9_]", "_", str(header_name)).upper()
        define = f"__GDEXTENSION_LITE_GENERATED_{guard_name}_{h_or_hpp.upper()}__"
        if is_cpp:
            contents.surround_prototype(
                "namespace godot {",
                "}",
            )
            contents.surround_implementation(
                "namespace godot {",
                "}",
            )
        lines = [
            "// This file was automatically generated",
            "// Do not modify this file",
            f"#ifndef {define}",
            f"#define {define}",
            "",
        ]
        if contents['includes']:
            lines.extend(contents['includes'])
            lines.append("")
        lines.extend([
            contents.prototype,
            "",
            f"#endif  // {define}",
        ])

        if contents.implementation:
            define = f"__GDEXTENSION_LITE_GENERATED_{guard_name}_{h_or_hpp.upper()}_IMPLEMENTATION__"
            implementation_macros_h = ("../" * len(pathsegments)) + "implementation-macros.h"
            lines.extend([
                "",
                "#ifdef GDEXTENSION_LITE_IMPLEMENTATION",
                f"#ifndef {define}",
                f"#define {define}",
                "",
                f'#include "{implementation_macros_h}"',
            ])
            if contents['implementation_includes']:
                lines.extend(contents['implementation_includes'])
                lines.append("")
            lines.extend([
                contents.implementation,
                "",
                f"#endif  // {define}",
                "#endif  // GDEXTENSION_LITE_IMPLEMENTATION",
            ])
        filename = self.base_dir.joinpath(header_name).with_suffix("." + h_or_hpp)
        filename.parent.mkdir(exist_ok=True, parents=True)
        with open(filename, 'w') as file:
            file.write('\n'.join(lines))

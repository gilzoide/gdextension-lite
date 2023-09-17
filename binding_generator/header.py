"""
C header file generator
"""

import os.path
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
        header_path = Path(*pathsegments)
        h_or_hpp = "hpp" if is_cpp else "h"
        guard_name = re.sub("[^a-zA-Z0-9_]", "_", str(header_path)).upper()
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
        else:
            contents.surround_prototype(
                "\n".join([
                    "#ifdef __cplusplus",
                    'extern "C" {',
                    "#endif",
                    "",
                ]),
                "\n".join([
                    "",
                    "#ifdef __cplusplus",
                    "}",
                    "#endif",
                ]),
                add_indent=False,
            )
            contents.surround_implementation(
                "\n".join([
                    "#ifdef __cplusplus",
                    'extern "C" {',
                    "#endif",
                    "",
                ]),
                "\n".join([
                    "",
                    "#ifdef __cplusplus",
                    "}",
                    "#endif",
                ]),
                add_indent=False,
            )
        lines = [
            "// This file was automatically generated",
            "// Do not modify this file",
            f"#ifndef {define}",
            f"#define {define}",
            "",
        ]
        if contents['includes']:
            lines.extend(self.process_include(header_path, include) for include in contents['includes'])
            lines.append("")
        lines.extend([
            contents.prototype,
            "",
            f"#endif  // {define}",
        ])

        if contents.implementation:
            define = f"__GDEXTENSION_LITE_GENERATED_{guard_name}_{h_or_hpp.upper()}_IMPLEMENTATION__"
            implementation_macros_h = self.process_include(header_path, f"../implementation-macros.{h_or_hpp}")
            lines.extend([
                "",
                "#ifdef GDEXTENSION_LITE_IMPLEMENTATION",
                f"#ifndef {define}",
                f"#define {define}",
                "",
                implementation_macros_h,
            ])
            if contents['implementation_includes']:
                lines.extend(self.process_include(header_path, include) for include in contents['implementation_includes'])
            lines.extend([
                "",
                contents.implementation,
                "",
                f"#endif  // {define}",
                "#endif  // GDEXTENSION_LITE_IMPLEMENTATION",
            ])
        filename = self.base_dir.joinpath(header_path).with_suffix("." + h_or_hpp)
        filename.parent.mkdir(exist_ok=True, parents=True)
        with open(filename, 'w') as file:
            file.write('\n'.join(lines))

    @classmethod
    def process_include(cls, header_path: Path, include: str) -> str:
        include = include.strip()
        if include.startswith("#include"):
            return include
        elif include.startswith("<"):
            return f'#include {include}'
        else:
            relative_path = os.path.relpath(include, header_path.parent)
            return f'#include "{relative_path}"'

"""
C header file generator
"""

import os.path
from pathlib import Path
import re

from common.binding_code import BindingCode


class CodeWriter:
    """C/C++ header file writer class"""
    def __init__(self, *pathsegments):
        self.base_dir = Path(*pathsegments)

    def write_file(self,
                   contents: BindingCode,
                   *pathsegments: str):
        header_path = Path(*pathsegments)
        guard_name = re.sub("[^a-zA-Z0-9_]", "_", str(header_path)).upper()
        define = f"__GDEXTENSION_LITE_GENERATED_{guard_name}_H__"
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
        ])
        if contents["prototype_outside_ifcpp"]:
            lines.extend(contents["prototype_outside_ifcpp"])
            lines.append("")
        lines.extend([
            f"#endif  // {define}",
            "",
        ])
        header_filename = self.base_dir.joinpath(header_path).with_suffix(".h")
        header_filename.parent.mkdir(exist_ok=True, parents=True)
        with open(header_filename, 'w') as file:
            file.write('\n'.join(lines))

        impl_lines = [
            "// This file was automatically generated",
            "// Do not modify this file",
        ]
        if contents.implementation:
            implementation_macros_h = self.process_include(header_path, f"../implementation-macros.h")
            impl_lines.extend([
                f'#include "{pathsegments[-1]}.h"',
                "",
                implementation_macros_h,
            ])
        if contents['implementation_includes']:
            impl_lines.extend(self.process_include(header_path, include) for include in contents['implementation_includes'])
        if contents.implementation:
            impl_lines.extend([
                "",
                contents.implementation,
                "",
            ])

        impl_filename = header_filename.with_suffix(".c")
        with open(impl_filename, 'w') as file:
            file.write('\n'.join(impl_lines))

    @classmethod
    def process_include(cls, header_path: Path, include: str) -> str:
        include = include.strip()
        if include.startswith("#"):
            return include
        elif include.startswith("<"):
            return f'#include {include}'
        else:
            relative_path = os.path.relpath(include, header_path.parent)
            return f'#include "{relative_path}"'

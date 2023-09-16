"""
C header file generator
"""

from pathlib import Path
import re

from format_utils import BindingCode


class HeaderWriter:
    """C header file writer class"""
    def __init__(self, *pathsegments):
        self.base_dir = Path(*pathsegments)

    def write_header(self,
                     contents: BindingCode,
                     *pathsegments: str):
        header_name = Path(*pathsegments)
        guard_name = re.sub("[^a-zA-Z0-9_]", "_", str(header_name)).upper()
        define = f"__GDEXTENSION_LITE_GENERATED_{guard_name}_H__"
        lines = [
            "// This file was automatically generated",
            "// Do not modify this file",
            f"#ifndef {define}",
            f"#define {define}",
            "",
        ]
        if contents['includes']:
            lines.append(contents['includes'])
            lines.append("")
        lines.extend([
            contents.prototype,
            "",
            f"#endif  // {define}",
        ])

        if contents.implementation:
            define = f"__GDEXTENSION_LITE_GENERATED_{guard_name}_H_IMPLEMENTATION__"
            implementation_macros_h = ("../" * len(pathsegments)) + "implementation-macros.h"
            lines.extend([
                "",
                "#ifdef GDEXTENSION_LITE_IMPLEMENTATION",
                f"#ifndef {define}",
                f"#define {define}",
                "",
                f'#include "{implementation_macros_h}"',
                "",
                contents.implementation,
                "",
                f"#endif  // {define}",
                "#endif  // GDEXTENSION_LITE_IMPLEMENTATION",
            ])
        filename = self.base_dir.joinpath(header_name).with_suffix(".h")
        filename.parent.mkdir(exist_ok=True)
        with open(filename, 'w') as file:
            file.write('\n'.join(lines))

"""
C header file generator
"""

from pathlib import Path


class HeaderWriter:
    """C header file writer class"""
    def __init__(self, *pathsegments):
        self.base_dir = Path(*pathsegments)
        self.base_dir.mkdir(exist_ok=True)

    def write_header(self, header_name: str, contents: str):
        filename = self.base_dir.joinpath(header_name + ".h")
        define = f"__GDEXTENSION_C_GENERATED_{header_name.upper()}_H__"
        lines = (
            "// This file was automatically generated",
            "// Do not modify this file",
            f"#ifndef {define}",
            f"#define {define}",
            "",
            contents,
            "",
            "#endif",
        )
        with open(filename, 'w') as file:
            file.write('\n'.join(lines))

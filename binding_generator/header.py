"""
C header file generator
"""

from pathlib import Path


class HeaderWriter:
    """C header file writer class"""
    def __init__(self, *pathsegments):
        self.base_dir = Path(*pathsegments)

    def write_header(self, contents: str, *pathsegments):
        filename = self.base_dir.joinpath(*pathsegments).with_suffix(".h")
        filename.parent.mkdir(exist_ok=True)
        define = f"__GDEXTENSION_LITE_GENERATED_{filename.stem}_H__"
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

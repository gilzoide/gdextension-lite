#!/bin/env python
"""
GDExtension C binding generator script

Given the path to `extension_api.json` file generated by Godot 4, it prints
several header files with generated bindings.

Usage:
    binding_generator.py EXTENSION_API_PATH OUTPUT_DIR
"""

import json
import sys

from enums import generate_all_enums
from header import HeaderWriter


def main():
    if len(sys.argv) < 3:
        sys.stderr.write(__doc__.lstrip())
        sys.exit(-1)

    extension_api_path = sys.argv[1]
    output_dir = sys.argv[2]

    with open(extension_api_path, 'r') as file:
        extension_api = json.load(file)

    header_writer = HeaderWriter(*output_dir.split("/"))
    header_writer.write_header(
        "global_enums",
        generate_all_enums(extension_api['global_enums'])
    )


if __name__ == "__main__":
    main()

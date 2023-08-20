#!/bin/env python
"""
GDExtension C binding generator script

Given the path to `extension_api.json` file generated by Godot 4, it writes
several header files with generated bindings in the given output directory.

Usage:
    binding_generator.py EXTENSION_API_PATH OUTPUT_DIR
"""

import json
import sys

from builtin_classes import generate_builtin_class, generate_initialize_all_builtin_classes
from classes import generate_class_stub_header, generate_all_class_stubs, generate_class_method_header, generate_initialize_all_classes
from enums import generate_all_enums
from format_utils import format_type_snake_case
from header import HeaderWriter
from json_types import ExtensionApi
from utility_functions import generate_utility_functions


def main():
    if len(sys.argv) < 3:
        sys.stderr.write(__doc__.lstrip())
        sys.exit(-1)

    extension_api_path = sys.argv[1]
    output_dir = sys.argv[2]

    with open(extension_api_path, 'r') as file:
        extension_api: ExtensionApi = json.load(file)

    header_writer = HeaderWriter(*output_dir.split("/"))
    header_writer.write_header(
        generate_all_enums(extension_api["global_enums"]),
        "global_enums",
    )

    # Builtin Classes (a.k.a Variants)
    builtin_classes = [
        cls
        for cls in extension_api["builtin_classes"]
        if cls["name"] != "Nil"
    ]
    for builtin_class in builtin_classes:
        contents, implementation = generate_builtin_class(builtin_class)
        header_writer.write_header(contents,
                                   "variant", format_type_snake_case(builtin_class["name"]),
                                   implementation=implementation)
    contents, implementation = generate_initialize_all_builtin_classes(builtin_classes)
    header_writer.write_header(contents,
                               "variant", "all",
                               implementation=implementation)

    contents, implementation = generate_utility_functions(extension_api["utility_functions"])
    header_writer.write_header(contents,
                               "utility_functions",
                               implementation=implementation)

    # Classes
    for cls in extension_api["classes"]:
        contents, implementation = generate_class_stub_header(cls)
        header_writer.write_header(contents,
                                   "class-stubs", format_type_snake_case(cls["name"]),
                                   implementation=implementation)
        contents, implementation = generate_class_method_header(cls)
        header_writer.write_header(contents,
                                   "class-methods", format_type_snake_case(cls["name"]),
                                   implementation=implementation)
    contents, implementation = generate_all_class_stubs(extension_api["classes"])
    header_writer.write_header(contents,
                               "class-stubs", "all",
                               implementation=implementation)
    contents, implementation = generate_initialize_all_classes(extension_api["classes"])
    header_writer.write_header(contents,
                               "class-methods", "all",
                               implementation=implementation)


if __name__ == "__main__":
    main()

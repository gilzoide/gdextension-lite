from textwrap import indent

from common.binding_code import BindingCode
from common.code_generator import CodeGenerator
from format_utils import (NON_STRUCT_TYPES,
                          format_cpp_argument_forward,
                          format_parameter,
                          format_parameter_const,
                          format_type_to_variant_enum,
                          format_value_to_ptr,
                          should_generate_constructor)
from json_types import *


class BuiltinClassConstructor(CodeGenerator):
    """
    Builtin classes (a.k.a Variants) Constructor structure
    """
    def __init__(self, type_name: str, constructor: Constructor):
        self.class_name = type_name
        self.constructor = constructor

        self.function_name = f"new_{type_name}"
        arguments = constructor.get("arguments", [])
        if arguments:
            self.function_name += "_from" + "".join(f"_{arg['type']}"
                                                    for arg in arguments)
        self.arguments = arguments
        proto_arguments = [
            format_parameter_const(arg["type"], arg["name"])
            for arg in arguments
        ]
        self.prototype = f"godot_{type_name} godot_{self.function_name}({', '.join(proto_arguments)})"
        self.placement_prototype = f"void godot_placement_{self.function_name}({', '.join([f'godot_{type_name} *self'] + proto_arguments)})"

    def get_c_code(self) -> BindingCode:
        call_arguments = "".join([", " + format_value_to_ptr(arg['type'], arg['name']) for arg in self.arguments])
        forward_arguments = "".join([", " + arg['name'] for arg in self.arguments])
        return BindingCode(
            "\n".join([
                f"static inline {self.placement_prototype} {{",
                    f"\tGDEXTENSION_LITE_VARIANT_CONSTRUCTOR_IMPL({format_type_to_variant_enum(self.class_name)}, {self.constructor['index']}{call_arguments});",
                f"}}",
                f"static inline {self.prototype} {{",
                    f"\tGDEXTENSION_LITE_RETURN_PLACEMENT_NEW(godot_{self.class_name}, godot_placement_{self.function_name}{forward_arguments});",
                f"}}",
            ]),
        )

    def get_cpp_code(self) -> BindingCode:
        if self.class_name in NON_STRUCT_TYPES:
            return BindingCode("", "")
        proto_arguments = [
            format_parameter(arg['type'], arg['name'], is_const=True, is_cpp=True, default_value=arg.get('default_value'))
            for arg in self.arguments
        ]
        placement_call_arguments = ["this"] + [
            format_cpp_argument_forward(arg['type'], arg['name'])
            for arg in self.arguments
        ]
        return BindingCode(
            f"{self.class_name}({', '.join(proto_arguments)});",
            "\n".join([
                f"{self.class_name}::{self.class_name}({', '.join(proto_arguments)}) {{",
                    f"\tgodot_placement_{self.function_name}({', '.join(placement_call_arguments)});",
                f"}}",
            ]),
        )

    @classmethod
    def get_all_constructors(
        cls,
        builtin_class: BuiltinClass,
    ) -> list['BuiltinClassConstructor']:
        type_name = builtin_class["name"]
        return [
            cls(type_name, ctor)
            for ctor in builtin_class["constructors"]
            if should_generate_constructor(type_name, ctor)
        ]


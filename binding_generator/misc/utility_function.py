import re

from common.binding_code import BindingCode
from common.code_generator import CodeGenerator
from format_utils import (format_parameter_const,
                          format_return_type,
                          format_value_to_ptr)

from json_types import *


class UtilityFunctionCode(CodeGenerator):
    """
    Utility Functions
    """
    SPLIT_ARGUMENTS_RE = re.compile(r"(?<=[\w)]),")
    ARGUMENT_NAME_RE = re.compile(r"(\w+)($|\))")

    def __init__(self, function: UtilityFunction):
        self.function = function
        self.return_type = format_return_type(function.get("return_type"))

        proto_args = []
        self.arguments = function.get("arguments", [])
        if self.arguments:
            proto_args.extend(
                format_parameter_const(arg["type"], arg["name"])
                for arg in self.arguments
            )

        self.is_vararg = function.get("is_vararg")
        if self.is_vararg:
            proto_args.append("const godot_Variant **argv")
            proto_args.append("godot_int argc")

        self.prototype = f"{self.return_type} godot_{function['name']}({', '.join(proto_args)})"

    def get_c_code(self) -> BindingCode:
        impl_macro = "GDEXTENSION_LITE_UTILITY_FUNCTION_IMPL"
        if self.is_vararg:
            impl_macro += "_VARIADIC"
        if self.return_type == "void":
            impl_macro += "_VOID"
        macro_args = [
            self.function['name'],
            str(self.function.get('hash', 0)),
            self.return_type,
            *(format_value_to_ptr(arg['type'], arg['name']) for arg in self.arguments),
        ]
        return BindingCode(
            f"GDEXTENSION_LITE_DECL {self.prototype};",
            "\n".join([
                f"{self.prototype} {{",
                    f"\t{impl_macro}({', '.join(macro_args)});",
                f"}}",
            ]),
        )

from textwrap import indent

from common.binding_code import BindingCode
from common.code_generator import CodeGenerator
from format_utils import (format_parameter,
                          format_parameter_const,
                          format_return_type,
                          format_value_to_ptr)
from json_types import *


class ClassMethod(CodeGenerator):
    """
    Builtin classes (a.k.a Variants) Constructor structure
    """
    def __init__(self, type_name: str, method: Method):
        self.class_name = type_name

        self.method = method
        return_value = method.get('return_value')
        return_type = return_value["type"] if return_value else None
        self.return_type = format_return_type(return_type)

        proto_arguments = []
        self.is_static = method.get('is_static', False)
        if not self.is_static:
            is_const = method.get('is_const', False)
            proto_arguments.append(format_parameter(type_name,
                                               "self",
                                               is_const=is_const))
        arguments = method.get("arguments", [])
        if arguments:
            proto_arguments.extend(
                format_parameter_const(arg["type"], arg["name"])
                for arg in arguments
            )

        self.is_vararg = method.get('is_vararg', False)
        if self.is_vararg:
            proto_arguments.append("godot_int argc")
            proto_arguments.append("const godot_Variant **argv")

        self.arguments = arguments
        self.function_name = f"{type_name}_{method['name']}"
        self.prototype = f"""{self.return_type} godot_{self.function_name}({
                                ', '.join(proto_arguments)
                            })"""

    def get_c_code(self) -> BindingCode:
        impl_macro = "GDEXTENSION_LITE_CLASS_METHOD_IMPL"
        if self.is_vararg:
            impl_macro += "_VARIADIC"
        if self.return_type == "void":
            impl_macro += "_VOID"
        macro_args = [
            self.class_name,
            self.method['name'],
            str(self.method.get('hash', 0)),
            self.return_type,
            "NULL" if self.is_static else "self",
            *(arg['name'] if self.is_vararg else format_value_to_ptr(arg['type'], arg['name'])
              for arg in self.arguments),
        ]
        return BindingCode(
            f"GDEXTENSION_LITE_DECL {self.prototype};",
            '\n'.join([
                f"{self.prototype} {{",
                    f"\t{impl_macro}({', '.join(macro_args)})",
                f"}}",
            ]),
        )

    @classmethod
    def get_all_methods(
        cls,
        target_class: Class,
    ) -> list['ClassMethod']:
        type_name = target_class['name']
        return [
            cls(type_name, method)
            for method in target_class.get('methods', [])
        ]




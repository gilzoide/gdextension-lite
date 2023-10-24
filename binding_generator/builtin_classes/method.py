from textwrap import indent

from common.binding_code import BindingCode
from common.code_generator import CodeGenerator
from format_utils import (format_cpp_argument_forward,
                          format_parameter,
                          format_parameter_const,
                          format_return_type,
                          format_type_to_variant_enum,
                          format_value_to_ptr,
                          should_generate_method)
from json_types import *


class BuiltinClassMethod(CodeGenerator):
    """
    Builtin classes (a.k.a Variants) Constructor structure
    """
    def __init__(self, type_name: str, method: BuiltinClassMethod):
        self.class_name = type_name
        self.variant_type_enum = format_type_to_variant_enum(type_name)

        self.method = method
        self.return_type = format_return_type(method.get('return_type'))

        proto_arguments = []
        self.is_static = method.get('is_static', False)
        self.is_const = method.get('is_const', False)
        if not self.is_static:
            proto_arguments.append(format_parameter(type_name,
                                                    "self",
                                                    is_const=self.is_const))
        arguments = method.get("arguments", [])
        if arguments:
            proto_arguments.extend(
                format_parameter_const(arg["type"], arg["name"])
                for arg in arguments
            )

        self.non_vararg_argc = len(proto_arguments)
        self.is_vararg = method.get('is_vararg', False)
        if self.is_vararg:
            proto_arguments.append("const godot_Variant **argv")
            proto_arguments.append("godot_int argc")

        self.arguments = arguments
        self.function_name = f"{type_name}_{method['name']}"
        self.prototype = f"""{self.return_type} godot_{self.function_name}({
                                ', '.join(proto_arguments)
                            })"""

    def get_c_code(self) -> BindingCode:
        impl_macro = "GDEXTENSION_LITE_VARIANT_METHOD_IMPL"
        if self.is_vararg:
            impl_macro += "_VARIADIC"
        if self.return_type == "void":
            impl_macro += "_VOID"
        macro_args = [
            self.method['name'],
            str(self.method.get('hash', 0)),
            self.variant_type_enum,
            self.return_type,
            "NULL" if self.is_static else "self",
            *(format_value_to_ptr(arg['type'], arg['name']) for arg in self.arguments),
        ]
        return BindingCode(
            f"GDEXTENSION_LITE_DECL {self.prototype};",
            '\n'.join([
                f"{self.prototype} {{",
                    f"\t{impl_macro}({', '.join(macro_args)})",
                f"}}",
            ]),
        )

    def get_cpp_code(self) -> BindingCode:
        proto_arguments_with_default = [
            format_parameter(arg['type'], arg['name'], is_const=True, is_cpp=True, default_value=arg.get('default_value'))
            for arg in self.arguments
        ]
        proto_arguments = [
            format_parameter(arg['type'], arg['name'], is_const=True, is_cpp=True)
            for arg in self.arguments
        ]
        call_arguments = ["this"] if not self.is_static else []
        call_arguments.extend([
            format_cpp_argument_forward(arg['type'], arg['name'])
            for arg in self.arguments
        ])
        if self.is_vararg:
            vararg_template = "template<class... Args> "
            vararg_to_array = "GDEXTENSION_LITE_VARIADIC_TEMPLATE_TO_ARRAY(args, argc, argv);"
            proto_arguments_with_default.append("Args ...args")
            proto_arguments.append("Args ...args")
            call_arguments.append("argc")
            call_arguments.append("argv")
        else:
            vararg_template = ""
            vararg_to_array = ""
        return BindingCode(
            (f"{vararg_template}"
             f"{'static ' if self.is_static else ''}"
             f"{self.return_type} {self.method['name']}({', '.join(proto_arguments_with_default)})"
             f"{' const' if self.is_const else ''};"),
            "\n".join(line for line in [
                (f"{vararg_template}"
                 f"{self.return_type} {self.class_name}::{self.method['name']}({', '.join(proto_arguments)})"
                 f"{' const' if self.is_const else ''} {{"),
                    f"\t{vararg_to_array}",
                    (f"\t{'return ' if self.return_type != 'void' else ''}"
                     f"godot_{self.function_name}({', '.join(call_arguments)});"),
                f"}}",
            ] if line.strip()),
        )

    @classmethod
    def get_all_methods(
        cls,
        builtin_class: BuiltinClass,
    ) -> list['BuiltinClassMethod']:
        type_name = builtin_class['name']
        members = builtin_class.get('members', [])
        return [
            cls(type_name, method)
            for method in builtin_class.get('methods', [])
            if should_generate_method(method, members)
        ]



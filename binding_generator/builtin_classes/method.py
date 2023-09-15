from textwrap import indent

from format_utils import (BindingCode,
                          format_arguments_array,
                          format_arguments_count,
                          format_parameter,
                          format_parameter_const,
                          format_return_type,
                          format_type_to_variant_enum,
                          format_vararg_macro,
                          should_generate_method)
from json_types import *


class BuiltinClassMethod:
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
        if not self.is_static:
            is_const = method.get('is_const', False)
            proto_arguments.append(format_parameter(type_name,
                                               "self",
                                               is_const=is_const))
        arguments = method.get("arguments")
        if arguments:
            proto_arguments.extend(
                format_parameter_const(arg["type"], arg["name"])
                for arg in arguments
            )

        self.non_vararg_argc = len(proto_arguments)
        self.is_vararg = method.get('is_vararg', False)
        if self.is_vararg:
            proto_arguments.append("godot_int argc")
            proto_arguments.append("const godot_Variant **argv")

        self.arguments = arguments
        self.function_name = f"{type_name}_{method['name']}"
        self.prototype = f"""{self.return_type} godot_{self.function_name}({
                                ', '.join(proto_arguments)
                            })"""

        self.ptr_function_name = f"godot_ptr_{type_name}_{method['name']}"
        self.ptr_prototype = f"GDExtensionPtrBuiltInMethod {self.ptr_function_name}"

    def get_c_code(self) -> BindingCode:
        vararg_macro = (
            format_vararg_macro(self.function_name, self.non_vararg_argc)
            if self.is_vararg
            else ""
        )
        return BindingCode(
            '\n'.join(line for line in [
                f"{self.prototype};",
                vararg_macro,
            ] if line.strip()),
            '\n'.join(line for line in [
                f"{self.ptr_prototype};",
                f"{self.prototype} {{",
                    f"""\tGDEXTENSION_LITE_LAZY_INIT_VARIANT_METHOD({
                            self.class_name
                        }, {
                            self.variant_type_enum
                        }, {
                            self.method['name']
                        }, {
                            self.method['hash']
                        });""",
                    (f"\t{self.return_type} _ret;"
                     if self.return_type != "void"
                     else ""),
                    f"{indent(format_arguments_array('_args', self.arguments, self.is_vararg), '	')}",
                    f"""\t{self.ptr_function_name}({
                        "NULL"
                        if self.is_static
                        else "(GDExtensionTypePtr) self"
                    }, _args, {
                        "&_ret"
                        if self.return_type != "void"
                        else "NULL"
                    }, {
                        format_arguments_count(self.arguments, self.is_vararg)
                    });""",
                    (f"\treturn _ret;"
                     if self.return_type != "void"
                     else ""),
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



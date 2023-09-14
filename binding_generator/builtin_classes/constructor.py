from textwrap import indent

from format_utils import (BindingCode,
                          code_block,
                          format_arguments_array,
                          format_parameter_const,
                          format_type_to_variant_enum,
                          should_generate_constructor)
from json_types import *


class BuiltinClassConstructor:
    """
    Builtin classes (a.k.a Variants) Constructor structure
    """
    def __init__(self, type_name: str, constructor: Constructor):
        self.class_name = type_name
        self.variant_type_enum = format_type_to_variant_enum(type_name)
        self.constructor_index = constructor["index"]
        self.constructor_name = f"new_{type_name}"
        arguments = constructor.get("arguments")
        if arguments:
            self.constructor_name += "_from" + "".join(f"_{arg['type']}"
                                                       for arg in arguments)

            proto_arguments = ", ".join(
                format_parameter_const(arg["type"], arg["name"])
                for arg in arguments
            )
        else:
            proto_arguments = ""
        self.arguments = arguments
        self.function_name = f"godot_{self.constructor_name}"
        self.return_type = f"godot_{type_name}"
        self.prototype = f"{self.return_type} {self.function_name}({proto_arguments})"

        self.ptr_type = "GDExtensionPtrConstructor"
        self.ptr_function_name = f"godot_ptr_{self.constructor_name}"
        self.ptr_prototype = f"{self.ptr_type} {self.ptr_function_name}"

    def get_c_code(self) -> BindingCode:
        return BindingCode(
            code_block(f"""
                extern {self.ptr_prototype};
                {self.prototype};
            """),
            '\n'.join([
                f"{self.ptr_prototype};",
                f"{self.prototype} {{",
                    f"""\tGDEXTENSION_LITE_LAZY_INIT_VARIANT_CONSTRUCTOR({
                            self.constructor_name
                        }, {
                            self.variant_type_enum
                        }, {
                            self.constructor_index
                        });""",
                    f"\t{self.return_type} self;",
                    f"{indent(format_arguments_array('_args', self.arguments), '	')}",
                    f"\t{self.ptr_function_name}(&self, _args);",
                    f"\treturn self;",
                "}",
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


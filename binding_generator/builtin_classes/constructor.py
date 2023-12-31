from textwrap import indent

from common.binding_code import BindingCode
from common.code_generator import CodeGenerator
from format_utils import (format_parameter_const,
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

        self.arguments = constructor.get("arguments", [])
        if self.arguments:
            function_suffix = "_with" + "".join(f"_{arg['type']}"
                                                for arg in self.arguments)
        else:
            function_suffix = ""
        
        proto_arguments = [
            format_parameter_const(arg["type"], arg["name"])
            for arg in self.arguments
        ]
        self.new_name = f"godot_new_{type_name}{function_suffix}"
        self.prototype = f"godot_{type_name} {self.new_name}({', '.join(proto_arguments)})"

    def get_c_code(self) -> BindingCode:
        macro_args = [
            f"{self.class_name}",
            format_type_to_variant_enum(self.class_name),
            str(self.constructor['index']),
            *(format_value_to_ptr(arg['type'], arg['name']) for arg in self.arguments),
        ]
        return BindingCode(
            "\n".join([
                f"GDEXTENSION_LITE_DECL {self.prototype};",
            ]),
            "\n".join([
                f"{self.prototype} {{",
                    f"\tGDEXTENSION_LITE_VARIANT_CONSTRUCTOR_IMPL({', '.join(macro_args)});",
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
            (
                BuiltinClassConstructorFromString(type_name, ctor)
                if BuiltinClassConstructorFromString.is_constructor_from_string(ctor)
                else cls(type_name, ctor)
            )
            for ctor in builtin_class["constructors"]
            if should_generate_constructor(type_name, ctor)
        ]


class BuiltinClassConstructorFromString(BuiltinClassConstructor):
    """
    Special handling of constructors that receive a single String parameter
    """
    EXTRA_CONSTRUCTORS = {
        'latin1': 'const char *',
        'utf8': 'const char *',
        'utf16': 'const char16_t *',
        'utf32': 'const char32_t *',
        'wide': 'const wchar_t *',
    }

    @classmethod
    def is_constructor_from_string(cls, ctor: Constructor) -> bool:
        arguments = ctor.get('arguments', [])
        return len(arguments) == 1 and arguments[0]['type'] == 'String'

    def get_c_code(self) -> BindingCode:
        code = super().get_c_code()
        for extra_name, extra_arg in self.EXTRA_CONSTRUCTORS.items():
            contents_arg = f"{extra_arg}p_contents"
            size_arg = "godot_int p_size"
            code.prototype += "\n".join([
                "",
                f"GDEXTENSION_LITE_DECL godot_{self.class_name} godot_new_{self.class_name}_with_{extra_name}_chars({contents_arg});",
                f"GDEXTENSION_LITE_DECL godot_{self.class_name} godot_new_{self.class_name}_with_{extra_name}_chars_and_len({contents_arg}, {size_arg});",
            ])
            impl_macro = "GDEXTENSION_LITE_VARIANT_CONSTRUCTOR_IMPL_FROM_CHARS" if self.class_name == "String" else "GDEXTENSION_LITE_VARIANT_CONSTRUCTOR_IMPL_FROM_STRING"
            code.implementation += "\n".join([
                "",
                f"godot_{self.class_name} godot_new_{self.class_name}_with_{extra_name}_chars({contents_arg}) {{",
                    f"\t{impl_macro}({self.class_name}, {extra_name}_chars, p_contents);",
                f"}}",
                f"godot_{self.class_name} godot_new_{self.class_name}_with_{extra_name}_chars_and_len({contents_arg}, {size_arg}) {{",
                    f"\t{impl_macro}({self.class_name}, {extra_name}_chars_and_len, p_contents, p_size);",
                f"}}",
            ])
        return code

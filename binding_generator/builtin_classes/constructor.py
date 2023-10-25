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
        self.new_name = f"godot_{type_name}_new{function_suffix}"
        self.placement_new_name = f"godot_{self.class_name}_placement_new{function_suffix}"
        self.prototype = f"godot_{type_name} {self.new_name}({', '.join(proto_arguments)})"
        self.placement_prototype = f"void {self.placement_new_name}({', '.join([f'godot_{type_name} *self'] + proto_arguments)})"

    def get_c_code(self) -> BindingCode:
        call_arguments = "".join([", " + format_value_to_ptr(arg['type'], arg['name']) for arg in self.arguments])
        forward_arguments = "".join([", " + arg['name'] for arg in self.arguments])
        return BindingCode(
            "\n".join([
                f"GDEXTENSION_LITE_DECL {self.placement_prototype};",
                f"GDEXTENSION_LITE_DECL {self.prototype};",
            ]),
            "\n".join([
                f"{self.placement_prototype} {{",
                    f"\tGDEXTENSION_LITE_VARIANT_CONSTRUCTOR_IMPL({format_type_to_variant_enum(self.class_name)}, {self.constructor['index']}{call_arguments});",
                f"}}",
                f"{self.prototype} {{",
                    f"\tGDEXTENSION_LITE_RETURN_PLACEMENT_NEW(godot_{self.class_name}, {self.placement_new_name}{forward_arguments});",
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
                    f"\t{self.placement_new_name}({', '.join(placement_call_arguments)});",
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
                f"GDEXTENSION_LITE_DECL void godot_{self.class_name}_placement_new_with_{extra_name}_chars(godot_{self.class_name} *self, {contents_arg});",
                f"GDEXTENSION_LITE_DECL void godot_{self.class_name}_placement_new_with_{extra_name}_chars_and_len(godot_{self.class_name} *self, {contents_arg}, {size_arg});",
                f"GDEXTENSION_LITE_DECL godot_{self.class_name} godot_{self.class_name}_new_with_{extra_name}_chars({contents_arg});",
                f"GDEXTENSION_LITE_DECL godot_{self.class_name} godot_{self.class_name}_new_with_{extra_name}_chars_and_len({contents_arg}, {size_arg});",
            ])
            impl_macro = "GDEXTENSION_LITE_VARIANT_CONSTRUCTOR_IMPL_FROM_CHARS" if self.class_name == "String" else "GDEXTENSION_LITE_VARIANT_CONSTRUCTOR_IMPL_FROM_STRING"
            code.implementation += "\n".join([
                "",
                f"void godot_{self.class_name}_placement_new_with_{extra_name}_chars(godot_{self.class_name} *self, {contents_arg}) {{",
                    f"\t{impl_macro}({self.class_name}, {extra_name}_chars, p_contents);",
                f"}}",
                f"void godot_{self.class_name}_placement_new_with_{extra_name}_chars_and_len(godot_{self.class_name} *self, {contents_arg}, {size_arg}) {{",
                    f"\t{impl_macro}({self.class_name}, {extra_name}_chars_and_len, p_contents, p_size);",
                f"}}",
                f"godot_{self.class_name} godot_{self.class_name}_new_with_{extra_name}_chars({contents_arg}) {{",
                    f"\tGDEXTENSION_LITE_RETURN_PLACEMENT_NEW(godot_{self.class_name}, godot_{self.class_name}_placement_new_with_{extra_name}_chars, p_contents);",
                f"}}",
                f"godot_{self.class_name} godot_{self.class_name}_new_with_{extra_name}_chars_and_len({contents_arg}, {size_arg}) {{",
                    f"\tGDEXTENSION_LITE_RETURN_PLACEMENT_NEW(godot_{self.class_name}, godot_{self.class_name}_placement_new_with_{extra_name}_chars_and_len, p_contents, p_size);",
                f"}}",
            ])
        return code

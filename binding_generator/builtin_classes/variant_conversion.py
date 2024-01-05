from common.binding_code import BindingCode
from common.code_generator import CodeGenerator
from format_utils import (format_parameter_const,
                          format_type_to_variant_enum,
                          format_value_to_ptr)
from json_types import *


class BuiltinClassFromVariantConversion(CodeGenerator):
    """
    Conversion from Variant to builtin class
    """
    def __init__(self, type_name: str):
        self.class_name = type_name
        self.variant_type_enum = format_type_to_variant_enum(type_name)
        parameter = format_parameter_const('Variant', 'value')
        self.prototype = f"godot_{type_name} godot_new_{type_name}_with_Variant({parameter})"

    def get_c_code(self) -> BindingCode:
        macro_args = [
            self.class_name,
            self.variant_type_enum,
            "value",
        ]
        return BindingCode(
            f"GDEXTENSION_LITE_DECL {self.prototype};",
            "\n".join([
                f"{self.prototype} {{",
                    f"\tGDEXTENSION_LITE_TYPE_FROM_VARIANT_IMPL({', '.join(macro_args)});",
                f"}}",
            ]),
        )


class BuiltinClassToVariantConversion(CodeGenerator):
    """
    Conversion from builtin class to Variant
    """
    def __init__(self, type_name: str):
        self.class_name = type_name
        self.variant_type_enum = format_type_to_variant_enum(type_name)
        parameter = format_parameter_const(type_name, 'value')
        self.prototype = f"godot_Variant godot_new_Variant_with_{type_name}({parameter})"

    def get_c_code(self) -> BindingCode:
        macro_args = [
            self.class_name,
            self.variant_type_enum,
            format_value_to_ptr(self.class_name, 'value'),
        ]
        return BindingCode(
            f"GDEXTENSION_LITE_DECL {self.prototype};",
            "\n".join([
                f"{self.prototype} {{",
                    f"\tGDEXTENSION_LITE_VARIANT_FROM_TYPE_IMPL({', '.join(macro_args)});",
                f"}}",
            ]),
        )



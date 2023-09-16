from common.binding_code import BindingCode
from common.code_generator import CodeGenerator
from format_utils import (format_parameter,
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
        self.return_type = f"godot_{type_name}"

        self.function_name = f"godot_new_{type_name}_from_Variant"
        parameter = format_parameter('Variant', 'value')
        self.prototype = f"{self.return_type} {self.function_name}({parameter})"

        self.ptr_function_name = f"godot_ptr_new_{type_name}_from_Variant"
        ptr_type = "GDExtensionTypeFromVariantConstructorFunc"
        self.ptr_prototype = f"{ptr_type} {self.ptr_function_name}"

    def get_c_code(self) -> BindingCode:
        return BindingCode(
            f"{self.prototype};",
            '\n'.join([
                f"{self.ptr_prototype};",
                f"{self.prototype} {{",
                    f"""\tGDEXTENSION_LITE_LAZY_INIT_TYPE_FROM_VARIANT({
                            self.class_name
                        }, {
                            self.variant_type_enum
                        });""",
                    f"\t{self.return_type} self;",
                    f"\t{self.ptr_function_name}(&self, value);",
                    f"\treturn self;",
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
        self.return_type = f"godot_Variant"

        self.function_name = f"godot_new_Variant_from_{type_name}"
        parameter = format_parameter(type_name, 'value')
        self.prototype = f"{self.return_type} {self.function_name}({parameter})"

        self.ptr_function_name = f"godot_ptr_new_Variant_from_{type_name}"
        ptr_type = "GDExtensionVariantFromTypeConstructorFunc"
        self.ptr_prototype = f"{ptr_type} {self.ptr_function_name}"

    def get_c_code(self) -> BindingCode:
        return BindingCode(
            f"{self.prototype};",
            '\n'.join([
                f"{self.ptr_prototype};",
                f"{self.prototype} {{",
                    f"""\tGDEXTENSION_LITE_LAZY_INIT_VARIANT_FROM_TYPE({
                            self.class_name
                        }, {
                            self.variant_type_enum
                        });""",
                    f"\t{self.return_type} self;",
                    f"""\t{self.ptr_function_name}(&self, {
                            format_value_to_ptr(self.class_name, 'value')
                        });""",
                    f"\treturn self;",
                f"}}",
            ]),
        )



from common.binding_code import BindingCode
from common.code_generator import CodeGenerator
from format_utils import (format_parameter,
                          format_type_to_variant_enum,
                          format_value_to_ptr)
from json_types import *


class VariantCode(CodeGenerator):
    """
    Generated code for Variant type
    """
    def __init__(self, types: list[BuiltinClass]) -> None:
        self.types = [t["name"] for t in types]

    def get_c_code(self) -> BindingCode:

        return BindingCode(
            "\n".join([
                f"#define godot_new_Variant(x) \\",
                f"\t_Generic((x), \\",
                *(f"\t\t{format_parameter(t, '')}: godot_new_Variant_from_{t}, \\" for t in self.types[:-1]),
                f"\t\t{format_parameter(self.types[-1], '')}: godot_new_Variant_from_{self.types[-1]} \\",
                f"\t)(x)"
            ]),
        )

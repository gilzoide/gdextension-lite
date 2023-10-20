from common.binding_code import BindingCode
from common.code_generator import CodeGenerator
from format_utils import (format_parameter)
from json_types import *


class VariantCode(CodeGenerator):
    """
    Generated code for Variant type
    """
    def __init__(self, types: list[BuiltinClass]) -> None:
        self.types = [t["name"] for t in types]
    
    def _format_new(self, t: str):
        return f"{format_parameter(t, '')}: godot_new_Variant_from_{t}, const {format_parameter(t, '')}: godot_new_Variant_from_{t}"

    def get_c_code(self) -> BindingCode:
        return BindingCode(
            "\n".join([
                f"#define godot_new_Variant(x) \\",
                f"\t_Generic((x), \\",
                *(f"\t\t{self._format_new(t)}, \\" for t in self.types),
                f"\t\tgodot_Object *: godot_new_Variant_from_Object, const godot_Object *: godot_new_Variant_from_Object \\",
                f"\t)(x)"
            ]),
        )

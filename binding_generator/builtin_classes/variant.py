from common.binding_code import BindingCode
from common.code_generator import CodeGenerator
from format_utils import (format_parameter,
                          format_parameter_const,
                          format_value_to_ptr)
from json_types import *


class VariantCode(CodeGenerator):
    """
    Generated code for Variant type
    """
    def __init__(self, types: list[BuiltinClass]) -> None:
        self.types = [t["name"] for t in types]
    
    def _format_new(self, t: str):
        return f"{format_parameter(t, '')}: godot_new_Variant_from_{t}, const {format_parameter(t, '')}: godot_new_Variant_from_{t}"

    def _get_c11_generic(self):
        return "\n".join([
            f"#define godot_new_Variant(x) \\",
            f"\t_Generic((x), \\",
            *(f"\t\t{self._format_new(t)}, \\" for t in self.types),
            f"\t\tgodot_Object *: godot_new_Variant_from_Object, const godot_Object *: godot_new_Variant_from_Object \\",
            f"\t)(x)"
        ])

    def _get_cpp_overload(self, t: str):
        prototype = f"GDEXTENSION_LITE_INLINE godot_Variant godot_new_Variant({format_parameter_const(t, 'value')})"
        return f"{prototype} {{ return godot_new_Variant_from_{t}(value); }}"

    def _get_cpp_overloads(self):
        return "\n".join([
            *(self._get_cpp_overload(t) for t in self.types),
            f"GDEXTENSION_LITE_INLINE godot_Variant godot_new_Variant(const godot_Object *value) {{ return godot_new_Variant_from_Object(value); }}",
        ])

    def get_c_code(self) -> BindingCode:
        return BindingCode(
            "\n".join([
                "#ifdef __cplusplus",
                self._get_cpp_overloads(),
                "#else",
                self._get_c11_generic(),
                "#endif",
            ]),
            includes=["variant/all.h"],
            cpp_in_h=["true"],
        )

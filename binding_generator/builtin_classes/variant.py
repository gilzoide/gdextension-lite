from .variant_conversion import (BuiltinClassToVariantConversion,
                                 BuiltinClassFromVariantConversion)
from common.binding_code import BindingCode
from common.code_generator import CodeGenerator
from format_utils import (format_parameter,
                          format_parameter_const)
from json_types import *


class VariantCode(CodeGenerator):
    """
    Generated code for Variant type
    """
    def __init__(self, types: list[BuiltinClass]) -> None:
        self.types = [t["name"] for t in types]
    
    def _format_new(self, t: str):
        return f"{format_parameter(t, '')}: godot_Variant_new_with_{t}, const {format_parameter(t, '')}: godot_Variant_new_with_{t}"

    def _get_c11_generic(self):
        return "\n".join([
            f"#define godot_Variant_new(x) \\",
            f"\t_Generic((x), \\",
            *(f"\t\t{self._format_new(t)}, \\" for t in self.types),
            f"\t\tgodot_Object *: godot_Variant_new_with_Object, const godot_Object *: godot_Variant_new_with_Object \\",
            f"\t)(x)"
        ])

    def _get_cpp_overload(self, t: str):
        prototype = f"GDEXTENSION_LITE_INLINE godot_Variant godot_Variant_new({format_parameter_const(t, 'value')})"
        return f"{prototype} {{ return godot_Variant_new_with_{t}(value); }}"

    def _get_cpp_overloads(self):
        return "\n".join([
            *(self._get_cpp_overload(t) for t in self.types),
            f"GDEXTENSION_LITE_INLINE godot_Variant godot_Variant_new(const godot_Object *value) {{ return godot_Variant_new_with_Object(value); }}",
        ])

    def get_c_code(self) -> BindingCode:
        return BindingCode.merge(
            [
                BindingCode.merge(BuiltinClassToVariantConversion(t).get_c_code() for t in self.types),
                BindingCode.merge(BuiltinClassFromVariantConversion(t).get_c_code() for t in self.types),
            ],
            prototype_outside_ifcpp=[
                "#ifdef __cplusplus",
                self._get_cpp_overloads(),
                "#else",
                self._get_c11_generic(),
                "#endif",
            ],
            includes=["../variant/all.h"],
            extra_newline=True,
        )

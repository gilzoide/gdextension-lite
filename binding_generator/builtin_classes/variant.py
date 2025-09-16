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
    
    def _format_new_variant(self, t: str):
        formatted_type = format_parameter(t, '')
        if formatted_type.endswith('*'):
            return f"{formatted_type}: godot_new_Variant_with_{t}, const {formatted_type}: godot_new_Variant_with_{t}"
        else:
            return f"{formatted_type}: godot_new_Variant_with_{t}"
    
    def _format_new_type(self, t: str):
        return f"godot_{t} *: godot_new_{t}_with_Variant"

    def _get_c11_generic(self):
        return "\n".join([
            f"#define godot_new_Variant(x) \\",
            f"\t_Generic((x), \\",
            *(f"\t\t{self._format_new_variant(t)}, \\" for t in self.types),
            f"\t\tgodot_Object *: godot_new_Variant_with_Object, const godot_Object *: godot_new_Variant_with_Object \\",
            f"\t)(x)",
            "",
            "GDEXTENSION_LITE_INLINE godot_Variant gdextension_lite_variant_deref(godot_Variant *value) { return *value; }",
            "",
            f"#define godot_Variant_extract(dest, variant) \\",
            f"\t(*dest = _Generic((dest), \\",
            *(f"\t\t{self._format_new_type(t)}, \\" for t in self.types),
            f"\t\tgodot_Object **: godot_new_Object_with_Variant, \\",
            f"\t\tgodot_Variant *: gdextension_lite_variant_deref, \\",
            f"\t\tgodot_Error *: godot_new_int_with_Variant \\",
            f"\t)(variant))",
        ])

    def _get_cpp_overload_variant(self, t: str):
        prototype = f"GDEXTENSION_LITE_INLINE godot_Variant godot_new_Variant({format_parameter_const(t, 'value')})"
        return f"{prototype} {{ return godot_new_Variant_with_{t}(value); }}"

    def _get_cpp_overload_type(self, t: str):
        prototype = f"GDEXTENSION_LITE_INLINE void godot_Variant_extract(godot_{t} *dest, godot_Variant *value)"
        return f"{prototype} {{ *dest = godot_new_{t}_with_Variant(value); }}"

    def _get_cpp_overloads(self):
        return "\n".join([
            *(self._get_cpp_overload_variant(t) for t in self.types),
            f"GDEXTENSION_LITE_INLINE godot_Variant godot_new_Variant(const godot_Object *value) {{ return godot_new_Variant_with_Object(value); }}",
            "",
            *(self._get_cpp_overload_type(t) for t in self.types),
            f"GDEXTENSION_LITE_INLINE void godot_Variant_extract(godot_Variant *dest, godot_Variant *value) {{ *dest = *value; }}",
        ])

    def get_c_code(self) -> BindingCode:
        return BindingCode.merge(
            [
                BindingCode.merge(BuiltinClassToVariantConversion(t).get_c_code() for t in self.types),
                BindingCode.merge(BuiltinClassFromVariantConversion(t).get_c_code() for t in self.types),
            ],
            prototype_outside_ifcpp=[
                "// Overloaded macros/functions",
                "#ifdef __cplusplus",
                self._get_cpp_overloads(),
                "#else",
                self._get_c11_generic(),
                "#endif",
            ],
            includes=["../variant/all.h"],
            extra_newline=True,
        )

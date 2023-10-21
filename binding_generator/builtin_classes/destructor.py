from common.binding_code import BindingCode
from common.code_generator import CodeGenerator
from format_utils import format_type_to_variant_enum
from json_types import *


class BuiltinClassDestructor(CodeGenerator):
    """
    Builtin classes (a.k.a Variants) Destructor structure
    """
    def __init__(self, type_name: str):
        self.class_name = type_name
        self.variant_type_enum = format_type_to_variant_enum(type_name)
        self.destructor_name = f"{type_name}_destroy"
        self.function_name = f"godot_{self.destructor_name}"
        self.prototype = f"void {self.function_name}(godot_{type_name} *self)"

    def get_c_code(self) -> BindingCode:
        return BindingCode(
            f"GDEXTENSION_LITE_DECL {self.prototype};",
            "\n".join([
                f"{self.prototype} {{",
                    f"\tGDEXTENSION_LITE_VARIANT_DESTRUCTOR_IMPL({self.variant_type_enum});",
                f"}}",
            ]),
        )

    def get_cpp_code(self) -> BindingCode:
        return BindingCode(
            f"~{self.class_name}();",
            "\n".join([
                f"{self.class_name}::~{self.class_name}() {{",
                    f"\t{self.function_name}(this);",
                f"}}",
            ]),
        )

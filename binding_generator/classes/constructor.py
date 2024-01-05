from common.binding_code import BindingCode
from common.code_generator import CodeGenerator
from json_types import *


class ClassConstructor(CodeGenerator):
    def __init__(self, type_name: str):
        self.class_name = type_name

    def get_c_code(self) -> BindingCode:
        prototype = f"godot_{self.class_name} *godot_{self.class_name}_new()"
        return BindingCode(
            f"GDEXTENSION_LITE_DECL {prototype};",
            '\n'.join([
                f"{prototype} {{",
                    f"\tGDEXTENSION_LITE_CLASS_CONSTRUCTOR_IMPL({self.class_name});",
                f"}}",
            ]),
        )

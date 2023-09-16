from format_utils import (BindingCode,
                          format_type_to_variant_enum)
from json_types import *


class BuiltinClassDestructor:
    """
    Builtin classes (a.k.a Variants) Destructor structure
    """
    def __init__(self, type_name: str):
        self.class_name = type_name
        self.variant_type_enum = format_type_to_variant_enum(type_name)
        self.destructor_name = f"destroy_{type_name}"
        self.function_name = f"godot_{self.destructor_name}"
        self.prototype = f"void {self.function_name}(godot_{type_name} *self)"
        
        self.ptr_function_name = f"godot_ptr_{self.destructor_name}"
        self.ptr_prototype = f"GDExtensionPtrDestructor {self.ptr_function_name}"

    def get_c_code(self) -> BindingCode:
        return BindingCode(
            f"{self.prototype};",
            '\n'.join([
                f"{self.ptr_prototype};",
                f"{self.prototype} {{",
                    f"""\tGDEXTENSION_LITE_LAZY_INIT_VARIANT_DESTRUCTOR({
                            self.class_name
                        }, {
                            self.variant_type_enum
                        });""",
                    f"\t{self.ptr_function_name}(self);",
                "}",
            ]),
        )


from .binding_code import BindingCode


class OpaqueStruct:
    def __init__(self, type_name: str, inherits: str | None):
        self.class_name = type_name
        self.struct_name = f"godot_{type_name}"
        self.inherits = inherits

    def get_c_code(self) -> BindingCode:
        inherits = f" /* extends {self.inherits} */" if self.inherits else ""
        return BindingCode(
            f"GDEXTENSION_LITE_OPAQUE_STRUCT({self.struct_name}{inherits});",
        )


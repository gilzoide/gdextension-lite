from format_utils import BindingCode


class OpaqueStruct:
    def __init__(self, type_name: str):
        self.class_name = type_name
        self.struct_name = f"godot_{type_name}"

    def get_c_code(self) -> BindingCode:
        return BindingCode(
            f"typedef struct {self.struct_name} {self.struct_name};",
            ""
        )


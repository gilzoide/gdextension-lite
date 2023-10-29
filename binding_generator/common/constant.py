import re

from .binding_code import BindingCode
from .code_generator import CodeGenerator
from json_types import *


class Constant(CodeGenerator):
    """
    Class constants structure and code generator
    """
    def __init__(self, type_name: str, constant: Constant | ValueOrConstant):
        self.class_name = type_name
        self.constant = constant

        value = str(constant["value"])
        if "(" in value:
            match = re.search(r"\(([^)]+)", value)
            if match:
                value = match.group(1).replace("inf", "godot_inf")
                value = "{ " + value + " }"
        self.value = value

        self.return_type = f"godot_{constant.get('type', 'int')}"
        self.constant_name = f"{type_name}_{constant['name']}"

    def get_c_code(self) -> BindingCode:
        prototype = f"{self.return_type} godot_{self.constant_name}()"
        return BindingCode(
            f"GDEXTENSION_LITE_DECL {prototype};  // {self.value}",
            "\n".join([
                f"{prototype} {{",
                    f"\t{self.return_type} value = {self.value};",
                    f"\treturn value;",
                f"}}",
            ]),
        )

    @classmethod
    def get_all_constants(
        cls,
        target_class: BuiltinClass | Class,
    ) -> list['Constant']:
        enum_names = {
            value["name"]
            for enum in target_class.get("enums", [])
            for value in enum["values"]
        }
        type_name = target_class["name"]
        return [
            cls(type_name, constant)
            for constant in target_class.get('constants', [])
            if constant['name'] not in enum_names
        ]

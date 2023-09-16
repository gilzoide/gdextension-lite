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
        return BindingCode(
            f"extern const {self.return_type} godot_{self.constant_name};  // {self.value}",
            f"const {self.return_type} godot_{self.constant_name} = {self.value};"
        )

    def get_cpp_code(self) -> BindingCode:
        constant_name = self.constant['name']
        type = self.constant.get('type', 'godot_int')
        return BindingCode(
            f"static const {type} {constant_name}; // {self.value}",
            f"const {type} {self.class_name}::{constant_name}({self.value.replace('{ ', '').replace(' }', '')});",
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

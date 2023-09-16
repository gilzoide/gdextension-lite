from textwrap import indent

from format_utils import BindingCode
from json_types import *


class ScopedEnum:
    """
    Enums scoped in classes
    """
    def __init__(self, scope: str, enum: Enum):
        self.scope = scope
        self.enum = enum
        self.enum_name = f"godot_{scope}_{enum['name']}"
        self.values = '\n'.join(
            f"godot_{scope}_{value['name']} = {value['value']},"
            for value in enum['values']
        )

    def get_c_code(self) -> BindingCode:
        return BindingCode(
            '\n'.join([
                f"typedef enum {self.enum_name} {{",
                indent(self.values, '\t'),
                f"}} {self.enum_name};",
            ]),
            "",
        )

    @classmethod
    def get_all_scoped_enums(
        cls,
        target_class: BuiltinClass | Class,
    ) -> list['ScopedEnum']:
        type_name = target_class['name']
        return [
            cls(type_name, enum)
            for enum in target_class.get('enums', [])
        ]

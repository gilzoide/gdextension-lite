from common.binding_code import BindingCode
from common.code_generator import CodeGenerator

from json_types import *


class SingletonGetterCode(CodeGenerator):
    """
    Singleton getter
    """
    def __init__(self, singleton: ArgumentOrSingletonOrMember) -> None:
        self.name = singleton['name']
        self.type = singleton['type']
    
    def get_c_code(self) -> BindingCode:
        prototype = f"godot_{self.type} *godot_{self.type}_singleton()"
        return BindingCode(
            f"GDEXTENSION_LITE_DECL {prototype};",
            "\n".join([
                f"{prototype} {{",
                    f"\tGDEXTENSION_LITE_GET_SINGLETON_IMPL({self.type}, \"{self.name}\");",
                f"}}",
            ]),
        )

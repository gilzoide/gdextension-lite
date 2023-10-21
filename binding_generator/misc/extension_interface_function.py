import re

from common.binding_code import BindingCode
from common.code_generator import CodeGenerator


class ExtensionInterfaceFunction(CodeGenerator):
    """
    GDExtension Interface method
    """
    SPLIT_ARGUMENTS_RE = re.compile(r"(?<=[\w)]),")
    ARGUMENT_NAME_RE = re.compile(r"(\w+)($|\))")

    def __init__(self, symbol: str, typedef_name: str, return_type: str, arguments: str):
        self.symbol = symbol
        self.typedef_name = typedef_name
        self.return_type = return_type.strip()
        
        self.arguments = arguments
        self.argument_list = self.SPLIT_ARGUMENTS_RE.split(arguments)

    def get_c_code(self) -> BindingCode:
        prototype = f"{self.return_type} godot_{self.symbol}({self.arguments})"
        call_args = ", ".join(self.ARGUMENT_NAME_RE.search(arg).group(1) for arg in self.argument_list)
        return BindingCode(
            f"GDEXTENSION_LITE_DECL {prototype};",
            "\n".join([
                f"{prototype} {{",
                    f"\tGDEXTENSION_LITE_EXTENSION_INTERFACE_IMPL({self.typedef_name}, {self.symbol}, {call_args});",
                f"}}",
            ]),
        )

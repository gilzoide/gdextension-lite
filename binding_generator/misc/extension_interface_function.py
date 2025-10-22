import re

from common.binding_code import BindingCode
from common.code_generator import CodeGenerator


class ExtensionInterfaceFunction(CodeGenerator):
    """
    GDExtension Interface method
    """
    SPLIT_ARGUMENTS_RE = re.compile(r"(?<=[\w)]),")
    ARGUMENT_NAME_RE = re.compile(r"(\w+)($|\))")

    def __init__(self, symbol: str, typedef_name: str, return_type: str, arguments: str, since: str):
        self.symbol = symbol
        self.typedef_name = typedef_name
        self.return_type = return_type.strip()
        
        self.arguments = arguments
        self.argument_list = self.SPLIT_ARGUMENTS_RE.split(arguments)

        self.since = since

    def get_c_code(self) -> BindingCode:
        impl_macro = "GDEXTENSION_LITE_EXTENSION_INTERFACE_IMPL"
        if self.return_type == "void":
            impl_macro += "_VOID"
        prototype = f"{self.return_type} godot_{self.symbol}({self.arguments})"
        call_args = ", ".join(self.ARGUMENT_NAME_RE.search(arg).group(1) for arg in self.argument_list)
        return BindingCode(
            f"GDEXTENSION_LITE_DECL {prototype}; /* since {self.since} */",
            "\n".join([
                f"{prototype} {{",
                    f"\t{impl_macro}({self.typedef_name}, {self.symbol}, {call_args});",
                f"}}",
            ]),
        )

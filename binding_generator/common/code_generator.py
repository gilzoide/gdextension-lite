from .binding_code import BindingCode


class CodeGenerator:
    """
    Base class for code generators
    """
    def get_c_code(self) -> BindingCode:
        return BindingCode()

    def get_code(self) -> BindingCode:
        return self.get_c_code()

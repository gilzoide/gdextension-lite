from .binding_code import BindingCode


class CodeGenerator:
    """
    Base class for code generators
    """
    def get_c_code(self) -> BindingCode:
        return BindingCode()

    def get_cpp_code(self) -> BindingCode:
        return BindingCode()

    def get_code(self, is_cpp: bool) -> BindingCode:
        return self.get_cpp_code() if is_cpp else self.get_c_code()

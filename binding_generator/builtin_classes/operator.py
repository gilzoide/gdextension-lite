from common.binding_code import BindingCode
from common.code_generator import CodeGenerator
from format_utils import (format_operator_to_enum,
                          format_parameter_const,
                          format_type_to_variant_enum,
                          format_value_to_ptr,
                          OPERATOR_TO_C,
                          should_generate_operator)
from json_types import *


class BuiltinClassOperator(CodeGenerator):
    """
    Builtin classes (a.k.a Variants) operator
    """
    def __init__(self, type_name: str, operator: Operator):
        self.class_name = type_name
        self.operator_name = OPERATOR_TO_C.get(operator['name'], operator['name'])

        function_name = f"{type_name}_op_{self.operator_name}"
        self.return_type = f"godot_{operator['return_type']}"
        self.right_type = operator.get('right_type')
        if self.right_type:
            function_name += "_" + self.right_type
            right_parameter = ", " + format_parameter_const(self.right_type, "b")
        else:
            right_parameter = ""

        self.prototype = f"""{self.return_type} godot_{function_name}({
                                format_parameter_const(type_name, "a")
                            }{
                                right_parameter
                            })"""

    def get_c_code(self) -> BindingCode:
        impl_macro = "GDEXTENSION_LITE_VARIANT_BINARY_OPERATOR_IMPL" if self.right_type else "GDEXTENSION_LITE_VARIANT_UNARY_OPERATOR_IMPL"
        macro_args = [
            self.return_type,
            format_operator_to_enum(self.operator_name),
            format_type_to_variant_enum(self.class_name),
            format_value_to_ptr(self.class_name, "a")
        ]
        if self.right_type:
            macro_args.extend([
                format_type_to_variant_enum(self.class_name),
                format_value_to_ptr(self.right_type, "b")
            ])
        return BindingCode(
            "\n".join([
                f"static inline {self.prototype} {{",
                    f"\t{impl_macro}({', '.join(macro_args)});",
                f"}}",
            ]),
        )

    @classmethod
    def get_all_operators(
        cls,
        builtin_class: BuiltinClass,
    ) -> list['BuiltinClassOperator']:
        type_name = builtin_class["name"]
        return [
            cls(type_name, operator)
            for operator in builtin_class["operators"]
            if should_generate_operator(type_name, operator.get('right_type'))
        ]

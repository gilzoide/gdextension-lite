from common.code_generator import CodeGenerator
from format_utils import (BindingCode,
                          format_operator_to_enum,
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
        self.return_type = operator['return_type']
        self.right_type = operator.get('right_type')
        if self.right_type:
            function_name += "_" + self.right_type
            right_parameter = ", " + format_parameter_const(self.right_type, "b")
        else:
            right_parameter = ""

        self.operator_function_name = function_name
        self.function_name = f"godot_{self.operator_function_name}"
        self.prototype = f"""godot_{self.return_type} {self.function_name}({
                                format_parameter_const(type_name, "a")
                            }{
                                right_parameter
                            })"""

        self.ptr_function_name = f"godot_ptr_{function_name}"
        self.ptr_prototype = f"GDExtensionPtrOperatorEvaluator {self.ptr_function_name}"

    def get_c_code(self) -> BindingCode:
        return BindingCode(
            f"{self.prototype};",
            '\n'.join([
                f"{self.ptr_prototype};",
                f"{self.prototype} {{",
                    f"""\tGDEXTENSION_LITE_LAZY_INIT_VARIANT_OPERATOR({
                            self.operator_function_name
                        }, {
                            format_operator_to_enum(self.operator_name)
                        }, {
                            format_type_to_variant_enum(self.class_name)
                        }, {
                            format_type_to_variant_enum(self.right_type)
                        });""",
                    f"\tgodot_{self.return_type} _ret;",
                    f"""\t{self.ptr_function_name}({
                            format_value_to_ptr(self.class_name, "a")
                        }, {
                            format_value_to_ptr(self.right_type, "b")
                        }, &_ret);""",
                    f"\treturn _ret;",
                "}",
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

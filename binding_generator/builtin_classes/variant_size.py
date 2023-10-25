from common.binding_code import BindingCode
from common.code_generator import CodeGenerator
from format_utils import format_type_snake_case
from json_types import *


class VariantSizeCode(CodeGenerator):
    """
    Builtin classes (a.k.a Variants) size constants
    """
    def __init__(self, size: BuiltinClassSize):
        self.build_configuration = size['build_configuration']
        self.sizes = size['sizes']
    
    def get_c_code(self) -> BindingCode:
        return BindingCode(
            "\n".join([
                f"#define GDEXTENSION_LITE_SIZE_{s['name']} {s['size']}"
                for s in self.sizes
            ])
        ).surround_prototype(
            f"#ifdef {self.build_configuration.upper()}",
            "#endif",
            add_indent=True,
        )

    @classmethod
    def get_all_sizes(cls, sizes: list[BuiltinClassSize]) -> BindingCode:
        return BindingCode.merge(
                cls(size).get_c_code()
                for size in sizes
            ).surround_prototype(
                "\n".join([
                    "#if INTPTR_MAX == INT32_MAX",
                        "\t#ifdef REAL_T_IS_DOUBLE",
                            "\t\t#define DOUBLE_32",
                        "\t#else",
                            "\t\t#define FLOAT_32",
                        "\t#endif",
                    "#elif INTPTR_MAX == INT64_MAX",
                        "\t#ifdef REAL_T_IS_DOUBLE",
                            "\t\t#define DOUBLE_64",
                        "\t#else",
                            "\t\t#define FLOAT_64",
                        "\t#endif",
                    "#endif",
                    "",
                ]),
                "",
                add_indent=False,
            ).add_extras(includes=["<stdint.h>"])

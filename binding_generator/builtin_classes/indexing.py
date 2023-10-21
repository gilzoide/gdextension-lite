from common.binding_code import BindingCode
from common.code_generator import CodeGenerator
from format_utils import (format_parameter,
                          format_parameter_const,
                          format_type_to_variant_enum,
                          format_value_to_ptr)
from json_types import *


class BuiltinClassIndexing(CodeGenerator):
    """
    Builtin classes (a.k.a Variants) indexing operators
    """
    def __init__(self, type_name: str, is_keyed: bool, return_type: str):
        self.class_name = type_name
        self.variant_type_enum = format_type_to_variant_enum(type_name)

        self.indexed_or_keyed = "keyed" if is_keyed else "indexed"
        self.key_type = "Variant" if is_keyed else "int"
        self.return_type = return_type

    @classmethod
    def get_all_indexers(
        cls,
        builtin_class: BuiltinClass,
    ) -> list['BuiltinClassIndexing']:
        return_type = builtin_class.get('indexing_return_type')
        if return_type:
            type_name = builtin_class['name']
            is_keyed = builtin_class['is_keyed']
            return [
                BuiltinClassIndexingSetter(type_name, is_keyed, return_type),
                BuiltinClassIndexingGetter(type_name, is_keyed, return_type),
            ]
        else:
            return []


class BuiltinClassIndexingSetter(BuiltinClassIndexing):
    """
    Builtin classes (a.k.a Variants) indexing setter
    """
    def __init__(self, type_name: str, is_keyed: bool, return_type: str):
        super().__init__(type_name, is_keyed, return_type)

        self.prototype = f"""void godot_{type_name}_{self.indexed_or_keyed}_set({
                                format_parameter(type_name, 'self')
                            }, {
                                format_parameter_const(self.key_type, 'key')
                            }, {
                                format_parameter_const(return_type, 'value')
                            })"""

    def get_c_code(self) -> BindingCode:
        impl_macro = "GDEXTENSION_LITE_VARIANT_INDEXED_SET_IMPL" if self.indexed_or_keyed == "indexed" else "GDEXTENSION_LITE_VARIANT_KEYED_SET_IMPL"
        macro_args = [
            self.variant_type_enum,
            "key",
            format_value_to_ptr(self.return_type, 'value'),
        ]
        return BindingCode(
            "\n".join([
                f"GDEXTENSION_LITE_INLINE {self.prototype} {{",
                    f"\t{impl_macro}({', '.join(macro_args)});",
                f"}}",
            ]),
        )


class BuiltinClassIndexingGetter(BuiltinClassIndexing):
    """
    Builtin classes (a.k.a Variants) indexing getter
    """
    def __init__(self, type_name: str, is_keyed: bool, return_type: str):
        super().__init__(type_name, is_keyed, return_type)

        self.prototype = f"""godot_{return_type} godot_{type_name}_{self.indexed_or_keyed}_get({
                                format_parameter_const(type_name, 'self')
                            }, {
                                format_parameter_const(self.key_type, 'key')
                            })"""

    def get_c_code(self) -> BindingCode:
        impl_macro = "GDEXTENSION_LITE_VARIANT_INDEXED_GET_IMPL" if self.indexed_or_keyed == "indexed" else "GDEXTENSION_LITE_VARIANT_KEYED_GET_IMPL"
        macro_args = [
            self.variant_type_enum,
            "key",
            f"godot_{self.return_type}",
        ]
        return BindingCode(
            "\n".join([
                f"GDEXTENSION_LITE_INLINE {self.prototype} {{",
                    f"\t{impl_macro}({', '.join(macro_args)});",
                f"}}",
            ]),
        )


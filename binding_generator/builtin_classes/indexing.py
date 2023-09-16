from common.code_generator import CodeGenerator
from format_utils import (BindingCode,
                          format_parameter,
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

        self.set_name = f"{type_name}_{self.indexed_or_keyed}_set"
        self.function_name = f"godot_{self.set_name}"
        self.prototype = f"""void {self.function_name}({
                                format_parameter(type_name, 'self')
                            }, {
                                format_parameter_const(self.key_type, 'key')
                            }, {
                                format_parameter_const(return_type, 'value')
                            })"""
        self.ptr_function_name = f"godot_ptr_{self.set_name}"
        ptr_type = f"GDExtensionPtr{self.indexed_or_keyed.title()}Setter"
        self.ptr_prototype = f"{ptr_type} {self.ptr_function_name}"

    def get_c_code(self) -> BindingCode:
        return BindingCode(
            f"{self.prototype};",
            '\n'.join([
                f"{self.ptr_prototype};",
                f"{self.prototype} {{",
                    f"""\tGDEXTENSION_LITE_LAZY_INIT_VARIANT_INDEXING(set, {
                            self.indexed_or_keyed
                        }, {
                            self.class_name
                        }, {
                            self.variant_type_enum
                        });""",
                    f"""\t{self.ptr_function_name}(self, key, {
                            format_value_to_ptr(self.return_type, 'value')
                        });""",
                f"}}",
            ])
        )


class BuiltinClassIndexingGetter(BuiltinClassIndexing):
    """
    Builtin classes (a.k.a Variants) indexing getter
    """
    def __init__(self, type_name: str, is_keyed: bool, return_type: str):
        super().__init__(type_name, is_keyed, return_type)

        self.get_name = f"{type_name}_{self.indexed_or_keyed}_get"
        self.function_name = f"godot_{self.get_name}"
        self.prototype = f"""godot_{return_type} {self.function_name}({
                                format_parameter_const(type_name, 'self')
                            }, {
                                format_parameter_const(self.key_type, 'key')
                            })"""
        self.ptr_function_name = f"godot_ptr_{self.get_name}"
        ptr_type = f"GDExtensionPtr{self.indexed_or_keyed.title()}Getter"
        self.ptr_prototype = f"{ptr_type} {self.ptr_function_name}"

    def get_c_code(self) -> BindingCode:
        return BindingCode(
            f"{self.prototype};",
            '\n'.join([
                f"{self.ptr_prototype};",
                f"{self.prototype} {{",
                    f"""\tGDEXTENSION_LITE_LAZY_INIT_VARIANT_INDEXING(get, {
                            self.indexed_or_keyed
                        }, {
                            self.class_name
                        }, {
                            self.variant_type_enum
                        });""",
                    f"\tgodot_{self.return_type} value;",
                    f"\t{self.ptr_function_name}(self, key, &value);",
                    f"\treturn value;",
                f"}}",
            ])
        )


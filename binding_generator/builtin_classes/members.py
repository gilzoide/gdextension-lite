from common.binding_code import BindingCode
from common.code_generator import CodeGenerator
from format_utils import (format_cpp_argument_forward,
                          format_parameter,
                          format_parameter_const,
                          format_type_to_variant_enum,
                          format_value_to_ptr)
from json_types import *


class BuiltinClassMember(CodeGenerator):
    """
    Builtin classes (a.k.a. Variants) member
    """
    def __init__(self, type_name: str, member: ArgumentOrSingletonOrMember):
        self.class_name = type_name
        self.variant_type_enum = format_type_to_variant_enum(type_name)
        self.member = member
        self.member_name, self.member_type = member['name'], member['type']

    @classmethod
    def get_all_members(
        cls,
        builtin_class: BuiltinClass,
    ) -> list['BuiltinClassMember']:
        type_name = builtin_class["name"]
        all_members = []
        for member in builtin_class.get("members", []):
            all_members.append(BuiltinClassMemberSetter(type_name, member))
            all_members.append(BuiltinClassMemberGetter(type_name, member))
        return all_members


class BuiltinClassMemberSetter(BuiltinClassMember):
    """
    Builtin classes (a.k.a. Variants) member setters
    """
    def __init__(self, type_name: str, member: ArgumentOrSingletonOrMember):
        super().__init__(type_name, member)

        self.set_name = f"{type_name}_set_{self.member_name}"
        self.function_name = f"godot_{self.set_name}"
        self.prototype = f"""void {self.function_name}({
                                format_parameter(type_name, 'self')
                            }, {
                                format_parameter_const(self.member_type, 'value')
                            })"""
        self.ptr_function_name = f"godot_ptr_{self.set_name}"
        self.ptr_prototype = f"GDExtensionPtrSetter {self.ptr_function_name}"

    def get_c_code(self) -> BindingCode:
        return BindingCode(
            f"{self.prototype};",
            '\n'.join([
                f"{self.ptr_prototype};",
                f"{self.prototype} {{",
                    f"""\tGDEXTENSION_LITE_LAZY_INIT_VARIANT_MEMBER(set, {
                            self.class_name
                        }, {
                            self.variant_type_enum
                        }, {
                            self.member['name']
                        });""",
                    f"\t{self.ptr_function_name}(self, {format_value_to_ptr(self.member['type'], 'value')});",
                f"}}",
            ]),
        )

    def get_cpp_code(self) -> BindingCode:
        arg_name = 'value'
        prototype_argument = format_parameter_const(self.member_type, arg_name, is_cpp=True)
        return BindingCode(
            "\n".join([
                f"void set_{self.member_name}({prototype_argument});",
            ]),
            "\n".join([
                f"void {self.class_name}::set_{self.member_name}({prototype_argument}) {{",
                    f"\t{self.function_name}(this, {format_cpp_argument_forward(self.member_type,  arg_name)});",
                f"}}",
            ]),
        )


class BuiltinClassMemberGetter(BuiltinClassMember):
    """
    Builtin classes (a.k.a. Variants) member getters
    """
    def __init__(self, type_name: str, member: ArgumentOrSingletonOrMember):
        super().__init__(type_name, member)
        member_name, member_type = member['name'], member['type']

        self.get_name = f"{type_name}_get_{member_name}"
        self.return_type = f"godot_{member_type}"
        self.function_name = f"godot_{self.get_name}"
        self.prototype = f"""{self.return_type} {self.function_name}({
                                format_parameter_const(type_name, 'self')
                            })"""
        self.ptr_function_name = f"godot_ptr_{self.get_name}"
        self.ptr_prototype = f"GDExtensionPtrGetter {self.ptr_function_name}"

    def get_c_code(self) -> BindingCode:
        return BindingCode(
            f"{self.prototype};",
            '\n'.join([
                f"{self.ptr_prototype};",
                f"{self.prototype} {{",
                    f"""\tGDEXTENSION_LITE_LAZY_INIT_VARIANT_MEMBER(get, {
                            self.class_name
                        }, {
                            self.variant_type_enum
                        }, {
                            self.member['name']
                        });""",
                    f"\t{self.return_type} value;",
                    f"\t{self.ptr_function_name}(self, &value);",
                    f"\treturn value;",
                f"}}",
            ]),
        )

    def get_cpp_code(self) -> BindingCode:
        return BindingCode(
            "\n".join([
                f"{self.member_type} get_{self.member_name}() const;",
            ]),
            "\n".join([
                f"{self.member_type} {self.class_name}::get_{self.member_name}() const {{",
                    f"\treturn {self.function_name}(this);",
                f"}}",
            ]),
        )

"""
Internal utilities for Godot types
"""

from __future__ import annotations
import re
from textwrap import dedent, indent
from typing import Sequence

from json_types import *

NON_STRUCT_TYPES = (
    'Nil',
    'bool',
    'int',
    'float',
)


OPERATOR_TO_C = {
    '+': 'add',
    '-': 'subtract',
    'unary+': 'positive',
    'unary-': 'negate',
    '*': 'multiply',
    '/': 'divide',
    '**': 'power',
    '<<': 'shift_left',
    '>>': 'shift_right',
    '&': 'bit_and',
    '|': 'bit_or',
    '^': 'bit_xor',
    '~': 'bit_negate',
    '%': 'module',
    '==': 'equal',
    '!=': 'not_equal',
    '<': 'less',
    '<=': 'less_equal',
    '>': 'greater',
    '>=': 'greater_equal',
}


IDENTIFIER_OVERRIDES = {
    'default': 'default_value',
    'char': 'chr',
}


INTERFACE_PARAMETER_NAME = "interface"


def code_block(
    code: str,
    remove_empty_lines: bool = True,
) -> str:
    code = dedent(code).strip()
    if remove_empty_lines:
        code = "\n".join(line for line in code.splitlines() if line.strip())
    return code


def should_generate_operator(
    type_name: str,
    arg_type: str | None,
) -> bool:
    return (type_name != 'Nil'
            and (type_name not in NON_STRUCT_TYPES
                 or (arg_type or 'Nil') not in NON_STRUCT_TYPES))


def should_generate_constructor(
    type_name: str,
    ctor: Constructor,
) -> bool:
    arguments = ctor.get("arguments")
    if arguments:
        return should_generate_operator(type_name, arguments[0]["type"])
    else:
        return should_generate_operator(type_name, None)


def should_generate_method(
    method: BuiltinClassMethod,
    members: list[ArgumentOrSingletonOrMember],
) -> bool:
    method_name = method["name"]
    if method_name.startswith("get_") or method_name.startswith("set_"):
        return method_name[4:] not in (member["name"] for member in members)
    else:
        return True


class BindingCode:
    """Object that contains the code necessary for each function binding"""
    def __init__(self, prototype: str, implementation: str, bind: str = ""):
        self.prototype = prototype
        self.implementation = implementation
        self.bind = bind

    def prepend_section_comment(self, comment: str):
        self.prototype = f"// {comment}\n{self.prototype}"
        self.implementation = f"// {comment}\n{self.implementation}"
        self.bind = f"// {comment}\n{self.bind}"

    @classmethod
    def merge(cls, bindings: Sequence[BindingCode]) -> BindingCode: 
        return BindingCode(
            "\n\n".join(b.prototype for b in bindings),
            "\n\n".join(b.implementation for b in bindings),
            "\n".join(b.bind for b in bindings),
        )


############################################################
# Functions pointer variables + custom implementations
############################################################
def format_constructor_pointer(
    type_name: str,
    ctor: Constructor,
) -> BindingCode:
    func_name = f"new_{type_name}"
    arguments = ctor.get("arguments")
    if arguments:
        func_name += "_from" + "".join(f"_{arg['type']}" for arg in arguments)

        proto_arguments = ", ".join(
            format_parameter_const(arg["type"], arg["name"])
            for arg in arguments
        )
    else:
        proto_arguments = ""
    proto_ptr = f"GDExtensionPtrConstructor godot_ptr_{func_name}"
    proto_typed = f"godot_{type_name} godot_{func_name}({proto_arguments})"
    return BindingCode(
        code_block(f"""
            extern {proto_ptr};
            {proto_typed};
        """),
        code_block(f"""
            {proto_ptr};
            {proto_typed} {{
            \tgodot_{type_name} self;
            \t{format_arguments_array('args', arguments)};
            \tgodot_ptr_{func_name}(&self, args);
            \treturn self;
            }}
        """),
        code_block(f"""
            godot_ptr_{func_name} = godot_variant_get_ptr_constructor({
                format_type_to_variant_enum(type_name)
            }, {ctor["index"]});
        """),
    )


def format_destructor_pointer(
    type_name: str,
) -> BindingCode:
    function_name = f"destroy_{type_name}"
    proto_ptr = f"GDExtensionPtrDestructor godot_ptr_{function_name}"
    proto_typed = (f"void godot_{function_name}("
                   f"{format_parameter(type_name, 'self')})")
    return BindingCode(
        code_block(f"""
            extern {proto_ptr};
            {proto_typed};
        """),
        code_block(f"""
            {proto_ptr};
            {proto_typed} {{
            \tgodot_ptr_{function_name}(self);
            }}
        """),
        code_block(f"""
            godot_ptr_{function_name} = godot_variant_get_ptr_destructor({
                format_type_to_variant_enum(type_name)
            });
        """),
    )


def format_type_from_to_variant(
    type_name: str,
) -> BindingCode:
    type_ptr_name = f"godot_ptr_{type_name}_from_Variant"
    proto_type_ptr = ("GDExtensionTypeFromVariantConstructorFunc"
                      f" {type_ptr_name}")
    proto_type_typed = (f"godot_{type_name}"
                        f" godot_{type_name}_from_Variant("
                        f"{format_parameter('Variant', 'value')})")
    variant_ptr_name = f"godot_ptr_Variant_from_{type_name}"
    proto_variant_ptr = ("GDExtensionVariantFromTypeConstructorFunc"
                         f" {variant_ptr_name}")
    proto_variant_typed = (f"godot_Variant"
                           f" godot_Variant_from_{type_name}("
                           f"{format_parameter(type_name, 'value')})")
    return BindingCode(
        code_block(f"""
            extern {proto_type_ptr};
            {proto_type_typed};

            extern {proto_variant_ptr};
            {proto_variant_typed};
        """),
        code_block(f"""
            {proto_type_ptr};
            {proto_type_typed} {{
            \tgodot_{type_name} self;
            \tgodot_ptr_{type_name}_from_Variant(&self, value);
            \treturn self;
            }}

            {proto_variant_ptr};
            {proto_variant_typed} {{
            \tgodot_Variant self;
            \tgodot_ptr_Variant_from_{type_name}(&self, {
                format_value_to_ptr(type_name, 'value')
            });
            \treturn self;
            }}
        """),
        code_block(f"""
            {type_ptr_name} = godot_get_variant_to_type_constructor({
                format_type_to_variant_enum(type_name)
            });
            {variant_ptr_name} = godot_get_variant_from_type_constructor({
                format_type_to_variant_enum(type_name)
            });
        """),
    )


def format_member_pointers(
    type_name: str,
    member: ArgumentOrSingletonOrMember,
) -> BindingCode:
    name = member['name']
    type = member['type']
    set_name = f"{type_name}_set_{name}"
    set_ptr = f"GDExtensionPtrSetter godot_ptr_{set_name}"
    set_typed = (f"void godot_{set_name}("
                 f"{format_parameter(type_name, 'self')}, "
                 f"{format_parameter_const(type, 'value')})")
    get_name = f"{type_name}_get_{name}"
    get_ptr = f"GDExtensionPtrGetter godot_ptr_{get_name}"
    get_typed = (f"godot_{type} godot_{get_name}("
                 f"{format_parameter_const(type_name, 'self')})")
    return BindingCode(
        code_block(f"""
            extern {set_ptr};
            {set_typed};

            extern {get_ptr};
            {get_typed};
        """),
        code_block(f"""
            {set_ptr};
            {set_typed} {{
            \tgodot_ptr_{set_name}(self, {format_value_to_ptr(type, 'value')});
            }}

            {get_ptr};
            {get_typed} {{
            \tgodot_{type} value;
            \tgodot_ptr_{get_name}(self, &value);
            \treturn value;
            }}
        """),
        code_block(f"""
            GDEXTENSION_LITE_WITH_STRING_NAME({name}, name, {{
            \tgodot_ptr_{set_name} = godot_variant_get_ptr_setter({
                format_type_to_variant_enum(type_name)
            }, &name);
            \tgodot_ptr_{get_name} = godot_variant_get_ptr_getter({
                format_type_to_variant_enum(type_name)
            }, &name);
            }})
        """),
    )


def format_indexing_pointers(
    type_name: str,
    is_keyed: bool,
    return_type: str,
) -> BindingCode:
    if is_keyed:
        set_name = f"{type_name}_keyed_set"
        set_ptr = f"GDExtensionPtrKeyedSetter godot_ptr_{set_name}"
        set_typed = (f"void godot_{set_name}("
                     f"{format_parameter(type_name, 'self')}, "
                     f"{format_parameter_const('Variant', 'key')}, "
                     f"{format_parameter_const(return_type, 'value')})")
        set_fetch_func = "variant_get_ptr_keyed_setter"
        get_name = f"{type_name}_keyed_get"
        get_ptr = f"GDExtensionPtrKeyedGetter godot_ptr_{get_name}"
        get_typed = (f"godot_{return_type} godot_{get_name}("
                     f"{format_parameter_const(type_name, 'self')}, "
                     f"{format_parameter_const('Variant', 'key')})")
        get_fetch_func = "variant_get_ptr_keyed_getter"
    else:
        set_name = f"{type_name}_indexed_set"
        set_ptr = f"GDExtensionPtrIndexedSetter godot_ptr_{set_name}"
        set_typed = (f"void godot_{set_name}("
                     f"{format_parameter(type_name, 'self')}, "
                     f"{format_parameter_const('int', 'key')}, "
                     f"{format_parameter_const(return_type, 'value')})")
        set_fetch_func = "variant_get_ptr_indexed_setter"
        get_name = f"{type_name}_indexed_get"
        get_ptr = f"GDExtensionPtrIndexedGetter godot_ptr_{get_name}"
        get_typed = (f"godot_{return_type} godot_{get_name}("
                     f"{format_parameter_const(type_name, 'self')}, "
                     f"{format_parameter_const('int', 'key')})")
        get_fetch_func = "variant_get_ptr_indexed_getter"
    return BindingCode(
        code_block(f"""
            extern {set_ptr};
            {set_typed};

            extern {get_ptr};
            {get_typed};
        """),
        code_block(f"""
            {set_ptr};
            {set_typed} {{
            \tgodot_ptr_{set_name}(self, key, {
                format_value_to_ptr(return_type, 'value')
            });
            }}

            {get_ptr};
            {get_typed} {{
            \tgodot_{return_type} value;
            \tgodot_ptr_{get_name}(self, key, &value);
            \treturn value;
            }}
        """),
        code_block(f"""
            godot_ptr_{set_name} = godot_{set_fetch_func}({
                format_type_to_variant_enum(type_name)
            });
            godot_ptr_{get_name} = godot_{get_fetch_func}({
                format_type_to_variant_enum(type_name)
            });
        """),
    )


def format_operator_pointer(
    type_name: str,
    operator: Operator,
) -> BindingCode:
    operator_name = OPERATOR_TO_C.get(operator["name"], operator["name"])
    function_name = f"{type_name}_op_{operator_name}"
    return_type = operator["return_type"]
    right_type = operator.get("right_type")
    if right_type:
        function_name += "_" + right_type
        right_parameter = ", " + format_parameter_const(right_type, "b")
    else:
        right_parameter = ""

    proto_ptr = f"GDExtensionPtrOperatorEvaluator godot_ptr_{function_name}"
    proto_typed = (f"godot_{return_type} godot_{function_name}("
                   f"{format_parameter_const(type_name, 'a')}"
                   f"{right_parameter})")
    return BindingCode(
        code_block(f"""
            extern {proto_ptr};
            {proto_typed};
        """),
        code_block(f"""
            {proto_ptr};
            {proto_typed} {{
            \tgodot_{return_type} result;
            \tgodot_ptr_{function_name}({
                format_value_to_ptr(type_name, 'a')
            }, {
                format_value_to_ptr(right_type, 'b')
                if right_type
                else "NULL"
            }, &result);
            \treturn result;
            }}
        """),
        code_block(f"""
            godot_ptr_{function_name} = godot_variant_get_ptr_operator_evaluator({
                format_operator_to_enum(operator_name)
            }, {
                format_type_to_variant_enum(type_name)
            }, {
                format_type_to_variant_enum(right_type)
            });
        """),
    )


def format_method_pointer(
    type_name: str,
    method: BuiltinClassMethod
) -> BindingCode:
    return_type = method.get("return_type")
    proto_return_type = format_return_type(return_type) if return_type else "void"

    proto_args = []
    is_static = method.get("is_static", False)
    if not is_static:
        is_const = method.get("is_const", False)
        proto_args.append(format_parameter(type_name,
                                           "self",
                                           is_const=is_const))
    arguments = method.get("arguments")
    if arguments:
        proto_args.extend(
            format_parameter_const(arg["type"], arg["name"])
            for arg in arguments
        )

    non_vararg_argc = len(proto_args)
    is_vararg = method.get("is_vararg")
    if is_vararg:
        proto_args.append("godot_int argc")
        proto_args.append("const godot_Variant **argv")

    proto_args = ", ".join(proto_args)

    method_name = method["name"]
    function_name = f"{type_name}_{method_name}"
    proto_ptr = f"GDExtensionPtrBuiltInMethod godot_ptr_{function_name}"
    proto_typed = f"{proto_return_type} godot_{function_name}({proto_args})"

    return BindingCode(
        code_block(f"""
            extern {proto_ptr};
            {proto_typed};
            {format_vararg_macro(function_name, non_vararg_argc) if is_vararg else ""}
        """),
        code_block(f"""
            {proto_ptr};
            {proto_typed} {{
            \t{proto_return_type + " result;" if return_type else ""}
{indent(format_arguments_array('args', arguments, is_vararg), '            	')}
            \tgodot_ptr_{function_name}({
                "NULL"
                if is_static
                else "(GDExtensionTypePtr) self"
            }, args, {
                "&result"
                if return_type
                else "NULL"
            }, {format_arguments_count(arguments, is_vararg)});
            \t{"return result;" if return_type else ""}
            }}
        """),
        code_block(f"""
            GDEXTENSION_LITE_WITH_STRING_NAME({method_name}, name, {{
            \tgodot_ptr_{function_name} = godot_variant_get_ptr_builtin_method({
                format_type_to_variant_enum(type_name)
            }, &name, {method['hash']});
            }})
        """),
    )


def format_utility_function(
    function: UtilityFunction
) -> BindingCode:
    return_type = function.get("return_type")
    proto_return_type = format_return_type(return_type) if return_type else "void"

    proto_args = []
    arguments = function.get("arguments")
    if arguments:
        proto_args.extend(
            format_parameter_const(arg["type"], arg["name"])
            for arg in arguments
        )

    non_vararg_argc = len(proto_args)
    is_vararg = function.get("is_vararg")
    if is_vararg:
        proto_args.append("godot_int argc")
        proto_args.append("const godot_Variant **argv")

    proto_args = ", ".join(proto_args)

    function_name = function["name"]
    proto_ptr = f"GDExtensionPtrUtilityFunction godot_ptr_{function_name}"
    proto_typed = f"{proto_return_type} godot_{function_name}({proto_args})"

    return BindingCode(
        code_block(f"""
            extern {proto_ptr};
            {proto_typed};
            {format_vararg_macro(function_name, non_vararg_argc) if is_vararg else ""}
        """),
        code_block(f"""
            {proto_ptr};
            {proto_typed} {{
            \t{proto_return_type + " result;" if return_type else ""}
{indent(format_arguments_array('args', arguments, is_vararg), '            	')}
            \tgodot_ptr_{function_name}({
                "&result"
                if return_type
                else "NULL"
            }, args, {format_arguments_count(arguments, is_vararg)});
            \t{"return result;" if return_type else ""}
            }}
        """),
        code_block(f"""
            GDEXTENSION_LITE_WITH_STRING_NAME({function_name}, name, {{
            \tgodot_ptr_{function_name} = godot_variant_get_ptr_utility_function(&name, {function['hash']});
            }})
        """),
    )


def format_binders(
    type_name: str,
    merged_binder_code: str,
) -> BindingCode:
    prototype = (f"void gdextension_lite_initialize_{type_name}()")
    return BindingCode(
        code_block(f"""
            {prototype};
        """),
        code_block(f"""
            {prototype} {{
{indent(merged_binder_code, '            	')}
            }}
        """),
    )


############################################################
# Parameter helpers
############################################################
def format_parameter(
    type_name: str,
    parameter_name: str,
    is_const: bool = False,
) -> str:
    parameter_name = IDENTIFIER_OVERRIDES.get(parameter_name, parameter_name)
    if type_name in NON_STRUCT_TYPES:
        return f"godot_{type_name} {parameter_name}"
    elif is_const:
        return f"const godot_{type_name} *{parameter_name or ''}"
    else:
        return f"godot_{type_name} *{parameter_name or ''}"


def format_parameter_const(
    type_name: str,
    parameter_name: str,
) -> str:
    return format_parameter(type_name, parameter_name, is_const=True)


def format_return_type(
    type_name: str,
) -> str:
    if type_name == "Object":
        return f"godot_{type_name} *"
    else:
        return f"godot_{type_name}"


def format_value_to_ptr(
    type_name: str,
    parameter_name: str,
) -> str:
    parameter_name = IDENTIFIER_OVERRIDES.get(parameter_name, parameter_name)
    if type_name in NON_STRUCT_TYPES:
        return "&" + parameter_name
    else:
        return parameter_name


def format_arguments_count(
    args: list[ArgumentOrSingletonOrMember] | list[Argument] | None,
    is_vararg: bool = False,
) -> str:
    argc = len(args or "")
    return f"{argc} + argc" if is_vararg else str(argc)


def format_arguments_array(
    array_name: str,
    args: list[ArgumentOrSingletonOrMember] | list[Argument] | None,
    is_vararg: bool = False,
) -> str:
    args = args or []
    args_len = len(args)
    array_size = f"{args_len} + argc" if is_vararg else str(args_len)
    lines = [
        f"GDExtensionConstTypePtr {array_name}[{array_size}];",
    ]
    for i, arg in enumerate(args):
        to_ptr = format_value_to_ptr(arg['type'], arg['name'])
        lines.append(f"{array_name}[{i}] = {to_ptr};")
    if is_vararg:
        lines.append(f"if (argc > 0) memcpy({array_name} + {args_len}, argv, argc * sizeof(const godot_Variant *));")
    return "\n".join(lines)


def format_type_snake_case(
    type_name: str,
) -> str:
    return re.sub("([a-z])([A-Z])|([0-9])(A)", r"\1\3_\2\4", type_name).lower()


def format_type_to_variant_enum(
    type_name: str | None,
) -> str:
    if type_name and type_name.lower() == 'variant':
        type_name = 'nil'
    return ("GDEXTENSION_VARIANT_TYPE_"
            + format_type_snake_case(type_name or 'nil').upper())


def format_operator_to_enum(
    name: str,
) -> str:
    return "GDEXTENSION_VARIANT_OP_" + OPERATOR_TO_C.get(name, name).upper()


def format_vararg_macro(
    name: str,
    non_vararg_arg_count: int,
) -> str:
    args = ", ".join(f"arg{i}" for i in range(non_vararg_arg_count))
    argv = "(const godot_Variant *[]){ __VA_ARGS__ }"
    argc = f"sizeof({argv}) / sizeof(const godot_Variant *)"
    return f"#define godot_{name}_v({args}, ...) godot_{name}({args}, {argc}, {argv})"

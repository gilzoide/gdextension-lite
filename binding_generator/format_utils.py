"""
Internal utilities for Godot types
"""

from textwrap import dedent
from typing import Tuple

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
    '<<': 'bit_shift_left',
    '>>': 'bit_shift_right',
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
}


def code_block(code: str) -> str:
    return dedent(code).strip()


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


############################################################
# Functions pointer variables + custom implementations
############################################################
def format_constructor_pointer(
    type_name: str,
    ctor: Constructor,
) -> Tuple[str, str]:
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
    return (
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
    )


def format_destructor_pointer(
    type_name: str,
) -> Tuple[str, str]:
    function_name = f"destroy_{type_name}"
    proto_ptr = f"GDExtensionPtrDestructor godot_ptr_{function_name}"
    proto_typed = (f"void godot_{function_name}("
                   f"{format_parameter(type_name, 'self')})")
    return (
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
    )


def format_type_from_to_variant(
    type_name: str,
) -> Tuple[str, str]:
    proto_type_ptr = ("GDExtensionTypeFromVariantConstructorFunc"
                      f" godot_ptr_{type_name}_from_Variant")
    proto_type_typed = (f"godot_{type_name}"
                        f" godot_{type_name}_from_Variant("
                        f"{format_parameter('Variant', 'value')})")
    proto_variant_ptr = ("GDExtensionVariantFromTypeConstructorFunc"
                         f" godot_ptr_Variant_from_{type_name}")
    proto_variant_typed = (f"godot_Variant"
                           f" godot_Variant_from_{type_name}("
                           f"{format_parameter(type_name, 'value')})")
    return (
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
    )


def format_member_pointers(
    type_name: str,
    member: ArgumentOrSingletonOrMember,
) -> Tuple[str, str]:
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
    return (
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
    )


def format_indexing_pointers(
    type_name: str,
    is_keyed: bool,
    return_type: str,
) -> Tuple[str, str]:
    if is_keyed:
        set_name = f"{type_name}_keyed_set"
        set_ptr = f"GDExtensionPtrKeyedSetter godot_ptr_{set_name}"
        set_typed = (f"void godot_{set_name}("
                     f"{format_parameter(type_name, 'self')}, "
                     f"{format_parameter_const('Variant', 'key')}, "
                     f"{format_parameter_const(return_type, 'value')})")
        get_name = f"{type_name}_keyed_get"
        get_ptr = f"GDExtensionPtrKeyedGetter godot_ptr_{get_name}"
        get_typed = (f"godot_{return_type} godot_{get_name}("
                     f"{format_parameter_const(type_name, 'self')}, "
                     f"{format_parameter_const('Variant', 'key')})")
    else:
        set_name = f"{type_name}_indexed_set"
        set_ptr = f"GDExtensionPtrIndexedSetter godot_ptr_{set_name}"
        set_typed = (f"void godot_{set_name}("
                     f"{format_parameter(type_name, 'self')}, "
                     f"{format_parameter_const('int', 'key')}, "
                     f"{format_parameter_const(return_type, 'value')})")
        get_name = f"{type_name}_indexed_get"
        get_ptr = f"GDExtensionPtrIndexedGetter godot_ptr_{get_name}"
        get_typed = (f"godot_{return_type} godot_{get_name}("
                     f"{format_parameter_const(type_name, 'self')}, "
                     f"{format_parameter_const('int', 'key')})")
    return (
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
    )


def format_operator_pointer(
    type_name: str,
    operator: Operator,
) -> Tuple[str, str]:
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
    return (
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
    )


def format_method_pointer(
    type_name: str,
    method: BuiltinClassMethod
) -> Tuple[str, str]:
    return_type = method.get("return_type")
    proto_return_type = f"godot_{return_type}" if return_type else "void"

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

    proto_args = ", ".join(proto_args)

    function_name = f"{type_name}_{method['name']}"
    proto_ptr = f"GDExtensionPtrBuiltInMethod godot_ptr_{function_name}"
    proto_typed = f"{proto_return_type} godot_{function_name}({proto_args})"

    return (
        code_block(f"""
            extern {proto_ptr};
            {proto_typed};
        """),
        code_block(f"""
            {proto_ptr};
            {proto_typed} {{
            \t{proto_return_type + " result;" if return_type else ""}
            \t{format_arguments_array('args', arguments)};
            \tgodot_ptr_{function_name}({
                "NULL"
                if is_static
                else "(GDExtensionTypePtr) self"
            }, args, {
                "&result"
                if return_type
                else "NULL"
            }, {
                len(arguments)
                if arguments
                else 0
            });
            \t{"return result;" if return_type else ""}
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


def format_value_to_ptr(
    type_name: str,
    parameter_name: str,
) -> str:
    parameter_name = IDENTIFIER_OVERRIDES.get(parameter_name, parameter_name)
    if type_name in NON_STRUCT_TYPES:
        return "&" + parameter_name
    else:
        return parameter_name


def format_arguments_array(
    array_name: str,
    args: list[ArgumentOrSingletonOrMember] | list[Argument] | None,
) -> str:
    if args:
        values = (" "
                  + ", ".join(format_value_to_ptr(arg["type"], arg["name"])
                              for arg in args)
                  + " ")

    else:
        values = ""
    return f"const GDExtensionConstTypePtr {array_name}[] = {{{values}}}"

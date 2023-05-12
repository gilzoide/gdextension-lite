"""
Internal utilities for Godot types
"""

from json_types import *

NON_STRUCT_TYPES = (
    'Nil',
    'bool',
    'int',
    'float',
)


OPERATOR_TO_C = {
    '+': 'plus',
    '-': 'minus',
    'unary+': 'unary_plus',
    'unary-': 'unary_minus',
    '*': 'multiply',
    '/': 'divide',
    '**': 'power',
    '~': 'bit_not',
    '%': 'modulo',
    '==': 'is_equal_to',
    '!=': 'is_not_equal_to',
    '<': 'is_less_than',
    '<=': 'is_less_than_or_equal_to',
    '>': 'is_greater_than',
    '>=': 'is_greater_than_or_equal_to',
    'in': 'is_in',
}


def should_generate_operator(type_name: str, arg_type: str | None) -> bool:
    return (type_name != 'Nil'
            and (type_name not in NON_STRUCT_TYPES
                 or (arg_type or 'Nil') not in NON_STRUCT_TYPES))


def should_generate_constructor(type_name: str, ctor: Constructor) -> bool:
    arguments = ctor.get("arguments")
    if arguments:
        return should_generate_operator(type_name, arguments[0]["type"])
    else:
        return should_generate_operator(type_name, None)


def format_operator_name(operator_name: str) -> str:
    return OPERATOR_TO_C.get(operator_name, operator_name)


def format_operator_pointer(operator_name: str,
                            type_name: str,
                            right_type: str | None) -> str:
    code = [
        "GDExtensionPtrOperatorEvaluator godot_ptr_",
        type_name,
        "_",
        format_operator_name(operator_name)
    ]
    if right_type:
        code.append("_")
        code.append(right_type)
    code.append(";")
    return "".join(code)


def format_constructor_pointer(type_name: str, ctor: Constructor) -> str:
    code = [
        "GDExtensionPtrConstructor godot_ptr_new_",
        type_name,
    ]
    arguments = ctor.get("arguments")
    if arguments:
        code.append("_from")
        code.extend(f"_{arg['type']}" for arg in arguments)
    code.append(";")
    return "".join(code)


def format_destructor_pointer(type_name: str) -> str:
    return f"GDExtensionPtrDestructor godot_ptr_destroy_{type_name};"


def format_method_pointer(type_name: str, method: BuiltinClassMethod) -> str:
    return "".join([
        "GDExtensionPtrBuiltInMethod godot_ptr_",
        type_name,
        "_",
        method["name"],
        ";",
    ])

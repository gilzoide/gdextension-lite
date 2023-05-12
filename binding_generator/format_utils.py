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


def format_operator_pointer(operator_name: str,
                            type_name: str,
                            right_type: str | None) -> str:
    code = [
        "GDExtensionPtrOperatorEvaluator godot_ptr_",
        type_name,
        "_op_",
        OPERATOR_TO_C.get(operator_name, operator_name),
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


def format_type_from_variant(type_name: str) -> str:
    return ("GDExtensionTypeFromVariantConstructorFunc"
            f" godot_ptr_{type_name}_from_Variant;")


def format_variant_from_type(type_name: str) -> str:
    return ("GDExtensionVariantFromTypeConstructorFunc"
            f" godot_ptr_Variant_from_{type_name};")

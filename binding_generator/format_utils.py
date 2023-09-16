"""
Internal utilities for Godot types
"""

from collections import defaultdict
import re
from textwrap import dedent
from typing import Sequence

from json_types import *

NON_STRUCT_TYPES = (
    'Nil',
    'bool',
    'int',
    'float',
)


VARIANT_TYPES = (
    'Nil',
    'bool',
    'int',
    'float',
    'String',
    'Vector2',
    'Vector2i',
    'Rect2',
    'Rect2i',
    'Vector3',
    'Vector3i',
    'Transform2d',
    'Vector4',
    'Vector4i',
    'Plane',
    'Quaternion',
    'AABB',
    'Basis',
    'Transform3d',
    'Projection',
    'Color',
    'StringName',
    'NodePath',
    'RID',
    'Callable',
    'Signal',
    'Dictionary',
    'Array',
    'PackedByteArray',
    'PackedInt32Array',
    'PackedInt64Array',
    'PackedFloat32Array',
    'PackedFloat64Array',
    'PackedStringArray',
    'PackedVector2Array',
    'PackedVector3Array',
    'PackedColorArray',
    'Variant',
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
    'bool': 'b',
    'char': 'chr',
    'class': 'cls',
    'default': 'default_value',
    'enum': 'enumeration',
    'operator': 'op',
    'template': 'tmplt',
}


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
    def __init__(self, prototype: str, implementation: str, **extras: str):
        self.prototype = prototype
        self.implementation = implementation
        self.extras = extras

    def __getitem__(self, key: str) -> str:
        return self.extras.get(key, "")

    def prepend_section_comment(self, comment: str):
        if self.prototype:
            self.prototype = f"// {comment}\n{self.prototype}"
        if self.implementation:
            self.implementation = f"// {comment}\n{self.implementation}"

    @classmethod
    def merge(cls, bindings: Sequence["BindingCode"], **kwargs: list[str]) -> "BindingCode":
        extras: dict = defaultdict(list, **kwargs)
        for b in bindings:
            for k, v in b.extras.items():
                extras[k].append(v)
        for k, v in extras.items():
            extras[k] = "\n".join(v)
        return BindingCode(
            "\n\n".join(b.prototype for b in bindings if b.prototype),
            "\n\n".join(b.implementation for b in bindings if b.implementation),
            **extras,
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
    elif type_name.startswith("enum::"):
        return f"godot_{type_name[6:].replace('.', '_')} {parameter_name}"
    elif type_name.endswith("*"):
        if 'void' in type_name or '_t' in type_name:
            return f"{type_name} {parameter_name}"
        else:
            return f"godot_{type_name} {parameter_name}"
    
    if type_name.startswith("typedarray::"):
        type_name = f"TypedArray(godot_{type_name[len('typedarray::'):]})"
    if type_name.startswith("bitfield::"):
        type_name = type_name[len("bitfield::"):].replace('.', '_')
    if is_const:
        return f"const godot_{type_name} *{parameter_name or ''}"
    else:
        return f"godot_{type_name} *{parameter_name or ''}"


def format_parameter_const(
    type_name: str,
    parameter_name: str,
) -> str:
    return format_parameter(type_name, parameter_name, is_const=True)


def format_return_type(
    type_name: str | None,
) -> str:
    if type_name is None:
        return "void"
    elif type_name.startswith("enum::"):
        return f"godot_{type_name[len('enum::'):].replace('.', '_')}"
    elif type_name.startswith("typedarray::"):
        return f"godot_TypedArray(godot_{type_name[len('typedarray::'):]})"
    elif type_name.startswith("bitfield::"):
        return f"godot_{type_name[len('bitfield::'):].replace('.', '_')}"
    elif type_name.endswith("*"):
        return type_name.replace('Glyph', 'godot_Glyph')
    elif type_name not in VARIANT_TYPES:
        return f"godot_{type_name} *"
    else:
        return f"godot_{type_name}"


def format_native_struct_field(
    field_declaration: str,
) -> str:
    if "=" in field_declaration:
        field_declaration = re.sub(r"\s*=.*", "", field_declaration)
    if "::" in field_declaration:
        return f"godot_{field_declaration.replace('::', '_').replace('.', '_')}"
    elif field_declaration.startswith('int') or field_declaration.startswith('float') or field_declaration.startswith('uint'):
        return field_declaration
    else:
        return f"godot_{field_declaration}"


def format_value_to_ptr(
    type_name: str | None,
    parameter_name: str,
) -> str:
    if type_name is None:
        return "NULL"

    parameter_name = IDENTIFIER_OVERRIDES.get(parameter_name, parameter_name)
    if type_name in NON_STRUCT_TYPES or type_name.startswith("enum::"):
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

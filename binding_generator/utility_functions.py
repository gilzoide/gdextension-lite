"""
Generates bindings for Godot's utility functions
"""

from textwrap import indent

from common.binding_code import BindingCode
from format_utils import (code_block,
                          format_arguments_array,
                          format_arguments_count,
                          format_parameter_const,
                          format_return_type,
                          format_vararg_macro)
from json_types import UtilityFunction


def format_utility_function(
    function: UtilityFunction
) -> BindingCode:
    return_type = function.get("return_type")
    proto_return_type = format_return_type(return_type)

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
            {proto_typed};
            {format_vararg_macro(function_name, non_vararg_argc) if is_vararg else ""}
        """),
        code_block(f"""
            {proto_ptr};
            {proto_typed} {{
            \tGDEXTENSION_LITE_LAZY_INIT_UTILITY_FUNCTION({function_name}, {function['hash']});
            \t{proto_return_type + " _ret;" if return_type else ""}
{indent(format_arguments_array('_args', arguments, is_vararg), '            	')}
            \tgodot_ptr_{function_name}({
                "&_ret"
                if return_type
                else "NULL"
            }, _args, {format_arguments_count(arguments, is_vararg)});
            \t{"return _ret;" if return_type else ""}
            }}
        """),
    )


def generate_utility_functions(
    utility_functions: list[UtilityFunction],
) -> BindingCode:
    definitions = [format_utility_function(f) for f in utility_functions]
    includes = [
        "../gdextension/gdextension_interface.h",
        "../variant/all.h",
    ]
    implementation_includes = [
        "<string.h>",
    ]
    return BindingCode.merge(definitions,
                             includes=includes,
                             implementation_includes=implementation_includes)

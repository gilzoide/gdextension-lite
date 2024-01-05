from common.binding_code import BindingCode
from misc.singleton_getter import SingletonGetterCode
from json_types import ArgumentOrSingletonOrMember

def generate_singleton_getters(
    singletons: list[ArgumentOrSingletonOrMember],
) -> BindingCode:
    definitions = [SingletonGetterCode(singleton).get_c_code() for singleton in singletons]
    includes = [
        "../definition-macros.h",
        "class-stubs/all.h",
    ]
    return BindingCode.merge(definitions, includes=includes)

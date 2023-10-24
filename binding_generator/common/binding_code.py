from collections import defaultdict
from collections.abc import Iterable
from textwrap import indent


class BindingCode:
    """Object that contains the code necessary for each function binding"""
    def __init__(self, prototype: str = "", implementation: str = "", **extras: list[str]):
        self.prototype = prototype
        self.implementation = implementation
        self.extras = extras

    def __getitem__(self, key: str) -> list[str]:
        return self.extras.get(key, [])

    def __bool__(self) -> bool:
        return bool(self.prototype) or bool(self.implementation) or bool(self.extras)

    def add_extras(self, **extras: list[str]) -> None:
        for k, v in extras.items():
            lst = self.extras.get(k, [])
            lst.extend(v)
            self.extras[k] = lst

    def surround_prototype(self, prefix: str, suffix: str, add_indent: bool = True) -> None:
        if self.prototype:
            self.prototype = "\n".join([
                prefix,
                indent(self.prototype, "\t") if add_indent else self.prototype,
                suffix,
            ])

    def surround_implementation(self, prefix: str, suffix: str, add_indent: bool = True) -> None:
        if self.implementation:
            self.implementation = "\n".join([
                prefix,
                indent(self.implementation, "\t") if add_indent else self.implementation,
                suffix,
            ])

    def format_as_section(self, comment: str):
        self.surround_prototype(f"// {comment}", "", add_indent=False)
        self.surround_implementation(f"// {comment}", "", add_indent=False)

    @classmethod
    def merge(cls, bindings: Iterable["BindingCode"], extra_newline=False, **kwargs: list[str]) -> "BindingCode":
        prototype = []
        implementation = []
        extras = defaultdict(list, **kwargs)
        for b in bindings:
            if b.prototype:
                prototype.append(b.prototype)
            if b.implementation:
                implementation.append(b.implementation)
            for k, v in b.extras.items():
                extras[k].extend(v)
        separator = "\n\n" if extra_newline else "\n"
        return BindingCode(
            separator.join(prototype),
            separator.join(implementation),
            **extras,
        )


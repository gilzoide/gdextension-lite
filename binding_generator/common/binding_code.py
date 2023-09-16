from collections import defaultdict
from textwrap import indent
from typing import Sequence


class BindingCode:
    """Object that contains the code necessary for each function binding"""
    def __init__(self, prototype: str = "", implementation: str = "", **extras: list[str]):
        self.prototype = prototype
        self.implementation = implementation
        self.extras = extras

    def __getitem__(self, key: str) -> list[str]:
        return self.extras.get(key, [])

    def add_extras(self, **extras: list[str]) -> None:
        for k, v in extras.items():
            lst = self.extras.get(k, [])
            lst.extend(v)
            self.extras[k] = lst

    def surround_prototype(self, prefix: str, suffix: str, add_indent: bool = True) -> None:
        self.prototype = "\n".join([
            prefix,
            indent(self.prototype, "\t") if add_indent else self.prototype,
            suffix,
        ])

    def surround_implementation(self, prefix: str, suffix: str, add_indent: bool = True) -> None:
        self.implementation = "\n".join([
            prefix,
            indent(self.implementation, "\t") if add_indent else self.implementation,
            suffix,
        ])

    def prepend_section_comment(self, comment: str):
        if self.prototype:
            self.prototype = f"// {comment}\n{self.prototype}"
        if self.implementation:
            self.implementation = f"// {comment}\n{self.implementation}"

    @classmethod
    def merge(cls, bindings: Sequence["BindingCode"], **kwargs: list[str]) -> "BindingCode":
        extras = defaultdict(list, **kwargs)
        for b in bindings:
            for k, v in b.extras.items():
                extras[k].extend(v)
        return BindingCode(
            "\n\n".join(b.prototype for b in bindings if b.prototype),
            "\n\n".join(b.implementation for b in bindings if b.implementation),
            **extras,
        )


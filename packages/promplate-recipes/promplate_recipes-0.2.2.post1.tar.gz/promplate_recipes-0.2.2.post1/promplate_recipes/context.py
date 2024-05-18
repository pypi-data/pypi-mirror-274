from collections import defaultdict
from functools import cached_property, partial
from pathlib import Path

from box import Box
from promplate import Context, Template
from promplate.prompt.template import SafeChainMapContext
from promplate.prompt.utils import get_builtins


@partial(partial, default_box=True)
class SilentBox(Box):
    def __str__(self):
        return super().__str__() if len(self) else ""

    if __debug__:

        def __call__(self, *args, **kwargs):
            print(f"{self.__class__} shouldn't be called {args = } {kwargs = }")
            return ""


class BuiltinsLayer(dict):
    def __getitem__(self, key):
        return get_builtins()[key]

    def __contains__(self, key):
        return key in get_builtins()

    def __repr__(self):
        return "{ builtins }"


class ComponentsLayer(dict):
    def __init__(self, path: str | Path, pattern="**/*"):
        self.path = Path(path)
        self.pattern = pattern

    if __debug__:

        def __getitem__(self, key: str):
            try:
                return DotTemplate.read(next(self.path.glob(f"**/{key}.*")))
            except StopIteration:
                raise KeyError(key) from None

    else:

        @cached_property
        def templates(self):
            return {i.name.split(".", 1)[0]: DotTemplate.read(i) for i in self.path.glob(self.pattern)}

        def __getitem__(self, key: str):
            return self.templates[key]

    def __repr__(self):
        return "{ components }"


layers = []


def make_context(context: Context | None = None):
    if context is None:
        return SafeChainMapContext(*layers, BuiltinsLayer(), defaultdict(SilentBox))
    return SafeChainMapContext(dict(SilentBox(context)), *layers, BuiltinsLayer(), defaultdict(SilentBox))


class DotTemplate(Template):
    def render(self, context=None):
        return super().render(make_context(context))

    async def arender(self, context=None):
        return await super().arender(make_context(context))


def register_components(path: str | Path, pattern="**/*"):
    layers.append(ComponentsLayer(path, pattern))

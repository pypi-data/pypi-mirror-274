"""
Parser registry.

List of available parsers.
"""

from importlib.metadata import entry_points

from lute.parse.base import AbstractParser
from lute.parse.space_delimited_parser import SpaceDelimitedParser, TurkishParser
from lute.parse.mecab_parser import JapaneseParser
from lute.parse.character_parser import ClassicalChineseParser


__LUTE_PARSERS__ = {
    "spacedel": SpaceDelimitedParser,
    "turkish": TurkishParser,
    "japanese": JapaneseParser,
    "classicalchinese": ClassicalChineseParser,
}


def init_parser_plugins():
    """
    Initialize parsers from plugins
    """
    custom_parser_eps = entry_points().get("lute.plugin.parse", [])
    for custom_parser_ep in custom_parser_eps:
        if _is_valid(custom_parser_ep.load()):
            __LUTE_PARSERS__[custom_parser_ep.name] = custom_parser_ep.load()
        else:
            raise ValueError(
                f"{custom_parser_ep.name} is not a subclass of AbstractParser"
            )


def _is_valid(custom_parser):
    return issubclass(custom_parser, AbstractParser)


def _supported_parsers():
    "Get the supported parsers."
    ret = {}
    for k, v in __LUTE_PARSERS__.items():
        if v.is_supported():
            ret[k] = v
    return ret


def get_parser(parser_name) -> AbstractParser:
    "Return the supported parser with the given name."
    if parser_name in _supported_parsers():
        pclass = __LUTE_PARSERS__[parser_name]
        return pclass()
    raise ValueError(f"Unknown parser type '{parser_name}'")


def is_supported(parser_name) -> bool:
    "Return True if the specified parser is present and supported."
    if parser_name not in __LUTE_PARSERS__:
        return False
    p = __LUTE_PARSERS__[parser_name]
    return p.is_supported()


def supported_parsers():
    """
    List of supported parser strings and class names, for UI.

    For select list entries, use supported_parsers().items().
    """
    return [(k, v.name()) for k, v in _supported_parsers().items()]


def supported_parser_types():
    """
    List of supported Language.parser_types
    """
    return list(_supported_parsers().keys())

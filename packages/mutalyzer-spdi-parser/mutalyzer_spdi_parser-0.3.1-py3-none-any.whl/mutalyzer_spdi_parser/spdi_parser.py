"""
Module for parsing SPDI variant descriptions.
"""

import os

from lark import Lark


def _read_grammar_file(file_name):
    grammar_path = os.path.join(os.path.dirname(__file__), f"ebnf/{file_name}")
    with open(grammar_path) as grammar_file:
        return grammar_file.read()


class SpdiParser:
    """
    SPDI parser object.
    """

    def __init__(self, grammar_path=None, ignore_white_spaces=True):
        """
        :arg str grammar_path: Path to a different EBNF grammar file.
        :arg str start_rule: Alternative start rule for the grammar.
        :arg bool ignore_white_spaces: Ignore or not white spaces in the description.
        """
        self._grammar_path = grammar_path
        self._ignore_whitespaces = ignore_white_spaces
        self._create_parser()

    def _create_parser(self):
        if self._grammar_path:
            with open(self._grammar_path) as grammar_file:
                grammar = grammar_file.read()
        else:
            grammar = _read_grammar_file("top.g")

        if self._ignore_whitespaces:
            grammar += "\n%import common.WS\n%ignore WS"

        self._parser = Lark(grammar, parser="earley", start="description")

    def parse(self, description):
        """
        Parse the provided description.

        :arg str description: An SPDI description.
        :returns: A parse tree.
        :rtype: lark.Tree
        """
        parse_tree = self._parser.parse(description)
        return parse_tree


def parse(description, grammar_path=None):
    """
    Parse the provided SPDI `description`, or the description part,
    e.g., a location, a variants list, etc., if an appropriate alternative
    `start_rule` is provided.

    :arg str description: Description (or description part) to be parsed.
    :arg str grammar_path: Path towards a different grammar file.
    :returns: Parse tree.
    :rtype: lark.Tree
    """
    parser = SpdiParser(grammar_path)

    return parser.parse(description)

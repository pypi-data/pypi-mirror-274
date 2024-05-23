"""
CLI entry point.
"""

import argparse
import json

from lark.tree import pydot__tree_to_png

from . import usage, version
from .convert import parse_tree_to_model, to_hgvs_internal_model
from .spdi_parser import parse


def _parse(description, grammar_path):
    """
    CLI wrapper for parsing with no conversion to model.
    """
    parse_tree = parse(description, grammar_path)
    print(f"Successfully parsed:\n {description}")
    return parse_tree


def _to_spdi_model(description):
    """
    CLI wrapper for parsing, converting, and printing the model.
    """
    parse_tree = parse(description)
    model = parse_tree_to_model(parse_tree)
    if isinstance(model, (dict, list)):
        print(json.dumps(model, indent=2))
    else:
        print(model)
    return parse_tree


def _to_hgvs_internal_model(description):
    """
    CLI wrapper for parsing, converting, and printing the HGVS internal model.
    """
    parse_tree = parse(description)
    model = to_hgvs_internal_model(description)
    if isinstance(model, (dict, list)):
        print(json.dumps(model, indent=2))
    else:
        print(model)
    return parse_tree


def _arg_parser():
    """
    Command line argument parsing.
    """
    parser = argparse.ArgumentParser(
        description=usage[0],
        epilog=usage[1],
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("description", help="the SPDI variant description to be parsed")

    alt = parser.add_mutually_exclusive_group()

    alt.add_argument(
        "-cs", action="store_true", help="convert the description to the model"
    )

    alt.add_argument(
        "-ch",
        action="store_true",
        help="convert to the HGVS internal coordinates model",
    )

    parser.add_argument(
        "-i", help="save the parse tree as a PNG image (pydot required!)"
    )

    parser.add_argument("-v", action="version", version=version(parser.prog))

    return parser


def _cli(args):
    if args.cs:
        parse_tree = _to_spdi_model(args.description)
    elif args.ch:
        parse_tree = _to_hgvs_internal_model(args.description)

    if args.i and parse_tree:
        pydot__tree_to_png(parse_tree, args.i)
        print(f"Parse tree image saved to:\n {args.i}")


def main():
    parser = _arg_parser()
    args = parser.parse_args()
    _cli(args)


if __name__ == "__main__":
    main()

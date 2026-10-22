"""Command line: python -m onyx <command>."""

import argparse
import sys

from onyx import audit, bakeoff, coordinator, data, eval, gaps, kb, runs, selftest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="onyx",
        description="Mizan (team Onyx): governed consumer-care agents. Synthetic operator and subscribers.",
    )
    subparsers = parser.add_subparsers(dest="command", metavar="<command>")
    kb.register(subparsers)
    data.register(subparsers)
    audit.register(subparsers)
    coordinator.register(subparsers)
    runs.register(subparsers)
    eval.register(subparsers)
    bakeoff.register(subparsers)
    selftest.register(subparsers)
    gaps.register(subparsers)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
        return 0
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())

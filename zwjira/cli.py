import argparse

from .config import command_config, command_reset_config
from .commands import command_mark_fixed


def parse_args():
    parser = argparse.ArgumentParser(prog="zwjira")
    parser.add_argument("subcommand")
    parser.add_argument("args", nargs="*")
    return parser.parse_args()


def main():
    args = parse_args()
    command = globals().get("command_" + args.subcommand)
    if command is None:
        print("Error: unknown command {!r}.".format(args.subcommand))
        return 1
    return command(*args.args)

import argparse
import pathlib
from dataclasses import dataclass


@dataclass
class ParsedArgs:
    bundle: bool
    project_ids: [str]
    destination_path: pathlib.Path


def valid_dir_arg(value):
    """Determine if the value is a valid directory"""
    filepath = pathlib.Path(value)

    if not filepath.exists() or not filepath.is_dir():
        msg = f"Error! This is not a directory: {value}"
        raise argparse.ArgumentTypeError(msg)
    else:
        return filepath


def parse_args(args):
    parser = argparse.ArgumentParser(description="Generate Watchtower content.")
    parser.add_argument("-b", "--bundle", action=argparse.BooleanOptionalAction)
    parser.add_argument(
        "-p",
        "--projects",
        nargs="*",
        type=str,
        default=[],
        help="Optional list of projects",
    )
    parser.add_argument("-d", "--destination", type=valid_dir_arg)
    args = parser.parse_args(args)
    destination_path = args.destination or pathlib.Path.cwd()

    return ParsedArgs(
        bundle=args.bundle,
        project_ids=[] or args.projects,
        destination_path=destination_path,
    )

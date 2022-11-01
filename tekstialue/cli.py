import argparse
import pathlib
import sys
from typing import List, Union

import tekstialue.tekstialue as api
from tekstialue import APP_ALIAS, APP_NAME, DEFAULT_CONFIG_NAME, log


def parse_request(argv: List[str]) -> Union[int, argparse.Namespace]:
    """DRY."""
    parser = argparse.ArgumentParser(
        prog=APP_ALIAS, description=APP_NAME, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '--config',
        '-c',
        dest='cfg_file',
        default='',
        help=f'Configuration file to read column defs from. Optional\n(default: {DEFAULT_CONFIG_NAME})',
        required=False,
    )
    parser.add_argument(
        '--input',
        '-i',
        dest='in_file',
        default='',
        help='File to transform from. Optional\n(default: positional in-file (first) value)',
        required=False,
    )
    parser.add_argument(
        'in_file_pos',
        nargs='?',
        default='',
        help='File to transform from. Optional\n(default: value of input option)',
    )
    parser.add_argument(
        '--output',
        '-o',
        dest='out_file',
        default='',
        help='File to transform to. Optional\n(default: in-file.out)',
        required=False,
    )
    parser.add_argument(
        '--from',
        '-f',
        dest='from_format',
        default='latex',
        help='format to transform from (default: latex)',
        required=False,
    )
    parser.add_argument(
        '--to',
        '-t',
        dest='to_format',
        default='latex',
        help='format to transform to (default: latex)',
        required=False,
    )
    parser.add_argument(
        '--verbose',
        '-v',
        dest='verbose',
        default=False,
        action='store_true',
        help='work logging more information along the way (default: False)',
    )
    parser.add_argument(
        '--debug',
        '-d',
        dest='debug',
        default=False,
        action='store_true',
        help='be even more vrbose to support debugging (default: False)',
    )
    if not argv:
        parser.print_help()
        return 0

    options = parser.parse_args(argv)

    if not options.in_file:
        if options.in_file_pos:
            options.in_file = options.in_file_pos

    if not options.out_file:
        options.out_file = f'{options.in_file}.out'

    if options.from_format != 'latex':
        log.error(f'unsupported from format {options.from_format} - only latex currently supported')
        return 2

    if options.to_format != 'latex':
        log.error(f'unsupported to format {options.to_format} - only latex currently supported')
        return 2

    if pathlib.Path(options.in_file).is_file():
        return options

    log.error(f'input {options.in_file} does not exist or is no file')
    return 1


def main(argv: Union[List[str], None] = None) -> int:
    """Delegate processing to functional module."""
    argv = sys.argv[1:] if argv is None else argv
    options = parse_request(argv)
    if isinstance(options, int):
        return options
    return api.main(options)  # type: ignore

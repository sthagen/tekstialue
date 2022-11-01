"""Purge monotonically named files in folders keeping range endpoints.

Implementation uses sha256 hashes for identity and assumes that
the natural order relates to the notion of fresher or better.
"""
import argparse
import datetime as dti
import logging
import typing

from tekstialue import ENCODING, log


@typing.no_type_check
def main(options: argparse.Namespace) -> int:
    """Process the text."""
    start_time = dti.datetime.utcnow()
    verbose = options.verbose
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    in_file, out_file = options.in_file, options.out_file
    with open(in_file, 'rt', encoding=ENCODING) as handle:
        lines = [line.rstrip() for line in handle.readlines()]
    log.debug(f'Read {len(lines)} lines from {in_file}')

    with open(out_file, 'wt', encoding=ENCODING) as handle:
        handle.write('\n'.joine(lines) + '\n')
    log.debug(f'Wrote {len(lines)} lines to {out_file}')

    duration_seconds = (dti.datetime.utcnow() - start_time).total_seconds()

    log.info(f'transformed tables in {in_file} into {out_file}' f' in {duration_seconds} secs')
    return 0

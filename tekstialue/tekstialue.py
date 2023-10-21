"""Purge monotonically named files in folders keeping range endpoints.

Implementation uses sha256 hashes for identity and assumes that
the natural order relates to the notion of fresher or better.
"""
import argparse
import datetime as dti
import json
import logging
import pathlib
from typing import no_type_check

from tekstialue import DEFAULT_CONFIG_NAME, ENCODING, log

TAB_START_TOK = r'\begin{longtable}[]{@{}'
TOP_RULE = r'\toprule()'
MID_RULE = r'\midrule()'
END_HEAD = r'\endhead'
END_DATA_ROW = r'\\'
BOT_RULE = r'\bottomrule()'
TAB_END_TOK = r'\end{longtable}'

TAB_NEW_START = r"""\begin{small}
\begin{longtable}[]{|
>{\raggedright\arraybackslash}p{(\columnwidth - 12\tabcolsep) * \real{0.1500}}|
>{\raggedright\arraybackslash}p{(\columnwidth - 12\tabcolsep) * \real{0.5500}}|
>{\raggedright\arraybackslash}p{(\columnwidth - 12\tabcolsep) * \real{0.1500}}|
>{\raggedright\arraybackslash}p{(\columnwidth - 12\tabcolsep) * \real{0.2000}}|}
\hline"""

TAB_HACKED_HEAD = r"""\begin{minipage}[b]{\linewidth}\raggedright
\ \mbox{\textbf{$COL1$}}
\end{minipage} & \begin{minipage}[b]{\linewidth}\raggedright
\mbox{\textbf{$COL2$}}
\end{minipage} & \begin{minipage}[b]{\linewidth}\raggedright
\mbox{\textbf{$COL3_A$}} \mbox{\textbf{$COL3_B$}}
\end{minipage} & \begin{minipage}[b]{\linewidth}\raggedright
\mbox{\textbf{$COL4_A$}} \mbox{\textbf{$COL4_B$}}
\end{minipage} \\
\hline
\endfirsthead
\multicolumn{4}{@{}l}{\small \ldots continued}\\\hline
\hline
\begin{minipage}[b]{\linewidth}\raggedright
\ \mbox{\textbf{$COL1$}}
\end{minipage} & \begin{minipage}[b]{\linewidth}\raggedright
\mbox{\textbf{$COL2$}}
\end{minipage} & \begin{minipage}[b]{\linewidth}\raggedright
\mbox{\textbf{$COL3_A$}} \mbox{\textbf{$COL3_B$}}
\end{minipage} & \begin{minipage}[b]{\linewidth}\raggedright
\mbox{\textbf{$COL4_A$}} \mbox{\textbf{$COL4_B$}}
\end{minipage} \\
\endhead
\hline"""

COL_1 = 'a'
COL_2 = 'b'
COL_3_A = 'c'
COL_3_B = 'cc'
COL_4_A = 'd'
COL_4_B = 'dd'

NEW_RULE = r'\hline'

TAB_NEW_END = r"""\end{longtable}
\end{small}
\vspace*{-2em}
\begin{footnotesize}
ANNOTATION
\end{footnotesize}"""

Slots = list[tuple[int, int]]
TableRanges = list[dict[str, int | list[int]]]


@no_type_check
def discover_configuration(conf: str) -> tuple[int, dict[str, object], str]:
    """Try to retrieve the configuration following the "(explicit, local, parents, home)
    first wun wins" strategy."""
    configuration = None
    if conf:
        cp = pathlib.Path(conf)
        if not cp.is_file() or not cp.stat().st_size:
            log.error('Given configuration path is no file or empty')
            return 1, {}, ''
        log.debug(f'Reading configuration file {cp} as requested...')
        with cp.open(encoding=ENCODING) as handle:
            configuration = json.load(handle)
    else:
        cn = DEFAULT_CONFIG_NAME
        cwd = pathlib.Path.cwd().resolve()
        for pp in (cwd, *cwd.parents):
            cp = pp / cn
            if cp.is_file() and cp.stat().st_size:
                log.debug(f'Reading from discovered configuration path {cp}')
                with cp.open() as handle:
                    configuration = json.load(handle)
                return 0, configuration, str(cp)

        cp = pathlib.Path.home() / DEFAULT_CONFIG_NAME
        if cp.is_file() and cp.stat().st_size:
            log.debug(f'Reading configuration file {cp} from home directory at {pathlib.Path.home()} ...')
            with cp.open() as handle:
                configuration = json.load(handle)
            return 0, configuration, str(cp)

        log.debug(f'User home configuration path to {cp} is no file or empty - ignoring configuration data')

    return 0, configuration, str(cp)


@no_type_check
def cue_tables(lines: list[str]) -> TableRanges:
    """Tag all tables extracting the relevant line information for elements."""
    table_section, head, annotation = False, False, False
    table_ranges = []
    guess_slot = 0
    table_range = {}
    for n, text in enumerate(lines):
        if not table_section:
            if not text.startswith(TAB_START_TOK):
                continue
            table_range['start'] = n
            table_section = True
            head = True
            table_range['end_data_row'] = []
            continue

        if text.startswith(TOP_RULE):
            table_range['top_rule'] = n
            continue

        if text.startswith(MID_RULE):
            table_range['mid_rule'] = n
            continue

        if text.startswith(END_HEAD):
            table_range['end_head'] = n
            head = False
            continue

        if not head and text.strip().endswith(END_DATA_ROW):
            table_range['end_data_row'].append(n)
            continue

        if text.startswith(BOT_RULE):
            table_range['bottom_rule'] = n
            continue

        if text.startswith(TAB_END_TOK):
            table_range['end'] = n
            annotation = True
            guess_slot = n + 2
            continue

        if annotation and n == guess_slot:
            table_range['amend'] = n
            table_ranges.append(table_range)
            table_range = {}
            annotation, table_section = False, False

    return table_ranges


@no_type_check
def extract_slots(table_ranges: TableRanges) -> Slots:
    """Extract the on and off slots for output processing."""
    on_off_slots = []
    for table in table_ranges:
        from_here = table['start']
        thru_there = table['amend']
        on_off = (from_here, thru_there + 1)
        on_off_slots.append(on_off)

    return on_off_slots


@no_type_check
def weave_table(lines: list[str], on_off_slots: Slots, table_ranges: TableRanges, tab_hacked_head: str) -> list[str]:
    """Generate the output."""
    out = []
    next_slot = 0
    for n, line in enumerate(lines):
        if next_slot < len(on_off_slots):
            trigger_on, trigger_off = on_off_slots[next_slot]
            tb = table_ranges[next_slot]
        else:
            trigger_on = None
        if trigger_on is None:
            out.append(line)
            continue

        if n < trigger_on:
            out.append(line)
            continue
        if n == trigger_on:
            out.append(TAB_NEW_START)
            out.append(tab_hacked_head)
            continue
        if n <= tb['end_head']:
            continue
        if n < tb['bottom_rule']:
            out.append(line)
            if n in tb['end_data_row']:
                out.append(NEW_RULE)
            continue
        if tb['bottom_rule'] <= n < tb['amend']:
            continue
        if n == tb['amend']:
            out.append(TAB_NEW_END.replace('ANNOTATION', line))
            next_slot += 1

    return out


@no_type_check
def main(options: argparse.Namespace) -> int:
    """Process the text."""
    start_time = dti.datetime.utcnow()
    verbose = options.verbose
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    in_file, out_file = options.in_file, options.out_file

    code, cfg, cp = discover_configuration(options.cfg_file)
    if code:
        return code
    log.info(f'Read configiration from {cp}')
    log.debug(f'{cfg=}')
    cols = cfg['columns']
    tab_hacked_head = TAB_HACKED_HEAD.replace('$COL1$', cols['col_1'][0])
    tab_hacked_head = tab_hacked_head.replace('$COL2$', cols['col_2'][0])
    tab_hacked_head = tab_hacked_head.replace('$COL3_A$', cols['col_3'][0])
    tab_hacked_head = tab_hacked_head.replace('$COL3_B$', cols['col_3'][1])
    tab_hacked_head = tab_hacked_head.replace('$COL4_A$', cols['col_4'][0])
    tab_hacked_head = tab_hacked_head.replace('$COL4_B$', cols['col_4'][1])

    with open(in_file, 'rt', encoding=ENCODING) as handle:
        lines = [''] + [line.rstrip() for line in handle.readlines()]
    log.debug(f'Read {len(lines)} lines from {in_file}')

    table_ranges = cue_tables(lines)
    on_off_slots = extract_slots(table_ranges)

    out = weave_table(lines, on_off_slots, table_ranges, tab_hacked_head)
    with open(out_file, 'wt', encoding=ENCODING) as handle:
        handle.write('\n'.join(out) + '\n')
    log.debug(f'Wrote {len(lines)} lines to {out_file}')

    duration_seconds = (dti.datetime.utcnow() - start_time).total_seconds()

    log.info(f'transformed tables in {in_file} into {out_file}' f' in {duration_seconds} secs')
    return 0

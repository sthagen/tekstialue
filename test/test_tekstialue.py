import pathlib

import tekstialue.tekstialue as api

TEST_PREFIX = pathlib.Path('test', 'fixtures', 'basic')
DEFAULT_CFG_PATH = TEST_PREFIX / 'dot.tekstialue.json'
DEFAULT_REAL_IN_FILE_PATH = TEST_PREFIX / 'real-la.tex.in'


def test_cue_tables():
    assert api.cue_tables([]) == []


def test_cue_tables_for_real():
    with open(DEFAULT_REAL_IN_FILE_PATH, 'rt', encoding=api.ENCODING) as handle:
        lines = [''] + [line.rstrip() for line in handle.readlines()]
    assert api.cue_tables(lines) == [
        {
            'start': 2,
            'end_data_row': [21, 24],
            'top_rule': 7,
            'mid_rule': 17,
            'end_head': 18,
            'bottom_rule': 25,
            'end': 26,
            'amend': 28,
        }
    ]


def test_discover_configuration():
    code, cfg, cp = api.discover_configuration(DEFAULT_CFG_PATH)
    assert not code
    assert cp == str(DEFAULT_CFG_PATH)
    cols = cfg['columns']
    assert cols['col_1'] == ['a']
    assert cols['col_2'] == ['b']
    assert cols['col_3'] == ['c', 'cc']
    assert cols['col_4'] == ['d', 'dd']


def test_extract_slots():
    assert api.extract_slots([{'start': 0, 'amend': 42}]) == [(0, 42 + 1)]


def test_weave_table():
    assert api.weave_table([''], [], [], '') == ['']

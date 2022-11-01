import pathlib

import tekstialue.cli as cli

TEST_PREFIX = pathlib.Path('test', 'fixtures', 'basic')
DEFAULT_IN_FILE_PATH = TEST_PREFIX / 'in-file.tex'
DEFAULT_CFG_PATH = TEST_PREFIX / 'dot.tekstialue.json'
TEST_MAKE_MISSING = 'missing-this-file-for-'


def test_parse_request(capsys):
    options = cli.parse_request(['-i', str(DEFAULT_IN_FILE_PATH)])
    assert options.in_file_pos == ''  # type: ignore
    assert options.in_file == str(DEFAULT_IN_FILE_PATH)  # type: ignore
    out, err = capsys.readouterr()
    assert not out
    assert not err


def test_parse_request_verbose(capsys):
    options = cli.parse_request(['-i', str(DEFAULT_IN_FILE_PATH), '-v'])
    assert options.verbose
    out, err = capsys.readouterr()
    assert not out
    assert not err


def test_parse_request_config(capsys):
    options = cli.parse_request(['-i', str(DEFAULT_IN_FILE_PATH), '-c', str(DEFAULT_CFG_PATH)])
    assert options.cfg_file == str(DEFAULT_CFG_PATH)
    out, err = capsys.readouterr()
    assert not out
    assert not err


def test_parse_request_config_home(capsys):
    options = cli.parse_request(['-i', str(DEFAULT_IN_FILE_PATH)])
    assert options.cfg_file == ''
    out, err = capsys.readouterr()
    assert not out
    assert not err


def test_parse_empty_request(capsys):
    options = cli.parse_request([])
    assert options == 0
    out, err = capsys.readouterr()
    assert 'input' in out
    assert not err

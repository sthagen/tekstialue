import pathlib

import tekstialue.cli as cli

TEST_PREFIX = pathlib.Path('test', 'fixtures', 'basic')
DEFAULT_IN_FILE_PATH = TEST_PREFIX / 'in-file.tex'
TEST_MAKE_MISSING = 'missing-this-file-for-'


def test_parse_request(capsys):
    options = cli.parse_request(['-i', str(DEFAULT_IN_FILE_PATH)])
    assert options.in_file_pos == ''  # type: ignore
    assert options.in_file == str(DEFAULT_IN_FILE_PATH)  # type: ignore
    out, err = capsys.readouterr()
    assert not out
    assert not err

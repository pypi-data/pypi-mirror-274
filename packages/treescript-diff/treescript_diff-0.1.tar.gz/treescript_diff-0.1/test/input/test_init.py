"""Testing Input Package Methods
"""
from pathlib import Path
import pytest

from treescript_diff.input import validate_arguments
from treescript_diff.input.input_data import InputData


@pytest.mark.parametrize(
    'test_input,expected',
    [
        (['origin', 'update'], InputData('src/', 'src/', None)),
        (['origin', 'update', '--added'], InputData('src/', 'src/', True)),
        (['origin', 'update', '-a'], InputData('src/', 'src/', True)),
        (['origin', 'update', '--removed'], InputData('src/', 'src/', False)),
        (['origin', 'update', '-r'], InputData('src/', 'src/', False)),
    ]
)
def test_validate_arguments_returns_input(test_input, expected):
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'read_text', lambda _: "src/")
        assert validate_arguments(test_input) == expected


@pytest.mark.parametrize(
    'test_input',
    [
        (['']),
        ([' ']),
        (['r']),
        (['eee']),
    ]
)
def test_validate_arguments_raises_exit(test_input):
	try:
		validate_arguments(test_input)
		assert False
	except SystemExit:
		assert True

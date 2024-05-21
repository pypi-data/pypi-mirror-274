"""Testing Argument Parser Methods
"""
import pytest

from treescript_diff.input.argument_data import ArgumentData
from treescript_diff.input.argument_parser import parse_arguments


@pytest.mark.parametrize(
    'test_input,expected',
    [
        (['origin', 'update'], ArgumentData('origin', 'update')),
        (['origin', 'update', '--add'], ArgumentData('origin', 'update', True)),
        (['origin', 'update', '-a'], ArgumentData('origin', 'update', True)),
        (['origin', 'update', '--removed'], ArgumentData('origin', 'update', False)),
        (['origin', 'update', '-r'], ArgumentData('origin', 'update', False)),
    ]
)
def test_parse_arguments_returns_input(test_input, expected):
	assert parse_arguments(test_input) == expected


@pytest.mark.parametrize(
    'test_input',
    [
        ([]),
        (['']),
        ([' ']),
        (['r']),
        (['origin', '']),
        (['', 'updated']),
        (['origin', 'updated', '--unknown']),
    ]
)
def test_parse_arguments_raises_exit(test_input):
	try:
		parse_arguments(test_input)
		assert False
	except SystemExit:
		assert True

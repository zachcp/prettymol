from click.testing import CliRunner
from prettymol.cli import cli
from prettymol.cli import simpleplot


def test_hello_command():
    runner = CliRunner()
    result = runner.invoke(simpleplot, ['1fap'])
    assert result.exit_code == 0
    assert 'Hello, World!' in result.output

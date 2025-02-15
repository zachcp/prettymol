from prettymol.cli import cli

from click.testing import CliRunner


def test_hello_command():
    runner = CliRunner()
    result = runner.invoke(cli, ['1fap', 'test.png'])
    assert result.exit_code == 0
    assert 'Hello, World!' in result.output

import os
from prettymol.cli import cli, render
from click.testing import CliRunner

def test_hello_command():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(render, ['--code', '1fap', '--output', 'test.png'])
        assert result.exit_code == 0
        assert os.path.exists('test.png')

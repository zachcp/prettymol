import os
from prettymol.cli import cli

from click.testing import CliRunner


def test_hello_command():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ['1fap', 'test.png'])
        assert os.path.exists('test.png')

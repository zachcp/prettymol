import os
from prettymol.cli import cli

from click.testing import CliRunner


def test_hello_command():
    runner = CliRunner()
    result = runner.invoke(cli, ['1fap', 'test.png'])
    assert os.path.exists('test.png')
    try:
        os.remove('test.png')
    except:
        pass

import subprocess
import sys


def test_cli_help():
    result = subprocess.run(
        [sys.executable, "-m", "onyx", "--help"], capture_output=True, text=True
    )
    assert result.returncode == 0, result.stderr
    assert "onyx" in result.stdout

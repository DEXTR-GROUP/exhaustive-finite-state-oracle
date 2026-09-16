from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def test_operational_state_is_synchronized() -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "validation" / "state_sync_check.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "STATE SYNCHRONIZATION: PASS" in result.stdout

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from efso_reproducibility import canonical_json, digest_text, reproducible, run_command


def test_canonical_json_is_stable():
    value = {"b": 2, "a": [1, 0]}
    assert canonical_json(value) == '{"a":[1,0],"b":2}\n'
    assert digest_text(canonical_json(value)) == digest_text(canonical_json(value))


def test_command_replay_is_reproducible():
    command = (sys.executable, "-c", "print('EFSO-E12')")
    first = run_command(command, Path(__file__).resolve().parents[1])
    second = run_command(command, Path(__file__).resolve().parents[1])
    assert first.return_code == 0
    assert second.return_code == 0
    assert reproducible(first, second)


def test_nonzero_command_remains_deterministic():
    command = (sys.executable, "-c", "raise SystemExit(7)")
    first = run_command(command, Path(__file__).resolve().parents[1])
    second = run_command(command, Path(__file__).resolve().parents[1])
    assert first.return_code == 7
    assert reproducible(first, second)

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from efso_transition import (  # noqa: E402
    IndependentTransitionEngine,
    Operation,
    TransitionError,
    attention,
    matmul,
    mlp,
    rms_norm,
    softmax,
)


def test_supported_operator_set_is_explicit():
    assert IndependentTransitionEngine.compose((Operation("ADD", (2, 3)),))[0].value == 5
    assert IndependentTransitionEngine.compose((Operation("MUL", (2, 3)),))[0].value == 6
    assert IndependentTransitionEngine.compose((Operation("REDUCE", ((1, 2, 3),)),))[0].value == 6


def test_matmul_is_shape_checked_and_deterministic():
    a = ((1, 2), (3, 4))
    b = ((5, 6), (7, 8))
    expected = ((19, 22), (43, 50))
    assert matmul(a, b) == expected
    assert matmul(a, b) == matmul(a, b)


def test_softmax_is_normalized_and_shift_stable():
    result = softmax((-1.0, 0.0, 1.0))
    assert abs(sum(result) - 1.0) <= 1e-15
    shifted = softmax((99.0, 100.0, 101.0))
    assert max(abs(a - b) for a, b in zip(result, shifted)) <= 1e-15


def test_rmsnorm_has_expected_rms():
    result = rms_norm((3.0, 4.0), epsilon=1e-5)
    rms = (sum(v * v for v in result) / len(result)) ** 0.5
    expected_rms = (12.5 / (12.5 + 1e-5)) ** 0.5
    assert abs(rms - expected_rms) <= 1e-12


def test_attention_and_mlp_are_compositions_of_owned_semantics():
    query = (1.0, 0.0)
    key = ((1.0, 0.0), (0.0, 1.0))
    value = ((2.0, 0.0), (0.0, 4.0))
    out = attention(query, key, value)
    e = 2.718281828459045
    expected = (2.0 * e / (1.0 + e), 4.0 / (1.0 + e))
    assert max(abs(a - b) for a, b in zip(out, expected)) <= 1e-12

    x = (1.0, -1.0)
    up = ((1.0, 0.0), (0.0, 1.0))
    gate = ((1.0, 0.0), (0.0, 1.0))
    down = ((1.0, 0.0), (0.0, 1.0))
    result = mlp(x, up, gate, down)
    assert len(result) == 2


def test_engine_rejects_unknown_operator_and_bad_shape():
    try:
        IndependentTransitionEngine.apply(Operation("UNKNOWN", (1,)))
    except TransitionError:
        pass
    else:
        raise AssertionError("unknown operation must fail")

    try:
        matmul(((1, 2),), ((1,),))
    except TransitionError:
        pass
    else:
        raise AssertionError("incompatible MATMUL must fail")

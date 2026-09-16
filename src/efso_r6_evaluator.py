"""Independent EFSO-side evaluator for the minimal R6 Transformer Block."""

from __future__ import annotations

import math

from efso_r6_space import EPSILON, R6State


def rms_norm(values: list[float], epsilon: float) -> list[float]:
    mean = sum(value * value for value in values) / len(values)
    scale = 1.0 / math.sqrt(mean + epsilon)
    return [value * scale for value in values]


def silu(value: float) -> float:
    return value / (1.0 + math.exp(-value))


def evaluate(state: R6State) -> list[float]:
    output: list[float] = []
    for token in range(2):
        base = token * 2
        x = list(state.input[base : base + 2])
        norm1 = rms_norm(x, EPSILON)
        if not all(math.isfinite(value) for value in norm1):
            raise ValueError("non-finite norm1")

        residual = [x[i] + state.attention_update[base + i] for i in range(2)]
        norm2 = rms_norm(residual, EPSILON)
        gated = [silu(norm2[i]) * norm2[i] for i in range(2)]
        output.extend(residual[i] + gated[i] for i in range(2))
    return output

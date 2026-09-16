from __future__ import annotations

import math

from efso_r4_space import R4State


def evaluate(state: R4State) -> tuple[float, float]:
    """Independent EFSO evaluation of the finite R4 Attention primitive."""
    scores = [
        sum(float(q) * float(k) for q, k in zip(state.query, row))
        for row in state.key
    ]
    maximum = max(scores)
    weights = [math.exp(score - maximum) for score in scores]
    total = sum(weights)
    normalized = [weight / total for weight in weights]

    return tuple(
        sum(normalized[index] * float(state.value[index][dimension]) for index in range(2))
        for dimension in range(2)
    )

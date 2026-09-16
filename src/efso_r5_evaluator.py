from __future__ import annotations

import math

from efso_r5_space import R5State


def silu(value: float) -> float:
    return value / (1.0 + math.exp(-value))


def evaluate(state: R5State) -> tuple[float]:
    """Independent EFSO-side R5 evaluator.

    This is a direct implementation of the formal R5 primitive contract. It
    does not import or execute the external witness.
    """

    x = float(state.input[0])
    gate = [x * float(state.gate_weight[i]) for i in range(2)]
    up = [x * float(state.up_weight[i]) for i in range(2)]
    gated = [silu(gate[i]) * up[i] for i in range(2)]
    output = sum(gated[i] * float(state.down_weight[i]) for i in range(2))
    return (output,)

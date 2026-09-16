#!/usr/bin/env python3
"""Independent batch numerical oracle for a tiny gated MLP.

Input: JSON array of objects containing input[1], gate_weight[2],
up_weight[2], and down_weight[2].
Output: JSON array of one-element output vectors.

No EFSO code, IUT code, or subprocess is used. Only Python's standard
library participates in the witness computation.
"""

from __future__ import annotations

import json
import math
import sys


def silu(value: float) -> float:
    return value / (1.0 + math.exp(-value))


def evaluate(case: dict[str, object]) -> list[float]:
    x = float(case["input"][0])
    gate_weight = [float(v) for v in case["gate_weight"]]
    up_weight = [float(v) for v in case["up_weight"]]
    down_weight = [float(v) for v in case["down_weight"]]

    gate = [x * gate_weight[i] for i in range(2)]
    up = [x * up_weight[i] for i in range(2)]
    gated = [silu(gate[i]) * up[i] for i in range(2)]
    output = sum(gated[i] * down_weight[i] for i in range(2))
    return [output]


def main() -> None:
    payload = json.load(sys.stdin)
    if not isinstance(payload, list):
        raise SystemExit("input must be a JSON array")
    json.dump([evaluate(case) for case in payload], sys.stdout, separators=(",", ":"))
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()

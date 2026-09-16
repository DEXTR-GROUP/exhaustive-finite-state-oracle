#!/usr/bin/env python3
"""External-origin R5 numerical witness snapshot.

Source: DEXTR-GROUP/QWENRNS/validation/r5_mlp_batch_oracle.py
Source blob SHA: 901125629523f473a597c9eeebdb8b6cb26a41d7
Source commit: 4db6a1d314a1d0becb63995927feb90f301eb20e

This file is executed only by the validation harness and is never imported by
EFSO runtime code. The snapshot is kept locally so CI does not require access
to the private QWENRNS repository.
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

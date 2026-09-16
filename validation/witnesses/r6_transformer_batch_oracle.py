#!/usr/bin/env python3
"""Batch external reference for the minimal R6 Transformer Block qualification space."""

from __future__ import annotations

import json
import math
import sys


def rms_norm(values: list[float], epsilon: float) -> list[float]:
    mean = sum(value * value for value in values) / len(values)
    scale = 1.0 / math.sqrt(mean + epsilon)
    return [value * scale for value in values]


def silu(value: float) -> float:
    return value / (1.0 + math.exp(-value))


def reference_block(input_values: list[float], attention_update: list[float], epsilon: float) -> list[float]:
    hidden_size = 2
    intermediate_size = 2
    output: list[float] = []

    for token in range(2):
        base = token * hidden_size
        x = input_values[base : base + hidden_size]
        norm1 = rms_norm(x, epsilon)
        if not all(math.isfinite(value) for value in norm1):
            raise ValueError("non-finite norm1")

        residual = [x[i] + attention_update[base + i] for i in range(hidden_size)]
        norm2 = rms_norm(residual, epsilon)

        gated = [silu(norm2[i]) * norm2[i] for i in range(intermediate_size)]
        mlp = [gated[i] for i in range(hidden_size)]
        output.extend(residual[i] + mlp[i] for i in range(hidden_size))

    return output


def main() -> None:
    payload = json.load(sys.stdin)
    if not isinstance(payload, list):
        raise SystemExit("input must be a JSON array")

    results = []
    for case in payload:
        input_values = [float(value) for value in case["input"]]
        attention_update = [float(value) for value in case["attention_update"]]
        epsilon = float(case.get("epsilon", 1e-6))
        if len(input_values) != 4 or len(attention_update) != 4:
            raise SystemExit("R6 case requires four input and four attention_update scalars")
        results.append(reference_block(input_values, attention_update, epsilon))

    json.dump(results, sys.stdout, separators=(",", ":"))
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()

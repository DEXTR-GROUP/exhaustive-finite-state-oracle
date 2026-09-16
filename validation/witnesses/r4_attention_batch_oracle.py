#!/usr/bin/env python3
"""External-origin R4 numerical witness snapshot.

Source: DEXTR-GROUP/QWENRNS/validation/r4_attention_batch_oracle.py
Source blob SHA: e4fea00d58ee1fe8e22ce3d502bf6aac0bfdfdaf

This file is executed only by the validation harness and is never imported by
EFSO runtime code. The snapshot is kept locally because the source repository
is private and GitHub Actions GITHUB_TOKEN is scoped to the EFSO repository.
"""

from __future__ import annotations

import json
import math
import sys


def attention(case: dict[str, object]) -> list[float]:
    query = [float(x) for x in case["query"]]
    key = [[float(x) for x in row] for row in case["key"]]
    value = [[float(x) for x in row] for row in case["value"]]

    scores = [sum(q * k for q, k in zip(query, row)) for row in key]
    maximum = max(scores)
    weights = [math.exp(score - maximum) for score in scores]
    total = sum(weights)
    weights = [weight / total for weight in weights]

    return [
        sum(weights[index] * value[index][dimension] for index in range(2))
        for dimension in range(2)
    ]


def main() -> None:
    payload = json.load(sys.stdin)
    if not isinstance(payload, list):
        raise SystemExit("input must be a JSON array")
    json.dump([attention(case) for case in payload], sys.stdout, separators=(",", ":"))
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()

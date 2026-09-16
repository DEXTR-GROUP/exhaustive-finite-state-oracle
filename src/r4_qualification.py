"""Independent R4 qualification adapter.

This module defines a finite attention domain and a local numerical
reference. It deliberately does not import the EFSO implementation.
"""

from itertools import product
from math import exp, isclose

VALUES = (-1, 0, 1)
WIDTH = 2


def states():
    for q in product(VALUES, repeat=WIDTH):
        for k in product(VALUES, repeat=WIDTH):
            for v in product(VALUES, repeat=WIDTH):
                yield (q, k, v)


def cardinality():
    return len(VALUES) ** (WIDTH * 3)


def reference(q, k, v):
    score = sum(a * b for a, b in zip(q, k))
    weight = exp(score)
    return tuple(weight * x / weight for x in v)


def compare(actual, expected, rel_tol=1e-12, abs_tol=1e-12):
    return all(isclose(a, e, rel_tol=rel_tol, abs_tol=abs_tol)
               for a, e in zip(actual, expected))

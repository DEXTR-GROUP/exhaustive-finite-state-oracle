#!/usr/bin/env python3
"""Независимый transition engine EFSO (E5).

Контур намеренно не импортирует IUT, QWENRNS или numerical oracle.
Он задаёт собственную модель значений, операций и детерминированных
переходов. Сложные операции построены из явно определённых primitive
semantics, а не из вызовов внешней реализации.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Any, Callable

Number = int | float
Vector = tuple[Number, ...]
Matrix = tuple[Vector, ...]


class TransitionError(ValueError):
    """Ошибка некорректного вычислительного перехода."""


@dataclass(frozen=True)
class Operation:
    """Каноническое описание одного перехода."""

    name: str
    args: tuple[Any, ...]


@dataclass(frozen=True)
class TransitionResult:
    """Результат перехода с детерминированным operation id."""

    operation: str
    value: Any



def _same_shape(a: Vector, b: Vector) -> bool:
    return len(a) == len(b)


def add(a: Number, b: Number) -> Number:
    return a + b


def mul(a: Number, b: Number) -> Number:
    return a * b


def reduce_sum(values: Vector) -> Number:
    if not values:
        raise TransitionError("REDUCE требует непустой vector")
    return sum(values)


def vector_add(a: Vector, b: Vector) -> Vector:
    if not _same_shape(a, b):
        raise TransitionError("ADD: несовместимые размеры vector")
    return tuple(x + y for x, y in zip(a, b))


def vector_mul(a: Vector, b: Vector) -> Vector:
    if not _same_shape(a, b):
        raise TransitionError("MUL: несовместимые размеры vector")
    return tuple(x * y for x, y in zip(a, b))


def matmul(a: Matrix, b: Matrix) -> Matrix:
    if not a or not b or not b[0]:
        raise TransitionError("MATMUL требует непустые matrices")
    inner = len(a[0])
    if any(len(row) != inner for row in a):
        raise TransitionError("MATMUL: matrix A не прямоугольная")
    if any(len(row) != len(b[0]) for row in b):
        raise TransitionError("MATMUL: matrix B не прямоугольная")
    if len(b) != inner:
        raise TransitionError("MATMUL: несовместимые размеры")
    columns = len(b[0])
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(inner)) for j in range(columns))
        for i in range(len(a))
    )


def rms_norm(x: Vector, epsilon: float = 1e-5) -> Vector:
    if not x:
        raise TransitionError("RMSNorm требует непустой vector")
    if epsilon <= 0.0:
        raise TransitionError("RMSNorm epsilon должен быть > 0")
    mean_square = sum(float(v) * float(v) for v in x) / len(x)
    scale = math.sqrt(mean_square + epsilon)
    return tuple(float(v) / scale for v in x)


def silu(x: Number) -> float:
    xf = float(x)
    return xf / (1.0 + math.exp(-xf))


def activation(x: Vector) -> Vector:
    return tuple(silu(v) for v in x)


def softmax(x: Vector) -> Vector:
    if not x:
        raise TransitionError("Softmax требует непустой vector")
    maximum = max(float(v) for v in x)
    exponentials = tuple(math.exp(float(v) - maximum) for v in x)
    total = sum(exponentials)
    return tuple(v / total for v in exponentials)


def residual(x: Vector, update: Vector) -> Vector:
    return vector_add(x, update)


def rope(x: Vector, cos_values: Vector, sin_values: Vector) -> Vector:
    if len(x) != len(cos_values) or len(x) != len(sin_values):
        raise TransitionError("RoPE: несовместимые размеры")
    if len(x) % 2:
        raise TransitionError("RoPE требует чётную размерность")
    result = list(x)
    for i in range(0, len(x), 2):
        c = float(cos_values[i])
        s = float(sin_values[i])
        a = float(x[i])
        b = float(x[i + 1])
        result[i] = a * c - b * s
        result[i + 1] = a * s + b * c
    return tuple(result)


def attention(query: Vector, key: Matrix, value: Matrix) -> Vector:
    if len(key) == 0 or len(value) == 0 or len(key) != len(value):
        raise TransitionError("Attention: key/value должны иметь одинаковую непустую длину")
    if len(query) == 0 or any(len(row) != len(query) for row in key):
        raise TransitionError("Attention: query/key dimension mismatch")
    if any(len(row) != len(query) for row in value):
        raise TransitionError("Attention: value dimension mismatch")
    scores = tuple(sum(float(q) * float(k) for q, k in zip(query, row)) for row in key)
    weights = softmax(scores)
    return tuple(
        sum(weights[i] * float(value[i][j]) for i in range(len(value)))
        for j in range(len(query))
    )


def mlp(x: Vector, up: Matrix, gate: Matrix, down: Matrix) -> Vector:
    up_out = matmul((x,), up)[0]
    gate_out = matmul((x,), gate)[0]
    if len(up_out) != len(gate_out):
        raise TransitionError("MLP: up/gate dimensions mismatch")
    gated = tuple(silu(g) * u for u, g in zip(up_out, gate_out))
    return matmul((gated,), down)[0]


_OPERATORS: dict[str, Callable[..., Any]] = {
    "ADD": add,
    "MUL": mul,
    "REDUCE": reduce_sum,
    "RMSNorm": rms_norm,
    "Activation": activation,
    "MatMul": matmul,
    "Softmax": softmax,
    "RoPE": rope,
    "Attention": attention,
    "MLP": mlp,
    "Residual": residual,
}


class IndependentTransitionEngine:
    """Собственный детерминированный исполнитель операций EFSO."""

    @staticmethod
    def apply(operation: Operation) -> TransitionResult:
        try:
            function = _OPERATORS[operation.name]
        except KeyError as exc:
            raise TransitionError(f"неизвестная операция: {operation.name}") from exc
        value = function(*operation.args)
        return TransitionResult(operation=operation.name, value=value)

    @staticmethod
    def compose(operations: tuple[Operation, ...]) -> tuple[TransitionResult, ...]:
        """Выполнить композицию в заданном порядке без скрытого состояния."""
        return tuple(IndependentTransitionEngine.apply(op) for op in operations)


SUPPORTED_OPERATORS = tuple(_OPERATORS)

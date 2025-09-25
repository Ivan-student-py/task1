from typing import List
from config import GOLDEN_SECH


def calculate_golden_weights(words: List[str], gender: str) -> List[float]:
    n = len(words)
    weights = [0] * n
    remainder = 1.0
    for i in range(n - 1):
        prob = remainder / GOLDEN_SECH
        if gender == "M":
            weights[i] = prob
        else:
            weights[n - 1 - i] = prob
        remainder -= prob
    if gender == "M":
        weights[n - 1] = remainder
    else:
        weights[0] = remainder
    return weights

#!/usr/bin/env python3
#
# Base class for generate dynamic variation (crossover and mutation) probabilities

import math
from collections.abc import Iterable

class VariationProbability(Iterable):
    """iterator to generate dynamic variation probabilities"""
    def __iter__(self):
        return iter(self)



class ConstantVariationProbability(VariationProbability):
    def __init__(self, value: float):
        assert value > 0.0 and value < 1.0, "A probability must be a number between 0.0 and 1.0"

        self.value = value

    def __next__(self):
        return self.value

class ExponentialDecayVariationProbability(VariationProbability):
    def __init__(self, initial: float, decay: float):
        assert initial > 0.0 and initial < 1.0, "Initial value must a valid probability (a number between 0.0 and 1.0)"
        assert decay > 0.0, "Decay constant must be positive number"

        self.initial = initial
        self.decay = decay
        self.step = 0

    def __iter__(self):
        self.step = 0
        return self

    def __next__(self):
        t = self.step
        self.step += 1
        return self.initial*math.exp(-self.decay*t)

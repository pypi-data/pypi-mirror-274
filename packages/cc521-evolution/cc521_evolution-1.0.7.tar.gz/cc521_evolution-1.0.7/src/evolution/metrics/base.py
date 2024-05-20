#!/usr/bin/env python3
#
# Base class to create metrics

from abc import ABC, abstractmethod
from typing import List
from ..individual import Individual

class EvolutionMetric(ABC):
    @abstractmethod
    def evaluate(self, individuals: List[Individual]):
        pass

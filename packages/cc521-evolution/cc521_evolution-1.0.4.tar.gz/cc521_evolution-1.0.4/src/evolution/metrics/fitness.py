#!/usr/bin/env python3
#
# Evaluate the fitness on a group of individuals and select the best and worse individuals,
# also compute the average fitness of the collection of individuals

from typing import List

from ..individual import Individual
from ..fitness import Fitness, FitnessEvaluation
from .base import EvolutionMetric

class FitnessMetric(EvolutionMetric):
    def __init__(self, fitness: Fitness):
        self.fitness_func = fitness
        self.avg_fitness: float = None
        self._best: FitnessEvaluation = None
        self._worse: FitnessEvaluation = None

    def evaluate(self, individuals: List[Individual]):
        fitnessEvaluation = [FitnessEvaluation(x, self.fitness_func(x)) for x in individuals]

        n = len(individuals)
        self.avg_fitness = sum([x.fitness for x in fitnessEvaluation]) / float(n)

        self._best = max(fitnessEvaluation, key=lambda t: t.fitness)
        self._worse = min(fitnessEvaluation, key=lambda t: t.fitness)

    @property
    def best(self) -> FitnessEvaluation:
        return self._best

    @property
    def worse(self) -> FitnessEvaluation:
        return self._worse

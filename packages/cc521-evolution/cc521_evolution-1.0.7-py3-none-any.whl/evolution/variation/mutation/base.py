#!/usr/bin/env python3
#
# base class for mutation operations

from typing import List
from abc import ABC, abstractmethod
from ...population import Individual

class MutationStrategy(ABC):
    # for generalization we suppose that the mutation process generate a list of new individuals,
    # in general only one is generated, but this extension is done to support weird mutation strategies
    # that could generate more than one individual
    @abstractmethod
    def mutate(self, parent: Individual) -> List[Individual]:
        pass

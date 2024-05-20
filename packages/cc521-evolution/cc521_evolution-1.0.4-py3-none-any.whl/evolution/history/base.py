#!/usr/bin/env python3
#
# History base classes - A history class records points of interest of an evolution process

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

class EvolutionHistory:
    def __init__(self, name: str, figure: Figure):
        self.name = name
        self.figure = figure
        self.history: List[tuple[int, object]] = [] # history of points of interest

    def add(self, generation: int, value: object):
        self.history.append((generation, value))

    @abstractmethod
    def plot(self, generation: int):
        """plot the history of evolution until an specified generation"""
        pass

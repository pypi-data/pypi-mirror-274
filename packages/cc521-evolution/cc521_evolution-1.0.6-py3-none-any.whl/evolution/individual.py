#!/usr/bin/env python3
#
# Individual class - Just an encapsulation of a cromosome and a domain encoder

from .encoding.base import DomainEncoder, Chromosome

class Individual:
    """Encapsulate a chromosome and the encoder that generated it"""
    def __init__(self, chromosome: Chromosome, encoder: DomainEncoder):
        self.encoder = encoder
        self._chromosome = chromosome

    @property
    def phenotype(self) -> object:
        #import pdb; pdb.set_trace()
        return self.encoder.decode(self._chromosome)

    @property
    def chromosome(self) -> object:
        return self._chromosome

    def __repr__(self) -> str:
        return self._chromosome.to_str()

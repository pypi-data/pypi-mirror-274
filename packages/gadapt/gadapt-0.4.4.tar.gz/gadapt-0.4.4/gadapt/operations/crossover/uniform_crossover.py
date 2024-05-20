import random
from typing import Tuple

from gadapt.operations.crossover.base_crossover import BaseCrossover
from gadapt.operations.immigration.chromosome_immigration.base_chromosome_immigrator import (
    BaseChromosomeImmigrator,
)
from gadapt.operations.mutation.chromosome_mutation.base_gene_mutation_selector import (
    BaseGeneMutationSelector,
)


class UniformCrossover(BaseCrossover):
    """
    Uniform Crossover. Genes from parents' chromosomes are combined in a uniform way.
    """

    def __init__(
        self,
        mutator: BaseGeneMutationSelector,
        immigrator: BaseChromosomeImmigrator,
    ):
        super(UniformCrossover, self).__init__(mutator, immigrator)

    def _combine(self) -> Tuple[float, float]:
        rnd = random.randint(0, 2)
        if rnd == 0:
            return self._father_gene.variable_value, self._mother_gene.variable_value
        elif rnd == 1:
            return self._father_gene.variable_value, self._father_gene.variable_value
        else:
            return self._mother_gene.variable_value, self._mother_gene.variable_value

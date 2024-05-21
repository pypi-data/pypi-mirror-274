import random

from gadapt.operations.crossover.base_crossover import BaseCrossover
from gadapt.operations.immigration.chromosome_immigration.base_chromosome_immigrator import (
    BaseChromosomeImmigrator,
)
from gadapt.operations.mutation.chromosome_mutation.base_gene_mutation_selector import (
    BaseGeneMutationSelector,
)


class BlendingCrossover(BaseCrossover):
    """
    Blending Crossover combines
    gene values from the two parents into new variable values in offsprings.
    One value of the offspring variable comes from a combination of the two
    corresponding values of the parental genes
    """

    def __init__(
        self,
        mutator: BaseGeneMutationSelector,
        immigrator: BaseChromosomeImmigrator,
    ):
        super(BlendingCrossover, self).__init__(mutator, immigrator)
        self._current_gene_number = -1

    def _combine(self):
        decision_variable = self._father_gene.decision_variable
        val_father = self._father_gene.variable_value
        val_mother = self._mother_gene.variable_value
        x = 1
        if val_mother > val_father:
            x = -1
        beta_steps = random.randint(
            0, round(abs((val_father - val_mother) / decision_variable.step))
        )
        val1 = round(
            val_father - (beta_steps * x) * decision_variable.step,
            decision_variable.decimal_places,
        )
        val2 = round(
            val_mother + (beta_steps * x) * decision_variable.step,
            decision_variable.decimal_places,
        )
        return val1, val2

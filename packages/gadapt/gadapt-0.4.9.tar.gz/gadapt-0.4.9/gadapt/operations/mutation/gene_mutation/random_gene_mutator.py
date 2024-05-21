from gadapt.operations.mutation.gene_mutation.base_gene_mutator import BaseGeneMutator


class RandomGeneMutator(BaseGeneMutator):
    """
    Generates a random value within the specified range of the decision variable.
    """

    def _make_mutated_value(self):
        return round(
            self.gene.decision_variable.make_random_value(),
            self.gene.decision_variable.decimal_places,
        )

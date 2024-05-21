import gadapt.utils.ga_utils as ga_utils
from gadapt.operations.mutation.chromosome_mutation.random_gene_mutation_rate_determinator import (
    RandomGeneMutationRateDeterminator,
)


class CrossDiversityGeneMutationRateDeterminator(RandomGeneMutationRateDeterminator):
    """
    Determines the number of mutation genes in a chromosome based on the cross diversity coefficient of the decision variables.
    """

    def __init__(
        self,
    ) -> None:
        super().__init__()

    def _get_number_of_mutation_genes(self) -> int:
        decision_variables = [g.decision_variable for g in self.chromosome]

        def get_mutation_rate() -> float:
            avg_rsd = ga_utils.average(
                [dv.cross_diversity_coefficient for dv in decision_variables]
            )
            if avg_rsd > 1:
                avg_rsd = 1
            if avg_rsd < 0:
                avg_rsd = 0
            return avg_rsd

        mutation_rate = get_mutation_rate()
        limit_number_of_mutation_genes = mutation_rate * float(
            self.max_number_of_mutation_genes
        )
        limit_number_of_mutation_genes_rounded = round(limit_number_of_mutation_genes)
        if limit_number_of_mutation_genes_rounded == 0:
            limit_number_of_mutation_genes_rounded = 1
        self.max_number_of_mutation_genes = limit_number_of_mutation_genes_rounded
        return super()._get_number_of_mutation_genes()

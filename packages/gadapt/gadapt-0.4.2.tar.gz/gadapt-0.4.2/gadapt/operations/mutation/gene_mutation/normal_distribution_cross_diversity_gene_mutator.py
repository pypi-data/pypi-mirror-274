import numpy as np

from gadapt.operations.mutation.gene_mutation.normal_distribution_gene_mutator import (
    NormalDistributionGeneMutator,
)


class NormalDistributionCrossDiversityGeneMutator(NormalDistributionGeneMutator):
    """
    Generates random or normally distributed values. Calculates standard deviation based on
    the cross-diversity coefficient
    """

    def _calculate_normal_distribution_standard_deviation(self):
        min_std_dev = 0.05
        max_std_dev = 0.5
        std_dev_range = max_std_dev - min_std_dev
        dv_rsd = np.clip(self.gene.decision_variable.cross_diversity_coefficient, 0, 1)
        return min_std_dev + (std_dev_range * dv_rsd)

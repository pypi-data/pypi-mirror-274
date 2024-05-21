import math

from gadapt.operations.population_update.base_population_updater import (
    BasePopulationUpdater,
)
from gadapt.utils import ga_utils


class CommonPopulationUpdater(BasePopulationUpdater):
    """
    Common population updater
    """

    def _calculate_average_cost_step(self):
        allocated_values = [
            c.cost_value
            for c in self.population.chromosomes
            if c.cost_value is not None and not math.isnan(c.cost_value)
        ]
        if allocated_values:
            return ga_utils.average_difference(allocated_values)
        return float("NaN")

    def _update_population(self):
        self.population.average_cost_step = self._calculate_average_cost_step()
        if math.isnan(self.population.average_cost_step_in_first_population):
            self.population.average_cost_step_in_first_population = (
                self.population.average_cost_step
            )

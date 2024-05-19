from abc import ABC, abstractmethod


class BasePopulationUpdater(ABC):
    """
    Base class for population update
    """

    def __init__(self):
        super().__init__()
        self.population = None

    def update_population(self, population):
        self.population = population
        self._update_population()

    @abstractmethod
    def _update_population(self):
        pass

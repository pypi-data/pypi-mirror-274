from abc import ABC, abstractmethod


class BaseVariableUpdater(ABC):
    """
    Base class for variable update
    """

    def __init__(self):
        self.population = None

    def update_variables(self, population):
        self.population = population
        self._update_variables()

    @abstractmethod
    def _update_variables(self):
        pass

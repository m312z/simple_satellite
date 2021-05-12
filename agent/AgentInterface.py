from abc import ABC, abstractmethod
from simulation.Simulation import SatelliteSim


class AgentInterface(ABC):

    def __init__(self, agentName: str):
        self.name = agentName

    @abstractmethod
    def getAction(self, sim: SatelliteSim):
        pass

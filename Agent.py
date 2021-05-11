from abc import ABC, abstractmethod
from Simulation import SatelliteSim

class Agent(ABC):

    def __init__(self, agentName : str):
        self.name = agentName

    @abstractmethod
    def getAction(self, sim : SatelliteSim):
        pass

class GreedyAgent(Agent):

    def __init__(self):
        super(GreedyAgent, self).__init__("GreedyAgent")

    def getAction(self, sim : SatelliteSim):

        # DUMP
        if any(i >= 0 and analysed for i, analysed in zip(sim.images, sim.analysis)):
            # there is an analysed image in the memory
            for gs in sim.groundStations:
                if gs[0] < sim.pos < gs[1]:
                    # the satellite is above a ground station
                    index = [i >= 0 and analysed for i, analysed in zip(sim.images, sim.analysis)].index(True)
                    # dump the first analysed image
                    return sim.ACTION_DUMP, index

        # TAKE
        if any(i < 0 for i in sim.images):
            # there is a space in the memory
            for index, t in enumerate(sim.targets):
                if t[0] < sim.pos < t[1]:
                    # the satellite is above a target
                    return sim.ACTION_TAKE_IMAGE, index

        # ANALYSE
        if any(i >= 0 and not analysed for i, analysed in zip(sim.images, sim.analysis)):
            # there is an image in the memory not analysed
            index = [i >= 0 and not analysed for i, analysed in zip(sim.images, sim.analysis)].index(True)
            return sim.ACTION_ANALYSE, index

        # no action available
        return None

class PDDLAgent(Agent):

    def __init__(self, plan : list):
        super(PDDLAgent, self).__init__("PDDLAgent")
        self.plan = plan
        self.current_action = None
        if len(plan)>0:
            self.current_action = plan.pop(0)

    def getAction(self, sim : SatelliteSim):

        # no more actions
        if not self.current_action: return

        # satellite is busy
        if sim.satellite_busy_time>0: return

        # check next action
        if sim.sim_time > self.current_action[0]:

            print(sim.sim_time, self.current_action)
            # prepare current action
            action = (self.current_action[1], self.current_action[2], self.current_action[3])

            # get next action ready
            if len(self.plan)>0:
                self.current_action = self.plan.pop(0)
            else:
                self.current_action = None

            return action




from agent.AgentInterface import AgentInterface
from simulation.Simulation import SatelliteSim

class GreedyAgent(AgentInterface):

    def __init__(self):
        super(GreedyAgent, self).__init__("GreedyAgent")

    def getAction(self, sim: SatelliteSim):

        # DUMP
        if any(i >= 0 and analysed for i, analysed in zip(sim.images, sim.analysis)):
            # there is an analysed image in the memory
            for gs in sim.groundStations:
                if gs[0] < sim.pos < gs[1]:
                    # the satellite is above a ground station
                    index = [i >= 0 and analysed for i, analysed in zip(sim.images, sim.analysis)].index(True)
                    # dump the first analysed image
                    return sim.ACTION_DUMP, sim.images[index], index

        # TAKE
        if any(i < 0 for i in sim.images):
            # there is a space in the memory
            memory = [i < 0 for i in sim.images].index(True)
            for index, t in enumerate(sim.targets):
                if t[0] < sim.pos < t[1]:
                    # the satellite is above a target
                    return sim.ACTION_TAKE_IMAGE, index, memory

        # ANALYSE
        if any(i >= 0 and not analysed for i, analysed in zip(sim.images, sim.analysis)):
            # there is an image in the memory not analysed
            index = [i >= 0 and not analysed for i, analysed in zip(sim.images, sim.analysis)].index(True)
            return sim.ACTION_ANALYSE, sim.images[index], index

        # no action available
        return None

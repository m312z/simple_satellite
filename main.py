import pygame

from agent.AgentGreedy import GreedyAgent
from agent.AgentPDDL import PDDLAgent
from simulation.DrawSim import SatelliteView
from simulation.Simulation import SatelliteSim

if __name__ == '__main__':

    pygame.display.init()
    finished = False
    clock = pygame.time.Clock()

    # create simulation
    sim = SatelliteSim()
    sim.initRandomStations(1)
    sim.initRandomTargets(10)
    sim.initRandomGoals(3)
    view = SatelliteView()

    # create agent
    agent = PDDLAgent()
    agent.generatePlan(sim)
    agent = GreedyAgent()

    while not finished:

        # check for window closed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True

        view.drawSim(sim)
        action = agent.getAction(sim)
        sim.update(action, 1)
        clock.tick(60)

    pygame.quit()

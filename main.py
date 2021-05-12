import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
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
    sim.initRandomStations(2)
    sim.initRandomTargets(10)
    sim.goalRef.generateSingleGoals(sim.targets, 5)
    sim.goalRef.generateCampaigns(sim.targets, sim.goalRef.MAX_CAMPAIGNS)
    view = SatelliteView()

    # create agent
    agent = PDDLAgent()
    #agent = GreedyAgent()

    while not finished:

        # check for window closed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True

        view.drawSim(sim)
        action = agent.getAction(sim)
        finished = finished or sim.update(action, 0.5)
        clock.tick(60)

    pygame.quit()

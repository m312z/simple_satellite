import pygame
from DrawSim import SatelliteView
from Simulation import SatelliteSim
from Agent import GreedyAgent, PDDLAgent
import PDDLManager

if __name__ == '__main__':

    pygame.display.init()
    finished = False
    clock = pygame.time.Clock()

    # create simulation
    sim = SatelliteSim()
    sim.initRandomStations(1)
    sim.initRandomTargets(10)
    sim.initRandomGoals(10)
    view = SatelliteView()

    # create Agent
    PDDLManager.writePDDLProblem(sim, "problem.pddl")
    print("generating plan...")
    if not PDDLManager.generatePlan("domain.pddl", "problem.pddl", "plan.pddl"): exit()
    print("planning complete")
    plan = PDDLManager.readPDDLPlan("plan.pddl")
    agent = PDDLAgent(plan)

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

from agent import PDDLManager
from agent.AgentInterface import AgentInterface
from simulation.Simulation import SatelliteSim


class PDDLAgent(AgentInterface):

    def __init__(self):
        super(PDDLAgent, self).__init__("PDDLAgent")
        self.plan_received = False
        self.plan = []
        self.current_action = None

    def generatePlan(self, sim: SatelliteSim):
        print("({name}) generating plan".format(name=self.name))
        PDDLManager.writePDDLProblem(sim, "pddl/problem.pddl", orbits=5)
        if PDDLManager.generatePlan("pddl/domain.pddl", "pddl/problem.pddl", "pddl/plan.pddl"):
            print("({name}) planning complete".format(name=self.name))
            self.plan = PDDLManager.readPDDLPlan("pddl/plan.pddl")
            if len(self.plan) > 0: self.current_action = self.plan.pop(0)
            self.plan_received = True
        else:
            print("({name}) planning failed".format(name=self.name))

    def getAction(self, sim: SatelliteSim):

        # no more actions
        if not self.current_action: return

        # satellite is busy
        if sim.satellite_busy_time > 0: return

        # check next action
        if sim.sim_time > self.current_action[0]:

            # prepare current action
            action = (self.current_action[1], self.current_action[2], self.current_action[3])

            # get next action ready
            if len(self.plan) > 0:
                self.current_action = self.plan.pop(0)
            else:
                print("({name}) plan complete".format(name=self.name))
                self.current_action = None

            return action

import math

from Simulation import SatelliteSim
import requests, sys


def generatePlan(domain: str, problem: str, plan: str):
    data = {'domain': open(domain, 'r').read(), 'problem': open(problem, 'r').read()}
    resp = requests.post('https://popf-cloud-solver.herokuapp.com/solve', verify=True, json=data).json()
    if not 'plan' in resp['result']:
        print("WARN: Plan was not found!")
        return False
    with open(plan, 'w') as f:
        f.write(''.join([act for act in resp['result']['plan']]))
    f.close()
    return True


def writePDDLProblem(sim: SatelliteSim, file: str, orbits=5):
    with open(file, "w") as f:
        f.write("(define(problem satprob)\n")
        f.write("(:domain SimpleSatellite)\n")
        f.write("(:objects\n ")
        for index in range(SatelliteSim.MEMORY_SIZE):
            f.write(" mem" + str(index))
        f.write(" - memory\n")
        for index, target in enumerate(sim.targets):
            f.write(" img" + str(index))
        f.write(" - image\n")
        f.write(")\n")
        f.write("(:init\n")
        f.write("  (sat_free)\n")
        f.write("  (= (total_score) 0)\n")
        f.write("\n")
        for index in range(SatelliteSim.MEMORY_SIZE):
            f.write("  (memory_free mem" + str(index) + ")\n")
        f.write("\n")
        for o in range(orbits):
            for index, target in enumerate(sim.targets):
                start = target[0] + SatelliteSim.PERIOD * o
                end = target[1] + SatelliteSim.PERIOD * o
                f.write("  (at " + str(round(start, 3)) + " (image_available img" + str(index) + "))\n")
                f.write("  (at " + str(round(end, 3)) + " (not (image_available img" + str(index) + ")))\n")
        f.write("\n")
        for o in range(orbits):
            for index, target in enumerate(sim.groundStations):
                start = target[0] + SatelliteSim.PERIOD * o
                end = target[1] + SatelliteSim.PERIOD * o
                f.write("  (at " + str(round(start, 3)) + " (dump_available))\n")
                f.write("  (at " + str(round(end, 3)) + " (not (dump_available)))\n")
        f.write(")\n")
        f.write("(:goal (and\n")
        for index, target in enumerate(sim.single_goals):
            f.write("  (image_dumped img" + str(index) + ")\n")
        f.write(")))\n")
        f.close()


def readPDDLPlan(file: str):
    actionMap = {"take_image": 0, "dump_image": 1, "analyse_image": 2}
    plan = []
    with open(file, "r") as f:
        line = f.readline().strip()
        while line:
            tokens = line.split()
            time = tokens[0][:-1]
            action = tokens[1][1:]
            image = tokens[2]
            memory = tokens[3][:-1]
            plan.append((float(time), actionMap[action], int(image[3:]), int(memory[3:])))

            line = f.readline().strip()
        f.close()
    return plan


if __name__ == '__main__':
    generatePlan("domain.pddl", "problem.pddl", "plan.pddl")
    print("done")

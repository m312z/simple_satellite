import math
import random
from simulation.GoalReferee import GoalReferee

class SatelliteSim:

    PERIOD = 600
    ACTION_THRESHOLD = 6

    MEMORY_SIZE = 10

    ACTION_TAKE_IMAGE = 0
    ACTION_DUMP = 1
    ACTION_ANALYSE = 2

    DURATION_TAKE_IMAGE = 2
    DURATION_DUMP = 19
    DURATION_ANALYSE = 49

    def __init__(self):

        self.sim_time = 0

        # satellite state
        self.pos = 0
        self.last_action = None

        # planet position
        self.groundStations = []
        self.targets = []

        # memory state
        self.images = [-1] * SatelliteSim.MEMORY_SIZE
        self.analysis = [False] * SatelliteSim.MEMORY_SIZE
        self.satellite_busy_time = 0

        # goals
        self.goalRef = GoalReferee()

    def initRandomStations(self, amount):
        for i in range(amount):
            s = random.random()*(SatelliteSim.PERIOD-50)
            self.groundStations.append((s, s+50))

    def initRandomTargets(self, amount):
        for i in range(amount):
            s = random.random()*(SatelliteSim.PERIOD-5)
            self.targets.append((s, s+5))

    def update(self, dt: float):
        self.update(None, dt)

    def update(self, action, dt: float):

        # position is time modulo period
        self.sim_time += dt
        orbit = math.floor(self.sim_time / SatelliteSim.PERIOD)

        # update orbit position
        self.pos = self.pos + dt
        while self.pos > SatelliteSim.PERIOD:
            self.pos = self.pos - SatelliteSim.PERIOD

        if self.pos <= dt:
            images = [ i for i in self.targets if i not in self.goalRef.single_goals ]
            self.goalRef.generateSingleGoals(self.targets,random.randint(0,len(images)-1))
            self.goalRef.generateCampaigns(self.targets, random.randint(0, 1))
            self.goalRef.checkCampaignFailure(orbit)

        # count down action duration
        if self.satellite_busy_time > 0:
            self.satellite_busy_time = self.satellite_busy_time - dt

        if not action or self.satellite_busy_time > 0:
            return

        if action[0] == SatelliteSim.ACTION_TAKE_IMAGE:

            # check image is in range (relax threshold by speed for checking)
            target = self.targets[action[1]]
            if not target[0]-self.ACTION_THRESHOLD < self.pos < target[1]+self.ACTION_THRESHOLD:
                print("WARN: action could not be accomplished as target out of range (take_image)")
                return

            # check mem location is really empty
            if self.images[action[2]] >= 0:
                print("WARN: action could not be accomplished as memory not empty (take_image)")
                return

            # add image to first empty memory location
            self.satellite_busy_time = SatelliteSim.DURATION_TAKE_IMAGE
            self.images[action[2]] = action[1]
            self.last_action = action
            return

        if action[0] == SatelliteSim.ACTION_DUMP:

            # check ground station is in range (relax threshold by speed for checking)
            if not any([gs[0]-self.ACTION_THRESHOLD < self.pos < gs[1]+self.ACTION_THRESHOLD for gs in self.groundStations]):
                print("WARN: action could not be accomplished as ground station out of range (dump)")
                return

            # check mem location holds that image
            if self.images[action[2]] != action[1]:
                print("WARN: action could not be accomplished as memory does not hold required image (dump)")
                return

            # check mem location is analysed
            if not self.analysis[action[2]]:
                print("WARN: action could not be accomplished as memory not analysed (dump)")
                return

            # dump image and reset memory location
            self.satellite_busy_time = SatelliteSim.DURATION_DUMP
            self.analysis[action[2]] = False
            self.images[action[2]] = -1
            self.last_action = action

            # score the goal value
            self.goalRef.evaluateDump(orbit, action[1])
            return

        if action[0] == SatelliteSim.ACTION_ANALYSE:

            # check mem location holds that image
            if self.images[action[2]] != action[1]:
                print("WARN: action could not be accomplished as memory does not hold required image (analyse)")
                return

            # set image to analysed or discarded
            self.satellite_busy_time = SatelliteSim.DURATION_ANALYSE
            self.last_action = action
            if random.random() > 0.0:
                self.analysis[action[2]] = True
            else:
                self.analysis[action[2]] = False
                self.images[action[2]] = -1
            return

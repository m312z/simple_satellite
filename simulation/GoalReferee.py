import math
import random

class CampaignGoal:

    def __init__(self, targets=[], reward=1):
        self.targets = targets
        self.targets_completed = [False]*len(targets)
        self.campaign_start_orbit = -1
        self.campaign_started = False
        self.campaign_failed = False
        self.campaign_completed = False
        self.reward = reward

class GoalReferee:

    MAX_SINGLE_GOALS = 10
    MAX_CAMPAIGNS = 3

    def __init__(self):
        self.single_goals = {}
        self.campaigns = []
        self.value = 0

    def generateSingleGoals(self, images, amount=1):
        amount = min(amount, GoalReferee.MAX_SINGLE_GOALS - len(self.single_goals))
        images = list(range(len(images)))
        goals = random.sample(images, amount)
        for g in goals: self.single_goals[g] = random.random()

    def generateCampaigns(self, images, amount=1):
        amount = min(amount, GoalReferee.MAX_CAMPAIGNS - len(self.campaigns))
        for _ in range(amount):
            targets = []
            campaign_size = random.randint(3,10)
            orbit = 0
            while len(targets) < campaign_size:
                orbit_targets = random.randint(1, min(2, campaign_size-len(targets)))
                image_list = list(range(len(images)))
                targets = targets + [(image, orbit) for image in random.sample(image_list, orbit_targets)]
                orbit += 1
            campaign = CampaignGoal(targets, campaign_size)
            self.campaigns.append(campaign)

    def evaluateDump(self, orbit, image):

        # check single goals
        self.value = self.value + self.single_goals.pop(image,0)

        # check campaigns
        for c in self.campaigns:
            for index, target in enumerate(c.targets):
                # start campaign
                if not c.campaign_started and image == target[0] and target[1] == 0:
                    c.campaign_started = True
                    c.campaign_start_orbit = orbit
                # complete target
                if c.campaign_started and image == target[0] and orbit==target[1]+c.campaign_start_orbit:
                    c.targets_completed[index] = True
                # check for completion
                if all(c.targets_completed):
                    self.value = self.value + c.reward
                    c.campaign_completed = True
        self.campaigns = [c for c in self.campaigns if not c.campaign_failed and not c.campaign_completed]

    def checkCampaignFailure(self, orbit):
        for c in self.campaigns:
            for index, target in enumerate(c.targets):
                if c.campaign_started and not c.targets_completed[index] and orbit > target[1] + c.campaign_start_orbit:
                    c.campaign_failed = True
        self.campaigns = [c for c in self.campaigns if not c.campaign_failed and not c.campaign_completed]
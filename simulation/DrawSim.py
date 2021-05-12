import math
import pygame
from simulation.Simulation import SatelliteSim


class SatelliteView:

    # Palette
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    PURPLE = (128, 0, 255)
    ORANGE = (255, 128, 0)

    # config
    WIDTH, HEIGHT = 800, 800
    PLANET_SIZE = WIDTH / 2
    SAT_SIZE = PLANET_SIZE / 40
    IMAGE_SIZE = PLANET_SIZE / 10
    GOAL_SIZE = PLANET_SIZE / 15
    ORBIT_DISTANCE = PLANET_SIZE / 10
    HUD_WIDTH = (SatelliteSim.MEMORY_SIZE - 1) * IMAGE_SIZE * 1.2 + IMAGE_SIZE * 0.8

    def __init__(self):

        # font
        pygame.font.init()
        self.font = pygame.font.SysFont(None, int(SatelliteView.IMAGE_SIZE / 2))
        self.text_digits = [self.font.render(str(i), True, SatelliteView.WHITE) for i in
                            range(SatelliteSim.MEMORY_SIZE)]
        self.text_goals = self.font.render("Open Goals", True, SatelliteView.WHITE)

        # Open a window
        self.screen = pygame.display.set_mode((SatelliteView.WIDTH, SatelliteView.HEIGHT))
        pygame.display.set_caption("Simple Satellite")

    def drawArc(self, color: pygame.Color, start: float, end: float, thickness: float):

        xpoints = [SatelliteView.WIDTH / 2 + (SatelliteView.PLANET_SIZE - thickness) / 2 * math.sin(
            start + (end - start) * i / 6.0 + math.pi / 2) for i in range(7)]
        xpoints += [SatelliteView.WIDTH / 2 + (SatelliteView.PLANET_SIZE + 1) / 2 * math.sin(
            start + (end - start) * i / 6.0 + math.pi / 2) for i in range(6, -1, -1)]

        ypoints = [SatelliteView.WIDTH / 2 + (SatelliteView.PLANET_SIZE - thickness) / 2 * math.cos(
            start + (end - start) * i / 6.0 + math.pi / 2) for i in range(7)]
        ypoints += [SatelliteView.WIDTH / 2 + (SatelliteView.PLANET_SIZE + 1) / 2 * math.cos(
            start + (end - start) * i / 6.0 + math.pi / 2) for i in range(6, -1, -1)]

        pygame.draw.polygon(self.screen, color, [(x, y) for x, y in zip(xpoints, ypoints)])

    def drawSim(self, sim: SatelliteSim):

        self.screen.fill(SatelliteView.BLACK)
        planetList = [(SatelliteView.WIDTH - SatelliteView.PLANET_SIZE) / 2,
                      (SatelliteView.HEIGHT - SatelliteView.PLANET_SIZE) / 2,
                      SatelliteView.PLANET_SIZE, SatelliteView.PLANET_SIZE]

        # draw planet
        pygame.draw.ellipse(self.screen, SatelliteView.WHITE, planetList)

        # draw ground station arcs
        for gs in sim.groundStations:
            self.drawArc(SatelliteView.PURPLE, 2*math.pi*gs[0]/SatelliteSim.PERIOD, 2*math.pi*gs[1]/SatelliteSim.PERIOD, int(SatelliteView.PLANET_SIZE / 16))

        # draw target arcs
        for t in sim.targets:
            self.drawArc(SatelliteView.ORANGE, 2*math.pi*t[0]/SatelliteSim.PERIOD, 2*math.pi*t[1]/SatelliteSim.PERIOD, int(SatelliteView.PLANET_SIZE / 32))

        # draw satellite
        pygame.draw.ellipse(self.screen, SatelliteView.WHITE,
                            [(SatelliteView.WIDTH - SatelliteView.SAT_SIZE) / 2 + (
                                        SatelliteView.PLANET_SIZE / 2 + SatelliteView.ORBIT_DISTANCE) * math.sin(
                                2*math.pi*sim.pos/SatelliteSim.PERIOD + math.pi / 2),
                             (SatelliteView.HEIGHT - SatelliteView.SAT_SIZE) / 2 + (
                                         SatelliteView.PLANET_SIZE / 2 + SatelliteView.ORBIT_DISTANCE) * math.cos(
                                 2*math.pi*sim.pos/SatelliteSim.PERIOD + math.pi / 2),
                             SatelliteView.SAT_SIZE, SatelliteView.SAT_SIZE], 0)
        pygame.draw.line(self.screen, SatelliteView.WHITE,
                         (SatelliteView.WIDTH / 2 + (
                                     SatelliteView.PLANET_SIZE / 2 + SatelliteView.ORBIT_DISTANCE) * math.sin(
                             2*math.pi*sim.pos/SatelliteSim.PERIOD + math.pi / 2),
                          SatelliteView.HEIGHT / 2 + (
                                      SatelliteView.PLANET_SIZE / 2 + SatelliteView.ORBIT_DISTANCE) * math.cos(
                              2*math.pi*sim.pos/SatelliteSim.PERIOD + math.pi / 2)),
                         (SatelliteView.WIDTH / 2 + (SatelliteView.PLANET_SIZE / 2) * math.sin(2*math.pi*sim.pos/SatelliteSim.PERIOD + math.pi / 2),
                          SatelliteView.HEIGHT / 2 + (SatelliteView.PLANET_SIZE / 2) * math.cos(2*math.pi*sim.pos/SatelliteSim.PERIOD + math.pi / 2))
                         )

        # draw images
        offset = (SatelliteView.WIDTH - SatelliteView.HUD_WIDTH) / 2
        for index, image in enumerate(sim.images):
            pygame.draw.rect(self.screen, SatelliteView.WHITE, [offset + index * (SatelliteView.IMAGE_SIZE * 1.2),
                                                                SatelliteView.IMAGE_SIZE, SatelliteView.IMAGE_SIZE,
                                                                SatelliteView.IMAGE_SIZE])
            if image >= 0:
                panelColor = SatelliteView.BLACK
                if sim.analysis[index] and sim.satellite_busy_time > 0 \
                        and sim.last_action[0] == SatelliteSim.ACTION_ANALYSE \
                        and sim.last_action[2] == index:
                    panelColor = [o + (p - o)*(sim.satellite_busy_time/SatelliteSim.DURATION_ANALYSE) for p,o in zip(SatelliteView.ORANGE, SatelliteView.PURPLE)]
                elif sim.analysis[index]:
                    panelColor = SatelliteView.PURPLE
                else:
                    panelColor = SatelliteView.ORANGE
                pygame.draw.rect(self.screen, panelColor,
                             [offset + index * (SatelliteView.IMAGE_SIZE * 1.2) + SatelliteView.IMAGE_SIZE * 0.1,
                              SatelliteView.IMAGE_SIZE * 1.1, SatelliteView.IMAGE_SIZE * 0.8,
                              SatelliteView.IMAGE_SIZE * 0.8])
                self.screen.blit(self.text_digits[image], (
                offset + index * (SatelliteView.IMAGE_SIZE * 1.2) + SatelliteView.IMAGE_SIZE * 0.2,
                SatelliteView.IMAGE_SIZE * 1.2))

        # draw satellite recovery time
        max_time = max(SatelliteSim.DURATION_ANALYSE, SatelliteSim.DURATION_DUMP, SatelliteSim.DURATION_TAKE_IMAGE)
        pygame.draw.rect(self.screen, SatelliteView.WHITE, [offset, 2.2 * SatelliteView.IMAGE_SIZE,
                                                            (len(sim.images) - 1) * SatelliteView.IMAGE_SIZE * 1.2 + SatelliteView.IMAGE_SIZE,
                                                            SatelliteView.IMAGE_SIZE])
        barWidth = SatelliteView.HUD_WIDTH * sim.satellite_busy_time / max_time
        pygame.draw.rect(self.screen, SatelliteView.PURPLE, [offset + SatelliteView.IMAGE_SIZE * 0.1,
                                                             2.3 * SatelliteView.IMAGE_SIZE, barWidth,
                                                             SatelliteView.IMAGE_SIZE * 0.8])

        # draw score
        max_score = max(sim.goalRef.value, 100)
        barWidth = SatelliteView.HUD_WIDTH * sim.goalRef.value / max_score
        pygame.draw.rect(self.screen, SatelliteView.WHITE, [offset + SatelliteView.GOAL_SIZE * 0.1,
                                                             SatelliteView.HEIGHT - 6.2 * SatelliteView.GOAL_SIZE,
                                                             SatelliteView.HUD_WIDTH, SatelliteView.GOAL_SIZE])
        pygame.draw.rect(self.screen, SatelliteView.PURPLE, [offset + SatelliteView.GOAL_SIZE * 0.1,
                                                             SatelliteView.HEIGHT - 6.1 * SatelliteView.GOAL_SIZE,
                                                             barWidth, SatelliteView.GOAL_SIZE * 0.8])

        # draw single goals
        if len(sim.goalRef.single_goals) >= 0:
            for index, target in enumerate(sim.goalRef.single_goals):
                pygame.draw.rect(self.screen, SatelliteView.ORANGE,
                             [offset + index * (SatelliteView.GOAL_SIZE * 1.1) + SatelliteView.GOAL_SIZE * 0.1,
                              SatelliteView.HEIGHT - SatelliteView.GOAL_SIZE * 5.1,
                              SatelliteView.GOAL_SIZE * 0.8, SatelliteView.GOAL_SIZE * 0.8])
                self.screen.blit(self.text_digits[target], (
                            offset + index * (SatelliteView.GOAL_SIZE * 1.1) + SatelliteView.GOAL_SIZE * 0.2,
                            SatelliteView.HEIGHT - SatelliteView.GOAL_SIZE * 5.0))

        # draw campaigns
        orbit = math.floor(sim.sim_time / SatelliteSim.PERIOD)
        if len(sim.goalRef.campaigns) >= 0:
            for index, c in enumerate(sim.goalRef.campaigns):
                pygame.draw.rect(self.screen, SatelliteView.WHITE,
                                 [offset + SatelliteView.GOAL_SIZE * 0.1,
                                  SatelliteView.HEIGHT - (1.2*SatelliteView.GOAL_SIZE) * (3.4 - index),
                                  len(c.targets) * (1.1*SatelliteView.GOAL_SIZE), SatelliteView.GOAL_SIZE])
                for ti, t in enumerate(c.targets):
                    color = SatelliteView.ORANGE
                    if not c.campaign_started or t[1]+c.campaign_start_orbit > orbit:
                        color = SatelliteView.BLACK
                    if c.targets_completed[ti]:
                        color = SatelliteView.PURPLE
                    pygame.draw.rect(self.screen, color,
                                 [offset + ti * (SatelliteView.GOAL_SIZE * 1.1) + SatelliteView.GOAL_SIZE * 0.2,
                                  SatelliteView.HEIGHT - (1.2*SatelliteView.GOAL_SIZE) * (3.3-index),
                                  SatelliteView.GOAL_SIZE * 0.8, SatelliteView.GOAL_SIZE * 0.8])
                    self.screen.blit(self.text_digits[t[0]], (
                                offset + ti * (SatelliteView.GOAL_SIZE * 1.1) + SatelliteView.GOAL_SIZE * 0.3,
                                SatelliteView.HEIGHT - (1.2*SatelliteView.GOAL_SIZE) * (3.2-index)))


        pygame.display.flip()

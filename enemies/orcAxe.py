import pygame
import os
from .enemy import Enemy

imgs = []
for x in range(6):
    add_str = str(x)
    imgs.append(pygame.transform.scale(
        pygame.image.load(os.path.join("assets/enemies/orcAxe/RUN", "RUN_00" + add_str + ".png")), (64, 64)))


class OrcAxe(Enemy):
    def __init__(self):
        super().__init__()
        self.maxHitPoints = 9
        self.hitPoints = self.maxHitPoints
        self.imgs = imgs[:]
        self.name = "axe"
        self.money = 3
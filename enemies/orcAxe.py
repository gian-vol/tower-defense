import pygame
import os
from .enemy import Enemy


class OrcAxe(Enemy):
    # Static asset loading
    imgs = []
    for x in range(6):
        add_str = str(x)
        imgs.append(pygame.transform.scale(
            pygame.image.load(os.path.join("assets/enemies/orcAxe/RUN", "RUN_00" + add_str + ".png")), (64, 64)))

    def __init__(self):
        super().__init__()
        self.maxHitPoints = 9
        self.hitPoints = self.maxHitPoints
        self.imgs = self.imgs.copy()
        self.name = "axe"
        self.money = 3

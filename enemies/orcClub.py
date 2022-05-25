import pygame
import os
from .enemy import Enemy


class OrcClub(Enemy):
    # Static asset loading
    imgs = []
    for x in range(6):
        add_str = str(x)
        imgs.append(pygame.transform.scale(
            pygame.image.load(os.path.join("assets/enemies/orcClub/RUN", "RUN_00" + add_str + ".png")), (64, 64)))

    def __init__(self):
        super().__init__()
        self.imgs = self.imgs.copy()
        self.maxHitPoints = 50
        self.hitPoints = self.maxHitPoints
        self.name = "club"
        self.money = 2

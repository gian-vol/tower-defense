import pygame
import os
from .enemy import Enemy


class OrcSword(Enemy):
    # Static asset loading
    imgs = []
    for x in range(6):
        add_str = str(x)
        imgs.append(pygame.transform.scale(
            pygame.image.load(os.path.join("assets/enemies/orcSword/RUN", "RUN_00" + add_str + ".png")), (64, 64)))

    def __init__(self):
        self.maxHitPoints = 9
        super().__init__()
        self.imgs = self.imgs.copy()
        self.name = "sword"
        self.money = 6

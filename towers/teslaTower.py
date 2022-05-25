import pygame
import os
import math
from .tower import Tower


class TeslaTower(Tower):
    """
    Tesla Tower class
    """
    # Load all images for the Tesla tower as static
    towerImages = []
    for x in range(3):
        add_str = str(x)
        towerImages.append(pygame.transform.scale(
            pygame.image.load(os.path.join("assets/towers/tesla", "teslaTower_0" + add_str + ".png")), (84, 84)))

    def __init__(self, x, y):
        self.upgrade_cost = [600, 900, "MAX"]
        super().__init__(x, y)
        self.name = "tesla"
        self.towerImages = self.towerImages.copy()
        self.archerCount = 0
        self.range = 200
        self.damage = 3
        self.inRange = False

    def draw(self, win):
        super().draw_radius(win)
        super().draw(win)

    def attack(self, enemies):
        """
        Attacks an enemy from the list and returns the gold if the enemy was killed
        :param enemies: list of enemies
        :return: int
        """
        self.inRange = False
        enemy_closest = []
        for enemy in enemies:
            enemy_x = enemy.x
            enemy_y = enemy.y

            distance = math.sqrt((self.x - enemy_x)**2 + (self.y - enemy_y)**2)
            if distance < self.range:
                self.inRange = True
                enemy_closest.append(enemy)

                if len(enemy_closest) > 0:
                    first_enemy = enemy_closest[0]
                    if first_enemy.hit(self.damage):
                        money = first_enemy.money
                        enemies.remove(first_enemy)
                        return money
        return 0

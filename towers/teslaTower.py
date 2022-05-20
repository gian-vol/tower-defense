import pygame
import os
import math
from .tower import Tower


class TeslaTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.towerImages = []
        self.archerCount = 0
        self.range = 200
        self.damage = 3
        self.inRange = False

        # cargar las imagenes de tesla tower
        for x in range(3):
            add_str = str(x)
            self.towerImages.append(pygame.transform.scale(
                pygame.image.load(os.path.join("assets/towers/tesla", "teslaTower_0" + add_str + ".png")), (84, 64)))

    def draw(self, win):
        super().draw_radius(win)
        super().draw(win)

    def attack(self, enemies):
        """
        ataca un enemigo en la lista
        :param enemies:
        :return:
        """
        money = 0
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
                    if first_enemy.hit(self.damage) == True:
                        money = first_enemy.money
                        enemies.remove(first_enemy)
            return money
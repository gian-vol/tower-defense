import pygame
import os
import math
from .tower import Tower


class ArcherTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.towerImages = []
        self.archerImages = []
        self.archerCount = 0
        self.range = 150
        self.damage = 1
        self.inRange = False
        self.facingLeft = True

        # cargar las imagenes de archer tower
        for x in range(3):
            add_str = str(x)
            self.towerImages.append(pygame.transform.scale(
                pygame.image.load(os.path.join("assets/towers/archer", "archerTower_0" + add_str + ".png")), (64, 64)))
        # cargar las imagenes de arquero
        for x in range(7):
            add_str = str(x)
            self.archerImages.append(pygame.transform.scale(
                pygame.image.load(os.path.join("assets/shooters/archer", "archer_0" + add_str + ".png")), (50, 50)))

    def draw(self, win):
        super().draw_radius(win)
        super().draw(win)

        if self.inRange:
            self.archerCount += 1
            if self.archerCount >= len(self.archerImages) * 3:
                self.archerCount = 0
        else:
            self.archerCount = 0

        archer = self.archerImages[self.archerCount // 3]
        win.blit(archer, (self.x - (archer.get_width() / 2), (self.y - archer.get_height() - 10)))

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

        #trackea posicion enemigo y gira derecha o izq
        enemy_closest.sort(key=lambda x: x.x)
        if len(enemy_closest) > 0:
            first_enemy = enemy_closest[0]
            if self.archerCount == 6:
                if first_enemy.hit(self.damage) == True:
                    money = first_enemy.money
                    enemies.remove(first_enemy)

            if first_enemy.x > self.x and not self.facingLeft:
                self.facingLeft = True
                for x, img in enumerate(self.archerImages):
                    self.archerImages[x] = pygame.transform.flip(img, True, False)
            elif self.facingLeft and first_enemy.x < self.x:
                self.facingLeft = False
                for x, img in enumerate(self.archerImages):
                    self.archerImages[x] = pygame.transform.flip(img, True, False)
        return money

    def get_upgrade_cost(self):
        return self.menu.get_item_cost()

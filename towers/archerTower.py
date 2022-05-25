import pygame
import os
import math
from .tower import Tower


class ArcherTower(Tower):
    """
    Archer Tower class
    """
    towerImages = []
    archerImages = []
    # Load all images for the archer tower as static
    for x in range(3):
        add_str = str(x)
        towerImages.append(pygame.transform.scale(
            pygame.image.load(os.path.join("assets/towers/archer", "archerTower_0" + add_str + ".png")), (64, 64)))
    # Load all images of the archer as static
    for x in range(7):
        add_str = str(x)
        archerImages.append(pygame.transform.scale(
            pygame.image.load(os.path.join("assets/shooters/archer", "archer_0" + add_str + ".png")), (50, 50)))

    def __init__(self, x, y):
        self.upgrade_cost = [20, 80, "MAX"]
        super().__init__(x, y)
        self.name = "archer"
        self.towerImages = self.towerImages.copy()
        self.archerImages = self.archerImages.copy()
        self.archerCount = 0
        self.range = 150
        self.damage = 1
        self.inRange = False
        self.facingLeft = True

    def draw(self, win):
        super().draw_radius(win)
        super().draw(win)

        if self.inRange and not self.moving:
            self.archerCount += 1
            if self.archerCount >= len(self.archerImages) * 3:
                self.archerCount = 0
        else:
            self.archerCount = 0

        archer = self.archerImages[self.archerCount // 3]
        win.blit(archer, (self.x - (archer.get_width() / 2), (self.y - archer.get_height() - 10)))

    def attack(self, enemies):
        """
        Attacks an enemy from the list and returns the gold if the enemy was killed
        :param enemies: list of enemies
        :return: int
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

        # Tracks the position of the enemy and faces right or left
        enemy_closest.sort(key=lambda x: x.x)
        if len(enemy_closest) > 0:
            first_enemy = enemy_closest[0]
            if self.archerCount == 6:
                if first_enemy.hit(self.damage):
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


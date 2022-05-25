import pygame
import os
import math
from .tower import Tower


class WizardTower(Tower):
    towerImages = []
    wizardImages = []
    # Load all images for the wizard tower as static
    for x in range(3):
        add_str = str(x)
        towerImages.append(pygame.transform.scale(
            pygame.image.load(os.path.join("assets/towers/wizard", "wizardTower_0" + add_str + ".png")), (94, 94)))
    # Load all images of the wizard as static
    for x in range(8):
        add_str = str(x)
        wizardImages.append(pygame.transform.scale(
            pygame.image.load(os.path.join("assets/shooters/wizard", "wizard_0" + add_str + ".png")), (80, 80)))

    def __init__(self, x, y):
        self.upgrade_cost = [20, 30, "MAX"]
        super().__init__(x, y)
        self.towerImages = self.towerImages.copy()
        self.wizardImages = self.wizardImages.copy()
        self.wizardCount = 0
        self.range = 100
        self.damage = 2
        self.inRange = False
        self.facingLeft = True

    def draw(self, win):
        super().draw_radius(win)
        super().draw(win)

        if self.inRange:
            self.wizardCount += 1
            if self.wizardCount >= len(self.wizardImages) * 3:
                self.wizardCount = 0
        else:
            self.wizardCount = 0

        wizard = self.wizardImages[self.wizardCount // 3]
        win.blit(wizard, (self.x - (wizard.get_width() / 2), (self.y - wizard.get_height() - 10)))

    def attack(self, enemies):
        """
        Attacks an enemy from the list
        :param enemies: list of enemies
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

        # Tracks the position of the enemy and faces right or left
        enemy_closest.sort(key=lambda x: x.x)
        if len(enemy_closest) > 0:
            first_enemy = enemy_closest[0]
            if self.wizardCount == 8:
                if first_enemy.hit(self.damage):
                    money = first_enemy.money
                    enemies.remove(first_enemy)

            if first_enemy.x > self.x and not self.facingLeft:
                self.facingLeft = True
                for x, img in enumerate(self.wizardImages):
                    self.wizardImages[x] = pygame.transform.flip(img, True, False)
            elif self.facingLeft and first_enemy.x < self.x:
                self.facingLeft = False
                for x, img in enumerate(self.wizardImages):
                    self.wizardImages[x] = pygame.transform.flip(img, True, False)
        return money

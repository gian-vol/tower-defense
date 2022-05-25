import pygame
import os
import random
import time

from enemies.orcSword import OrcSword
from enemies.orcAxe import OrcAxe
from enemies.orcClub import OrcClub
from towers.archerTower import ArcherTower
from towers.wizardTower import WizardTower
from towers.teslaTower import TeslaTower
from menu.menu import VerticalMenu


class Game:
    """
    Main game class
    """
    # Static asset loading
    pygame.font.init()
    lives_image = pygame.image.load(os.path.join("assets", "heart.png"))
    gold_image = pygame.image.load(os.path.join("assets", "gold.png"))
    side_menu_image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "HUD.png")), (90, 40))

    def __init__(self):
        self.width = 960
        self.height = 720
        self.window = pygame.display.set_mode((self.width, self.height))
        self.enemies = [OrcSword()]
        self.towers = [ArcherTower(300, 300), WizardTower(500, 300), TeslaTower(680, 300)]
        self.lives = 3
        self.money = 500
        self.background = pygame.image.load(os.path.join("assets", "background.png"))
        self.timer = time.time()
        self.life_font = pygame.font.SysFont("italic", 50)
        self.selected_tower = None
        self.menu = VerticalMenu(self.width - self.side_menu_image.get_width(), 150, self.side_menu_image)

    def run(self):
        """
        Main game loop
        :return: None
        """
        run = True
        clock = pygame.time.Clock()
        while run:
            if time.time() - self.timer >= random.randrange(4, 15)/2:
                self.timer = time.time()
                self.enemies.append(random.choice([OrcAxe(), OrcClub(), OrcSword()]))
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    button_clicked = None
                    if self.selected_tower:
                        button_clicked = self.selected_tower.menu.get_clicked(pos[0], pos[1])
                        if button_clicked:
                            cost = self.selected_tower.get_upgrade_cost()
                            if cost != "MAX" and self.money >= cost:
                                self.money -= cost
                                self.selected_tower.upgrade()
                    if not button_clicked:
                        for tower in self.towers:
                            if tower.click(pos[0], pos[1]):
                                tower.selected = True
                                self.selected_tower = tower
                            else:
                                tower.selected = False
            # Loop all the enemies
            to_del = []
            for en in self.enemies:
                if en.y >= self.height:
                    to_del.append(en)
            # Delete enemies
            for d in to_del:
                self.lives -= 1
                self.enemies.remove(d)

            # Loop all the towers
            for tower in self.towers:
                self.money += tower.attack(self.enemies)
            # If you loose
            if self.lives <= 0:
                print("You loose")
                run = False
            self.draw()
        pygame.quit()

    def draw(self):
        """
        Main draw function
        :return: None
        """
        self.window.blit(self.background, (0, 0))

        # Draw enemies
        for en in self.enemies:
            en.draw(self.window)

        # Draw towers
        for tw in self.towers:
            tw.draw(self.window)

        # Draw lives
        life_text = self.life_font.render(str(self.lives), True, (0, 0, 0))
        life = pygame.transform.scale(self.lives_image, (100, 100))
        start_x = self.width - life.get_width() - 10
        self.window.blit(life_text, (start_x - life_text.get_width() + 30, 40))
        self.window.blit(life, (start_x, 10))
        # Draw gold
        gold_text = self.life_font.render(str(self.money), True, (0, 0, 0))
        gold = pygame.transform.scale(self.gold_image, (100, 100))
        start_x = self.width - gold.get_width() - 80
        self.window.blit(gold_text, (start_x - gold_text.get_width() - 30, 40))
        self.window.blit(gold, (start_x - 25, 5))

        pygame.display.update()

    def draw_menu(self):
        """
        Draws the side menu
        """
        pass


g = Game()
g.run()

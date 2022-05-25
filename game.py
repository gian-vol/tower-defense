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
    side_menu_image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "sideMenu.png")), (90, 290))
    archer_menu = pygame.transform.scale(pygame.image.load(
        os.path.join("assets/towers/archer", "archerTower_00.png")), (80, 80))
    wizard_menu = pygame.transform.scale(pygame.image.load(
        os.path.join("assets/towers/wizard", "wizardTower_00.png")), (80, 80))
    tesla_menu = pygame.transform.scale(pygame.image.load(
        os.path.join("assets/towers/tesla", "teslaTower_00.png")), (80, 80))
    tower_names = ["archer", "wizard", "tesla"]

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
        self.menu = VerticalMenu(self.width - self.side_menu_image.get_width() + 15, 120, self.side_menu_image)
        self.menu.add_button(self.archer_menu, "archer", 200)
        self.menu.add_button(self.wizard_menu, "wizard", 300)
        self.menu.add_button(self.tesla_menu, "tesla", 2000)
        self.moving_tower = False

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
            pos = pygame.mouse.get_pos()
            if self.moving_tower:
                self.moving_tower.move(pos[0], pos[1])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.moving_tower:
                        if self.moving_tower.name in self.tower_names:
                            self.towers.append(self.moving_tower)
                        self.moving_tower.moving = False
                        self.moving_tower = None
                    else:
                        side_menu_button = self.menu.get_clicked(pos[0], pos[1])
                        if side_menu_button:
                            tower_cost = self.menu.get_tower_cost(side_menu_button)
                            if self.money >= tower_cost:
                                self.add_tower(side_menu_button)
                                self.money -= tower_cost
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

        # Draw moving tower
        if self.moving_tower:
            self.moving_tower.draw(self.window)

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
        # Draw side menu
        self.menu.draw(self.window)
        pygame.display.update()

    def add_tower(self, name):
        x, y = pygame.mouse.get_pos()
        tower_list = ["archer", "wizard", "tesla"]
        tower_object_list = [ArcherTower(x, y), WizardTower(x, y), TeslaTower(x, y)]
        tower = tower_object_list[tower_list.index(name)]
        self.moving_tower = tower
        tower.moving = True


g = Game()
g.run()

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

pygame.font.init()
lives_image = pygame.image.load(os.path.join("assets", "heart.png"))
gold_image = pygame.image.load(os.path.join("assets", "gold.png"))


class Game:
    def __init__(self):
        self.width = 960
        self.height = 720
        self.window = pygame.display.set_mode((self.width, self.height))
        self.enemies = [OrcSword()]
        self.towers = [ArcherTower(300, 300), WizardTower(500, 300), TeslaTower(980, 300)]
        self.lives = 3
        self.money = 50
        self.background = pygame.image.load(os.path.join("assets", "background.png"))
        self.timer = time.time()
        self.life_font = pygame.font.SysFont("italic", 50)
        self.selected_tower = None

    def run(self):
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
                            if self.money >= cost:
                                self.money -= cost
                                self.selected_tower.upgrade()
                    if not(button_clicked):
                        for tower in self.towers:
                            if tower.click(pos[0], pos[1]):
                                tower.selected = True
                                self.selected_tower = tower
                            else:
                                tower.selected = False
            # Loopear los enemigos
            to_del = []
            for en in self.enemies:
                if en.y >= self.height:
                    to_del.append(en)
            # Deletear enemigos
            for d in to_del:
                self.lives -= 1
                self.enemies.remove(d)

            # loopear las torres
            for tower in self.towers:
                self.money += tower.attack(self.enemies)
            # si perdes
            if self.lives <= 0:
                print("You loose")
                run = False
            self.draw()
        pygame.quit()

    def draw(self):
        self.window.blit(self.background, (0, 0))

        #Dibujar enemigos
        for en in self.enemies:
            en.draw(self.window)

        #Dibujar torres
        for tw in self.towers:
            tw.draw(self.window)

        #Dibujar vidas
        life_text = self.life_font.render(str(self.lives), True, (0, 0, 0))
        life = pygame.transform.scale(lives_image, (100, 100))
        start_x = self.width - life.get_width() - 10
        self.window.blit(life_text, (start_x - life_text.get_width() + 30, 40))
        self.window.blit(life, (start_x, 10))
        #Dibujar oro
        gold_text = self.life_font.render(str(self.money), True, (0, 0, 0))
        gold = pygame.transform.scale(gold_image, (100, 100))
        start_x = self.width - gold.get_width() - 80
        self.window.blit(gold_text, (start_x - gold_text.get_width() - 30, 40))
        self.window.blit(gold, (start_x - 25, 5))

        pygame.display.update()

    def draw_menu(self):
        pass

g = Game()
g.run()

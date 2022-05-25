import pygame
from menu.menu import Menu
import os


class Tower:
    """
    Main tower class
    """
    # Static asset loading
    menu_background = pygame.transform.scale(pygame.image.load(os.path.join("assets", "HUD.png")), (90, 40))
    upgrade_button = pygame.transform.scale(pygame.image.load(os.path.join("assets", "upgradeIcon.png")), (35, 35))

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0
        self.level = 1
        self.damage = 1
        self.selected = False
        self.moving = False
        # Define menu and buttons
        self.menu = Menu(self.x, self.y, self.menu_background, self.upgrade_cost, self)
        self.menu.add_button(self.upgrade_button, "Upgrade")

    def draw(self, win):
        """
        Draws the towers
        :param win:
        :return: None
        """
        image = self.towerImages[self.level - 1]
        win.blit(image, (self.x - image.get_width() // 2, self.y - image.get_height() // 2))

        # To draw the menu
        if self.selected:
            self.menu.draw(win)

    def draw_radius(self, win):
        """
        Draws the circle that represents the shooting radius
        :param win: The surface int
        :return: None
        """
        if self.selected:
            range_circle = pygame.Surface((self.range * 2, self.range * 2), pygame.SRCALPHA, 32)
            pygame.draw.circle(range_circle, (0, 0, 255, 50), (self.range, self.range), self.range, 0)
            win.blit(range_circle, (self.x - self.range, self.y - self.range))

    def click(self, X, Y):
        """
        Returns if the tower was clicked and selects it
        :param X: int
        :param Y: int
        :return: bool
        """
        image = self.towerImages[self.level - 1]

        return (self.x + image.get_width() // 3 >= X >= self.x - image.get_width() // 3) \
               and (self.y + image.get_height() // 2 >= Y >= self.y - image.get_height() // 2)

    def upgrade(self):
        """
        Upgrades the selected tower
        :return: None
        """
        if self.level < len(self.towerImages):
            self.level += 1
            self.damage += 1

    def get_upgrade_cost(self):
        """
        Gets the upgrade cost and returns it
        :return: int
        """
        return self.upgrade_cost[self.level - 1]

    def move(self, x, y):
        """
        Moves the tower to the defined position
        :param x: int
        :param y: int
        :return:
        """
        self.x = x
        self.y = y
        self.menu.x = x
        self.menu.y = y
        self.menu.update()

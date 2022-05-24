import pygame
import os
pygame.font.init()

gold = pygame.transform.scale(pygame.image.load(os.path.join("assets", "gold.png")), (35, 35))


class Menu:
    def __init__(self, x, y, image, item_cost, tower):
        self.x = x
        self.y = y
        self.width = image.get_width()
        self.height = image.get_height()
        self.item_cost = item_cost
        self.images = []
        self.buttons = []
        self.items = 0
        self.background = image
        self.font = pygame.font.SysFont("arial", 20)
        self.tower = tower

    def draw(self, win):
        """
        Draws buttons and the background of the menu
        :param win: The surface
        :return:
        """
        win.blit(self.background, (self.x - self.background.get_width() / 2, self.y + 20))
        for item in self.buttons:
            item.draw(win)
            win.blit(gold, (item.x + item.width + 10, item.y + 8))
            text = self.font.render(str(self.item_cost[self.tower.level - 1]), True, (255, 255, 255))
            win.blit(text, (item.x + item.width + 15, item.y - 3))

    def click(self, X, Y):
        """
        Returns if the position collided with the menu
        :param X: X position int
        :param Y: Y posiition int
        :return:
        """
        if X <= self.x + self.width and X >= self.x:
            if Y <= self.y + self.height and Y >= self.y:
                return True
        return False

    def get_item_cost(self):
        """
        :returns: The cost of the upgrade
        """
        return self.item_cost[self.tower.level - 1]

    def get_clicked(self, X, Y):
        """
        Returns the clicked item in the menu
        :param X: X position int
        :param Y: Y position int
        :return: the item clicked
        """
        for button in self.buttons:
            if button.click(X, Y):
                return button.name
        return None

    def add_button(self, image, name):
        """
        Adds the button to the menu
        :param image: The button image
        :param name: The button name
        :return: None
        """
        self.items += 1
        increment_x = self.width / self.items / 2
        button_x = self.x - self.background.get_width() // 2 + 5
        button_y = self.y + 23
        self.buttons.append(Button(button_x, button_y, image, name))


class VerticalMenu(Menu):
    """
    Class fot the vertical menu on the side bar
    """
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.width = image.get_width()
        self.height = image.get_height()
        self.images = []
        self.buttons = []
        self.items = 0
        self.background = image
        self.font = pygame.font.SysFont("arial", 20)

    def add_button(self, image, name, cost):
        """
        Adds the button to the menu
        :param image: The button image
        :param name: The button name
        :return: None
        """
        self.items += 1
        button_x = self.x
        button_y = self.y + (self.items - 1) * 40
        self.buttons.append(VerticalButton(button_x, button_y, image, name, cost))

    def get_tower_cost(self):
        """

        :return:
        """
        return None


class Button:
    """
    Class for the buttons in the menu
    """
    def __init__(self, x, y, image, name):
        self.image = image
        self.x = x
        self.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.name = name

    def click(self, X, Y):
        """
        Returns if the position collided with the menu
        :param X: X position int
        :param Y: Y position int
        :return: bool
        """
        if X <= self.x + self.width and X >= self.x:
            if Y <= self.y + self.height and Y >= self.y:
                return True
        return False

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))


class VerticalButton(Button):
    """
    Class for the vertical buttons in the menu
    """
    def __init__(self, x, y, image, name, cost):
        super().__init__(x, y, img, name)
        self.cost = cost

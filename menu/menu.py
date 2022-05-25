import pygame
import os


class Menu:
    pygame.font.init()
    # Static asset loading
    gold = pygame.transform.scale(pygame.image.load(os.path.join("assets", "gold.png")), (35, 35))

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
        :return: None
        """
        win.blit(self.background, (self.x - self.background.get_width() / 2, self.y + 20))
        for item in self.buttons:
            item.draw(win)
            win.blit(self.gold, (item.x + item.width + 10, item.y + 8))
            text = self.font.render(str(self.item_cost[self.tower.level - 1]), True, (255, 255, 255))
            win.blit(text, (item.x + item.width + 15, item.y - 3))

    def click(self, X, Y):
        """
        Returns if the position collided with the menu
        :param X: X position int
        :param Y: Y posiition int
        :return: bool
        """
        return (self.x + self.width >= X >= self.x) \
               and (self.y + self.height >= Y >= self.y)

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
        self.buttons.append(Button(self, image, name))

    def update(self):
        """
        Updates the menu and button location
        :return: None
        """
        for button in self.buttons:
            button.update()


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

    def draw(self, win):
        """
        Draws buttons and the background of the menu
        :param win: The surface
        :return: None
        """
        win.blit(self.background, (self.x - self.background.get_width() / 2, self.y + 20))
        for item in self.buttons:
            item.draw(win)
            win.blit(self.gold, (item.x - 8, item.y + 8))
            text = self.font.render(str(item.cost), True, (255, 255, 255))
            win.blit(text, (item.x + 5, item.y - 10))

    def add_button(self, image, name, cost):
        """
        Adds the button to the menu
        :param image: The button image
        :param name: The button name
        :return: None
        """
        self.items += 1
        button_x = self.x - 35
        button_y = self.y + 30 + (self.items - 1) * 100
        self.buttons.append(VerticalButton(button_x, button_y, image, name, cost))

    def get_tower_cost(self, name):
        """
        Gets the cost of the tower
        :param name: The button name
        :return: int
        """
        for button in self.buttons:
            if button.name == name:
                return button.cost
        return -1


class Button:
    """
    Class for the buttons in the menu
    """

    def __init__(self, menu, image, name):
        self.image = image
        self.menu = menu
        self.x = menu.x - 40
        self.y = menu.y + 23
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.name = name

    def draw(self, win):
        """
        Draws the button
        :param win: The surface
        :return: None
        """
        win.blit(self.image, (self.x, self.y))

    def update(self):
        """
        Updates the position of the button
        :return: None
        """
        self.x = self.menu.x - 40
        self.y = self.menu.y + 23

    def click(self, X, Y):
        """
        Returns if the position collided with the menu
        :param X: X position int
        :param Y: Y position int
        :return: bool
        """
        return (self.x + self.width >= X >= self.x) \
               and (self.y + self.height >= Y >= self.y)


class VerticalButton(Button):
    """
    Class for the vertical buttons in the menu
    """

    def __init__(self, x, y, image, name, cost):
        self.image = image
        self.x = x
        self.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.name = name
        self.cost = cost

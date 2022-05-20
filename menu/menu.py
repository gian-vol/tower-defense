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
        dibuja botones y fondo del menu
        :param win:
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
        retorna si la posicion colisiono con el menu
        :param X:
        :param Y:
        :return:
        """
        if X <= self.x + self.width and X >= self.x:
            if Y <= self.y + self.height and Y >= self.y:
                return True
        return False

    def get_item_cost(self):
        """
        retorna el costo de upgrade
        """
        return self.item_cost[self.tower.level - 1]

    def get_clicked(self, X, Y):
        """
        retorna el item clikeado del menu
        :param X:
        :param Y:
        :return:
        """
        for button in self.buttons:
            if button.click(X, Y):
                return button.name
        return None

    def add_button(self, image, name):
        """
        agrega el boton al menu
        :param image:
        :param name:
        :return:
        """
        self.items += 1
        increment_x = self.width / self.items / 2
        button_x = self.x - self.background.get_width() // 2 + 5
        button_y = self.y + 23
        self.buttons.append(Button(button_x, button_y, image, name))


class Button:
    """
    clase de botones para el menu
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
        retorna si la posicion colisiono con el menu
        :param X:
        :param Y:
        :return:
        """
        if X <= self.x + self.width and X >= self.x:
            if Y <= self.y + self.height and Y >= self.y:
                return True
        return False

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))
import pygame
import math


class Enemy:
    """
    Main enemy class
    """
    def __init__(self):
        self.height = 50
        self.width = 50
        self.hitPoints = self.maxHitPoints
        self.path = [(162, -10), (162, 38), (162, 70), (162, 101), (162, 132), (162, 168), (162, 199), (194, 209), (238, 209),
                     (277, 209), (323, 209), (365, 209), (412, 209), (455, 209), (500, 209), (549, 209), (593, 209),
                     (639, 209), (674, 209), (709, 209), (709, 250), (709, 291), (709, 324), (709, 362), (709, 398),
                     (709, 431), (709, 471), (709, 509), (667, 519), (629, 519), (594, 519), (560, 519), (526, 519),
                     (497, 519), (459, 519), (422, 519), (388, 519), (362, 519), (361, 561), (361, 602), (361, 637),
                     (361, 673), (-20, 673)]
        self.x = self.path[0][0]
        self.y = self.path[0][1]
        self.path_position = 0
        self.img = None
        self.distance = 0
        self.move_distance = 0
        self.animation_count = 0
        self.flipped = False

    def draw(self, win):
        """
        Draws the enemy
        :param win: The surface
        :return: None
        """
        self.img = self.imgs[self.animation_count]
        self.animation_count += 1
        if self.animation_count >= len(self.imgs):
            self.animation_count = 0

        win.blit(self.img, (self.x - self.img.get_width()/2, self.y - self.img.get_height()/2))
        self.draw_health_bar(win)
        self.move()

    def collide(self, X, Y):
        """
        Returns if we hit an enemy
        :param x: X position int
        :param y: Y position int
        :return: bool
        """
        return self.x + self.width >= X >= self.x\
               and self.Y + self.height >= Y >= self.y

    def draw_health_bar(self, win):
        """
        Draw the bar under the enemies
        :param win: The surface we are drawing
        :return:
        """
        length = 50
        move_by = round(length / self.maxHitPoints)
        health_bar = move_by * self.hitPoints

        pygame.draw.rect(win, (255, 0, 0), (self.x - 30, self.y + 35, length, 10), 0)
        pygame.draw.rect(win, (0, 255, 0), (self.x - 30, self.y + 35, health_bar, 10), 0)

    def move(self):
        """
        Moves the enemy
        :return: None
        """
        x1, y1 = self.path[self.path_position]
        if self.path_position + 1 > len(self.path):
            x2, y2 = (-10, 673)
        else:
            x2, y2 = self.path[self.path_position + 1]

        dirn = ((x2 - x1), (y2 - y1))
        length = math.sqrt((dirn[0])**2 + (dirn[1])**2)
        dirn = (dirn[0]/length, dirn[1]/length)

        if dirn[0] < 0 and not self.flipped:
            self.flipped = True
            for x, img in enumerate(self.imgs):
                self.imgs[x] = pygame.transform.flip(img, True, False)

        move_x, move_y = (self.x + dirn[0], self.y + dirn[1])

        self.x = move_x
        self.y = move_y

        # Moving to the next point
        if dirn[0] >= 0:  # Moving right
            if dirn[1] >= 0:  # Moving down
                if self.x >= x2 and self.y >= y2:
                    self.path_position += 1
            else:
                if self.x >= x2 and self.y <= y2:
                    self.path_position += 1
        else:  # Moving left
            if dirn[1] >= 0:  # Moving down
                if self.x <= x2 and self.y >= y2:
                    self.path_position += 1
            else:
                if self.x <= x2 and self.y >= y2:
                    self.path_position += 1

    def hit(self, damage):
        """
        Returns if the hitted enemy is dead
        :param damage: Damage int
        :return: bool
        """
        self.hitPoints -= damage
        return self.hitPoints <= 0

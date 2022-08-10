import pygame
from pygame.sprite import Sprite  # 他是pygame本身自带的一个精灵


class Alien(Sprite):
    """
    表示单个外星人
    """

    def __init__(self, ai_game):
        """ 初始化外星人并设置其起始位置"""
        super(Alien, self).__init__()
        self.screen = ai_game.screen
        self.settings=ai_game.settings

        # 加载外星人的图像并设置rect属性
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        # 每个外星人最初都在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # 储存外星人的精确水平
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        """ 向右移动外星人"""

        self.x+=(self.settings.alien_speed
                 *self.settings.alien_fleet_direction)
        self.rect.x=self.x

    def check_edges(self):
        "如果外星人位于屏幕边缘，就返回True"
        screen_rent=self.screen.get_rect()
        if self.rect.right>=screen_rent.right or self.rect.left<=0:
            return True

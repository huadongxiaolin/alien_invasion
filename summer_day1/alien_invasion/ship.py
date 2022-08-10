import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """
    管理飞船的类
    """

    def __init__(self, ai_game):
        """
        初始化飞船并设置其初始位置
        :param ai_game:
        """
        super(Ship, self).__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # 加载飞船并获取其外接矩阵
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # 对于每艘新飞船，都将其放在屏幕底部中央
        self.rect.midbottom = self.screen_rect.midbottom

        # 在飞船属性中存储小数值
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # 移动标志
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def blitme(self):
        """
        在指定位置绘画飞船
        :return:
        """
        self.screen.blit(self.image, self.rect)

    def update(self):
        "根据移动标志来调整飞船状态"
        # 更新飞船而非rect对象的值

        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed
        # 根据self.x,y更新rect对象
        self.rect.x = self.x
        self.rect.y=self.y

    def center_ship(self):
        """让飞船在屏幕底端居中"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

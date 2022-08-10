import pygame
from pygame.sprite import Sprite #他是pygame本身自带的一个精灵
#12.8.2创建bullet类
class Bullet(Sprite):
    """
    管理飞船所发射的子弹类型
    """
    def __init__(self,ai_game):
        """
        在飞船当前位置创建一个子弹对象
        :param ai_game:
        """
        super(Bullet, self).__init__()
        self.screen=ai_game.screen
        self.settings = ai_game.settings
        self.color=self.settings.bullet_color

        #在（0，0）处创建一个表示子弹的矩形，再设置正确的位置
        self.rect=pygame.Rect(0,0,self.settings.bullet_width,self.settings.bullet_height)
        self.rect.midtop=ai_game.ship.rect.midtop

        #存储用小数来表示子弹位置
        self.y=float(self.rect.y)

    def update(self):
        """
        向上移动子弹
        :return:
        """
        #更新表示子弹位置的小数值
        self.y-=self.settings.bullet_speed
        self.rect.y=self.y

    def draw_bullet(self):
        """
        绘制子弹在屏幕上
        :return:
        """
        pygame.draw.rect(self.screen,self.color,self.rect)



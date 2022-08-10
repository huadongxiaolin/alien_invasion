import pygame.font
from ship import Ship
from pygame.sprite import Group


class Scoreboard:
    """显示得分信息的类"""

    def __init__(self, ai_game):
        "初始化显示得分所涉及的属性"
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # 显示得分时所用字体
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont("SimHei", 32)  # 显示中文
        #作各种图
        self.prep_images()


    def prep_images(self):
        """初始化渲染，作图"""
        # 准备初始得分图像及最高得分
        self.prep_score()
        self.prep_high_score()
        # 显示当前等级
        self.prep_level()
        # 显示当前飞船
        self.prep_ships()

    def check_high_score(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_score(self):
        """将得分转化为一副渲染的图像"""
        # round 让小数精确到小数点的后一位
        # 小数位数由第二个实参控制，-1表示舍入到最近的10的倍数
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # 在屏幕右上角显示得分
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """将得分转化为一副渲染的图像"""
        # round 让小数精确到小数点的后一位
        # 小数位数由第二个实参控制，-1表示舍入到最近的10的倍数
        rounded_score = round(self.stats.high_score, -1)
        high_score_str = "最高:{:,}".format(rounded_score)
        self.score_high_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        # 在屏幕顶部中央
        self.score_high_rect = self.score_high_image.get_rect()
        self.score_high_rect.centerx = self.screen_rect.centerx  # 水平居中
        self.score_high_rect.top = self.score_high_rect.top

    def show_score(self):
        """在屏幕上显示得分,最高分，等级,飞船数"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.score_high_image, self.score_high_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def prep_level(self):
        """将等级转换为渲染的图像"""
        level_str = "le:"+str(self.stats.level)
        #重新调整字体大小
        self.font = pygame.font.SysFont("SimHei", 25)  # 显示中文
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)
        # 将等级放在得分下方
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """显示还剩下多少艘飞船"""
        self.ships=Group()
        for ship_number in range(self.stats.ships_left):
            ship=Ship(self.ai_game)
            ship.rect.x=5+ship_number*ship.rect.width
            ship.rect.y=self.screen_rect.top
            self.ships.add(ship)

# 12.3.3创建设置类
class Settings:
    """
    存储游戏中的谁有设置类
    """

    def __init__(self):
        """
        初始化游戏设置
        """
        # 设置屏幕
        self.screen_width = 1000
        self.screen_height = 600
        # 设置颜色
        self.bg_color = (240, 240, 255)

        #设置最大飞船量
        self.ship_limit=3

        # 设置子弹
        self.bullet_width = 3
        self.bullet_height = 5
        self.bullet_color = (60, 60, 60)
        # 设置最大存储子弹数
        self.bullets_allowed = 3

        #撞到边缘后的垂直速度
        self.alien_fleet_drop_speed=3

        #加快游戏节奏
        self.speedup_scale=1.1
        #分数的提高速度
        self.score_scale=1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而发生变化的设置"""
        #设置子弹速度
        self.bullet_speed = 1
        # 设置船速度
        self.ship_speed = 1
        # 设置外星人移动速度
        self.alien_speed = 0.5
        # 1右-1左
        self.alien_fleet_direction = 1
        #击杀一个外星人的得分
        self.alien_points=50

    def increase_speed(self):
        """提高速度设置和外星人分数"""
        #船，子弹，外星人
        self.ship_speed*=self.speedup_scale
        self.bullet_speed*=self.speedup_scale
        self.alien_speed*=self.speedup_scale
        #提高子弹量
        self.bullets_allowed+=1
        #单个外星人的得分
        self.alien_points=int(self.alien_points*self.score_scale)

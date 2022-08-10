import sys
import pygame  # 包含开发游戏需要的功能

from summer_day1.alien_invasion.settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from time import sleep
from game_stats import GameStats
from button import BUtton
from scoreboard import Scoreboard


class AlienInvasion:
    """
    掌握游戏资源和行为的类
    """

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        # 12.3.3创建设置类
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self._init_parameters()

    def _init_parameters(self):
        """引入其他各种"""
        # 引入飞船
        self.ship = Ship(self)
        # 创建存储子弹的编组
        self.bullets = pygame.sprite.Group()
        # 创建存储外星人的编组
        self.aliens = pygame.sprite.Group()
        self._creat_fleet()
        # 创建一个用于存储游戏统计信息的实例
        self.stats = GameStats(self)
        # 创建一个按钮
        self.play_button = BUtton(self, "Play")
        # 创建一个记分牌
        self.sb = Scoreboard(self)

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    # 将run_game中的代码重构为以下两个辅助方法
    def _check_events(self):
        """
        响应按键和鼠标事件
        :return:
        """
        # 监视键盘和鼠标事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._game_over()  # 用sys中工具退出
            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self.check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()  # 获取单击位置
                self._check_play_button(mouse_pos)

    # 监视键盘的按下事件
    def check_keydown_events(self, event):

        if event.key == pygame.K_RIGHT:
            # 向右一定飞船
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # 向左
            self.ship.moving_left = True
        elif event.key == pygame.K_DOWN:
            # 向下
            self.ship.moving_down=True
        elif event.key == pygame.K_UP:
            #向上
            self.ship.moving_up = True
            # self.ship.rect.y -= 1
        # 按q退出
        elif event.key == pygame.K_q:
            self._game_over()
        # 按空格发射子弹
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        # 按p开始游戏,游戏开始后按此无效
        elif event.key == pygame.K_p and not self.stats.game_active:
            self._start_game()
        elif event.key == pygame.K_ESCAPE:
            # 按esc全屏
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_rect().width
            self.settings.screen_height = self.screen.get_rect().height
            self.ship = Ship(self)
        #按q暂停
        elif event.key == pygame.K_s:
            if self.stats.game_active:
                self.stats.game_active = False
                pygame.mouse.set_visible(True)
                self.play_button._pre_msg("Continue")
            else:
                self.stats.game_active=True
                pygame.mouse.set_visible(False)


    # 监视键盘的松开事件
    def check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            # 向右一定飞船
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            # 向左
            self.ship.moving_left = False
        elif event.key == pygame.K_DOWN:
            # 向下
            self.ship.moving_down=False
        elif event.key == pygame.K_UP:
            #向上
            self.ship.moving_up = False

    def _check_play_button(self, mouse_pos):
        """在玩家单击play按钮开始新游戏"""
        # 检查鼠标单机位置是否在play按钮的rect内
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self._start_game()

    def _start_game(self):
        """游戏开始"""
        self.stats.reset_status()
        self.stats.game_active = True
        # 重置得分
        self.sb.prep_score()
        # 重置等级
        self.sb.prep_level()
        #重置初始飞船量
        self.sb.prep_ships()
        # 重置为初始速度
        self.settings.initialize_dynamic_settings()

        # 清空余下的外星人和子弹
        self.aliens.empty()
        self.bullets.empty()

        # 创建一群新的外星人并让飞船居中
        self._creat_fleet()
        self.ship.center_ship()
        # 隐藏光标
        pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        """
        创建一颗子弹，并将其加入编组bullets中
        :return:
        """
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        "更新子弹的位置并删除消失的子弹"
        "更新子弹的位置"
        self.bullets.update()
        # 删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # print(len(self.bullets))
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """响应子弹和外星人碰撞"""
        # 检查是否有子弹击中了外星人,
        # 如果是，则删除对应的外星人和子弹
        # True就消失
        # flase,true 则只有外星人消失
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )  # 进行比较，观察是否重叠
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)  # 一颗子弹可能击中多个
                self.sb.prep_score()  # 更新一下得分
                self.sb.check_high_score()  # 更新一下最高分

        self.start_new_level()


    def start_new_level(self):
        """在外星人群体消失干净后进入下一等级"""
        # 检查aliens是否为空
        if not self.aliens:
            self.bullets.empty()  # 清空所有子弹
            self._creat_fleet()
            self.settings.increase_speed()
            # 提高等级
            self.stats.level += 1
            self.sb.prep_level()

    def _creat_fleet(self):
        """创建外星人群"""
        # 先建个外星人看看x,y
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        available_space_x = self.settings.screen_width - (2 * alien_width)  # 减去俩边边距的可用空间
        number_aliens_x = available_space_x // (2 * alien_width)  # 计算一行有多少个外星人

        available_space_y = self.settings.screen_height - (3 * alien_height) - self.ship.rect.height  # 减去俩边边距的可用空间
        number_rows = available_space_y // (2 * alien_height)  # 计算可以容纳几行外星人
        # 创建第一行外星人
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._creat_alien(alien_number, row_number)

    def _creat_alien(self, alien_number, row_number):
        """创建一个外星人并放在当前行"""
        new_alien = Alien(self)
        alien_width, alien_height = new_alien.rect.size  # 获取个宽度,高度
        new_alien.x = alien_width + 2 * alien_width * alien_number
        new_alien.y = alien_height + 2 * alien_height * row_number
        new_alien.rect.x = new_alien.x  # 更新rect对象
        new_alien.rect.y = new_alien.y  # 更新rect对象
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """有外星人达到边缘时采取相应的措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """将整体下移，并改变方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.alien_fleet_drop_speed
        self.settings.alien_fleet_direction *= -1

    def _update_aliens(self):
        """检查有木有外星人到边缘，并更新位置"""
        self._check_fleet_edges()
        self.aliens.update()
        # 检查外星人和飞船的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # 检查是否有外星人到达了底部
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """检查是否有外星人到达了底部"""
        screen_rent = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rent.bottom:
                # 像飞船碰到一样处理
                self._ship_hit()
                break

    def _ship_hit(self):
        """响应飞船被外星人撞到"""
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            #更新剩余飞船数
            self.sb.prep_ships()
            # 清空剩下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            # 创建一群新的外星人
            self._creat_fleet()

            self.ship.center_ship()
            # 暂停一下
            sleep(0.5)
        else:
            self.stats.game_active = False
            self.play_button._pre_msg("Play")
            # 显示鼠标光标
            pygame.mouse.set_visible(True)
            # print("game over")


    def _update_screen(self):
        """
        更新屏幕上的图像，并切换到新的屏幕
        """
        # 每次循环重绘
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.sb.show_score()

        # 如果游戏处于非活动状态，则绘制play按钮
        if not self.stats.game_active:
            self.play_button.draw_button()

        # 让最近绘制的屏幕可见
        pygame.display.flip()

    def _game_over(self):
        with open('high_score.txt','w') as f:
            high_score=str(self.stats.high_score)
            f.write(high_score)
        sys.exit()


if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()

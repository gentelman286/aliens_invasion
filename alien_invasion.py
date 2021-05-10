import pygame

from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
import game_functions as gf     # 出于简化考虑，起个别名

from pygame.sprite import Group     # 编组（group）用于存储所有有效的子弹，
# 类似于列表，但提供了有助于开发游戏的额外功能


def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()  # 创建一个settings实例
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))  # 显示窗口的尺寸

    pygame.display.set_caption("Alien Invasion")  # 设置屏幕标题

    # 创建一个play按钮
    play_button = Button(ai_settings, screen, "Play")

    # 创建一个用于存储游戏统计信息的实例,并创建记分牌
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # 创建一艘飞船
    ship = Ship(ai_settings, screen)

    # 创建外星人编组
    aliens = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # 创建一个用于存储子弹的编组
    bullets = Group()

    # 开始游戏的主循环
    while True:
        # 监视键盘和鼠标事件
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship,
                        aliens, bullets)   # 检查时会修改标志位，
        # 标志位影响到update方法的运行

        if stats.game_active:
            ship.update()   # 飞船位置将在检测到键盘事件后更新，从而确保更新后的位置绘制到屏幕上
            # 子弹更新
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens,
                              bullets)
            # 外星人更新
            gf.update_aliens(ai_settings, screen, stats, sb,  ship, aliens,
                             bullets)

        # 更新屏幕
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                         play_button)


run_game()

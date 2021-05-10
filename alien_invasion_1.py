import sys

import pygame


def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))   # 显示窗口的尺寸
    pygame.display.set_caption("Alien Invasion")      # 设置屏幕标题

    # 系统默认创建一个黑色屏幕，我们可以设置背景颜色
    bg_color = (230, 230, 230)      # 创建一个背景色并存储在bg_color，颜色由RGB值指定，0~255，分别是红绿蓝的量

    # 开始游戏的主循环
    while True:
        # 监视键盘和鼠标事件
        for event in pygame.event.get():        # 检测事件
            if event.type == pygame.QUIT:       # 判断事件类型
                sys.exit()

        # 每次循环时都重绘屏幕
        screen.fill(bg_color)       # 用创建的背景色填充,该方法只接受一个实参即一个颜色

        # 让最近绘制的屏幕可见
        pygame.display.flip()       # 每次循环都更新屏幕，擦去旧的，可见新的


run_game()

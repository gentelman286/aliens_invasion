import pygame
from pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self, ai_settings, screen):     # screen参数指定飞船绘制地方
        """初始化飞船并设置其初始值"""
        super(Ship, self).__init__()
        self.screen = screen

        self.ai_settings = ai_settings

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/spacecraft.bmp')     # 返回
        # 一个飞船的surface

        self.rect = self.image.get_rect()       # 获取相应surface的属性rect
        # 类似于处理一个矩形即rect对象

        self.screen_rect = screen.get_rect()

        # 将每艘新飞船放在屏幕底部中央(在属性中存储小数)
        self.center = float(self.screen_rect.centerx)    # 先将元素居中（边缘对齐：top,bottom,left,right）
        # 水平或垂直：x,y

        self.rect.bottom = self.screen_rect.bottom      # 再将元素置底部

        # 移动标志
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """"根据移动标志调整飞船的位置"""
        # 更新飞船的certer值，而不是rect
        if self.moving_right and self.rect.right < self.screen_rect.right:  # 如果满足条件则说明未触及屏幕右边缘
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:     # 左边缘坐标大于零就说明未触及屏幕左边缘
            self.center -= self.ai_settings.ship_speed_factor

        # 根据self.center更新rect对象
        self.rect.centerx = self.center

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """让飞船在屏幕上居中"""
        self.center = self.screen_rect.centerx



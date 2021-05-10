import pygame.font      # 可以让Pygame能够将文本渲染到屏幕上


class Button():

    def __init__(self, ai_settings, screen, msg):       # msg是要在按钮中显示的文本
        """初始化按钮的属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # 设置按钮的尺寸和其他属性值
        self.width, self.heigth = 200, 50
        self.button_color = (0, 255, 0)     # 让按钮的rect对象为亮绿色
        self.text_color = (255, 255, 255)   # 让文本为白色
        self.font = pygame.font.SysFont(None, 48)   # 指定使用的字体，none让pygame
        # 使用默认字体，48指定文本字号

        # 创建按钮的rect对象，并使其居中
        self.rect = pygame.Rect(0, 0, self.width, self.heigth)
        self.rect.center = self.screen_rect.center

        # 按钮的标签只需创建一次
        self.prep_msg(msg)      # 调用方法将想要显示的字符串渲染为图像来处理文本

    def prep_msg(self, msg):
        """将msg渲染为图像，并使其在按钮上居中"""
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        # 调用font.render()将存储在msg中的文本转换为图像，然后将图像存储在msg_image中。
        # 布尔参数指定是否开启反锯齿功能（反锯齿让文本的边缘更平滑），文本颜色，背景色

        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # 绘制一个用颜色填充的按钮，在绘制文本
        self.screen.fill(self.button_color, self.rect)  # 绘制按钮矩形
        self.screen.blit(self.msg_image, self.msg_image_rect)   # 传递一幅图像以及
        # 与该图像相关联的rect对象


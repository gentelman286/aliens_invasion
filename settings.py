class Settings:
    """存储《外星人入侵》的所有设置的类"""

    def __init__(self):
        """初始化游戏的设置"""
        # 屏幕初始化设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)         # 系统默认创建一个黑色屏幕，我们可以设置背景颜色
        # 创建一个背景色并存储在bg_color
        # 颜色由RGB值指定，0~255，分别是红绿蓝的量

        # 子弹设置
        """创建一个宽3像素，高15像素的深灰色子弹"""

        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullet_allowed = 3     # 未消失的最大子弹数

        # 外星人设置

        self.fleet_drop_speed = 10
        self.ship_limit = 3

        # 以什么样的速度加快游戏节奏
        self.speedup_scale = 1.1

        # 外星人点数提高速度
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        # 飞船设置
        self.ship_speed_factor = 1.5  # 决定飞船在每次循环时最多移动多少距离,这样
        # 只要该速度属性值大于1，飞船移动速度就会比以前快，有助于提升反应速度，还可以方便调整游戏节奏

        self.bullet_speed_factor = 3
        self.alien_speed_factor = 0.5
        self.fleet_direction = 1      # fleet_direction为1 表示向右移动，为-1表示向左移动

        # 记分
        self.alien_points = 50      # 每击落一个外星人将得到多少个点

    def increase_speed(self):
        """提高速度设置"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)

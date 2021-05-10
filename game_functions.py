"""存储大量让游戏运行的函数"""
import sys

from time import sleep
import pygame
from bullet import Bullet
from alien import Alien


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def fire_bullet(ai_settings, screen, ship, bullets):
    """如果还没有达到限制，就发射一颗子弹"""
    # 创建一颗子弹，并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullet_allowed:  # 创建新子弹前检查未消失的子弹数是否小于该设置
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    """响应按键松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
                 bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:  # 按下
            check_keydown_events(event, ai_settings, screen, ship, bullets)
            # 按键响应
        elif event.type == pygame.KEYUP:    # 抬起
            check_keyup_events(event, ship)  # 抬起响应
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()   # 返回一个元组，包含玩家单击
            # 时鼠标的x和y坐标
            check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                              aliens, bullets,  mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens,
                      bullets, mouse_x, mouse_y):
    """在玩家单击play时开始新游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    # 使用collidepoint检查鼠标单击位置是否在play按钮的rect内

    if button_clicked and not stats.game_active:
        # 重置游戏设置
        ai_settings.initialize_dynamic_settings()

        # 隐藏光标
        pygame.mouse.set_visible(False)     # 让pygame在光标位于游戏窗口内时将其隐藏起来

        # 重置游戏统计信息
        stats.reset_stats()
        stats.game_active =True

        # 重置计分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并让飞船居中
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """需要三个参数，设置实例，屏幕，飞船"""
    """更新屏幕上的图像，并切换到新屏幕"""
    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)  # 用创建的背景色填充,该方法只接受一个实参即一个颜色

    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():        # 方法sprites返回一个列表，其中包含编组中的所有精灵
        bullet.draw_bullet()

    ship.blitme()  # 绘制飞船到屏幕上，确保会出现在背景前面
    aliens.draw(screen)  # 绘制外星人编组中的每个外星人到屏幕上

    # 显示得分
    sb.show_score()

    # 如果游戏处于非活动状态，就显示play按钮
    if not stats.game_active:
        play_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()  # 每次循环都更新屏幕，擦去旧的，可见新的


def update_bullets(ai_settings, screen, stats, sb,  ship, aliens, bullets):
    """更新子弹位置，并删除已消失的子弹"""
    # 更新子弹位置
    bullets.update()  # 更新绘制子弹，对编组调用update，编组会自动对其中每个精灵都调用update

    # 删除已消失的子弹
    for bullet in bullets.copy():  # 循环中不应从列表或编组中删除条目，因此必须遍历编组的副本
        if bullet.rect.bottom <= 0:  # 表明子弹已穿过屏幕顶端
            bullets.remove(bullet)

    check_bullet_alien_collision(ai_settings, screen, stats, sb, ship, aliens,
                                 bullets)


def check_bullet_alien_collision(ai_settings, screen, stats, sb, ship, aliens,
                                 bullets):
    # 检测是否有子弹击中外星人
    # 如果发生碰撞就删除相应子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    # 该方法将每颗子弹的rect同每个外星人的rect进行比较，并返回一个字典，其中包含发生碰撞的子弹和外星人，两个实参true
    # 告诉pygame删除发生碰撞分子弹和外星人

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)    # 遍历列表中
            # 的外星人，对于每个列表，都将一个外星人的点数乘以其中包含的外星人数量，并将结果
            # 加入到当前得分中
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        #  删除现有的子弹并新建一群外星人
        bullets.empty()
        ai_settings.increase_speed()    # 加快游戏节奏

        # 提高等级
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)


def get_number_aliens_x(ai_settings, alien_width):
    """计算每行可容纳多少个外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width  # 放置外星人的
    # 宽度和高度
    number_aliens_x = int(available_space_x / (2 * alien_width))  # 可容纳外星人数目
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height - (3*alien_height) -
                         ship_height)
    number_rows = int(available_space_y / (2*alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    # 创建一个外星人并将其加入当前行
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2*alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)

    # 创建外星人群
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def change_fleet_direction(ai_settings, aliens):
    """将整群外星人下移，并改变它们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """响应被外星人撞到的飞船"""
    # 将ship_left减一
    stats.ships_left -= 1

    # 清空外星人列表和子弹列表
    aliens.empty()
    bullets.empty()

    # 创建一群新的外星人，并将飞船放到屏幕底端中央
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()      # 将飞船居中

    # 暂停
    sleep(0.5)  # 模块time中导入函数sleep，以便使用它来让游戏暂停


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """响应被外星人撞到的飞船"""
    if stats.ships_left > 0:
        # 将ship_left减1
        stats.ships_left -= 1

        # 更新记分牌
        sb.prep_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)  # 进入非活动状态立即让光标可见

    # 暂停
    sleep(0.5)


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """检查是否有外星人位于屏幕边缘，并更新外星人群中所有外星人的位置"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    """检测外星人和飞船之间的碰撞"""
    if pygame.sprite.spritecollideany(ship, aliens):    # 该方法接收两个实参，一个精灵和一个编组。
        # 检查编组是否有成员与精灵发生碰撞，并在找到与精灵发生了碰撞的成员后就停止遍历编组。
        # 如果没有发生碰撞就返回none，如果找到了就返回这个外星人
        # print("Ship hit!!!")
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    # 检查是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """检查是否有外星人到达屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞到一样进行处理
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break


def check_high_score(stats, sb):
    """检查是否诞生了新的最高得分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

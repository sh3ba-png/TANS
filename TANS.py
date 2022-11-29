import random
import venue
import pygame
from castle import Castle
from mob import Mob
from bullet import Bullet
pygame.mixer.pre_init(44100, -16, 3, 512)

pygame.init()

STEP = 2  # шаг/скорость
WIDTH = 1000  # ширина окна х
HEIGHT = 700  # высота окна у
INDENT = 120  # отступ от края
BULLET_SPEED = 8  # > 2
MOB_SPEED = 2

cell_width = (WIDTH - 2 * INDENT) / 3  # ширина клетки
cell_height = (HEIGHT - 2 * INDENT) / 3  # высота клетки
sc = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)  # окно
pygame.display.set_caption("TANS")  # название окна
pygame.display.set_icon(pygame.image.load("icon.bmp"))  # иконка окна

img_m1_1 = pygame.image.load('monster1.1.png')
img_m1_2 = pygame.image.load('monster1.2.png')
img_m2_1 = pygame.image.load('monster2.1.png')
img_m2_2 = pygame.image.load('monster2.2.png')
img_c1_1 = pygame.image.load('castle1.1.png')
img_c1_2 = pygame.image.load('castle1.2.png')
img_c2_1 = pygame.image.load('castle2.1.png')
img_c2_2 = pygame.image.load('castle2.2.png')
heart = pygame.image.load('heart.png')

HIT_SOUND = pygame.mixer.Sound('hit.wav')
MONEY_SOUND = pygame.mixer.Sound('money.wav')
HP_SOUND = pygame.mixer.Sound('hp.wav')
WIN_SOUND = pygame.mixer.Sound('win.wav')
LOSS_SOUND = pygame.mixer.Sound('loss.wav')

MONEY_SOUND.set_volume(0.5)
WIN_SOUND.set_volume(0.5)
LOSS_SOUND.set_volume(0.1)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
WHITE_BLUE = (73, 156, 222)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (185, 165, 237)
FPS = 60
clock = pygame.time.Clock()


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# создание массива шагов для моба
def create_mas_position(point):
    point.x += INDENT - 60
    point.y -= INDENT - 60
    mas_coordinate = []
    mas_for_venue.append(Point(point.x, point.y))
    while point.y != INDENT - 50:
        mas_coordinate.append(Point(point.x, point.y))
        point.y -= STEP
    mas_for_venue.append(Point(point.x, point.y))
    while point.x != WIDTH - INDENT + 60:
        mas_coordinate.append(Point(point.x, point.y))
        point.x += STEP
    mas_for_venue.append(Point(point.x, point.y))
    while point.y <= HEIGHT - INDENT:
        mas_coordinate.append(Point(point.x, point.y))
        point.y += STEP
    mas_for_venue.append(Point(point.x, point.y))
    return mas_coordinate


# возвращает центральную координату клетки
def return_centre_rect(position):
    if INDENT < position.x < INDENT + cell_width:
        if INDENT < position.y < INDENT + cell_height:
            return Point((INDENT + INDENT + cell_width) / 2, (INDENT + INDENT + cell_height) / 2)
        if INDENT + cell_height < position.y < INDENT + 2 * cell_height:
            return Point((INDENT + INDENT + cell_width) / 2, (INDENT + cell_height + INDENT + 2 * cell_height) / 2)
        if INDENT + 2 * cell_height < position.y < INDENT + 3 * cell_height:
            return Point((INDENT + INDENT + cell_width) / 2, (INDENT + 2 * cell_height + INDENT + 3 * cell_height) / 2)
    if INDENT + cell_width < position.x < INDENT + 2 * cell_width:
        if INDENT < position.y < INDENT + cell_height:
            return Point((INDENT + cell_width + INDENT + 2 * cell_width) / 2, (INDENT + INDENT + cell_height) / 2)
        if INDENT + cell_height < position.y < INDENT + 2 * cell_height:
            return Point((INDENT + cell_width + INDENT + 2 * cell_width) / 2,
                         (INDENT + cell_height + INDENT + 2 * cell_height) / 2)
        if INDENT + 2 * cell_height < position.y < INDENT + 3 * cell_height:
            return Point((INDENT + cell_width + INDENT + 2 * cell_width) / 2,
                         (INDENT + 2 * cell_height + INDENT + 3 * cell_height) / 2)
    if INDENT + 2 * cell_width < position.x < INDENT + 3 * cell_width:
        if INDENT < position.y < INDENT + cell_height:
            return Point((INDENT + 2 * cell_width + INDENT + 3 * cell_width) / 2, (INDENT + INDENT + cell_height) / 2)
        if INDENT + cell_height < position.y < INDENT + 2 * cell_height:
            return Point((INDENT + 2 * cell_width + INDENT + 3 * cell_width) / 2,
                         (INDENT + cell_height + INDENT + 2 * cell_height) / 2)
        if INDENT + 2 * cell_height < position.y < INDENT + 3 * cell_height:
            return Point((INDENT + 2 * cell_width + INDENT + 3 * cell_width) / 2,
                         (INDENT + 2 * cell_height + INDENT + 3 * cell_height) / 2)
    return None


# рисуем сетку
def draw_line():
    pygame.draw.line(sc, BLUE, (INDENT, HEIGHT - INDENT), (INDENT, INDENT), 5)
    pygame.draw.line(sc, BLUE, (INDENT, INDENT), (WIDTH - INDENT, INDENT), 5)
    pygame.draw.line(sc, BLUE, (WIDTH - INDENT, INDENT), (WIDTH - INDENT, HEIGHT - INDENT), 5)

    pygame.draw.line(sc, BLUE, (INDENT, HEIGHT - cell_height - INDENT), (WIDTH - INDENT, HEIGHT - cell_height - INDENT),
                     5)
    pygame.draw.line(sc, BLUE, (INDENT, HEIGHT - 2 * cell_height - INDENT), (WIDTH - INDENT, HEIGHT - 2 * cell_height -
                                                                             INDENT), 5)
    pygame.draw.line(sc, BLUE, (INDENT + cell_width, INDENT), (INDENT + cell_width, HEIGHT - INDENT), 5)
    pygame.draw.line(sc, BLUE, (INDENT + 2 * cell_width, INDENT), (INDENT + 2 * cell_width, HEIGHT - INDENT), 5)
    pygame.draw.line(sc, BLUE, (INDENT, HEIGHT - INDENT), (WIDTH - INDENT, HEIGHT - INDENT), 5)


# выводим информацию (количество денег, хп)
def draw_info():
    font = pygame.font.SysFont(None, 50)
    img1 = font.render("Quantity money: " + str(money), True, pygame.Color(178, 222, 100))
    sc.blit(img1, (WIDTH / 2, HEIGHT - INDENT + 50))
    for i in range(HP):
        img = heart
        img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
        rect = img.get_rect()
        rect.center = INDENT * 2 + i * 50, HEIGHT - INDENT + 60
        sc.blit(img, rect)


# рисуем башни
def draw_castle(castle):
    rect = castle.img.get_rect()  # получить середину картинки
    rect.center = castle.position.x, castle.position.y  # устанавливаем середину картинки в середину клетки
    sc.blit(castle.img, rect)  # рисуем героя

    f1 = pygame.font.Font(None, 30)
    text1 = f1.render(str(castle.lvl), True, (193, 83, 208))
    sc.blit(text1, (castle.position.x - 10, castle.position.y - 60))


# рисуем мобов
def draw_mob(mob):
    if TICK % 30 < 15:
        img = mob.picture1
    else:
        img = mob.picture2
    if mob.get_currant_position().y <= HEIGHT - INDENT and mob.get_currant_position().x >= WIDTH - INDENT + 60:
        img = pygame.transform.flip(img, True, False)
    img.convert()
    rect = img.get_rect()
    rect.center = mob.get_currant_position().x, mob.get_currant_position().y
    sc.blit(img, rect)

    f1 = pygame.font.Font(None, 25)
    text1 = f1.render(str(mob.hp), True, (180, 0, 0))
    sc.blit(text1, (mob.get_currant_position().x - 10, mob.get_currant_position().y - 60))


# рисуем пули
def draw_bullet(bullet):
    if bullet.castle.type == 0:
        pygame.draw.circle(sc, PURPLE, (bullet.cur_pos.x, bullet.cur_pos.y), 9)
    else:
        pygame.draw.circle(sc, WHITE_BLUE, (bullet.cur_pos.x, bullet.cur_pos.y), 9)


# наносим урон мобу
def fight(mob, damage):
    if mob.hp > 0:
        mob.get_damage(damage)


TICK = 0
HP = 3
point = Point(0, HEIGHT)
money = 400
mas_for_venue = []  # массив для места встречи пули и моба
mas_coordinate_mobs = create_mas_position(point)
bullets = []  # массив пуль
mobs = []  # массив мобов
castles = []  # массив башен
positions_castles = []  # позиции башен
flag = True
mob_index = 0
while flag:
    TICK += 1
    sc.fill(BLACK)

    if TICK % 80 == 0:
        rand = random.randint(0, 1)
        if rand == 0:
            mob = Mob(mas_coordinate_mobs, 0, TICK)
            mob_index += 1
            mob.id = mob_index
            mob.set_hp()
            mob.picture1 = pygame.transform.scale(img_m1_1, (img_m1_1.get_width() * 5, img_m1_1.get_height() * 5))
            mob.picture2 = pygame.transform.scale(img_m1_2, (img_m1_2.get_width() * 5, img_m1_2.get_height() * 5))
        if rand == 1:
            mob = Mob(mas_coordinate_mobs, 1, TICK)
            mob_index += 1
            mob.id = mob_index
            mob.set_hp()
            mob.picture1 = pygame.transform.scale(img_m2_1, (img_m2_1.get_width() * 3, img_m2_1.get_height() * 3))
            mob.picture2 = pygame.transform.scale(img_m2_2, (img_m2_2.get_width() * 3, img_m2_2.get_height() * 3))
        mobs.append(mob)

    i = 0
    while i < len(mobs):
        draw_mob(mobs[i])
        mobs[i].next_position()
        if mobs[i].get_currant_position() == mobs[i].mas_coordinate[-1]:
            HP_SOUND.play()
            mobs[i].hp = 0
            mobs[i].hp_mn = 0
            mobs.pop(i)
            i -= 1
            HP -= 1
            print("HP:", HP)
            if HP < 1:
                print("Game over!")
        i += 1

    for i in range(len(castles)):
        draw_castle(castles[i])
        if TICK % 30 == 0:
            j = 0
            while j < len(mobs) and mobs[j].hp_mn <= 0:
                j += 1
            while j < len(mobs):
                tryst, time = venue.core(castles[i].position,
                                         Point(mobs[j].get_currant_position().x, mobs[j].get_currant_position().y),
                                         MOB_SPEED, BULLET_SPEED,
                                         mas_for_venue[0], mas_for_venue[1], mas_for_venue[2], mas_for_venue[3])
                if mobs[j].will_hp_at_tick(TICK + time, castles[i].damage):
                    bullet = Bullet(Point(castles[i].position.x, castles[i].position.y), tryst, castles[i].damage,
                                    mobs[j], castles[i], BULLET_SPEED, INDENT, WIDTH)
                    castles[i].img = castles[i].picture2
                    # разворачиваем башню в сторону моба
                    if mobs[j].get_currant_position().y <= HEIGHT - INDENT and mobs[j].get_currant_position().x >= \
                            WIDTH - INDENT + 60:
                        castles[i].img = pygame.transform.flip(castles[i].img, True, False)
                        castles[i].img.convert()
                    mobs[j].hp_mn -= castles[i].damage
                    bullets.append(bullet)
                    mobs[j].damages.append((castles[i].damage, TICK + time))
                    break
                else:
                    j += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if (INDENT < event.pos[0] < WIDTH - INDENT) and (INDENT < event.pos[1] < HEIGHT - INDENT):
                    position = return_centre_rect(Point(event.pos[0], event.pos[1]))  # находим середину нажатой клетки
                    # если здесь еще никто не стоит
                    if (position.x, position.y) not in positions_castles and money >= 50:
                        money -= 50
                        castle = Castle(position, random.randint(1, 2), random.randint(10, 50))
                        positions_castles.append((position.x, position.y))
                        if castle.type == 1:
                            castle.picture1 = pygame.transform.scale(img_c1_1, (
                                img_c1_1.get_width() * 5, img_c1_1.get_height() * 5))
                            castle.picture2 = pygame.transform.scale(img_c1_2, (
                                img_c1_2.get_width() * 5, img_c1_2.get_height() * 5))
                            castle.damage = castle.lvl * 5 + castle.type * 10
                        if castle.type == 2:
                            castle.picture1 = pygame.transform.scale(img_c2_1, (
                                img_c2_1.get_width() * 4, img_c2_1.get_height() * 4))
                            castle.picture2 = pygame.transform.scale(img_c2_2, (
                                img_c2_2.get_width() * 4, img_c2_2.get_height() * 4))
                            castle.damage = castle.lvl * 5 + castle.type * 10
                        castle.img = castle.picture1
                        castles.append(castle)
                    # если здесь уже кто-то стоит => увеличиваем уровень башни
                    else:
                        if money >= 100:
                            for i in range(len(castles)):
                                if castles[i].position.x == position.x and castles[i].position.y == position.y:
                                    castles[i].lvl += 1
                                    castles[i].damage = castles[i].lvl * 5 + castles[i].type * 10
                                    money -= 100
    draw_line()
    draw_info()

    k = 0
    while k < len(bullets):
        draw_bullet(bullets[k])
        if bullets[k].new_step() == 0:
            fight(bullets[k].mob, bullets[k].damage)
            HIT_SOUND.play()
            if bullets[k].mob.hp <= 0 and bullets[k].mob.get_currant_position() != bullets[k].mob.mas_coordinate[-1]:
                money += 20
                MONEY_SOUND.play()
                if bullets[k].mob in mobs:
                    mobs.pop(mobs.index(bullets[k].mob))
            bullets[k].castle.img = bullets[k].castle.picture1
            if bullets[k].mob.get_currant_position().y <= HEIGHT - INDENT and \
                    bullets[k].mob.get_currant_position().x >= WIDTH - INDENT + 60:
                bullets[k].castle.img = pygame.transform.flip(bullets[k].castle.img, True, False)
            bullets.pop(k)
            k -= 1
        k += 1

    if HP > 0:
        pygame.display.update()
    if money >= 500:
        flag = False
        WIN_SOUND.play()
    if HP <= 0:
        flag = False
        LOSS_SOUND.play()
    clock.tick(FPS)

while True:
    sc.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    if HP > 0:
        font = pygame.font.SysFont(None, WIDTH // 7)
        img1 = font.render('YOU WIN!', True, pygame.Color(185, 165, 237))
        sc.blit(img1, (WIDTH / 4, HEIGHT / 2 - WIDTH // 14))
    else:
        font = pygame.font.SysFont(None, WIDTH // 7)
        img1 = font.render('GAME OVER', True, pygame.Color(185, 165, 237))
        sc.blit(img1, (WIDTH / 5, HEIGHT / 2 - WIDTH // 14))
    pygame.display.update()


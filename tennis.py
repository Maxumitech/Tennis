import time
import pygame as pg
import random
import pygame_menu

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60

pg.init()
screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pg.display.set_caption('Tennis')

current_difficulty = 5


class LeftPlaswyer:
    def __init__(self):
        self.img = pg.image.load('img/rect.png')
        self.sprite = pg.transform.scale(self.img, (30, 100))
        self.hitbox = self.sprite.get_rect()
        self.hitbox.y = 250
        #Функция, которая описывает левый прямоугольник

    def draw(self):
        screen.blit(self.sprite, self.hitbox)
        # Функция, которая рисует левый прямоугольник

    def move(self):
        keys = pg.key.get_pressed()
        # Обработка нажатий клавиш
        if keys[pg.K_w] and self.hitbox.y > 0:
            self.hitbox.y -= 12
        if keys[pg.K_s] and self.hitbox.y < 500:
            self.hitbox.y += 12


class RightPlayer:
    def __init__(self):
        self.img = pg.image.load('img/rect.png')
        self.sprite = pg.transform.scale(self.img, (30, 100))
        self.hitbox = self.sprite.get_rect()
        self.hitbox.y = 250
        self.hitbox.x = 770
        # Функция, которая описывает правый прямоугольник

    def draw(self):
        screen.blit(self.sprite, self.hitbox)
        # Функция, которая рисует правый прямоугольник

    def move(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            if self.hitbox.y > 0:
                self.hitbox.y -= 12
        if keys[pg.K_DOWN]:
            if self.hitbox.y < 500:
                self.hitbox.y += 12


class Ball:
    def __init__(self):
        self.sprite = pg.image.load('img/bol.png')
        self.hitbox = self.sprite.get_rect()
        self.hitbox.x = 380
        self.hitbox.y = 280
        # Функция, которая описывает шарик

    def draw(self):
        screen.blit(self.sprite, self.hitbox)
        # Функция, которая рисует шарик

    def move(self, direction, step):
        # Direction - это переменная в которую будет записываться
        # направление шара, например case 1 - это в правый верхний угол.
        # Step - это скорость шара
        match direction:
            case 1:
                self.hitbox.x = self.hitbox.x - step
                self.hitbox.y = self.hitbox.y - step
            case 2:
                self.hitbox.x = self.hitbox.x + step
                self.hitbox.y = self.hitbox.y - step
            case 3:
                self.hitbox.x = self.hitbox.x + step
                self.hitbox.y = self.hitbox.y + step
            case 4:
                self.hitbox.x = self.hitbox.x - step
                self.hitbox.y = self.hitbox.y + step


def draw_score(scorel, scorer):
    # Функция, которая считывает очки
    font = pg.font.get_default_font()
    font = pg.font.Font(font, 48)
    render = font.render(str(scorel) + '   ' + str(scorer), 1, 'green')
    render_hitbox = render.get_rect(topleft=(360, 0))
    screen.blit(render, render_hitbox)


def main():
    leftp = LeftPlayer()
    rightp = RightPlayer()
    bolp = Ball()
    scorel = 0
    scorer = 0
    bg = pg.image.load('img/background.jpg')
    bg = pg.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.mixer.set_num_channels(4)
    pg.mixer.music.load('sound/pin.mp3')
    pg.mixer.music.load('sound/pong.mp3')
    pg.mixer.music.load('sound/bgmusic.mp3')
    pg.mixer.Channel(2).play(pg.mixer.Sound('sound/bgmusic.mp3'), loops=-1)
    pg.mixer.Channel(2).set_volume(0.05)
    pg.mixer.music.load('sound/winsound.mp3')
    direction = random.randint(1, 4)
    gh = True
    clock = pg.time.Clock()
    step = current_difficulty
    while True:
        # 1
        for i in pg.event.get():
            if i.type == pg.QUIT:
                return
        # 2
        leftp.move()
        rightp.move()
        if bolp.hitbox.top == 0: #bolp.hitbox.top - это верхний угол шарика\
            # \по оси y. 0 - это верхняя стенка
            if direction == 2:
                direction = 3
            if direction == 1:
                direction = 4
        if bolp.hitbox.bottom == 600: #bolp.hitbox.bottom - это нижний угол шарика\
            # \по оси y. 600 - это нижняя стенка
            if direction == 3:
                direction = 2
            if direction == 4:
                direction = 1
        if rightp.hitbox.y < bolp.hitbox.y + 20 < rightp.hitbox.y + 100 and \
                rightp.hitbox.x == bolp.hitbox.right:
            pg.mixer.Channel(0).play(pg.mixer.Sound('sound/pin.mp3'))
            if direction == 2:
                direction = 1
            if direction == 3:
                direction = 4
        if leftp.hitbox.y < bolp.hitbox.y + 20 < leftp.hitbox.y + 100 and \
                leftp.hitbox.x + 30 == bolp.hitbox.left:
            pg.mixer.Channel(1).play(pg.mixer.Sound('sound/pong.mp3'))
            if direction == 1:
                direction = 2
            if direction == 4:
                direction = 3
        if bolp.hitbox.x > 800:# Условие
            scorel += 1
            bolp.hitbox.x = 380
            bolp.hitbox.y = 280
            direction = random.randint(1, 4)
            time.sleep(1)
        if bolp.hitbox.x < -40:# Условие
            scorer += 1
            bolp.hitbox.x = 380
            bolp.hitbox.y = 280
            direction = random.randint(1, 4)
            time.sleep(1)
        bolp.move(direction, step)
        # 3
        screen.blit(bg, (0, 0))
        leftp.draw()
        rightp.draw()
        bolp.draw()
        draw_score(scorel, scorer)
        if scorel == 5:
            if gh:
                pg.mixer.Channel(3).play(pg.mixer.Sound('sound/winsound.mp3'))
                gh = False
            show_end_screen(scorel, scorer)
            time.sleep(2)
        if scorer == 5:
            if gh:
                pg.mixer.Channel(3).play(pg.mixer.Sound('sound/winsound.mp3'))
                gh = False
            show_end_screen(scorel, scorer)
            time.sleep(2)
        pg.display.update()
        pg.time.delay(1000 // FPS)


def show_end_screen(scorel, scorer):
    # Кнопки и надписи
    end_menu = pygame_menu.Menu('Игра окончена', 800, 600,
                                theme=pygame_menu.themes.THEME_SOLARIZED)
    end_menu.add.label(f'Счёт: {scorel}  {scorer}', font_size=30)#Счёт
    end_menu.add.button('Заново', show_start_screen)#На начальный экран
    end_menu.add.button('Выйти', pygame_menu.events.EXIT)
    end_menu.mainloop(screen)# Зафиксировать экран


def show_start_screen():
    menu = pygame_menu.Menu('Tennis', 800, 600, theme=pygame_menu.themes.THEME_SOLARIZED)
    # Кнопки и надписи
    menu.add.label('Чтобы управлять нажимайте:')
    menu.add.label('1 игрок w, s')
    menu.add.label('2 игрок /\, \/')
    menu.add.button('Начать', main)
    menu.add.button('Выйти', pygame_menu.events.EXIT)
    menu.add.button('Сложность', show_complexity)
    menu.mainloop(screen)# Зафиксировать экран


def show_complexity():
    menu = pygame_menu.Menu('Выбор сложности', 800, 600, theme=pygame_menu.themes.THEME_SOLARIZED)
    menu.add.selector('Сложность', [('Легко', 1), ('Нормально', 2), ('Сложно', 3)],
                      onchange=set_difficulty)# Кнопки
    menu.add.button('Назад', show_start_screen)# Обратно на начальный экран
    menu.mainloop(screen)# Зафиксировать экран


def set_difficulty(value, difficulty):
    # Функция, которая меняет скорость шарика
    speed = 5
    if difficulty == 1:
        speed = 5
    if difficulty == 2:
        speed = 7
    if difficulty == 3:
        speed = 10
    global current_difficulty
    current_difficulty = speed


if __name__ == '__main__':
    show_start_screen()

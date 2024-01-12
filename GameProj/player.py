from rogue_player import RoguePlayer
from graphics import KEY_UP, KEY_DOWN, KEY_LEFT, KEY_SPACE, KEY_RIGHT, KEY_1, KEY_Q
import graphics as gr
from sprite import Sprite

class Player(RoguePlayer):
    speed_x = 2
    speed_y = 2
    attack = False
    death_e = False
    s_frame = Sprite("spell_frame.png", 1070, 10, 120, 120)

    def __init__(self, world, sprite, key_pressed, pos_x, pos_y, target):
        """
        Инициализация объекта игрока.

        :param sprite: Спрайт игрока.
        :param key_pressed: Функция для проверки, какие клавиши нажаты.
        """
        super().__init__(world, sprite, 14, 23, pos_x, pos_y)
        self.key_pressed = key_pressed
        self.target = target


    def update(self):
        """
        Обновление состояния игрока.

        """
        if (self.attack):
            if self.key_pressed(KEY_UP):
                self.velocity_y = -self.speed_y
            elif self.key_pressed(KEY_DOWN):
                self.velocity_y = self.speed_y
            else:
                self.velocity_y = 0

            if self.key_pressed(KEY_LEFT):
                self.velocity_x = -self.speed_x
            elif self.key_pressed(KEY_RIGHT):
                self.velocity_x = self.speed_x
            else:
                self.velocity_x = 0

            if self.key_pressed(KEY_1):
                self.velocity_x = 0
                self.velocity_y = 0
                self.target.x = int(self.sprite.x/60)*60
                self.target.y = int(self.sprite.y/60) * 60 - 60
                gr.add_sprite(self.target)
                gr.add_sprite(self.s_frame)
                self.attack = False
        else:
            if self.key_pressed(KEY_UP):
                self.target.x = int(self.sprite.x / 60) * 60
                self.target.y = int(self.sprite.y / 60) * 60 - 60
            elif self.key_pressed(KEY_DOWN):
                self.target.x = int(self.sprite.x / 60) * 60
                self.target.y = int(self.sprite.y / 60) * 60 + 60
            elif self.key_pressed(KEY_LEFT):
                self.target.x = int(self.sprite.x / 60) * 60 - 60
                self.target.y = int(self.sprite.y / 60) * 60
            elif self.key_pressed(KEY_RIGHT):
                self.target.x = int(self.sprite.x / 60) * 60 + 60
                self.target.y = int(self.sprite.y / 60) * 60
            if self.key_pressed(KEY_SPACE):
                gr.remove_sprite(self.target)
                gr.remove_sprite(self.s_frame)
                self.p_attack()
                self.attack = True
            if self.key_pressed(KEY_Q):
                gr.remove_sprite(self.target)
                gr.remove_sprite(self.s_frame)
                self.attack = True
        super().update()

    def p_attack(self):
        for i in range(0, len(self.world.thLevel.enemies)):
            if not self.death:
                if self.target.x == self.world.thLevel.enemies[i].x and self.target.y == self.world.thLevel.enemies[i].y:
                    self.world.thLevel.enemies[i].health -= 10
                    self.death = self.world.thLevel.check_death(self.world.thLevel.enemies[i])
        self.death = False
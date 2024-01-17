import graphics
from state import State

class RoguePlayer(State):
    anim = []
    animStep = 0
    spells = []

    def __init__(self, world, sprite, width, height, pos_x=0, pos_y=0, velocity_x=0, velocity_y=0):
        """

        Инициализирует объект GameObject.

        :param world: Экземпляр класса, представляющий мир, в котором находится объект.
        :param sprite: Спрайт, связанный с объектом.
        :param width: Ширина объекта.
        :param height: Высота объекта.
        :param pos_x: Начальная позиция по оси X.
        :param pos_y: Начальная позиция по оси Y.
        :param velocity_x: Начальная скорость по оси X.
        :param velocity_y: Начальная скорость по оси Y.
        """
        super().__init__()
        self.world = world
        self.sprite = sprite
        self.anim.append(sprite)
        self.width = width
        self.height = height
        self.x = pos_x
        self.y = pos_y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.health = 20

    def update(self):
        """
        Обновляет состояние объекта GameObject.
        """
        # self.run_state()
        if self.velocity_x != 0 or self.velocity_y != 0:
            self.collision_with_wall()
        if (self.velocity_x != 0 or self.velocity_y != 0) and len(self.anim) > 1:
            graphics.remove_sprite(self.sprite)
            self.sprite = self.anim[self.animStep]
            self.x += self.velocity_x
            self.y += self.velocity_y
            self.sprite.x = int(self.x)
            self.sprite.y = int(self.y)
            self.animStep += 1
            graphics.add_sprite(self.sprite)
        elif self.velocity_x != 0 or self.velocity_y != 0:
            graphics.remove_sprite(self.sprite)
            self.sprite = self.anim[0]
            self.x += self.velocity_x
            self.y += self.velocity_y
            self.sprite.x = int(self.x)
            self.sprite.y = int(self.y)
            graphics.add_sprite(self.sprite)
        else:
            graphics.remove_sprite(self.sprite)
            self.sprite = self.anim[0]
            graphics.add_sprite(self.sprite)
        if self.animStep == (len(self.anim)):
            self.animStep = 0

    def collision_with_wall(self):
        """
        Обрабатывает столкновение.
        """
        x_right = int(self.x + self.width)
        x_left = int(self.x)
        y_bottom = int(self.y + self.height)
        y_top = int(self.y)
        if self.velocity_x > 0 and self.world.get_coll(x_right, self.y):  # Движение вправо
            while self.world.get_coll(x_right, self.y):
                x_right -= 1
            self.x = x_right - self.width
            self.velocity_x = 0
        elif self.velocity_x < 0 and self.world.get_coll(x_left, self.y):  # Движение влево
            while self.world.get_coll(x_left, self.y):
                x_left += 1
            self.x = x_left + 1
            self.velocity_x = 0
        if self.velocity_y > 0 and self.world.get_coll(self.x, y_bottom):
            while self.world.get_coll(self.x, y_bottom):
                y_bottom -= 3
            self.y = y_bottom - self.height
            self.velocity_y = 0
        elif self.velocity_y < 0 and self.world.get_coll(self.x, y_top):
            while self.world.get_coll(self.x, y_top):
                y_top += 1
            self.y = y_top + 1
            self.velocity_y = 0

    def collision_with_triggers(self):
        """
        Обрабатывает соприкосновение с триггерами.
        """
        if (self.velocity_x != 0 or self.velocity_y != 0) and self.world.get_trigger(self.x, self.y):
            return self.world.get_num_trig(self.x, self.y)
        return [0, 0]

    def set_anim(self, anims):
        for i in range(0, len(anims)):
            self.anim.append(anims[i])

    def add_spell(self, spell):
        self.spells.append(spell)

    def set_spell(self):
        graphics.add_sprite(self.spells[0].sprite)

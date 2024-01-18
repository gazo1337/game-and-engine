from state import State


class Enemy(State):
    anim = []
    animStep = 0
    dmg = 2
    x_move = False
    y_move = False
    x_dist = 0
    y_dist = 0
    start_x = 0
    start_y = 0

    def __init__(self, sprite, width, height, pos_x=0, pos_y=0, velocity_x=0, velocity_y=0):
        """

        Инициализирует объект Enemy.
        :param sprite: Спрайт, связанный с объектом.
        :param width: Ширина объекта.
        :param height: Высота объекта.
        :param pos_x: Начальная позиция по оси X.
        :param pos_y: Начальная позиция по оси Y.
        :param velocity_x: Начальная скорость по оси X.
        :param velocity_y: Начальная скорость по оси Y.
        """
        super().__init__()
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
        self.x += self.velocity_x
        self.sprite.x = self.x + 10
        self.y += self.velocity_y
        self.sprite.y = self.y + 10

    def damage(self, player):
        player.health -= self.dmg

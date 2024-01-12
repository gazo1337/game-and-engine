from state import State


class Enemy(State):
    anim = []
    animStep = 0

    def __init__(self, sprite, width, height, pos_x=0, pos_y=0, velocity_x=1, velocity_y=1):
        """

        Инициализирует объект Enemy.

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
        self.sprite = sprite
        self.anim.append(sprite)
        self.width = width
        self.height = height
        self.x = pos_x
        self.y = pos_y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.health = 20

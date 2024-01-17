import generate_module
import graphics
from level import Level

tpos = {
        1: [-1, 0],
        2: [0, -1],
        3: [0, 1],
        4: [1, 0]
    }

class World:
    width = 30
    height = 30
    objects = []
    pos = None
    tile_map = []
    tile_width = 60
    tile_height = 60
    thLevel = None
    world_map = None
    world_lvls = []
    world_lvls_map = None
    def __init__(self):
        self.world_map = generate_module.gen_map(self.width, self.height)
        self.pos = [int(self.width/2), int(self.height/2)]
        self.world_lvls.append(Level(self.world_map, self.pos))
        self.thLevel = self.world_lvls[0]
        self.world_lvls_map = [[0 for i in range(0, self.width)] for j in range(0, self.height)]
        self.world_lvls_map[self.pos[0]][self.pos[1]] = 1


    def set_level(self, level_class):
        self.thLevel = level_class()

    def add_object(self, game_object):
        """
        Добавить игровой объект в мир.
        """
        self.objects.append(game_object)

    def remove_object(self, game_object):
        """
        Удалить игровой объект из мира.
        """
        if game_object in self.objects:
            self.objects.remove(game_object)

    def update(self):
        """
        Обновить состояние всех объектов в мире.
        """
        for game_object in self.objects:
            game_object.update()

    def get_tile(self, x, y):
        if x >= 0 and y >= 0 and x < self.count_w * self.tile_width and y < self.count_h * self.tile_height:
            return self.thLevel.map[int(y / self.tile_height)][int(x / self.tile_width)]
        else:
            return None

    def get_coll(self, x, y):
        """
        Проверяет на позиции игрока наличие позиции коллизионного объекта
        :param x: позиция игрока по x
        :param y: позиция игрока по y
        :return: true, если коллизионный объект найден, false - если не найден
        """
        tile = self.thLevel.lvl[int(y / self.tile_height)][int(x / self.tile_width)]
        tile1 = self.thLevel.step_map[int(y / self.tile_height)][int(x / self.tile_width)]
        if int(y / self.tile_height) >= len(self.thLevel.lvl) or int(x / self.tile_width) >= len(self.thLevel.lvl):
            return True
        if tile == 0 or tile == 2 or tile1 == 6:
            return True
        else:
            return False

    def get_trigger(self, x, y):
        """
        Проверяет на позиции игрока наличие позиции триггера
        :param x: позиция игрока по x
        :param y: позиция игрока по y
        :return: true, если триггер найден, false - если не найден
        """
        if self.thLevel.lvl[int(y / self.tile_height)][int(x / self.tile_width)] == 4:
            return True
        else:
            return False

    def get_num_trig(self, x, y):
        return tpos[self.thLevel.trig_map[int(y / self.tile_height)][int(x / self.tile_width)]]

    def level_change(self, new):
        self.pos[0] += new[0]
        self.pos[1] += new[1]
        if self.world_lvls_map[self.pos[0]][self.pos[1]] == 0:
            self.world_lvls_map[self.pos[0]][self.pos[1]] = 1
            self.thLevel.objects.clear()
            self.world_lvls.append(Level(self.world_map, self.pos))
            self.thLevel = self.world_lvls[len(self.world_lvls) - 1]
            graphics.clear()
            self.thLevel.set_enemies()
        else:
            for i in range(0, len(self.world_lvls)):
                if self.world_lvls[i].pos[0] == self.pos[0] and self.world_lvls[i].pos[1] == self.pos[1]:
                    self.thLevel.objects.clear()
                    self.thLevel = self.world_lvls[i]
                    graphics.clear()

    def set_map_steps(self):
        for i in range(0, len(self.thLevel.lvl)):
            for j in range(0, len(self.thLevel.lvl)):
                if self.thLevel.lvl[i][j] != 0 and self.thLevel.lvl[i][j] != 2:
                    if ((i == int(self.objects[0].sprite.y/60) or i == int(self.objects[0].sprite.y/60) + 1 or i == int(self.objects[0].sprite.y/60) - 1)
                    and (j == int(self.objects[0].sprite.x/60) or j == int(self.objects[0].sprite.x/60) + 1 or j == int(self.objects[0].sprite.x/60) - 1)):
                        self.thLevel.step_map[i][j] = 5
                    else:
                        self.thLevel.step_map[i][j] = 6
        graphics.set_other_tiles(self.thLevel.step_map, "tiles.png")

    def remove_map_steps(self):
        graphics.other_tile_map = None
        self.thLevel.step_map = [[9 for i in range(0, len(self.thLevel.lvl))] for j in range(0, len(self.thLevel.lvl))]
import generate_module
from graphics import *
from enemy import Enemy
from sprite import Sprite

tiles = {
        '#': 0, #Стены
        '.': 1, #Полы
        '/': 2, #Двери
        '_': 4 #Триггеры
    }

class Level:
    tile_width = 60
    tile_height = 60
    width = 30
    height = 30
    pos = None
    collision_tiles = []
    lvl = None
    enemies = []
    enemiesMap = None
    step_map = []
    breaked = False

    def __init__(self, map, pos):
        self.pos = [pos[0], pos[1]]
        self.lvl = generate_module.gen_level(map, self.pos[0], self.pos[1])
        self.objects = []
        for i in range(0, len(self.lvl)):
            for j in range(0, len(self.lvl[0])):
                if self.lvl[i][j] == 1:
                    self.collision_tiles.append(True)
                else:
                    self.collision_tiles.append(False)
        self.trig_map = [[0 for i in range(0, len(self.lvl[0]))] for j in range(0, len(self.lvl))]
        for i in range(0, len(self.lvl)):
            for j in range(0, len(self.lvl[0])):
                if self.lvl[i][j] == 2 and i == 0:
                    self.trig_map[i][j] = 1
                elif self.lvl[i][j] == 2 and i == len(self.lvl) - 1:
                    self.trig_map[i][j] = 4
                elif self.lvl[i][j] == 2 and j == 0:
                    self.trig_map[i][j] = 2
                elif self.lvl[i][j] == 2 and j == len(self.lvl) - 1:
                    self.trig_map[i][j] = 3
        self.step_map = [[9 for i in range(0, len(self.lvl))] for j in range(0, len(self.lvl))]




    def add_object(self, object):
        object.sprite_id = add_sprite(object.sprite)
        self.objects.append(object)

    def enemies_update(self):
        for i in range(0, len(self.enemies)):
            self.enemies[i].update()

    def break_doors(self):
        for i in range(0, len(self.lvl)):
            for j in range(0, len(self.lvl)):
                if self.lvl[i][j] == 2:
                    self.lvl[i][j] = 4
        self.breaked = True

    def set_enemies(self):
        self.enemiesMap = generate_module.gen_enemies(self.lvl)
        for i in range(0, len(self.enemiesMap)):
            for j in range(0, len(self.enemiesMap)):
                if self.enemiesMap[i][j] == 1:
                    x = j * tile_width
                    y = i * tile_height
                    self.enemies.append(Enemy(Sprite("enemie1.png", height=23, width=28, pos_x=x + 10, pos_y=y + 10), 28, 23, pos_x=x, pos_y=y))
                    self.add_object(self.enemies[len(self.enemies)-1])

    def check_death(self, enemy):
        if enemy.health <= 0:
            remove_sprite(enemy.sprite)
            self.enemiesMap[int(enemy.sprite.y / 60)][int(enemy.sprite.x / 60)] = 0
            self.enemies.remove(enemy)
            return True
        return False

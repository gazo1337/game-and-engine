import generate_module
from graphics import *
from enemy import Enemy
from sprite import Sprite
import time

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

    def enemies_turn(self, player):
        player_x = int(player.x / tile_width)
        player_y = int(player.y / tile_height)
        for i in range(0, len(self.enemies)):
            enemy_x = int(self.enemies[i].x/self.tile_width)
            enemy_y = int(self.enemies[i].y/self.tile_height)
            if (abs(player_x-enemy_x) == 1 and abs(player_y - enemy_y) == 0) or (abs(player_x-enemy_x) == 0 and abs(player_y - enemy_y) == 1):
                self.enemies[i].damage(player)
            else:
                if player_x - enemy_x != 0:
                    x_dist = int((player_x - enemy_x) / abs(player_x-enemy_x))
                else:
                    x_dist = 0
                if player_y - enemy_y != 0:
                    y_dist = int((player_y - enemy_y) / abs(player_y - enemy_y))
                else:
                    y_dist = 0
                if x_dist != 0 and self.enemiesMap[enemy_y][enemy_x + x_dist] != 1:
                    while self.enemies[i].x != (enemy_x + x_dist) * self.tile_width:
                        self.enemies[i].velocity_x = x_dist
                        self.enemies[i].update()
                    self.enemies[i].velocity_x = 0
                    self.enemiesMap[enemy_y][enemy_x] = 0
                    self.enemiesMap[enemy_y][int(self.enemies[i].x/self.tile_width)] = 1
                if y_dist != 0 and self.enemiesMap[enemy_y + y_dist][enemy_x] != 1:
                    while self.enemies[i].y != (enemy_y + y_dist) * self.tile_height:
                        self.enemies[i].velocity_y = y_dist
                        self.enemies[i].update()
                    self.enemies[i].velocity_y = 0
                    self.enemiesMap[enemy_y][enemy_x] = 0
                    self.enemiesMap[int(self.enemies[i].y / self.tile_height)][enemy_x] = 1
                if (abs(player_x - enemy_x) == 1 and abs(player_y - enemy_y) == 0) or (
                        abs(player_x - enemy_x) == 0 and abs(player_y - enemy_y) == 1):
                    self.enemies[i].damage(player)

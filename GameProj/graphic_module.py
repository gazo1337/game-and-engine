import sys
import sdl2
import sdl2.ext as sdlgame
from sdl2.ext import Window
import generate_module as generate
import Objs

global window_r, RESOURCES, room_pos_x, room_pos_y, levelr
RESOURCES = sdlgame.Resources(__file__, "models")
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 720
ENEMY_HP = 2
ENEMY_DMG = 2
FLOOR = '.'
WALL = '#'
DOOR = '/'
TRIGGER = '_'
ENEMY = '!'
CELL_HEIGHT = 60
CELL_WIDTH = 60
PLAYER_SPEED = 1
keys = {
    'D': PLAYER_SPEED,
    'S': PLAYER_SPEED,
    'A': -PLAYER_SPEED,
    'W': -PLAYER_SPEED,
    'Wrong': 0
}


def run(map_height, map_width):
    global wall, fl, tr, doors, enemies, en_data, not_destroyed, levelr, spells, acceses
    spells = []
    sdlgame.init()
    window = Window("Waiting for the Sun", size=(WINDOW_WIDTH, WINDOW_HEIGHT), flags=sdl2.SDL_WINDOW_FULLSCREEN)
    window.show()
    pfont = sdlgame.FontTTF(RESOURCES.get_path("pfont.ttf"), 50, sdl2.SDL_Color(255, 255, 255))

    world = sdlgame.World()
    movement = Objs.MovementSystem(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    rend = Objs.SoftwareRenderer(window)
    world.add_system(movement)
    world.add_system(rend)
    factory = sdlgame.SpriteFactory(sdlgame.SOFTWARE)
    w_path = RESOURCES.get_path("tile.png")
    g_path = RESOURCES.get_path("grass.png")
    t_path = RESOURCES.get_path("grass.png")
    d_path = RESOURCES.get_path("door.png")
    e_path = RESOURCES.get_path("enemie1.png")
    a_path = RESOURCES.get_path("acces.png")
    p_sprite = []
    p_sprite.append(factory.from_image(RESOURCES.get_path("person.png")))
    p_sprite.append(factory.from_image(RESOURCES.get_path("person1.png")))
    p_sprite.append(factory.from_image(RESOURCES.get_path("person2.png")))
    h_sprite = factory.from_image(RESOURCES.get_path("heart_hp.png"))
    spells.append(Objs.Icon(world, factory.from_image(RESOURCES.get_path("punch_icon.png")), 40, 180))

    tiles = {
        WALL: w_path,
        FLOOR: g_path,
        DOOR: d_path,
        TRIGGER: t_path,
        ENEMY: e_path
    }

    levelr = generate.gen_map(map_width, map_height)
    acces_matrix = [[0 for i in range(0, map_width)] for j in range(0, map_height)]
    generate.print_level(levelr)
    room_pos_x = round(map_width / 2)
    room_pos_y = round(map_height / 2)
    acces_matrix[room_pos_x][room_pos_y] = 1
    room = generate.gen_level(levelr, room_pos_x, room_pos_y)
    wall = []
    fl = []
    tr = []
    doors = []
    enemies = []
    en_data = []
    for i in range(0, len(room)):
        for j in range(0, len(room[i])):
            if room[i][j] == WALL:
                wall.append(Objs.Wall(world, factory.from_image(tiles[room[i][j]]),
                                      round(WINDOW_WIDTH / 2 - (len(room) / 2) * CELL_WIDTH) + CELL_WIDTH * i,
                                      round(WINDOW_HEIGHT / 2 - (len(room[i]) / 2) * CELL_HEIGHT) + CELL_HEIGHT * j))
            if room[i][j] == FLOOR:
                fl.append(Objs.Floor(world, factory.from_image(tiles[room[i][j]]),
                                     round(WINDOW_WIDTH / 2 - (len(room) / 2) * CELL_WIDTH) + CELL_WIDTH * i,
                                     round(WINDOW_HEIGHT / 2 - (len(room[i]) / 2) * CELL_HEIGHT) + CELL_HEIGHT * j))
            if room[i][j] == TRIGGER:
                tr.append(Objs.Trigger(world, factory.from_image(tiles[room[i][j]]),
                                       round(WINDOW_WIDTH / 2 - (len(room) / 2) * CELL_WIDTH) + CELL_WIDTH * i,
                                       round(WINDOW_HEIGHT / 2 - (len(room[i]) / 2) * CELL_HEIGHT) + CELL_HEIGHT * j))

    player = Objs.Player(world, p_sprite[0], round(WINDOW_WIDTH / 2), round(WINDOW_HEIGHT / 2))
    player_data = Objs.PlayerData(20, 0, 2)
    hp_icon = Objs.Floor(world, h_sprite, 40, 20)
    pfont.render_text(str(player_data.hp), line_h=2)
    running = True
    not_destroyed = True
    attack = False
    tile_position = []
    acceses = []
    not_acces = []
    target = None
    fight = False
    pg_pos = []
    pstep = True

    while running:
        if not_destroyed and not(attack):
            actkeyx = ''
            actkeyy = ''
            for event in sdlgame.get_events():
                if event.type == sdl2.SDL_QUIT:
                    running = False
                if event.type == sdl2.SDL_KEYDOWN:
                    if event.key.keysym.sym == sdl2.SDLK_w:
                        actkeyy = 'W'
                    if event.key.keysym.sym == sdl2.SDLK_s:
                        actkeyy = 'S'
                    if event.key.keysym.sym == sdl2.SDLK_a:
                        actkeyx = 'A'
                    if event.key.keysym.sym == sdl2.SDLK_d:
                        actkeyx = 'D'
                    if event.key.keysym.sym == sdl2.SDLK_1:
                        for f in fl:
                            left, top, right, bottom = f.sprite.area
                            if (left - 30 < player.sprite.position[0] < right) and (
                                    top - 30 < player.sprite.position[1] < bottom):
                                tile_position = (f.sprite.position[0], f.sprite.position[1])
                        target = Objs.Target(world, factory.from_image(RESOURCES.get_path("target.png")),
                                             tile_position[0], tile_position[1] - 60)
                        frame = Objs.Icon(world, factory.from_image(RESOURCES.get_path("spell_frame.png")), spells[0].sprite.position[0], spells[0].sprite.position[1])
                        attack = True
                if event.type == sdl2.SDL_KEYUP:
                    if event.key.keysym.sym in (sdl2.SDLK_w, sdl2.SDLK_s):
                        actkeyy = ''
                        player.velocity.vy = 0
                    if event.key.keysym.sym in (sdl2.SDLK_a, sdl2.SDLK_d):
                        actkeyx = ''
                        player.velocity.vx = 0

            if actkeyx != '':
                if player.sprite.position[0] + keys[actkeyx] <= wall[0].sprite.position[0]:
                    new_position = (player.sprite.position[0] + 4, player.sprite.position[1])
                    player.sprite.position = new_position
                    player.velocity.vx = 0
                    actkeyx = ''
                elif player.sprite.position[0] + keys[actkeyx] > wall[0].sprite.position[0]:
                    player.velocity.vx = keys[actkeyx]
            if actkeyy != '':
                if player.sprite.position[1] + keys[actkeyy] > wall[0].sprite.position[1]:
                    player.velocity.vy = keys[actkeyy]
                if player.sprite.position[1] + keys[actkeyy] <= wall[0].sprite.position[1]:
                    new_position = (player.sprite.position[0], player.sprite.position[1] + 4)
                    player.sprite.position = new_position
                    player.velocity.vy = 0
                    actkeyy = ''
            Objs.coll(wall, player, actkeyx, actkeyy)
            Objs.coll(doors, player, actkeyx, actkeyy)
            Objs.coll(not_acces, player, actkeyx, actkeyy)
        pstep = Objs.animation(player, p_sprite, pstep)
        if Objs.trigger(tr, player):
            player.velocity.vx = 0
            player.velocity.vy = 0
            not_destroyed = False
            world.delete_entities(wall)
            world.delete_entities(fl)
            world.delete_entities(tr)
            wall.clear()
            fl.clear()
            tr.clear()
            room_pos_x, room_pos_y = Objs.telep(player, room_pos_x, room_pos_y)
            world.delete(player)
            if acces_matrix[room_pos_x][room_pos_y] == 0:
                room = generate.gen_lvl_enemies(levelr, room_pos_x, room_pos_y)
                fight = True
            else:
                room = generate.gen_level(levelr, room_pos_x, room_pos_y)
            for i in range(0, len(room)):
                for j in range(0, len(room[i])):
                    if room[i][j] == WALL:
                        wall.append(Objs.Wall(world, factory.from_image(tiles[room[i][j]]),
                                              round(WINDOW_WIDTH / 2 - (len(room) / 2) * CELL_WIDTH) + CELL_WIDTH * i,
                                              round(WINDOW_HEIGHT / 2 - (
                                                      len(room[i]) / 2) * CELL_HEIGHT) + CELL_HEIGHT * j))
                    if room[i][j] == FLOOR:
                        fl.append(Objs.Floor(world, factory.from_image(tiles[room[i][j]]),
                                             round(WINDOW_WIDTH / 2 - (len(room) / 2) * CELL_WIDTH) + CELL_WIDTH * i,
                                             round(WINDOW_HEIGHT / 2 - (
                                                     len(room[i]) / 2) * CELL_HEIGHT) + CELL_HEIGHT * j))
                    if room[i][j] == DOOR:
                        doors.append(Objs.Wall(world, factory.from_image(tiles[room[i][j]]),
                                               round(WINDOW_WIDTH / 2 - (len(room) / 2) * CELL_WIDTH) + CELL_WIDTH * i,
                                               round(WINDOW_HEIGHT / 2 - (
                                                       len(room[i]) / 2) * CELL_HEIGHT) + CELL_HEIGHT * j))
                    if room[i][j] == ENEMY:
                        fl.append(Objs.Floor(world, factory.from_image(tiles[FLOOR]),
                                             round(WINDOW_WIDTH / 2 - (len(room) / 2) * CELL_WIDTH) + CELL_WIDTH * i,
                                             round(WINDOW_HEIGHT / 2 - (
                                                     len(room[i]) / 2) * CELL_HEIGHT) + CELL_HEIGHT * j))
                        enemies.append(Objs.Enemy(world, factory.from_image(tiles[room[i][j]]), ENEMY_HP,
                                             round(WINDOW_WIDTH / 2 - (len(room) / 2) * CELL_WIDTH) + CELL_WIDTH * i,
                                             round(WINDOW_HEIGHT / 2 - (
                                                     len(room[i]) / 2) * CELL_HEIGHT) + CELL_HEIGHT * j))
                        en_data.append(Objs.EnemyData(ENEMY_HP, ENEMY_DMG))
                    if room[i][j] == TRIGGER:
                        tr.append(Objs.Trigger(world, factory.from_image(tiles[room[i][j]]),
                                               round(WINDOW_WIDTH / 2 - (len(room) / 2) * CELL_WIDTH) + CELL_WIDTH * i,
                                               round(WINDOW_HEIGHT / 2 - (
                                                           len(room[i]) / 2) * CELL_HEIGHT) + CELL_HEIGHT * j))

            player = Objs.Player(world, p_sprite[0], round(WINDOW_WIDTH / 2), round(WINDOW_HEIGHT / 2))
            not_destroyed = True
        if attack:
            player.velocity.vx = 0
            player.velocity.vy = 0
            for event in sdlgame.get_events():
                if event.type == sdl2.SDL_KEYDOWN:
                    if event.key.keysym.sym == sdl2.SDLK_w:
                        world.delete(target)
                        target = Objs.Target(world, factory.from_image(RESOURCES.get_path("target.png")),tile_position[0], tile_position[1]-60)
                    if event.key.keysym.sym == sdl2.SDLK_s:
                        world.delete(target)
                        target = Objs.Target(world, factory.from_image(RESOURCES.get_path("target.png")),tile_position[0], tile_position[1]+60)
                    if event.key.keysym.sym == sdl2.SDLK_a:
                        world.delete(target)
                        target = Objs.Target(world, factory.from_image(RESOURCES.get_path("target.png")),tile_position[0]-60, tile_position[1])
                    if event.key.keysym.sym == sdl2.SDLK_d:
                        world.delete(target)
                        target = Objs.Target(world, factory.from_image(RESOURCES.get_path("target.png")),tile_position[0]+60, tile_position[1])
                    if event.key.keysym.sym == sdl2.SDLK_q:
                        world.delete(target)
                        world.delete(frame)
                        attack = False
                    if event.key.keysym.sym == sdl2.SDLK_SPACE and target != None:
                        Objs.damage(target, enemies, en_data, world)
                        world.delete(frame)
                        attack = False
        if len(enemies) == 0:
            for d in doors:
                pos = (d.sprite.position[0], d.sprite.position[1])
                world.delete(d)
                doors.remove(d)
                tr.append(Objs.Trigger(world, factory.from_image(tiles[TRIGGER]), pos[0], pos[1]))
                acces_matrix[room_pos_x][room_pos_y] = 1
        # if len(enemies) != 0 and fight:
        #     for f in fl:
        #         if ((f.sprite.position[0] >= player.sprite.position[0] - CELL_WIDTH*player_data.steps) and (f.sprite.position[0] <= player.sprite.position[0] + CELL_WIDTH*player_data.steps)) and ((f.sprite.position[1] >= player.sprite.position[1] - CELL_HEIGHT*player_data.steps) and (f.sprite.position[1] <= player.sprite.position[1] + CELL_HEIGHT*player_data.steps)):
        #             acceses.append(Objs.Floor(world, factory.from_image(a_path),
        #                                      f.sprite.position[0],
        #                                      f.sprite.position[1]))
        #         else:
        #             not_acces.append(Objs.Wall(world, factory.from_image(RESOURCES.get_path("not_access.png")), f.sprite.position[0], f.sprite.position[1]))
        #     fight = False
        sdl2.SDL_Delay(1)
        world.process()




if __name__ == "__main__":
    sys.exit(run(20, 20))

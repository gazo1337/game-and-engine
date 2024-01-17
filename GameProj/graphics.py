from sdl2 import *
import sdl2.ext

KEY_LEFT = SDLK_a
KEY_RIGHT = SDLK_d
KEY_UP = SDLK_w
KEY_DOWN = SDLK_s
KEY_SPACE = SDLK_SPACE
KEY_1 = SDLK_1
KEY_Q = SDLK_q

RESOURCES = None
SPRITES = ""
window_width = 1024
window_height = 768
window = None
renderer = None
sprites = []
keys = {}
tile_map = None
other_tile_map = None
tiles = None
tile_width = 60
tile_height = 60
tiles_count_w = 0
tiles_count_h = 0
other_tiles_count_w = 0
other_tiles_count_h = 0

def init(width, height):
    """
    Инициализация окна и графики.
    """
    global RESOURCES, window, renderer, window_width, window_height
    window_width = width
    window_height = height
    sdl2.ext.init()
    RESOURCES = sdl2.ext.Resources(__file__, SPRITES)
    window = sdl2.ext.Window("WFTS", size=(window_width, window_height))
    window.show()
    renderer = SDL_CreateRenderer(window.window, -1, SDL_RENDERER_ACCELERATED)

def set_tiles(tile_map_data, tiles_image):
    global tile_map, tiles, tiles_count_w, tiles_count_h
    tile_map = tile_map_data
    tiles = sdl2.ext.load_image(sdl2.ext.Resources(__file__, SPRITES).get_path(tiles_image))
    print('ren', renderer)
    tiles = SDL_CreateTextureFromSurface(renderer, tiles)
    tiles_count_w = len(tile_map_data[0])
    tiles_count_h = len(tile_map_data)

def set_other_tiles(tile_map_data, tiles_image):
    global other_tile_map, tiles, other_tiles_count_w, other_tiles_count_h
    other_tile_map = tile_map_data
    tiles = sdl2.ext.load_image(sdl2.ext.Resources(__file__, SPRITES).get_path(tiles_image))
    print('ren', renderer)
    tiles = SDL_CreateTextureFromSurface(renderer, tiles)
    other_tiles_count_w = len(tile_map_data[0])
    other_tiles_count_h = len(tile_map_data)

def add_sprite(sprite):
    """
    Добавляет спрайт на экран

    :param file_name: Имя файла с изображением спрайта.
    :param pos_x: Начальная позиция по оси X.
    :param pos_y: Начальная позиция по оси Y.
    :return: Созданный спрайт.
    """
    sprite.image = sdl2.ext.load_image(sdl2.ext.Resources(__file__, SPRITES).get_path(sprite.file_name))
    if sprite.width is None:
        sprite.width = sprite.image.w
    if sprite.height is None:
        sprite.height = sprite.image.h
    sprite.image = SDL_CreateTextureFromSurface(renderer, sprite.image)
    sprites.append(sprite)
    return len(sprites) - 1

def set_sprite(sprite_id, new_sprite):
    sprites[sprite_id] = new_sprite


def remove_sprite(sprite):
    if sprite in sprites:
        sprites.remove(sprite)


def clear():
    sprites.clear()


def draw_all():
    """
    Отрисовывает все спрайты на экране.
    """
    SDL_RenderClear(renderer)
    if tile_map is not None:
        for y in range(tiles_count_h):
            for x in range(tiles_count_w):
                cell = tile_map[y][x]
                SDL_RenderCopy(renderer, tiles,
                                SDL_Rect(cell * tile_width, 0, tile_width, tile_height),
                                SDL_Rect(x * tile_width, y * tile_height,
                                         tile_width, tile_height))
    if other_tile_map is not None:
        for y in range(other_tiles_count_h):
            for x in range(other_tiles_count_w):
                cell = other_tile_map[y][x]
                SDL_RenderCopy(renderer, tiles,
                                SDL_Rect(cell * tile_width, 0, tile_width, tile_height),
                                SDL_Rect(x * tile_width, y * tile_height,
                                         tile_width, tile_height))
    for sprite in sprites:
        sdl_rect = SDL_Rect(sprite.start_x, sprite.start_y, sprite.width, sprite.height)
        SDL_RenderCopy(renderer, sprite.image, sdl_rect,
                        SDL_Rect(sprite.x, sprite.y, sprite.width, sprite.height))
        sprite.update()

    SDL_RenderPresent(renderer)
    sdl2.SDL_Delay(5)


def process_events():
    """
    Обрабатывает события SDL.

    :return: True, если событие SDL_QUIT обнаружено, в противном случае False.
    """
    for event in sdl2.ext.get_events():
        if event.type == SDL_QUIT:
            return True
        elif event.type == SDL_KEYDOWN:
            keys[event.key.keysym.sym] = True
        elif event.type == SDL_KEYUP:
            keys[event.key.keysym.sym] = False

    return False

def key_pressed(key):
    """
    Проверяет, нажата ли клавиша.

    :param key: Код клавиши.
    :return: True, если клавиша нажата, в противном случае False.
    """
    if key in keys:
        return keys[key]
    else:
        return False

def quit():
    """
    Завершает работу графической подсистемы
    """
    sdl2.SDL_QUIT()
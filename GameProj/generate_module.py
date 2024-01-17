import random

rooms = {
    5: "5x5",
    6: "6x6",
    7: "7x7",
    8: "8x8",
    9: "9x9",
    10: "10x10",
    11: "11x11"
}

def gen_enemies(lvl):
    en_map = [[0 for i in range(0, len(lvl))] for j in range(0, len(lvl))]
    for i in range(0, len(lvl)):
        for j in range(0, len(lvl[0])):
            rand = random.randint(0, 10)
            if lvl[i][j] != 0 and lvl[i][j] != 4 and lvl[i][j] != 2 and rand < 1:
                en_map[i][j] = 1
    return en_map


def gen_level(map, x, y):
    size = rooms[map[x][y]].split('x')
    count_height = int(size[0])
    count_width = int(size[1])
    offset = -1
    level = [[0 for i in range(0, count_width)] for j in range(0, count_height)]
    for i in range(1, count_width - 1):
        for j in range(1, count_height - 1):
            level[i][j] = 1
    if round(map[x][y] / 2) < map[x][y] / 2:
        offset = 0
    if map[x - 1][y] != 0:
        level[0][round(count_height / 2)] = 2
    if map[x][y - 1] != 0:
        level[round(count_width / 2)][0] = 2
    if map[x + 1][y] != 0:
        level[count_width - 1][round(count_height / 2)] = 2
    if map[x][y + 1] != 0:
        level[round(count_width / 2)][count_height - 1] = 2

    return level


def gen_map(map_width, map_height):
    global width
    global height
    map = [[0 for i in range(map_width)] for j in range(map_height)]
    range_down = round((map_width + map_height) / 6)
    range_up = round((map_width + map_height) / 4)
    up_direct = random.randint(range_down, range_up)
    down_direct = random.randint(range_down, range_up)
    left_direct = random.randint(range_down, range_up)
    right_direct = random.randint(range_down, range_up)
    width = round(map_width / 2)
    height = round(map_height / 2)
    map[width][height] = 5
    map[width - 1][height] = random.randint(6, 11)
    map[width + 1][height] = random.randint(6, 11)
    map[width][height - 1] = random.randint(6, 11)
    map[width][height + 1] = random.randint(6, 11)
    map[width - 2][height] = random.randint(6, 11)
    map[width + 2][height] = random.randint(6, 11)
    map[width][height - 2] = random.randint(6, 11)
    map[width][height + 2] = random.randint(6, 11)
    width -= 2
    height = round(map_height / 2)
    block_direction = 2
    for a in range(0, up_direct):
        map = direct_change(block_direction, map)
    width = round(map_width / 2) + 2
    height = round(map_height / 2)
    block_direction = 1
    for a in range(0, down_direct):
        map = direct_change(block_direction, map)
    width = round(map_width / 2)
    height = round(map_height / 2) - 2
    block_direction = 4
    for a in range(0, left_direct):
        map = direct_change(block_direction, map)
    width = round(map_width / 2)
    height = round(map_height / 2) + 2
    block_direction = 3
    for a in range(0, right_direct):
        map = direct_change(block_direction, map)
    return map


def direct_change(block_direction, map):
    global width, height
    upDown = 0
    rightLeft = 0
    direction = random.randint(1, 5)
    # 1 - вверх
    # 2 - вниз
    # 3 - влево
    # 4 - вправо
    if direction == 1:
        upDown = -1
        if (map[width + upDown][height] != 0) or (block_direction == direction):
            direct_change(block_direction, map)
        else:
            map[width + upDown][height] = random.randint(6, 11)
            width += upDown
            height += rightLeft
    elif direction == 2:
        upDown = 1
        if (map[width + upDown][height] != 0) or (block_direction == direction):
            direct_change(block_direction, map)
        else:
            map[width + upDown][height] = random.randint(6, 11)
            width += upDown
            height += rightLeft
    elif direction == 3:
        rightLeft = -1
        if (map[width][height + rightLeft] != 0) or (block_direction == direction):
            direct_change(block_direction, map)
        else:
            map[width][height + rightLeft] = random.randint(6, 11)
            width += upDown
            height += rightLeft
    elif direction == 4:
        rightLeft = 1
        if (map[width][height + rightLeft] != 0) or (block_direction == direction):
            direct_change(block_direction, map)
        else:
            map[width][height + rightLeft] = random.randint(6, 11)
            width += upDown
            height += rightLeft
    return map

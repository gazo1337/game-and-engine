import sdl2.ext as sgame
import graphic_module


class SoftwareRenderer(sgame.SoftwareSpriteRenderSystem):
    def __init__(self, window):
        super(SoftwareRenderer, self).__init__(window)

    def render(self, components):
        sgame.fill(self.surface, sgame.Color(0, 0, 0))
        super(SoftwareRenderer, self).render(components)


class MovementSystem(sgame.Applicator):
    def __init__(self, minx, miny, maxx, maxy):
        super(MovementSystem, self).__init__()
        self.componenttypes = Velocity, sgame.Sprite
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy

    def process(self, world, components):
        for velocity, sprite in components:
            swidth, sheight = sprite.size
            sprite.x += velocity.vx
            sprite.y += velocity.vy

            sprite.x = max(self.minx, sprite.x)
            sprite.y = max(self.miny, sprite.y)

            pmaxx = sprite.x + swidth
            pmaxy = sprite.y + sheight
            if pmaxx > self.maxx:
                sprite.x = self.maxx - swidth
            if pmaxy > self.maxy:
                sprite.y = self.maxy - sheight


class Enemy(sgame.Entity):
    def __init__(self, world, sprite, hp, x, y):
        self.sprite = sprite
        self.sprite.position = x, y
        self.velocity = Velocity()

class EnemyData():
    def __init__(self, hp, dmg):
        self.hp = hp
        self.dmg = dmg

class Player(sgame.Entity):
    def __init__(self, world, sprite, x, y):
        self.sprite = sprite
        self.sprite.position = x, y
        self.velocity = Velocity()


class PlayerData():
    def __init__(self, hp, dmg, steps):
        self.hp = hp
        self.dmg = dmg
        self.steps = steps


class Wall(sgame.Entity):
    def __init__(self, world, sprite, x, y):
        self.sprite = sprite
        self.sprite.position = x, y

class Target(sgame.Entity):
    def __init__(self, world, sprite, x, y):
        self.sprite = sprite
        self.sprite.position = x, y

class Icon(sgame.Entity):
    def __init__(self, world, sprite, x, y):
        self.sprite = sprite
        self.sprite.position = x, y


class Floor(sgame.Entity):
    def __init__(self, world, sprite, x, y):
        self.sprite = sprite
        self.sprite.position = x, y


class Trigger(sgame.Entity):
    def __init__(self, world, sprite, x, y):
        self.sprite = sprite
        self.sprite.position = x, y


class Velocity(object):
    def __init__(self):
        super(Velocity, self).__init__()
        self.vx = 0
        self.vy = 0


def coll(obj, player, actkeyx, actkeyy):
    if len(obj) != 0:
        for w in obj:
            left, top, right, bottom = w.sprite.area
            if (left - 30 < player.sprite.position[0] < right) and (top - 30 < player.sprite.position[1] < bottom):
                if player.velocity.vx < 0 or actkeyx == 'A':
                    new_position = (player.sprite.position[0] - player.velocity.vx * 4, player.sprite.position[1])
                    if (left - 30 < new_position[0] < right) and (top - 30 < new_position[1] < bottom):
                        new_position = (player.sprite.position[0] + player.velocity.vx * 4, player.sprite.position[1])
                    player.sprite.position = new_position
                    player.velocity.vx = 0
                if player.velocity.vx > 0 or actkeyx == 'D':
                    new_position = (player.sprite.position[0] - player.velocity.vx * 4, player.sprite.position[1])
                    if (left - 30 < new_position[0] < right) and (top - 30 < new_position[1] < bottom):
                        new_position = (player.sprite.position[0] + player.velocity.vx * 4, player.sprite.position[1])
                    player.sprite.position = new_position
                    player.velocity.vx = 0
                if player.velocity.vy > 0 or actkeyy == 'S':
                    new_position = (player.sprite.position[0], player.sprite.position[1] - player.velocity.vy * 4)
                    if (left - 30 < new_position[0] < right) and (top - 30 < new_position[1] < bottom):
                        new_position = (player.sprite.position[0], player.sprite.position[1] + player.velocity.vy * 4)
                    player.sprite.position = new_position
                    player.velocity.vy = 0
                if player.velocity.vy < 0 or actkeyy == 'W':
                    new_position = (player.sprite.position[0], player.sprite.position[1] - player.velocity.vy * 4)
                    if (left - 30 < new_position[0] < right) and (top - 30 < new_position[1] < bottom):
                        new_position = (player.sprite.position[0], player.sprite.position[1] + player.velocity.vy * 4)
                    player.sprite.position = new_position
                    player.velocity.vy = 0


def trigger(trig, player):
    for t in trig:
        left, top, right, bottom = t.sprite.area
        if (left - 30 < player.sprite.position[0] < right) and (top - 30 < player.sprite.position[1] < bottom):
            return True

def animation(person, animation, steps):
    if person.velocity.vx != 0 or person.velocity.vy != 0:
        if steps:
            new_position = person.sprite.position
            person.sprite = animation[1]
            person.sprite.position = new_position
            steps = False
            return steps
        else:
            new_position = person.sprite.position
            person.sprite = animation[2]
            person.sprite.position = new_position
            steps = True
            return steps
    else:
        new_position = person.sprite.position
        person.sprite = animation[0]
        person.sprite.position = new_position


def telep(player, roomx, roomy):
    if (player.sprite.position[0] < graphic_module.WINDOW_WIDTH / 2) and (
            abs(player.sprite.position[0] - graphic_module.WINDOW_WIDTH / 2) > abs(
        player.sprite.position[1] - graphic_module.WINDOW_HEIGHT / 2)):
        roomx -= 1
        return roomx, roomy
    if (player.sprite.position[0] > graphic_module.WINDOW_WIDTH / 2) and (
            abs(player.sprite.position[0] - graphic_module.WINDOW_WIDTH / 2) > abs(
        player.sprite.position[1] - graphic_module.WINDOW_HEIGHT / 2)):
        roomx += 1
        return roomx, roomy
    if (player.sprite.position[1] < graphic_module.WINDOW_HEIGHT / 2) and (
            abs(player.sprite.position[0] - graphic_module.WINDOW_WIDTH / 2) < abs(
        player.sprite.position[1] - graphic_module.WINDOW_HEIGHT / 2)):
        roomy -= 1
        return roomx, roomy
    if (player.sprite.position[1] > graphic_module.WINDOW_HEIGHT / 2) and (
            abs(player.sprite.position[0] - graphic_module.WINDOW_WIDTH / 2) < abs(
        player.sprite.position[1] - graphic_module.WINDOW_HEIGHT / 2)):
        roomy += 1
        return roomx, roomy


def damage(target, enemies, en_data, world):
    left, top, right, bottom = target.sprite.area
    for e in enemies:
        if (left - 30 < e.sprite.position[0] < right) and (top - 30 < e.sprite.position[1] < bottom):
            data = enemies.index(e)
            en_data[data].hp -= 1
            if en_data[data].hp == 0:
                world.delete(e)
                enemies.remove(e)
                en_data.remove(en_data[data])
    world.delete(target)
def fight_pos(player, floor):
    for f in floor:
        left, top, right, bottom = f.sprite.area
        if (left - 30 < player.sprite.position[0] < right) and (top - 30 < player.sprite.position[1] < bottom):
            return f.sprite.position

# def enemy_attack(enemy, player, maxsteps):
#     stepsx, stepsy = maxsteps
#     enemy_velocity = 1

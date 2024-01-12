from sdl2.sdlttf import *
from world import  World
from rogue import RogueGame
import graphics as gr
from sprite import Sprite
from player import Player
from spell import Spell

world = World()
target = Sprite("target.png", 0, 0, 60, 60)
player_class = Player(world, Sprite("person.png", 150, 150, height=23, width=14), gr.key_pressed, 150, 150, target)
player_class.set_anim([Sprite("person1.png", height=23, width=14), Sprite("person2.png", height=23, width=14)])
player_class.add_spell(Spell(Sprite("punch_icon.png", 1070, 10, 120, 120), 10))


class WaitingGame(RogueGame):
    tiles_image = "tiles.png"
    texture = None

    def __init__(self):
        super().__init__()
        gr.SPRITES = "models"
        gr.init(1200, 720)
        TTF_Init()
        self.states = {
            'Intro': self.intro,
            'Game': self.game
        }
        self.set_state('Intro')
        gr.add_sprite(Sprite("sun.jpg"))

    def intro(self):
        if gr.key_pressed(gr.KEY_SPACE):
            self.set_state('Game')
            gr.clear()
            self.set_level(world.thLevel)
            self.level.add_object(player_class)
            player_class.set_spell()


    def game(self):
        player_class.update()
        if len(world.thLevel.enemies) == 0 and not world.thLevel.breaked:
            world.thLevel.break_doors()
            self.set_level(world.thLevel)
        new_pos = player_class.collision_with_triggers()
        if new_pos[0] != 0 or new_pos[1] != 0:
            world.level_change(new_pos)
            self.set_level(world.thLevel)
            if new_pos[0] != 0:
                player_class.y = int(len(world.thLevel.lvl)/2 - (len(world.thLevel.lvl)/2 - 1)*new_pos[0]) * 60 + 20 * new_pos[0]
                player_class.sprite.y = int(len(world.thLevel.lvl)/2 - (len(world.thLevel.lvl)/2 - 1)*new_pos[0]) * 60 + 20 * new_pos[0]
                player_class.x = int(len(world.thLevel.lvl)/2) * 60
                player_class.sprite.x = int(len(world.thLevel.lvl)/2) * 60
            if new_pos[1] != 0:
                player_class.x = int(len(world.thLevel.lvl) / 2 - (len(world.thLevel.lvl) / 2 - 1) * new_pos[1]) * 60 + 20 * new_pos[1]
                player_class.sprite.x = int(len(world.thLevel.lvl) / 2 - (len(world.thLevel.lvl) / 2 - 1) * new_pos[1]) * 60 + 20 * new_pos[1]
                player_class.y = int(len(world.thLevel.lvl) / 2) * 60
                player_class.sprite.y = int(len(world.thLevel.lvl) / 2) * 60
            self.level.add_object(player_class)
            player_class.set_spell()






if __name__ == "__main__":
    game = WaitingGame()
    game.run()
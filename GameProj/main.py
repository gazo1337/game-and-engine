from  rogue import RogueGame
import graphics as gr
from sprite import Sprite
from player import RoguePlayer
from level import Level

import sys

#def main():
#    sys.exit(graphics.run(20, 20))

class Level2:
    pass

class Level1(Level):
    width = 20
    height = 20
    start_pos = (5, 5)
    portals = [(10, 1, Level2, 1, 10)]


class Level2(Level):
    portals = [(1, 10, Level1, 10, 1)]


class Player(RoguePlayer):
    anim_left = []
    anim_right = []
    anim_up = []
    anim_down = []

class WaitingGame(RogueGame):
    tiles_image = "tiles.png"
    player_class = Player
    def __init__(self):
        super().__init__()
        gr.SPRITES = "models"
        gr.init(1200, 720)
        self.states = {
            'Intro': self.intro,
            'Game': self.game
        }
        self.set_state('Intro')
        gr.add_sprite(Sprite("person.png"))

    def intro(self):
        if gr.key_pressed(gr.KEY_SPACE):
            self.set_state('Game')
            gr.clear()
            self.set_level(Level1)

    def game(self):
        pass


if __name__ == "__main__":
    game = WaitingGame()
    game.run()
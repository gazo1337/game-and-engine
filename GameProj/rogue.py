from state import State
from player import RoguePlayer
import graphics as gr


class RogueGame(State):
    tiles_image = ""
    player_class = RoguePlayer

    def __init__(self):
        self.player = self.player_class()


    def set_level(self, level_class):
        self.level = level_class()
        gr.set_tiles(self.level.map, self.tiles_image)


    def update(self):
        self.level.update()

    def run(self):
        """
        Игровой цикл.
        """
        while True:
            if gr.process_events():
                break
            self.run_state()
            self.update()
            gr.draw_all()
        gr.quit()
import pygame as pg 
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *
from main_menu import *

class Game:
    def __init__(self):
        # Game initialization.
        pg.init()  # Initialize the Pygame library.
        pg.mouse.set_visible(False)  # Hide the mouse cursor.
        self.screen = pg.display.set_mode(RES)  # Create a window with the specified resolution.
        self.clock = pg.time.Clock()  # Clock for controlling frame rate.
        self.delta_time = 1  # Time since the last frame.
        self.global_trigger = False  # Flag for triggering global events.
        self.global_event = pg.USEREVENT + 0  # Define a custom event.
        pg.time.set_timer(self.global_event, 40)  # Set a timer for the global event.
        self.new_game()  # Initialize a new game.
        self.state = 'MENU'  # Possible states: 'MENU', 'PLAYING', 'OPTIONS'

    def new_game(self):
        # Set up a new game.
        self.map = Map(self)  # Create a map object.
        self.player = Player(self)  # Create a player object.
        self.object_renderer = ObjectRenderer(self)  # Object renderer for 3D objects.
        self.raycasting = RayCasting(self)  # Ray casting for 3D rendering.
        self.object_handler = ObjectHandler(self)  # Handler for in-game objects.
        self.weapon = Weapon(self)  # Player's weapon.
        self.sound = Sound(self)  # Sound manager.
        self.pathfinding = PathFinding(self)  # Pathfinding algorithm.
        pg.mixer.music.play(-1)  # Play background music indefinitely.
        self.main_menu = MainMenu(self) 

    def update(self):
        # Update game state.
        self.player.update()  # Update player's state.
        self.raycasting.update()  # Update raycasting calculations.
        self.object_handler.update()  # Update in-game objects.
        self.weapon.update()  # Update weapon state.
        pg.display.flip()  # Update the full display Surface to the screen.
        self.delta_time = self.clock.tick(FPS)  # Control frame rate and calculate delta time.
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')  # Update the window title with FPS.

    def draw(self):
        # Draw game objects.
        self.object_renderer.draw()  # Draw 3D objects.
        self.weapon.draw()  # Draw the weapon.

    def check_events(self):
        # Check for Pygame events.
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                # Exit the game if the window is closed or Escape key is pressed.
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                # Handle custom global event.
                self.global_trigger = True
            self.player.single_fire_event(event)  # Handle player-specific events.

    def start_game(self):
        self.state = 'PLAYING'
        self.new_game()

    def show_options(self):
        # Handle options display and settings here.
        pass

    def run(self):
        while True:
            if self.state == 'MENU':
                self.main_menu.update()
                self.main_menu.draw()
                pg.display.flip()
            elif self.state == 'PLAYING':
                self.check_events()
                self.update()
                self.draw()
            # Add more states as needed (like 'OPTIONS').

if __name__ == '__main__':
    game = Game()
    game.run()  # Start the game loop.

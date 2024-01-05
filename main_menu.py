import pygame as pg
from settings import *
import sys


class MainMenu:
    def __init__(self, game):
        self.game = game
        self.font = pg.font.Font(None, 36) # TO DO: Customize font
        self.menu_items = ['Start', 'Options', 'Exit']
        self.selected_item = 0

    def draw(self):
        self.game.screen.fill(BACKGROUND_COLOR) # Set the background color.
        for index, item in enumerate(self.menu_items):
            if index == self.selected_item:
                label = self.font.render(f"> {item}", True, SELECTED_ITEM_COLOR)
            else:
                label = self.font.render(item, True, ITEM_COLOR)
            width = label.get_width()
            height = label.get_height()
            posX = (RES[0] - width) // 2
            posY = (RES[1] - height) // 2 + index * 40  # 40 is the vertical space between menu items.
            self.game.screen.blit(label, (posX,posY))

    def update(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_DOWN:
                    self.selected_item = (self.selected_item + 1) % len(self.menu_items)
                elif event.key == pg.K_UP:
                    self.selected_item = (self.selected_item - 1) % len(self.menu_items)
                elif event.key == pg.K_RETURN:
                    self.select_option()

    def select_option(self):
        if self.menu_items[self.selected_item] == 'Start':
            self.game.start_game()
        elif self.menu_items[self.selected_item] == 'Options':
            self.game.show_options()
        elif self.menu_items[self.selected_item] == 'Exit':
            pg.quit()
            sys.exit()
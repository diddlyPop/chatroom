"""
yahtzee.py
Kyle Guss

chatroom client yahtzee?
"""

import pygame
import PySimpleGUI as sg
import os
import random


# --- Globals ---
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GAME_SIZE = (600, 160)
sg.change_look_and_feel("DarkAmber")
# Set the width and height of each snake segment
dice_width = 50
dice_height = 25
dice_margin = 25


dice_events = ['1', '2', '3', '4', '5']

selected_dice = []


class Roll(pygame.sprite.Sprite):
    """ Class to represent one segment of the snake. """
    # -- Methods
    # Constructor function

    def __init__(self, x, placement):
        # Call the parent's constructor
        super().__init__()

        # Set height, width
        self.image = pygame.Surface([dice_width, dice_height])
        self.roll = random.randint(1, 6)          # todo generate random dice roll
        dice_image = f"sprites/{self.roll}.png"
        self.image = pygame.image.load(dice_image)      # TODO fill with roll of dice

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 30

        self.placement = placement

    def __str__(self):
        return f"Roll: {self.roll} @ slot {self.placement}"


class Session:
    """ Class to represent each game instance """
    def __init__(self, players=None):
        if players is None or len(players) < 2:
            print("Need more players to start")
        else:
            self.game_start()

    def session_start(self):
        layout = [
            [sg.Text()],
            [sg.Text('Username: ', size=(15, 1)), sg.InputText('')],
            [sg.Submit(), sg.Quit()]
        ]
        window = sg.Window('Login').Layout(layout)
        event, values = window.Read()
        if event in (None, 'Quit'):
            exit()
        window.close()

# --------------------------- GUI Setup & Create Window -------------------------------


layout = [[sg.Text('YAHTZEE - PySimpleGUI + PyGame')],
          [sg.Graph(GAME_SIZE, (0, 0), GAME_SIZE,
                    background_color='lightgreen', key='-GRAPH-')],
          [sg.Button(button_text="1"), sg.Button(button_text="2"),
           sg.Button(button_text="3"), sg.Button(button_text="4"), sg.Button(button_text="5")],
          [sg.Submit("Reroll"), sg.Exit()]]

window = sg.Window('Yahtzee Game using PySimpleGUI and PyGame',
                   layout, finalize=True)


# ------------------------ Do the magic that integrates PyGame and Graph Element ------------------
graph = window['-GRAPH-']           # type: sg.Graph
embed = graph.TKCanvas
os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
os.environ['SDL_VIDEODRIVER'] = 'windib'

# ----------------------------- PyGame Code -----------------------------
# Call this function so the Pygame library can initialize itself
# pygame.init()
screen = pygame.display.set_mode(GAME_SIZE)
screen.fill(pygame.Color(255, 255, 255))

pygame.display.init()
pygame.display.update()

# Set the title of the window
pygame.display.set_caption('YAHTZEE')

allspriteslist = pygame.sprite.Group()

# Create an initial roll
rolls = []
for i in range(1, 6):
    x = (dice_width + dice_margin) * i
    roll = Roll(x, i)
    rolls.append(roll)
    allspriteslist.add(roll)

print(f"rolls length: {len(rolls)}")

clock = pygame.time.Clock()

while True:
    event, values = window.read(timeout=10)
    if event != "__TIMEOUT__":
        print(event)
    if event in (None, 'Exit'):
        break
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
    if event in dice_events:
        if event in selected_dice:
            selected_dice.remove(event)
        else:
            selected_dice.append(event)
    if event == "Reroll":
        print(f"selected_dice: {selected_dice}")
        for slot in selected_dice:
            pos = int(slot) - 1
            print(f"slot: {slot}")
            x = (dice_width + dice_margin) * int(slot)        # spreads out rolls
            allspriteslist.remove(rolls[pos])                       # remove pygame sprite group
            roll = Roll(x, int(slot))                               # roll a die
            rolls[pos] = roll
            allspriteslist.add(roll)
            for index in rolls:
                print(index)

    # -- Draw everything
    # Clear screen
    screen.fill(BLACK)

    allspriteslist.draw(screen)

    # Flip screen
    pygame.display.flip()


window.close()

from tkinter import Tk
from func import InvaderScreen
screen = Tk()

screen.title("Space Invaders")

screen.geometry("810x710")

screen.iconbitmap(default='data/Blank.ico')

screen.resizable(False, False)

game_screen = InvaderScreen(screen)

game_screen.grid()


while True:
    game_screen.game()
    screen.update()

import os
import tkinter as ttk
from tkinter import *
from SpaceDefenders import load_settings, run_game

def launch():
    """Function to launch the game"""

    #Load files
    config = load_settings('settings.cfg')

    #Get the resolution chosen
    config['game_height'],config['game_width'] = tuple(map(lambda x: int(x), tkvar.get().split("x")))

    #Launch the game
    run_game(config)

    #Quit the launcher
    root.quit()

#If this file is run as main file
if __name__ == "__main__":

    #Create windows
    root = Tk()

    #Set title of window
    root.title("Space Defenders Launcher")

    # Add a grid
    mainframe = Frame(root)
    mainframe.grid(column=0,row=0, sticky=(N,W,E,S) )
    mainframe.columnconfigure(0, weight = 1)
    mainframe.rowconfigure(0, weight = 1)
    mainframe.pack(pady = 100, padx = 100)

    # Create a Tkinter variable
    tkvar = StringVar(root)

    # Set with options
    choices = {'680x510','800x600','1600x1200'}
    tkvar.set('800x600') # set the default option

    popupMenu = OptionMenu(mainframe, tkvar, *choices)
    launchBtn = Button(mainframe, text = "Launch", command = launch)
    Label(mainframe, text="Choose a Resolution").grid(row = 1, column = 1)
    popupMenu.grid(row = 2, column = 1)
    launchBtn.grid(row = 3, column = 1)

    #Launch the launcher
    root.mainloop()

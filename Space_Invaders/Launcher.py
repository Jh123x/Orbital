import os
import tkinter as ttk
import multiprocessing as mp
from tkinter import *
from SpaceDefenders import load_settings, run_game

def launch(result:str, root):
    """Function to launch the game"""

    #Load files
    config = load_settings('settings.cfg')

    #Get the resolution chosen
    config['game_height'],config['game_width'] = tuple(map(lambda x: int(x), result.split("x")))

    #Launch the game
    process = mp.Process(target = run_game, args = (config,))
    process.daemon = False
    process.start()

def main():
    """Main function for the screen launcher"""
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
    choices = {'680x510','800x600'}
    tkvar.set('800x600') # set the default option

    popupMenu = OptionMenu(mainframe, tkvar, *choices)
    launchBtn = Button(mainframe, text = "Launch", command = lambda : launch(tkvar.get(), root))
    Label(mainframe, text="Choose a Resolution").grid(row = 1, column = 1)
    popupMenu.grid(row = 2, column = 1)
    launchBtn.grid(row = 3, column = 1)

    #Launch the launcher
    root.mainloop()

#If this file is run as main file
if __name__ == "__main__":
    main()


import os
import tkinter as tk

import pygame


class Application(tk.Frame):
    def __init__(self, master=None):
        """Main frame for the tkinter window"""
        # Call the superclass
        super().__init__(master)

        # Create a Tkinter string variable
        self.tkvar = tk.StringVar(self.master)

        # Choices
        self.choices = {'680x510', '800x600'}

        # Create layout
        self.set_layout()

        # Create widgets
        self.create_widgets()

    def set_layout(self):
        """Set the layout of the frame"""

        # Set the grid
        self.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

        # Set the maximum column for the configuration
        self.columnconfigure(0, weight=5)

        # Set the maximum number of rows
        self.rowconfigure(0, weight=3)

        # Add the padding of 100 px in both dimensions
        self.pack(pady=100, padx=100)

    def create_widgets(self):
        """Create the widgets"""

        # Set with options
        self.tkvar.set('800x600')  # set the default option

        # Create popup menu
        self.popupMenu = tk.OptionMenu(self, self.tkvar, *self.choices)

        # Create the launch button
        self.launchBtn = tk.Button(self, text="Launch", command=lambda: print("hello"))

        # Create a label
        self.label = tk.Label(self, text="Choose a Resolution")

        # Grid the items
        self.label.grid(row=1, column=2)
        self.popupMenu.grid(row=2, column=2)
        self.launchBtn.grid(row=3, column=2)


def main():
    """Main function for the screen launcher"""

    # Create windows
    root = tk.Tk()

    # Set title of window
    root.title("Space Defenders Launcher")

    # Add a grid
    mainframe = Application(root)

    # Launch the launcher
    root.mainloop()


# If this file is run as main file
if __name__ == "__main__":
    # Run the main function
    main()

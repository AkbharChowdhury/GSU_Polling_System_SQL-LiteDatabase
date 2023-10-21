import tkinter as tk
import tkinter.messagebox as tm
from tkinter import *
from tkinter.ttk import *


class Navigation(Frame):
    def __init__(self, master, can, vote):
        super().__init__(master)
        self.master = master
        self.candidate = can
        self.vote = vote

    """This class is used for navigation purposes using file menu as the primary navgation method
    This class has two functions.
    open_window() - used to redirect to another form by class name
    file menu - used to navigate throughout the system
    """

    def open_window(self, location):  # Opens a new window based on class location
        self.new_window = Toplevel(self.master)
        self.app = location(self.new_window)
        self.master.withdraw()

    def file_menu(self):  # UI without logging in
        menuBar = Menu()
        # Create a pull-down menu for file operations
        module_menu = Menu(menuBar, tearoff=False)
        module_menu.add_command(label="View Candidates", command=lambda: self.open_window(self.candidate))
        module_menu.add_command(label="Vote Candidate", command=lambda: self.open_window(self.vote))
        module_menu.add_command(label="View Results", command=lambda: self.open_window(self.vote))

        menuBar.add_cascade(menu=module_menu, label="File")

        # Create a pull-down menu for help operations
        profile_menu = Menu(menuBar, tearoff=False)
        profile_menu.add_command(label="Logout", command=lambda: self.open_window(Login))
        profile_menu.add_command(label="Exit", command=lambda: exit())
        menuBar.add_cascade(menu=profile_menu, label="Profile")
        self.master.config(menu=menuBar)

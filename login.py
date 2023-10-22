from tkinter.ttk import *
import tkinter.messagebox as tm
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from db import Database
from  main import get_nav
db = Database()
class Login:
    def authenticate(self):
        """This function checks if the login button has been clicked"""
        # check login credentials by calling the is_authorized function from Database class

        if db.is_authorized(self.entry_username.get().strip(), self.entry_password.get()):
            self.nav.open_window(self.candidate)

    def enter_key(self, *args):
        self.authenticate()

    def __init__(self, master, candidate):
        self.master = master
        self.candidate = candidate

        self.master.title("Student Login Form")
        self.master.geometry("350x120")
        self.frame = Frame(self.master)
        self.master.resizable(0, 0)  # set resizable to false

        # login UI
        self.label_username = Label(self.frame, text="Enter username")
        self.label_password = Label(self.frame, text="Enter Password")

        self.entry_username = Entry(self.frame)
        self.entry_password = Entry(self.frame, show="*")
        self.entry_username.focus_set()  # sets focus on username Entry

        self.label_username.grid(row=1, sticky=E)
        self.label_password.grid(row=2, sticky=E)

        self.entry_username.grid(row=1, column=1)
        self.entry_password.grid(row=2, column=1)
        self.entry_password.bind('<Return>', self.enter_key)

        self.login_Button = Button(self.frame, text="Login", command=self.authenticate)
        self.login_Button.grid(columnspan=2)

        self.frame.pack()
        self.nav = get_nav(master)
        self.nav.file_menu()



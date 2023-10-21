# Importing from tkinter library
try:
    from tkinter.ttk import *
    import tkinter.messagebox as tm
    import tkinter as tk
    import tkinter.ttk as ttk
    from datetime import datetime
    from tkinter import *
    # from abc import abc, abstractmethod  # abstract classes

except ImportError:
    pass

from db import Database

# creating an instance of database class
db = Database()


class Navigation:
    def __init__(self, master):
        self.master = master

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
        module_menu.add_command(label="View Candidates", command=lambda: self.open_window(Candidate))
        module_menu.add_command(label="Vote Candidate", command=lambda: self.open_window(Vote))
        module_menu.add_command(label="View Results", command=lambda: self.open_window(Vote))

        menuBar.add_cascade(menu=module_menu, label="File")

        # Create a pull-down menu for help operations
        profile_menu = Menu(menuBar, tearoff=False)
        profile_menu.add_command(label="Logout", command=lambda: self.open_window(Login))
        profile_menu.add_command(label="Exit", command=lambda: exit())
        menuBar.add_cascade(menu=profile_menu, label="Profile")
        self.master.config(menu=menuBar)


class CheckLogin(Navigation):

    def is_logged_in(self):
        if db.get_student_id() is None:
            tm.showerror('Login Error', 'Error: You must be logged in to vote')
            self.open_window(Login)


# ------------------------
# A.2 Login with UID and password class Login
# ------------------------


class Login(Navigation):  # Developed by Akbhar 001084214
    def authenticate(self):
        """This function checks if the login button has been clicked"""
        # check login credentials by calling the is_authorized function from Database class

        if db.is_authorized(self.entry_username.get().strip(), self.entry_password.get()):
            self.open_window(Candidate)

    def enter_key(self, *args):
        self.authenticate()

    def __init__(self, master):
        self.master = master
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


# ------------------------
# A.3 Upload Candidates
# ------------------------

class Candidate(Navigation):

    def __init__(self, master):

        self.master = master

        self.master.title("Candidate Form")
        self.file_menu()
        self.master.geometry("800x500")
        # Create widgets/grid
        self.create_widgets()
        # Populate initial list
        self.populate_list()

    def candidate_listbox(self):
        # Candidate list (listbox)
        self.candidate_list = Listbox(self.master, height=8, width=50, border=0)
        self.candidate_list.grid(row=3, column=0, columnspan=3, rowspan=6, pady=20, padx=20)
        # Create scrollbar
        self.scrollbar = Scrollbar(self.master)
        self.scrollbar.grid(row=3, column=3)
        # Set scrollbar to modules
        self.candidate_list.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.candidate_list.yview)

    def update_candidate_details(self, event):
        self.populate_list()

    def generate_list(self):
        """Get candidate position"""
        position_list = db.get_candidate_positions()  # get positions from database
        # using list comprehension
        # Converting list of tuples into list
        filter_candidate_positions = [item for positions in position_list for item in positions]
        # appending a default value to combo-box
        filter_candidate_positions.insert(0, "View All")
        return filter_candidate_positions

    def search_by_candidate_position(self):
        """filter results"""
        # position widget
        # label
        self.label_position = Label(self.master, text='search by candidate position', font=('bold', 14))
        self.label_position.grid(row=1, column=2, sticky=W)
        # combo
        self.combo_search_position = Combobox(self.master, state='readonly', width=20)
        self.combo_search_position['values'] = self.generate_list()
        self.combo_search_position.current(0)
        self.combo_search_position.grid(row=1, column=3)
        # Bind select from candidate position from como-box
        self.combo_search_position.bind('<<ComboboxSelected>>', self.update_candidate_details)

    def candidate_first_name(self):
        # Candidate first-name
        self.label_firstname = Label(self.master, text='FirstName', font=('bold', 14), pady=20)
        self.label_firstname.grid(row=0, column=0, sticky=W)
        self.firstname_entry = Entry(self.master)
        self.firstname_entry.grid(row=0, column=1)
        self.firstname_entry.focus()

    def candidate_last_name(self):
        # Candidate last-name
        self.label_lastname = Label(self.master, text='Lastname', font=('bold', 14))
        self.label_lastname.grid(row=0, column=2, sticky=W)
        self.lastname_entry = Entry(self.master)
        self.lastname_entry.grid(row=0, column=3)

    def show_candidate_positions(self):
        # Candidate position
        self.candidate_position_label = Label(self.master, text='Candidate Position', font=('bold', 14))
        self.candidate_position_label.grid(row=1, column=0, sticky=W)
        self.combo_candidate_position = Combobox(self.master, state='readonly', width=20)
        self.combo_candidate_position['values'] = tuple(db.get_candidate_positions())
        self.combo_candidate_position.current(0)
        self.combo_candidate_position.grid(row=1, column=1)

    def display_buttons(self):
        # Buttons
        # Add Button
        self.add_candidate_button = Button(self.master, text="Add Candidate", width=12, command=self.add_candidate)
        self.add_candidate_button.grid(row=2, column=0, pady=20)
        # Clear Button
        self.clear_candidate_button = Button(self.master, text="Clear Input", width=12,
                                             command=self.clear_button)
        self.clear_candidate_button.grid(row=2, column=1, pady=20)

    def create_widgets(self):
        # Constructing Candidate UI
        self.candidate_first_name()
        self.candidate_last_name()
        self.show_candidate_positions()
        self.search_by_candidate_position()
        self.candidate_listbox()
        self.display_buttons()

    def populate_list(self):
        self.candidate_list.delete(0, END)
        # Loop through records
        for row in db.get_candidate_by_position(self.combo_search_position.get()):
            # Insert into list
            self.candidate_list.insert(END, row)

        # upload candidate

    def add_candidate(self):
        if self.lastname_entry.get() == '' or self.firstname_entry == '':
            tm.showerror("Required Fields", "Please include all fields")
            return
        # Insert into Candidates table
        db.insert_candidate(self.firstname_entry.get(), self.lastname_entry.get(), self.combo_candidate_position.get())
        # Clear list
        self.candidate_list.delete(0, END)
        # Insert into list

        self.clear_button()
        self.populate_list()

        # Clear all text fields

    def clear_button(self):
        self.lastname_entry.delete(0, END)
        self.firstname_entry.delete(0, END)
        self.frame = Frame(self.master)


# ------------------------
# A.4 Cast Vote
# ------------------------


class Vote(Navigation):

    def __init__(self, master):
        self.master = master
        self.master.title("Vote Form")
        self.file_menu()
        self.master.geometry("700x400")
        # Create widgets/grid
        self.create_widgets()
        # Populate initial list
        self.populate_list()
        # check if user is logged in to vote
        CheckLogin.is_logged_in(self)

    def create_listbox(self):
        # Candidate list (listbox)
        self.candidate_list = Listbox(self.master, height=8, width=50, border=0)
        self.candidate_list.grid(row=4, column=0, columnspan=3, rowspan=6, pady=20, padx=20)
        # Create scrollbar
        self.scrollbar = Scrollbar(self.master)
        self.scrollbar.grid(row=4, column=3)
        # Set scrollbar to modules
        self.candidate_list.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.candidate_list.yview)

    def create_combo_1(self):
        # 1st pref
        self.label_first = Label(self.master, text='1st Preference', font=('bold', 14), pady=20)
        self.label_first.grid(row=0, column=0, sticky=W)

        # combo
        self.comb1 = Combobox(self.master, state='readonly', width=20)
        self.comb1['values'] = tuple(self.get_candidate_name(self.combo_position.get()))
        self.comb1.current(0)
        self.comb1.grid(row=0, column=1)

    def create_combo_2(self):
        # 2nd pref
        # label
        self.label_second = Label(self.master, text='2nd Preference', font=('bold', 14))
        self.label_second.grid(row=0, column=2, sticky=W)
        # combo
        self.comb2 = Combobox(self.master, state='readonly', width=20)
        self.comb2['values'] = tuple(self.get_candidate_name(self.combo_position.get()))
        self.comb2.current(0)
        self.comb2.grid(row=0, column=3)

    def create_combo_3(self):
        # 3rd pref
        self.label_third = Label(self.master, text='3rd Preference', font=('bold', 14))
        self.label_third.grid(row=1, column=0, sticky=W)
        # combo
        self.comb3 = Combobox(self.master, state='readonly', width=20)
        self.comb3['values'] = tuple(self.get_candidate_name(self.combo_position.get()))
        self.comb3.current(0)
        self.comb3.grid(row=1, column=1)

    def create_combo_4(self):
        # 4th pref
        self.label_third = Label(self.master, text='4th Preference', font=('bold', 14))
        self.label_third.grid(row=1, column=2, sticky=W)
        # combo
        self.comb4 = Combobox(self.master, state='readonly', width=20)
        self.comb4['values'] = tuple(self.get_candidate_name(self.combo_position.get()))
        self.comb4.current(0)
        self.comb4.grid(row=1, column=3)

    def select_candidate_details(self, event):
        # refreshing combo-boxes and listbox
        self.populate_list()
        self.create_combo_1()
        self.create_combo_2()
        self.create_combo_3()
        self.create_combo_4()

    def create_widgets(self):

        self.create_listbox()
        # Candidate Position Select
        self.label_select_position = Label(self.master, text='Select Position', font=('bold', 14), pady=20)
        self.label_select_position.grid(row=2, column=0, sticky=W)
        # combo
        self.combo_position = Combobox(self.master, state='readonly', width=20)
        self.combo_position['values'] = tuple(db.get_candidate_positions())
        self.combo_position.current(0)
        self.combo_position.grid(row=2, column=1)
        # Bind select from candidate position from como-box
        self.combo_position.bind('<<ComboboxSelected>>', self.select_candidate_details)

        # constructing UI with combo-boxes
        self.create_combo_1()
        self.create_combo_2()
        self.create_combo_3()
        self.create_combo_4()

        # Buttons
        # Add Button
        self.add_vote_button = Button(self.master, text="Cast Vote", width=12, command=self.add_vote)
        self.add_vote_button.grid(row=3, pady=20)

    def get_candidate_name(self, position):
        return db.candidate_name(position)

    def populate_list(self):
        self.candidate_list.delete(0, END)
        # Loop through records
        for row in db.get_candidate_by_position(self.combo_position.get()):
            # Insert into list
            self.candidate_list.insert(END, row)

    def duplicate_rank_number(self, rank_list):
        """This is function check for duplicate rank numbers"""
        # Compare length for unique elements
        return not len(set(rank_list)) == len(rank_list)

    def add_vote(self):
        """checks for duplicate entries and inserts voting details to the voting table"""
        # retrieving the user preferences 1-4 and the current candidate position
        option_1 = self.comb1.get()
        option_2 = self.comb2.get()
        option_3 = self.comb3.get()
        option_4 = self.comb4.get()
        candidate_position = self.combo_position.get()

        if db.check_duplicate_ranks(candidate_position):  # checking if user has already voted for candidate position
            tm.showerror("duplicate entry", "Error: you have already voted for this position")
            return
            # check for duplicate rank number and if no duplicate rank number is found cast vote

        if self.duplicate_rank_number([option_1, option_2, option_3, option_4]):
            tm.showerror(f"Duplicate Entries",
                         "You cannot select the same preference.\n please enter unique candidates names")
            return

        # Insert into Vote table
        db.insert_vote(option_1, option_2, option_3, option_4, candidate_position)
        # Clear list
        self.candidate_list.delete(0, END)
        # Insert into list
        self.populate_list()


def main():
    """Initialise the Window and class the home class"""
    root = tk.Tk()
    Login(root)  # Start up form
    root.resizable(0, 0)  # set resizable to false
    root.mainloop()


if __name__ == '__main__':
    main()

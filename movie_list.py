# Import the required libraries
from tkinter import *
from tkinter import ttk

from movie import Movie


class MovieList:
    @staticmethod
    def calc_duration(minutes=90):
        h = minutes // 60
        m = minutes % 60
        return f'{h}:{m}'

    def __init__(self, master):
        self.master = master
        self.master.title("Movie List")
        self.master.geometry("900x950")

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.columns = Movie.columns()
        self.col_length = tuple([f"c{i}" for i, column in enumerate(self.columns, start=1)])

        self.tree = ttk.Treeview(self.master, column=self.col_length, show='headings', height=5)
        for i, column in enumerate(self.columns, start=1):
            self.tree.column(f"# {i}", anchor=CENTER)
            self.tree.heading(f"# {i}", text=column)

        movie_data = Movie.get_movie_data()
        for i in movie_data:
            data = movie_data.get(i)
            genres = '/'.join(data.get('genres'))
            lst = [data.get('title'), MovieList.calc_duration(int(data.get('duration'))), data.get('rating'),  genres ]
            print(lst)
            # display
            self.tree.insert('', 'end', text="1", values=lst)

        # for movie in movie_data:
        #     self.tree.insert('', 'end', text="1", values=movie)

        self.tree.pack()


def main():
    import tkinter as tk

    root = tk.Tk()
    MovieList(root)
    root.resizable()
    root.mainloop()


if __name__ == '__main__':
    main()

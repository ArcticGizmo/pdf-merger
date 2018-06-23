import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo


def popup_bonus():
    win = tk.Toplevel()
    win.title('Window')

    label = tk.Label(win, text='Input')
    label.grid(row=0, column=0)

    button = ttk.Button(win, text='Ok', command=win.destroy)
    button.grid(row=1, column=0)


def popup_showinfo():
    showinfo('Info window', 'Hello world')


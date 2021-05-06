import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import os

window=tk.Tk()
window.title("Person Identifier")
window.geometry('300x200')
window.config(bg='#040C23')
img = ImageTk.PhotoImage(Image.open('FCS.png'))
panel = Label(window, image = img, bd=0)
panel.grid(row=0, column=1)

def register():
    window.destroy()
    os.system('python register.py')

def identify():
    window.destroy()
    os.system('python identify.py')

b1 = Button(window, text="Recognize",bg="#0B6563", font = ("Times New Roman", 12), command=identify)
b1.grid(row=1, column=1, padx=40, pady=10)
b2 = Button(window, text="Register", bg="#0B6563", font = ("Times New Roman", 12), command=register)
b2.grid(row=1, column=2, padx=20, pady=10)
l1 = Label(window, text="S.E.I.S", bg="#0B6563", fg="#040C23", justify=tk.LEFT, font = ("Arial", 26))
l1.grid(row=0, column=2)
window.mainloop()
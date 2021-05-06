import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import os
import cv2

global E1
global E2
global E3
global window1

window=tk.Tk()
window.title("Person Identifier")
window.geometry('300x200')
window.config(bg='#040C23')
img = ImageTk.PhotoImage(Image.open('FCS.png'))
panel = Label(window, image = img, bd=0)
panel.grid(row=0, column=1)


def register():
    window1 = tk.Tk()
    window1.title("Register")
    window1.geometry('320x200')
    window1.config(bg='#040C23')

    def click(*args):
        E1.delete(0, 'end')

    def click_num(*args):
        E2.delete(0, 'end')

    def click_desig(*args):
        E3.delete(0, 'end')

    def leave(*args):
        if E1.get() == '':
            E1.insert(0, 'Enter full name')
            window1.focus()

    def leave_num(*args):
        if E2.get() == '':
            E2.insert(0, 'Enter Number')
            window1.focus()

    def leave_desig(*args):
        if E3.get() == '':
            E3.insert(0, 'Enter Designation')
            window1.focus()

    l2 = Label(window1, text="Name:", justify=tk.LEFT, bg='#040C23', fg="#04AC96", font=("Times New Roman", 12))
    l2.grid(row=0, column=1, sticky="W", padx=10)
    E1 = Entry(window1, bd=5, bg="#02574C", fg="white")
    E1.grid(row=0, column=2, padx=40, pady=10)
    E1.insert(0, "Enter full name")
    E1.bind("<Button-1>", click)
    E1.bind("<Leave>", leave)
    l3 = Label(window1, text="Number:", justify=tk.LEFT, bg='#040C23', fg="#04AC96", font=("Times New Roman", 12))
    l3.grid(row=1, column=1, sticky="W", padx=10)
    E2 = Entry(window1, bd=5, bg="#02574C", fg="white")
    E2.grid(row=1, column=2, padx=40, pady=10)
    E2.insert(0, "Enter Number")
    E2.bind("<Button-1>", click_num)
    E2.bind("<Leave>", leave_num)
    l4 = Label(window1, text="Designation:", justify=tk.LEFT, bg='#040C23', fg="#04AC96", font=("Times New Roman", 12))
    l4.grid(row=2, column=1, sticky="W", padx=10)
    E3 = Entry(window1, bd=5, bg="#02574C", fg="white")
    E3.grid(row=2, column=2, padx=40, pady=10)
    E3.insert(0, "Enter Designation")
    E3.bind("<Button-1>", click_desig)
    E3.bind("<Leave>", leave_desig)
    b3 = Button(window1, text="Capture", bg="#0B6563", font=("Times New Roman", 12), command=func1)
    b3.grid(row=3, column=1, padx=20, pady=10, columnspan=2)
    window1.mainloop()

def func1():
    cap = cv2.VideoCapture(0)
    Input_name = str(E1.get())
    Input_name = str.upper(Input_name)
    Input_num = str(E2.get())
    Input_desig = str(E3.get())
    window.destroy()
    haar_file = 'haarcascade_frontalface_default.xml'

    # All the faces data will be
    # present this folder
    datasets = 'datasets'

    # These are sub data sets of folder,
    # for my faces I've used my name you can
    # change the label here
    sub_data = Input_name

    path = os.path.join(datasets, sub_data)
    if not os.path.isdir(path):
        os.mkdir(path)

    # defining the size of images
    (width, height) = (130, 100)

    # '0' is used for my webcam,
    # if you've any other camera
    # attached use '1' like this
    face_cascade = cv2.CascadeClassifier(haar_file)
    webcam = cv2.VideoCapture(0)

    # The program loops until it has 30 images of the face.
    count = 1
    while count < 30:
        (_, im) = webcam.read()
        gray1 = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray1, 1.3, 4)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)
            face = gray1[y:y + h, x:x + w]
            face_resize = cv2.resize(face, (width, height))
            cv2.imwrite('% s/% s.png' % (path, count), face_resize)
        count += 1

        cv2.imshow('OpenCV', im)
        key = cv2.waitKey(10)
        if key == 27:
            break
    window1.destroy()
    cv2.destroyAllWindows()
    cap.release()



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
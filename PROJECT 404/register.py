import tkinter as tk
from tkinter import *
import db_register
from tkinter import messagebox
import cv2
import os
import re

window1 = tk.Tk()
window1.title("Register")
window1.geometry('320x200')
window1.config(bg='#040C23')
cap = cv2.VideoCapture(0)

try:
    def func1():
        Input_name = str(E1.get())
        Input_name = str.upper(Input_name)
        Input_num = str(E2.get())
        Input_desig = str(E3.get())

        if len(Input_name) == 0 or Input_name == 'ENTER FULL NAME':
            messagebox.showwarning("Warning", "Enter valid Name")
            return
        if len(Input_num) == 0 or not re.match('^[789]\d{9}$', Input_num):
            messagebox.showwarning("Warning", "Enter valid Number")
            return
        if len(Input_desig) == 0 or Input_desig == 'Enter Designation':
            messagebox.showwarning("Warning", "Enter valid Designation")
            return

        db_register.insert_db(Input_name, Input_num, Input_desig)
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
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 4)
            for (x, y, w, h) in faces:
                cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)
                face = gray[y:y + h, x:x + w]
                face_resize = cv2.resize(face, (width, height))
                cv2.imwrite('% s/% s.png' % (path, count), face_resize)
            count += 1

            cv2.imshow('OpenCV', im)
            key = cv2.waitKey(10)
            if key == 27:
                break
        window1.destroy()
        cv2.destroyAllWindows()
        os.system('python UI1.py')

except(Exception) as e:
    print("Error",e)

def click(*args):
    E1.delete(0,'end')

def click_num(*args):
    E2.delete(0,'end')

def click_desig(*args):
    E3.delete(0,'end')

def leave(*args):
    if E1.get() == '':
        E1.insert(0,'Enter full name')
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
E1.insert(0,"Enter full name")
E1.bind("<Button-1>",click)
E1.bind("<Leave>",leave)
l3 = Label(window1, text="Number:", justify=tk.LEFT, bg='#040C23', fg="#04AC96", font=("Times New Roman", 12))
l3.grid(row=1, column=1, sticky="W", padx=10)
E2 = Entry(window1, bd=5, bg="#02574C", fg="white")
E2.grid(row=1, column=2, padx=40, pady=10)
E2.insert(0,"Enter Number")
E2.bind("<Button-1>",click_num)
E2.bind("<Leave>",leave_num)
l4 = Label(window1, text="Designation:", justify=tk.LEFT, bg='#040C23', fg="#04AC96", font=("Times New Roman", 12))
l4.grid(row=2, column=1, sticky="W", padx=10)
E3 = Entry(window1, bd=5, bg="#02574C", fg="white")
E3.grid(row=2, column=2, padx=40, pady=10)
E3.insert(0,"Enter Designation")
E3.bind("<Button-1>",click_desig)
E3.bind("<Leave>",leave_desig)
b3 = Button(window1, text="Capture", bg="#0B6563", font=("Times New Roman", 12), command=func1)
b3.grid(row=3, column=1, padx=20, pady=10, columnspan=2)
window1.mainloop()
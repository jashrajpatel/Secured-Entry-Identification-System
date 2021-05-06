import numpy
import os
import cv2
import pyttsx3
import tkinter as tk
global root
Person_name = ""
predicted=0

def SayName(a):
    engine.say("Hello " + str(a))
    engine.runAndWait()

size = 4
haar_file = 'haarcascade_frontalface_default.xml'
datasets = 'datasets'
engine = pyttsx3.init()
# Part 1: Create fisherRecognizer
print('Recognizing Face Please Be in sufficient Lights...')

# Create a list of images and a list of corresponding names
(images, lables, names, id) = ([], [], {}, 0)
for (subdirs, dirs, files) in os.walk(datasets):
    for subdir in dirs:
        names[id] = subdir
        subjectpath = os.path.join(datasets, subdir)
        for filename in os.listdir(subjectpath):
            path = subjectpath + '/' + filename
            lable = id
            images.append(cv2.imread(path, 0))
            lables.append(int(lable))
        id += 1
(width, height) = (130, 100)

# Create a Numpy array from the two lists above
(images, lables) = [numpy.array(lis) for lis in [images, lables]]

# OpenCV trains a model from the images
# NOTE FOR OpenCV2: remove '.face'
model = cv2.face.LBPHFaceRecognizer_create()
model.train(images, lables)
# engine.say(names)
# engine.runAndWait()
# Part 2: Use fisherRecognizer on camera stream
face_cascade = cv2.CascadeClassifier(haar_file)
webcam = cv2.VideoCapture(0)
count = 0
predicted=0
root = tk.Tk()

def back():
    cv2.destroyAllWindows()
    root.destroy()
    exit()

def display(row):
    root.title("Details")
    root.config(bg='#040C23')
    root.geometry("400x200")
    l1 = tk.Label(root, text="Name: ", bg='#040C23', fg="#04AC96", justify=tk.LEFT, font=("Arial", 18))
    l1.grid(row=0, column=1,sticky="W")
    l2 = tk.Label(root, text="Phone: ", bg='#040C23', fg="#04AC96", justify=tk.LEFT, font=("Arial", 18))
    l2.grid(row=1, column=1,sticky="W")
    l3 = tk.Label(root, text="Designation: ", bg='#040C23', fg="#04AC96", justify=tk.LEFT, font=("Arial", 18))
    l3.grid(row=2, column=1, sticky="W")
    l1 = tk.Label(root, text=row[0],  bg='#040C23', fg="#04AC96", justify=tk.LEFT, font=("Arial", 18))
    l1.grid(row=0, column=2, sticky="W")
    l2 = tk.Label(root, text=row[1], bg='#040C23', fg="#04AC96", justify=tk.LEFT, font=("Arial", 18))
    l2.grid(row=1, column=2, sticky="W")
    l3 = tk.Label(root, text=row[2], bg='#040C23', fg="#04AC96", justify=tk.LEFT, font=("Arial", 18))
    l3.grid(row=2, column=2, sticky="W")
    b1 = tk.Button(root, text="Okay", bg="#0B6563",justify=tk.CENTER, font=("Times New Roman", 12), command=back)
    b1.grid(row=3, column=1,columnspan=2, padx=40, pady=10)
    root.mainloop()


def insert_db():
    import pymysql
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="person_identification")
    cursor = connection.cursor()
    sql = "select * from employee where name='%s'"
    args=(Person_name)
    cursor.execute(sql % args)
    row = cursor.fetchone()
    display(row)


while True:
    (_, im) = webcam.read()
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)
        face = gray[y:y + h, x:x + w]
        face_resize = cv2.resize(face, (width, height))
        # Try to recognize the face
        prediction = model.predict(face_resize)
        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 3)
        if predicted!=1:
            if prediction[1] < 500:
                cv2.putText(im, '% s - %.0f' % (names[prediction[0]], prediction[1]), (x - 10, y - 10),
                            cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
                Person_name = names[prediction[0]]
                SayName(Person_name)
                predicted=1
            else:
                cv2.putText(im, 'not recognized', (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))

    cv2.imshow('OpenCV', im)

    if predicted == 1:
        insert_db()
        cv2.destroyAllWindows()
        os.system('python UI1.py')

    key = cv2.waitKey(10)
    if key == 27:
        break
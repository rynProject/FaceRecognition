import urllib
import numpy as np
import mysql.connector
import cv2
import pyttsx3
import pickle
from datetime import datetime

# create database connection
myconn = mysql.connector.connect(host="localhost", user="pmauser", passwd="root", database="facerecognition")
date = datetime.utcnow()
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
cursor = myconn.cursor()

#open camera and detect face
# url = "http://192.168.1.13:8080/shot.jpg"
face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

#recognize and read label from model
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("train.yml")

#create text to speech
engine = pyttsx3.init()
rate = engine.getProperty("rate")
engine.setProperty("rate", 175)

labels = {"person_name": 1}
with open("labels.pickle", "rb") as f:
    labels = pickle.load(f)
    labels = {v: k for k, v in labels.items()}

while True:
    # imgResp = urllib.urlopen(url)
    # imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
    # img = cv2.imdecode(imgNp, 1)
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

    for (x, y, w, h) in faces:
        print(x, w, y, h)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]
        id_, conf = recognizer.predict(roi_gray)
        if conf >= 60:
           print(id_)
           print(labels[id_])
           font = cv2.QT_FONT_NORMAL
           id = 0
           id += 1
           name = labels[id_]
           color = (255, 0, 0)
           stroke = 2
           cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)
           cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), (2))

           select = "SELECT DAY(tanggal), MONTH(tanggal), YEAR(tanggal), nama FROM absen WHERE nama='%s'" % (name)
           nama = cursor.execute(select)
           result = cursor.fetchall()
           data = "error"

           for x in result:
               data = x

           if data == "error":
               # print("Data belum ada")
               insert = "INSERT INTO absen (nama, waktu_absen, tanggal) VALUES (%s, %s, %s)"
               val = (name, current_time, date)
               cursor.execute(insert, val)
               myconn.commit()
               hello = ("Hello ", name, "Have A Nice Day")
               engine.say(hello)

           else:
               hello = ("Hello ", name, "You did attendance today")
               engine.say(hello)

           #Create text to speech


        else:
            color = (255, 0, 0)
            stroke = 2
            font = cv2.QT_FONT_NORMAL
            cv2.putText(cap, "UNKNOWN", (x, y), font, 1, color, stroke, cv2.LINE_AA)
            cv2.rectangle(cap, (x, y), (x + w, y + h), (255, 0, 0), (2))
            engine.say("your face is not recognized")
            engine.runAndWait()
    cv2.imshow('Attendance System', frame)
    k = cv2.waitKey(20) & 0xff
    if k == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

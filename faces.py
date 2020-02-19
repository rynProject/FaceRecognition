import mysql.connector
import cv2
import pyttsx3
import pickle
from datetime import datetime

# create database connection
myconn = mysql.connector.connect(host="localhost", user="pmauser", passwd="root", database="facerecognition")
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
cursor = myconn.cursor()

#open camera and detect face
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
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

    for (x, y, w, h) in faces:
        print(x, w, y, h)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]
        id_, conf = recognizer.predict(roi_gray)
        if conf >= 80:
           print(id_)
           print(labels[id_])
           font = cv2.QT_FONT_NORMAL
           id = 0
           id += 1
           name = labels[id_]
           hello = ("Hello " ,name ,"you have a successful absence, saving absence data")
           color = (255, 0, 0)
           stroke = 2
           cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)
           cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), (2))
           engine.say(hello)
           sql = "INSERT INTO absen (nama, waktu_absen) VALUES (%s, %s)"
           val = (name, current_time)
           cursor.execute(sql, val)
           myconn.commit()
           # print("Berhasil Absen".format(cursor.rowcount))

        else:
            color = (255, 0, 0)
            stroke = 2
            font = cv2.QT_FONT_NORMAL
            # print("Unknown")
            # print("Gagal Absen, Wajah Anda Tidak Di Kenali")
            cv2.putText(frame, "UNKNOWN", (x, y), font, 1, color, stroke, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), (2))
            engine.say("your face is not recognized")
            engine.runAndWait()
    cv2.imshow('Face Absence', frame)
    k = cv2.waitKey(20) & 0xff
    if k == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

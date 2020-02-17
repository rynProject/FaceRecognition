import mysql.connector
import cv2
import pickle
from datetime import datetime

myconn = mysql.connector.connect(host="localhost", user="pmauser", passwd="root", database="facerecognition")
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
cursor = myconn.cursor()

face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("train.yml")

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
        if conf >= 45:
            print(id_)
            print(labels[id_])
            font = cv2.QT_FONT_NORMAL
            name = labels[id_]
            color = (255, 0, 0)
            stroke = 2
            cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), (2))

            sql = "INSERT INTO absen (nama, waktu_absen) VALUES (%s, %s)"
            val = (name, current_time)
            cursor.execute(sql, val)
            myconn.commit()

            print("{} data ditambahkan".format(cursor.rowcount))
        cv2.imshow('Face Detection', frame)
        k = cv2.waitKey(20) & 0xff
        if k == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()
import mysql.connector
from datetime import  datetime

myconn = mysql.connector.connect(host="localhost", user="pmauser", passwd="root", database="facerecognition")
cursor = myconn.cursor()
name = "RYAN"
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
date = datetime.today()
date = date.strftime("%y-%m-%d")
# print(date)
# dt = date.strptime("%YYYY-%MM-%DD")

select_date = "SELECT DAY(tanggal), MONTH(tanggal), YEAR(tanggal), nama FROM absen WHERE nama='%s'" %(name)
nama = cursor.execute(select_date)
result_name = cursor.fetchall()
data = "error"

for x in result_name:
    data = x

if  data == "error":
    # print("Data belum ada")
    insert = "INSERT INTO absen (nama, waktu_absen, tanggal) VALUES (%s, %s, %s)"
    val = (name, current_time, date)
    cursor.execute(insert, val)
    myconn.commit()

else:
    print("Data sudah ada")
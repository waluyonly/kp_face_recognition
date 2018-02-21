import cv2
import numpy as np
import pymysql
import time
import datetime

conn = pymysql.connect(db="facedata", user="root", passwd="",host="localhost",port=3306,autocommit=True)
cursor = conn.cursor()
count = 0
recognizer = cv2.createLBPHFaceRecognizer()
recognizer.load('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
faceCascade = cv2.CascadeClassifier(cascadePath);
font = cv2.FONT_HERSHEY_SIMPLEX
cam = cv2.VideoCapture(0)

while True:
    ret, im =cam.read()
    gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, 1.2,5)
    
    for(x,y,w,h) in faces:
        cv2.rectangle(im, (x-20,y-20), (x+w+20,y+h+20), (0,255,0), 2)
        Id, conf = recognizer.predict(gray[y:y+h,x:x+w])
        
        if (conf<=70):
            if(Id == 5):
                Id = "Waluyo"
                cursor.execute("INSERT INTO facedetect(Id,Name, t1) VALUES(5,'Waluyo', CURRENT_TIMESTAMP);")
                if count>2:
                    break

            elif(Id == 2):
                Id = "WLY"
                cursor.execute("INSERT INTO facedetect(Id,Name, t1) VALUES(2,'WLY', CURRENT_TIMESTAMP);")
                if count>2:
                    break
                
        else:
            Id = "Siapa??"
            cursor.execute("INSERT INTO facedetect(Id,Name, t1) VALUES(0,'Siapa?', CURRENT_TIMESTAMP);")
            if count>2:
                break


        cv2.rectangle(im, (x-22,y-90), (x+w+22, y-22), (0,255,0), -1)
        cv2.putText(im, str(Id), (x,y-40), font, 2, (255,255,255), 3)
        eyes = eye_cascade.detectMultiScale(gray, 1.2, 5)

        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(im, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

    cv2.imshow('DETECT',im) 
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
    
   
cursor.execute("SELECT * FROM facedetect WHERE ID=100")
results = cursor.fetchall()

for row in results:
    print row[0]
               
cam.release()
cv2.destroyAllWindows()

conn.commit()
cursor.close()
conn.close()

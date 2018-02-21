import cv2
vid_cam = cv2.VideoCapture(0)
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eyceglasses_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
face_id = 1
count = 0

while(True):
    _, image_frame = vid_cam.read()
    gray = cv2.cvtColor(image_frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)
    
    for (x,y,w,h) in faces:
        count += 1
        cv2.imwrite("datasets/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
        cv2.imshow('frame', image_frame)
        
        eyeglasses = eyceglasses_cascade.detectMultiScale(image_frame)
        for (gx,gy,gw,gh) in eyeglasses:
            cv2.rectangle(image_frame,(gx,gy), (gx+gw, gy+gh), (0,0,255),2)

    if cv2.waitKey(200) & 0xFF == ord('q'):
        break
    
    elif count>10:
        break

vid_cam.release()
cv2.destroyAllWindows()

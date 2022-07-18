import cv2
import serial

eye = cv2.CascadeClassifier("eye_cascade")
face = cv2.CascadeClassifier("face_cascade.xml")
video = cv2.VideoCapture(0)
x = 0

while True:
    grapped , frame = video.read()

    frame = cv2.flip(frame , 1)
    gray = cv2.cvtColor (frame , cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray , 7 , 31 , 31)
    faces = face.detectMultiScale(gray)
    
    if len(faces)>0:
        for (x,y,w,h) in faces:
            frame = cv2.rectangle(frame , (x,y),(x+w , y+h) , (0,255,0) , 5)
            x_center = int ((x + (x+w)/2))
            y_center = int ((y + (y+h)/2))
            print (f"{x_center} {y_center}")
            face_part = gray [y:y+h,x:x+w]
            eyes = eye.detectMultiScale(face_part)
            print(eyes)
            if len (eyes) >= 2:
                cv2.putText (frame , "Eyes Open" , (70,70) , cv2.FONT_HERSHEY_PLAIN , 3 , (255,0,0) , 3)
                x = 1
            else:
                cv2.putText (frame , "Eyes Close" , (70,70) , cv2.FONT_HERSHEY_PLAIN , 3 , (0,0,255) , 3)
                x = 0
    else:
        cv2.putText (frame , "No Face" , (70,70) , cv2.FONT_HERSHEY_PLAIN , 3 , (0,0,0) , 3)

    x = str(x)
    cv2.imshow("Video2",frame)
    if cv2.waitKey(1) & 0xFF == ord ('q'):
        break

video.release()
cv2.destroyAllWindows()

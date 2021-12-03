import cv2  
import os  
import time

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
video = cv2.VideoCapture(0);

count = 0
directory = "knownImages"

#os.mkdir(directory)
path = "/root/projects/projectFelix/faceAuthentication/"

fullPath = os.path.join(path, directory)
os.chdir(directory)
while True:
    check, frame = video.read();
    faces = face_cascade.detectMultiScale(frame,scaleFactor=1.1, minNeighbors=5);
    for x,y,w,h in faces:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 3);
        roiColor = frame[y:y + h, x:x + w]
    cv2.imshow('Face Detector', frame);

    key = cv2.waitKey(1000);
    
    #if key == ord('q'):
    imageName = "Image{}.jpg".format(count)
    cv2.imwrite(imageName, roiColor)
    count += 1
    break;


video.release();
cv2.destroyAllWindows();

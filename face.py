import cv2
import numpy as np
from flask import Flask, render_template,Blueprint,Response
import pickle
import face_recognition
import os
import numpy as np
import cvzone
from datetime import datetime

face=Blueprint('face',__name__)


def gen_frames():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    imgBackground = cv2.imread('/home/hacker/Desktop/pro/resources/background.png')

    folderModePath = '/home/hacker/Desktop/pro/resources/Modes'
    modePathList = os.listdir(folderModePath)
    imgModeList = []
    for path in modePathList:
        imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))

    print("Loading Encode File....")
    file = open('pro/EncodeFile.p', 'rb')
    encodeListKnownWithIds = pickle.load(file)
    file.close()
    encodeListKnown, studentIds = encodeListKnownWithIds
    print("Encode File Loaded")

    modeType = 0
    counter = 0
    id = -1
    imgStudent = []

    while True:
        success, img = cap.read()

        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        faceCurrentFrame = face_recognition.face_locations(imgS)
        encodeCurrentFrame = face_recognition.face_encodings(imgS, faceCurrentFrame)

        imgBackground[162:162 + 480, 55:55 + 640] = img
        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

        if faceCurrentFrame:

            for encodeFace, faceLoc in zip(encodeCurrentFrame, faceCurrentFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDistance = face_recognition.face_distance(encodeListKnown, encodeFace)

                matchIndex = np.argmin(faceDistance)

                if matches[matchIndex]:
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1 
                    imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                    id = studentIds[matchIndex]

                    if counter == 0:
                        cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                        counter = 1
                        modeType = 1

            if counter != 0:
                if counter == 1:
                    # Load student info directly from the filesystem or any other storage
                    student_info_path = f'student_info/{id}.txt'
                    with open(student_info_path, 'r') as f:
                        student_info = f.read()
                    print(student_info)

                    # Load student image directly from the filesystem or any other storage
                    img_student_path = f'student_images/{id}.png'
                    imgStudent = cv2.imread(img_student_path)

                if modeType != 3:
                    if 10 < counter < 20:
                        modeType = 2

                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                    if counter <= 10:
                        cv2.putText(imgBackground, str(student_info), (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

                        imgBackground[175:175 + 216, 909:909 + 216] = imgStudent

                    counter += 1

                    if counter >= 20:
                        counter = 0 
                        modeType = 0
                        student_info = {}
                        imgStudent = []
                        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
        else:
            modeType = 0
            counter = 0

        ret, buffer = cv2.imencode('.jpg', imgBackground)
        imgBackground = cv2.imdecode(buffer, 1)
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')




@face.route('/face')
def facef():

    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from PyQt5.QtWidgets import QMessageBox
import time

import pandas as pd


def collect(path='std_images_faces'):
    images, classname = [], []
    mylist = os.listdir(path)
    print(mylist)
    for cl in mylist:
        curimg = cv2.imread(f'{path}/{cl}')
        images.append(curimg)
        classname.append(os.path.splitext(cl)[0])
        # print(classname)
    return images, classname


# encode images
def findencodeings(images):
    encodlist = []
    for img in images:
        print('ok')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodes = face_recognition.face_encodings(img)
        if encodes != []:
            encodlist.append(encodes[0])
            print(encodes[0])
    return encodlist


# report
# ___________________NEW Attendence__________________________
# _________________________________________________
def markattendance(name, self=None):
    namelist = set([x.split('\t')[0] for x in open('attendace.txt').read().split('\n')])
    print(namelist)

    if name not in namelist:
        now = datetime.now()
        dtstring = now.strftime("%H:%M:%S")
        f = open('attendace.txt', 'a')
        f.write(f'{name}\t{dtstring}\n')
        f.close()


def train():
    imgs, _ = collect()
    encodelistknown = findencodeings(imgs)
    print('Encoding complete')
    return encodelistknown
    # print(len(encodelistknown))
    # صور في مصفوفه مع عددهن


def run(encodelistknown):
    if 'attendace.txt' not in os.listdir('.'):
        f = open('attendace.txt', 'w')
        f.close()
        # namelist = set([x.split('\t')[0] for x in open('attendace.txt').read().split('\n')])
    elif QMessageBox.question(None, "Question", "Create new attendance file?",
                              (QMessageBox.Yes | QMessageBox.No)) == QMessageBox.Yes:
        f = open('attendace.txt', 'w')
        f.close()
    _, classname = collect()
    cap = cv2.VideoCapture(0,cv2.CAP_V4L2)
    while True:
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        facesCurFrame = face_recognition.face_locations(imgS)[:]  # ايجاد location imges
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        print(encodesCurFrame)
        # الان خطوه مقارنه للوجوه encodings

        for encodeface, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodelistknown, encodeface)
            faceDis = face_recognition.face_distance(encodelistknown, encodeface)
            #print(faceDis)
            matchIndex = np.argmin(faceDis)
            try:
                if matches[matchIndex]:
                    name = classname[matchIndex].upper().split('_')[0]
                    print(name)
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                    markattendance(name)
                    # mark_attendance_new(name)
            except IndexError:
                pass
        cv2.imshow('webcam', img)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break
            cap.release()
            cv2.destroyAllWindows()
        # الى هنا تفتح الكامره وتتعرف على وجه

# import numpy as np
import cv2
import pickle


def run():
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    # recognizer = cv2.face.createLBPHFaceRecognizer()
    recognizer.read("./trainner.yml")

    # labels = {"person_name": 1}
    with open("labels.pickle", 'rb') as f:
        og_labels = pickle.load(f)
        labels = {v: k for k, v in og_labels.items()}
        print(labels)
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        for (x, y, w, h) in faces:
            print(x, y, w, h)
            roi_gray = gray[y:y + h, x:x + w]  # (ycord_start, ycord_end)
            # roi_color = frame[y:y + h, x:x + w]
            # .cv2.imshow('frame',roi_color)
            # recognize? deep learned model predict keras tensorflow pytorch scikit learn
            id_, conf = recognizer.predict(roi_gray)
            print(conf)
            #if conf >= 0.0 or conf <= 95:
            if conf < 37:
                print(id_)
                print(labels[id_])
                font = cv2.FONT_HERSHEY_SIMPLEX
                name = labels[id_]
                color = (255, 255, 255)
                stroke = 2
                cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)
            # img_item = "my-image.png"
            # cv2.imwrite(img_item, roi_color) #Save face to file

            # Draw rectangle around face
            color = (255, 0, 0)  # BGR 0-255
            stroke = 2
            end_cord_x = x + w
            end_cord_y = y + h
            cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)

            # Display the resulting frame
        cv2.imshow('frame', frame)
        print('ok')
        # if cv2.waitKey(20) & 0xFF == ord('q'):
        #    cap.release()
        #    cv2.destroyAllWindows()
        # break
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break
            cap.release()
            cv2.destroyAllWindows()

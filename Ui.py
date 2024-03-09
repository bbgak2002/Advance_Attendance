import os
import sqlite3
import sys
from datetime import date
from os import mkdir
from os.path import exists

import pickle
import att
import cv2
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMessageBox
from PyQt5.uic import loadUi

import lina_ex as detect


class Ui1(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui1, self).__init__()
        loadUi('first.ui', self)
        self.button = self.findChild(QtWidgets.QPushButton, 'pushButton')
        self.button.clicked.connect(self.saveButtonPressed)

    def saveButtonPressed(self):
        window1.hide()
        window2.show()


class Ui2(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui2, self).__init__()
        loadUi('second.ui', self)
        self.count = 0
        # self.msgbox = QMessageBox()
        self.connect_db()
        # self.chk_tables()
        self.user = ''
        self.nameADMText = self.findChild(QtWidgets.QLineEdit, 'nameADM')
        self.passwardText = self.findChild(QtWidgets.QLineEdit, 'passward')
        self.passwardText.setEchoMode(QtWidgets.QLineEdit.Password)
        self.alarmLabel = self.findChild(QtWidgets.QLabel, 'alarm')

        self.loginb = self.findChild(QtWidgets.QPushButton, 'login')
        self.quitb = self.findChild(QtWidgets.QPushButton, 'quit')

        self.loginb.clicked.connect(self.login_click)
        self.quitb.clicked.connect(self.Quit)

    def connect_db(self):
        try:
            self.conn = sqlite3.connect('FaceRecognition.db')
            self.sql = self.conn.cursor()
        except sqlite3.Error as error:
            self.Message(error)

    # def chk_tables(self):
    #   try:
    #       statement = """CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)"""
    #       self.sql.execute(statement)
    #       statement = """CREATE TABLE IF NOT EXISTS students (std_id INT, std_name TEXT, std_class TEXT, std_gender TEXT, std_email TEXT, std_images TEXT)"""
    #       self.sql.execute(statement)
    #       statement = """CREATE TABLE IF NOT EXISTS courses (crs_id INT, crs_name TEXT, crs_class TEXT, crs_students TEXT)"""
    #       self.sql.execute(statement)
    # Add more tables here
    #       self.conn.commit()
    #   except sqlite3.Error as error:
    #       self.message(error)

    def Message(self, text):
        QMessageBox.about(self, 'error', text)

    def Quit(self):
        self.conn.close()
        cv2.destroyAllWindows()
        exit(0)

    def login_click(self):
        # print(self.count)
        if self.nameADMText.text() != '' and self.passwardText.text() != '' and self.count < 3:
            self.count = self.count + 1
            statement = f"SELECT AdminName, Password from users WHERE AdminName='{self.nameADMText.text()}' AND Password ='{self.passwardText.text()}';"
            self.sql.execute(statement)
            if self.sql.fetchone():
                print('ok')
                self.user = self.nameADMText.text()
                self.alarmLabel.setText("Login Successfully")

            else:
                self.alarmLabel.setText("Teacher Login!")
                self.nameADMText.clear()
                self.passwardText.clear()
                self.user = 'teacher'
        else:
            self.alarmLabel.setText("Teacher Login!")
            self.nameADMText.clear()
            self.passwardText.clear()
            self.user = 'teacher'

        self.window3 = Ui3(self.user)
        window2.hide()
        self.window3.show()

        # else:
        #    if self.count < 3:
        #        self.Message('Please fill the fields.')
        #    else:
        #        self.alarmLabel.setText("Access denied")
        #        self.nameADMText.setEnabled(False)
        #        self.passwardText.setEnabled(False)


class Ui3(QtWidgets.QMainWindow):
    def __init__(self, user):
        super(Ui3, self).__init__()
        loadUi('fourth1.ui', self)
        self.user = user

        self.button = self.findChild(QtWidgets.QPushButton, 'saveButton')
        self.admtext = self.findChild(QtWidgets.QLineEdit, 'nameADM')
        self.pasText = self.findChild(QtWidgets.QLineEdit, 'paswardd')
        self.repasText = self.findChild(QtWidgets.QLineEdit, 'repasward')

        self.cancelbutton = self.findChild(QtWidgets.QPushButton, 'cancel')

        self.addbutton = self.findChild(QtWidgets.QPushButton, 'add')
        self.clearbutton = self.findChild(QtWidgets.QPushButton, 'clear')
        self.capturebutton = self.findChild(QtWidgets.QPushButton, 'start')
        self.datasetbutton = self.findChild(QtWidgets.QPushButton, 'ShowDS2')
        # ______________________________________update frame widget_________________

        self.listv = self.findChild(QtWidgets.QListWidget, 'list')
        self.text_id = self.findChild(QtWidgets.QLineEdit, 'id')
        self.text_name = self.findChild(QtWidgets.QLineEdit, 'id_name')
        self.stagetxt = self.findChild(QtWidgets.QLineEdit, 'stage_txt')
        self.styptxt = self.findChild(QtWidgets.QLineEdit, 'styp_txt')
        self.branch_txt = self.findChild(QtWidgets.QLineEdit, 'branch_txt')
        self.gender_txt = self.findChild(QtWidgets.QLineEdit, 'gender_txt')
        self.email_txt = self.findChild(QtWidgets.QLineEdit, 'email_txt')
        self.updatebutton = self.findChild(QtWidgets.QPushButton, 'update_butt')
        self.updatebutton.clicked.connect(self.Update_St_DB_ButtonPressed)
        self.deletbutton = self.findChild(QtWidgets.QPushButton, 'deletST')
        self.deletbutton.clicked.connect(self.deleteRecord)

        # _______________________________________________________________________
        self.idText = self.findChild(QtWidgets.QLineEdit, 'st_id')
        self.nameText = self.findChild(QtWidgets.QLineEdit, 'st_name')
        self.departmentcom = self.findChild(QtWidgets.QComboBox, 'department')
        self.classcombo = self.findChild(QtWidgets.QComboBox, 'stage')
        self.studytype_combo = self.findChild(QtWidgets.QComboBox, 'study_type')
        self.branch_combo = self.findChild(QtWidgets.QComboBox, 'branch')
        self.gendercombo = self.findChild(QtWidgets.QComboBox, 'gender')
        self.emailText = self.findChild(QtWidgets.QLineEdit, 'email')
        self.trainbutton = self.findChild(QtWidgets.QPushButton, 'start_training')
        self.recognizebutton = self.findChild(QtWidgets.QPushButton, 'f_recognation')
        self.logoutbtn = self.findChild(QtWidgets.QPushButton, 'logout')
        self.exitbtn = self.findChild(QtWidgets.QPushButton, 'exit')

        self.tabs = self.findChild(QtWidgets.QTabWidget)
        self.tab1 = self.tabs.findChild(QtWidgets.QWidget, 'edit_tab')
        self.tab2 = self.tabs.findChild(QtWidgets.QWidget, 'Add_tab')
        self.tab3 = self.tabs.findChild(QtWidgets.QWidget, 'update_tab')
        self.tab4 = self.tabs.findChild(QtWidgets.QWidget, 'dataset_tab')
        self.tab5 = self.tabs.findChild(QtWidgets.QWidget, 'train_tab')
        self.tab6 = self.tabs.findChild(QtWidgets.QWidget, 'recognizer_tab')
        self.tab7 = self.tabs.findChild(QtWidgets.QWidget, 'report_tab')

        self.button.clicked.connect(self.EditDB_ButtonPressed)
        self.cancelbutton.clicked.connect(self.cancelpressed)
        self.clearbutton.clicked.connect(self.clearpressed)
        self.addbutton.clicked.connect(self.addButtonPressed)
        self.recognizebutton.clicked.connect(self.Recognition)
        self.logoutbtn.clicked.connect(self.log_out)
        self.exitbtn.clicked.connect(self.quit)
        self.datasetbutton.clicked.connect(self.show_dataset)

        self.capturebutton.clicked.connect(self.start_camera)
        self.capturebutton.setEnabled(False)
        self.cameraLabel = self.findChild(QtWidgets.QLabel, 'camera_label')
        self.cameraLabel.setScaledContents(True)
        self.stopCameraButton = self.findChild(QtWidgets.QPushButton, 'stop')
        self.stopCameraButton.clicked.connect(self.stop_Capture)
        self.stopCameraButton.setEnabled(False)
        self.takePhotoBtn = self.findChild(QtWidgets.QPushButton, 'capture')
        self.takePhotoBtn.clicked.connect(self.Capture)
        self.takePhotoBtn.setEnabled(False)
        self.trainbutton.clicked.connect(self.train)

        self.showDBButton = self.findChild(QtWidgets.QPushButton, 'showAllDB')
        self.showDBButton.clicked.connect(self.show_all_DB)

        self.listv.clicked.connect(self.clicked)
        # ________________________________________________________________________
        self.teacher_Text = self.findChild(QtWidgets.QLineEdit, 'teacher_name')
        self.course_combo = self.findChild(QtWidgets.QComboBox, 'co_department_2')
        self.dep_combo = self.findChild(QtWidgets.QComboBox, 'co_department')
        self.branch_combo = self.findChild(QtWidgets.QComboBox, 'co_branch')
        self.semester_combo = self.findChild(QtWidgets.QComboBox, 'semester')
        self.class_2_combo = self.findChild(QtWidgets.QComboBox, 'class_2')
        self.units_combo = self.findChild(QtWidgets.QComboBox, 'units')

        self.showrep_button = self.findChild(QtWidgets.QPushButton, 'showreport')
        self.showrep_button.clicked.connect(self.show_att_rep)
        self.export_button = self.findChild(QtWidgets.QPushButton, 'export_report')
        self.export_button.clicked.connect(self.export_report1)
        self.studytype = self.findChild(QtWidgets.QComboBox, 'study_type_2')
        self.lis_report = self.findChild(QtWidgets.QListWidget, 'list_2')
        self.reset_rep_button = self.findChild(QtWidgets.QPushButton, 'reset')
        self.reset_rep_button.clicked.connect(self.reset_att_rep)
        # _____________________________________________________________________________
        self.demo_image = 'cam5.jpg'
        self.out_folder = 'std_images_faces'
        if not exists(self.out_folder):
            mkdir(self.out_folder)
        self.image_count = 5
        self.std_images = []
        self.chk_login()

    # _______________________________________update students database_________________________

    def chk_login(self):
        if 'admin' in self.user:
            self.admin = True
            print('admin login')
            self.tabs.setCurrentIndex(1)
            self.tab1.setEnabled(True)
            self.tab2.setEnabled(True)
            self.tab3.setEnabled(True)
            self.tab4.setEnabled(True)
            self.tab5.setEnabled(True)

        else:
            self.admin = False
            print('user login')
            self.tabs.setCurrentIndex(5)
            self.tab1.setEnabled(False)
            self.tab2.setEnabled(False)
            self.tab3.setEnabled(False)
            self.tab4.setEnabled(False)
            self.tab5.setEnabled(False)

    def show_all_DB(self):
        print('showdb')
        conn = sqlite3.connect('FaceRecognition.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM students")
        rows = cur.fetchall()
        print(len(rows))
        c = 0
        conn.close()
        self.listv.clear()
        for i in rows:
            print(i)
            self.listv.insertItem(c, str(i))
            c = c + 1

    def clicked(self):
        # item = self.listv.currentIndex()
        # idx=item.row()+1
        item = self.listv.currentItem()
        arr = item.text().split(",")
        self.text_id.setText(arr[1].split(' ')[1].replace("'", ""))
        self.text_name.setText(arr[2].replace("'", ""))
        self.stagetxt.setText(arr[4].replace("'", ""))
        self.styptxt.setText(arr[5].replace("'", ""))
        self.branch_txt.setText(arr[6].replace("'", ""))
        self.gender_txt.setText(arr[7].replace("'", ""))
        self.email_txt.setText(arr[8].replace("'", ""))

    def deleteRecord(self):
        # item = self.listv.currentIndex()
        # idx=item.row()
        d = self.text_id.text()
        nam = self.text_name.text()
        data = [(d)]
        print(data)
        statement = """DELETE from students Where st_id=? """
        print(statement)
        # statement2 = """select ID from users AdminName = ?"""
        try:
            # window2.sql.execute(statement, data)
            window2.sql.execute(statement, data)
            window2.conn.commit()
            self.Message(f'Delete successfully.')
        except sqlite3.Error as error:
            self.Message(f'Error of deleting Student information: {error}')
        print(nam, self.out_folder)
        for n in os.listdir(self.out_folder):
            if nam.lower() == (n.split('_')[0].lower()):
                file = self.out_folder + n
                # if os.path.isfile(file):
                print('Deleting file:', file)
                os.remove(file)

    def Update_St_DB_ButtonPressed(self):
        d = self.text_id.text()
        data = (self.text_name.text(), self.stagetxt.text(), self.styptxt.text(), self.branch_txt.text(),
                self.gender_txt.text(), self.email_txt.text(), d)
        statement = """Update students set name=?,stage=?,study_type=?,branch=?,gender=?,email=? WHERE st_id=? """  # VALUES (?,?,?,?,?,?,?)"""
        print(statement)
        # statement2 = """select ID from users AdminName = ?"""
        try:
            # window2.sql.execute(statement, data)
            window2.sql.execute(statement, data)
            window2.conn.commit()
            self.Message(f'Student {self.admtext.text()} update successfully.')
        except sqlite3.Error as error:
            self.Message(f'Error updating new Student information: {error}')
        # else:
        #   self.Message('updating error')

    # _______________________________________Show the dataset of students images_______________
    def show_dataset(self):
        print('dataset')
        path = 'std_images_faces'
        images = []
        classname = []
        mylist = os.listdir(path)
        print(mylist)
        for cl in mylist:
            print(cl)
            cur = cv2.imread(f'{path}/{cl}')
            images.append(cur)
        # cv2.imshow('mmmm',curimg)

        n_col = len(mylist)
        n_row = 1
        # Function to plot images in 3 * 4
        # def plot_gallery(images, titles, h, w, n_row = 3, n_col = 4):
        plt.figure(figsize=(1.8 * n_col, 2.4 * n_row))
        plt.subplots_adjust(bottom=0, left=.01, right=.99, top=.90, hspace=.35)
        for i in range(n_row * n_col):
            plt.subplot(n_row, n_col, i + 1)
            plt.imshow(images[i])  # .reshape((h, w)), cmap = plt.cm.gray)
            plt.title(mylist[i], size=12)
        #  plt.xticks(())
        #  plt.yticks(())
        plt.show()

    # _____________________________________________________________________________________
    # ___________________________________Attendance Report__________________________________________________
    def export_report1(self):
        f1 = open('Attendance_Report.txt', 'w')
        for i in range(self.lis_report.count() - 1):
            f1.write(self.lis_report.item(i).text() + '\n')
        f1.close()
        self.Message('File (Attendance_Report.txt) exported Successfully.')

    def show_att_rep(self):
        f = open('attendace.txt').read().split('\n')
        today = date.today()
        self.lis_report.insertItem(0, '================ Students Attendance Report =================')
        self.lis_report.insertItem(1,
                                   'Department: ' + self.departmentcom.currentText() + '\t\tSemester: ' + self.semester_combo.currentText())
        self.lis_report.insertItem(2,
                                   'Stage     : ' + self.classcombo.currentText() + '-' + self.studytype.currentText() + '\t\tBranch: ' + self.branch_combo.currentText() + '\t\tDate: ' + today.strftime(
                                       "%d/%m/%Y"))
        self.lis_report.insertItem(3,
                                   'Course Name: ' + self.course_combo.currentText() + '\t\tAttendant Hours: ' + self.units_combo.currentText())
        self.lis_report.insertItem(4, 'Instructor: ' + self.teacher_Text.text())
        self.lis_report.insertItem(5, '===================================================================')

        for i, st in enumerate(f):
            self.lis_report.insertItem(i + 7, f'{i + 1}.  ' + st)
        print(self.lis_report.count())

    def reset_att_rep(self):
        self.lis_report.clear()

    # __________________________________________________________________________________________

    def Message(self, text):
        QMessageBox.about(self, 'Message', text)

    def train(self):
        self.encodelist = att.train()
        self.Message('Training Complete')
        f = open('trained_objects.obj', 'ab')
        pickle.dump(self.encodelist, f)
        f.close()

    def Recognition(self):
        if 'trained_objects.obj' in os.listdir('.'):
            f = open('trained_objects.obj', 'rb')
            self.encodelist = pickle.load(f)
            f.close()
        else:
            self.train()
        att.run(self.encodelist)

    def insertDB_ButtonPressed(self):
        # print(self.nameText.text())
        data = (
            self.idText.text(), self.nameText.text(), self.departmentcom.currentText(), self.classcombo.currentText(),
            self.studytype_combo.currentText(), self.branch_combo.currentText(), self.gendercombo.currentText(),
            self.emailText.text())
        statement = """INSERT INTO students (st_id,name,department,stage,study_type,branch,gender,email) VALUES (?,?,?,?,?,?,?,?)"""
        try:
            window2.sql.execute(statement, data)
            window2.conn.commit()
            self.Message(f'User {self.admtext.text()} added successfully.')
        except sqlite3.Error as error:
            self.Message(f'Error adding new student information: {error}')

    def EditDB_ButtonPressed(self):
        n = window2.nameADMText.text()
        if len(self.admtext.text()) != 0 and len(self.pasText.text()) != 0:
            data = (self.pasText.text(), n)
            statement = """Update users set Password = ? where AdminName = ?"""
            # statement2 = """select ID from users AdminName = ?"""
            try:
                # window2.sql.execute(statement, data)
                window2.sql.execute(statement, data)
                window2.conn.commit()
                self.Message(f'User {self.admtext.text()} update successfully.')
            except sqlite3.Error as error:
                self.Message(f'Error updating new admin information: {error}')
        else:
            self.Message('updating error')

    def cancelpressed(self):
        self.pasText.setText('')
        self.repasText.setText('')
        self.admtext.setText('')

    def addButtonPressed(self):
        print('add')
        print(self.nameText.text())
        if len(self.idText.text()) != 0 and \
                len(self.departmentcom.currentText()) != 0 and \
                len(self.classcombo.currentText()) != 0 and \
                len(self.studytype_combo.currentText()) != 0 and \
                len(self.branch_combo.currentText()) != 0 and \
                len(self.gendercombo.currentText()) != 0 and \
                len(self.emailText.text()) != 0:
            # self.out_folder += f'{self.nameText.text()}_{self.idText.text()}'
            self.addbutton.setEnabled(False)
            self.capturebutton.setEnabled(True)
            self.insertDB_ButtonPressed()

        else:
            self.Message('Please fill all fields')

    def log_out(self):
        window2.window3.hide()
        window2.nameADMText.clear()
        window2.passwardText.clear()
        window2.alarmLabel.clear()
        window2.show()

    def quit(self):
        cv2.destroyAllWindows()
        exit(0)

    def clearpressed(self):
        print('clear')
        self.idText.setText('')
        self.nameText.setText('')
        # self.departmentcom.clear()
        # self.classcombo.clear()
        # self.studytype_combo.clear()
        # self.branch_combo.clear()
        # self.gendercombo.clear()
        self.emailText.setText('')
        self.addbutton.setEnabled(True)
        self.capturebutton.setEnabled(False)
        self.takePhotoBtn.setEnabled(False)
        self.stopCameraButton.setEnabled(False)
        self.out_folder = 'std_images_faces'

    # @pyqtSlot()
    def start_camera(self):
        self.capturebutton.setEnabled(False)
        self.takePhotoBtn.setEnabled(True)
        self.stopCameraButton.setEnabled(True)
        self.cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
        while self.cap.isOpened():
            ret, img = self.cap.read()
            if ret:
                img = detect.detect2(img)
                self.displayImage(img[0])
                cv2.waitKey(500)

    # @pyqtSlot()
    def stop_Capture(self):
        self.cap.release()
        img = cv2.imread(self.demo_image)
        img = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
        self.cameraLabel.setPixmap(QPixmap.fromImage(img))
        self.stopCameraButton.setEnabled(False)
        self.capturebutton.setEnabled(True)

    def displayImage(self, img):
        img = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
        img = img.rgbSwapped()
        self.cameraLabel.setPixmap(QPixmap.fromImage(img))

    # @pyqtSlot()
    def Capture(self):
        if not exists(self.out_folder):
            mkdir(self.out_folder)
        try:
            for i in range(self.image_count):
                flag, frame = self.cap.read()
                imagen = self.nameText.text()
                if flag:
                    img = detect.detect2(frame)
                    # path = f'{self.out_folder}\\image_{i + 1}.jpg'
                    path = f'{self.out_folder}/{self.nameText.text()}_{i + 1}.jpg'
                    # self.std_images.append(path)
                    cv2.imwrite(path, img[1])
                    self.takePhotoBtn.setText(f'Capture ({i + 1}/{self.image_count})')
                    cv2.waitKey(1000)
            self.takePhotoBtn.setEnabled(False)
            self.Message('Captured Images Saved Successfully!')
            print(self.std_images)

        except QPictureIO:
            self.Message('Destination folder error.')


app = QtWidgets.QApplication(sys.argv)
window1 = Ui1()
window1.show()
window2 = Ui2()
app.exec_()

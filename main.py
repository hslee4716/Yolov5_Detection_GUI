# -*- coding: cp949 -*- 
from custom_detect_module import yolov5_custom
from glob import glob
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import QImage, QPixmap, QPalette
from PyQt5.QtWidgets import *
import cv2
import os, sys, time

import tkinter
from tkinter import filedialog

IMG_FORMATS = ['bmp', 'jpg', 'jpeg', 'png', 'tif', 'tiff', 'dng', 'webp', 'mpo']  # acceptable image suffixes
VID_FORMATS = ['mov', 'avi', 'mp4', 'mpg', 'mpeg', 'm4v', 'wmv', 'mkv']  # acceptable video suffixes
CLASSES = ["������","������","��ŸƯ����(������, ��������, ũ���� ��)","����(��������)","���","������","�������","������/����ű����/������ü��","����(����,����)", "����","���й���(����,����)","Ʈ��","SUV/������"]

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.yolo = yolov5_custom()

        # parameters ��  ----------------------------------------------------------------
        self.dataset_dir = None
        # parameters ��  ----------------------------------------------------------------

        # conponents ��  ----------------------------------------------------------------
        # labels
        self.label_dir = QLabel('�ҽ� ���� ����')
        self.label_dir.setStyleSheet("border-radius: 25px;border: 1px solid black;")
        self.label_dir.setAlignment(Qt.AlignCenter)

        self.label_weight = QLabel('����ġ ���� ����')
        self.label_weight.setStyleSheet("border-radius: 25px;border: 1px solid black;")
        self.label_weight.setAlignment(Qt.AlignCenter)

        self.label_imgsz = QLabel('img size ����')
        self.label_imgsz.setStyleSheet("border-radius: 25px;border: 1px solid black;")
        self.label_imgsz.setAlignment(Qt.AlignCenter)

        self.label_skipFrame = QLabel('�ǳʶ� frame �� ����')
        self.label_skipFrame.setStyleSheet("border-radius: 25px;border: 1px solid black;")
        self.label_skipFrame.setAlignment(Qt.AlignCenter)

        self.label_classes = QLabel('�˻��� ��ü ����(����Ŭ��)')
        self.label_classes.setStyleSheet("border-radius: 25px;border: 1px solid black;")
        self.label_classes.setFont(QtGui.QFont(None, 10))
        self.label_classes.setAlignment(Qt.AlignCenter)

        self.label_result = QLabel('�������� ������ ����(����Ŭ��)')
        self.label_result.setStyleSheet("border-radius: 25px;border: 1px solid black;")
        self.label_result.setFont(QtGui.QFont(None,10))
        self.label_result.setAlignment(Qt.AlignCenter)

        self.label_arrow = QLabel('=>')
        # self.label_arrow.setStyleSheet("border-radius: 25px;border: 1px solid black;")
        self.label_arrow.setAlignment(Qt.AlignCenter)

        self.label_img = QLabel()
        self.label_img.setBackgroundRole(QPalette.Base)
        self.label_img.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.label_img.setScaledContents(True)

        self.label_model_info = None

        # buttons
        self.btn_select_dir = QPushButton('...', self)
        self.btn_select_dir.clicked.connect(self.btn_select_dir_func)

        self.btn_quit = QPushButton('������', self)
        self.btn_quit.clicked.connect(QCoreApplication.instance().quit)

        self.btn_load_model = QPushButton('�� �ҷ�����', self)
        self.btn_load_model.clicked.connect(self.btn_load_model_func)

        self.btn_load_dataset = QPushButton('�����ͼ� �ҷ�����', self)
        self.btn_load_dataset.clicked.connect(self.btn_load_dataset_func)

        self.btn_detect = QPushButton('�м�', self)
        self.btn_detect.clicked.connect(self.btn_detect_func)

        # comboboxes
        self.cb_select_weight = QComboBox(self)
        weights = glob('weights/*')
        for weight in weights:
            temp = weight.split('\\')[1]
            self.cb_select_weight.addItem(temp)

        self.cb_select_imgsz = QComboBox(self)
        for imgsz in range(64,801,32):
            self.cb_select_imgsz.addItem(str(imgsz))

        self.cb_skipFrame = QComboBox(self)
        for frame in [1, 2, 3, 5, 10, 30, 60]:
            self.cb_skipFrame.addItem(str(frame))

        # List Widget
        self.lw_imgs = QListWidget()
        self.lw_imgs.setAlternatingRowColors(True)

        self.lw_results = QListWidget()
        self.lw_results.setAlternatingRowColors(True)
        self.lw_results.doubleClicked.connect(self.lw_results_doubleclicked_func)
        

        self.lw_classes = QListWidget()
        self.lw_classes.setAlternatingRowColors(True)
        self.lw_classes.doubleClicked.connect(self.lw_classes_doubleclicked_func)

        # Image, pixmap
        self.qimg = QImage()
        # conponents ��  ----------------------------------------------------------------


        # set Layout ��  ----------------------------------------------------------------
        ## set component position - form lbx
        self.form_lbx = QBoxLayout(QBoxLayout.TopToBottom, parent=self)
        self.setLayout(self.form_lbx)

        # group box_1 -> �� ����
        self.gb_1 = QGroupBox(self)
        self.gb_1.setTitle("�� ����")
        self.form_lbx.addWidget(self.gb_1)

        self.grid_1 = QGridLayout()
        self.gb_1.setLayout(self.grid_1)

        self.grid_1.addWidget(self.label_weight,0,0,1,3)
        self.grid_1.addWidget(self.cb_select_weight,0,3,1,1)

        self.grid_1.addWidget(self.label_imgsz,1,0,1,3)
        self.grid_1.addWidget(self.cb_select_imgsz,1,3,1,1)

        self.grid_1.addWidget(self.btn_load_model,2,0,1,4)
        
        # group box_2 -> �����ͼ� �ε�
        self.gb_2 = QGroupBox(self)
        self.gb_2.setTitle("�����ͼ� �ҷ�����")
        self.form_lbx.addWidget(self.gb_2)

        self.grid_2 = QGridLayout()
        self.gb_2.setLayout(self.grid_2)

        self.grid_2.addWidget(self.label_dir,0,0,1,3)
        self.grid_2.addWidget(self.btn_select_dir,0,3,1,1)
        
        self.grid_2.addWidget(self.lw_imgs,1,0,1,4)
        self.grid_2.addWidget(self.btn_load_dataset,2,0,1,4)

        # group box_3 -> �м�
        self.gb_3 = QGroupBox(self)
        self.gb_3.setTitle("�м�")
        self.form_lbx.addWidget(self.gb_3)

        self.grid_3 = QGridLayout()
        self.gb_3.setLayout(self.grid_3)

        self.grid_3.addWidget(self.label_skipFrame, 0,0,1,2)
        self.grid_3.addWidget(self.cb_skipFrame,0,2,1,1)

        self.grid_3.addWidget(self.btn_detect, 1,0,1,4)

        self.grid_3.addWidget(self.label_classes, 2,0)
        self.grid_3.addWidget(self.label_result, 2,2)

        self.grid_3.addWidget(self.lw_classes,3,0)
        self.grid_3.addWidget(self.label_arrow, 3, 1, 2, 1)
        self.grid_3.addWidget(self.lw_results,3,2)

        # group box_4 -> ������ �̹���
        self.gb_4 = QGroupBox(self)
        self.gb_4.setTitle("�м�")
        self.form_lbx.addWidget(self.gb_4)

        self.grid_4 = QGridLayout()
        self.gb_4.setLayout(self.grid_4)
        
        self.grid_4.addWidget(self.label_img,0,0)

        

        # set Layout ��  ----------------------------------------------------------------

        # â ����
        self.setWindowTitle('Yolo_v5_Object_Detection')
        self.setGeometry(300, 300, 600, 500)
        self.form_lbx.addWidget(self.btn_quit)
        self.show()

    def btn_load_model_func(self):
        text = "model => Yolo_v5 / weights: " + self.cb_select_weight.currentText() +" / imgsz : " + self.cb_select_imgsz.currentText() + "px"
        if self.label_model_info == None:
            self.label_model_info = QLabel('')
            self.label_model_info.setStyleSheet("border-radius: 3px;border: 1px solid black;")
            self.label_model_info.setAlignment(Qt.AlignCenter)
            self.label_model_info.setFont(QtGui.QFont("arial", 15))
            self.grid_1.addWidget(self.label_model_info,3,0,1,4)
        self.yolo.load_model(weights='weights/'+self.cb_select_weight.currentText(), imgsz= int(self.cb_select_imgsz.currentText()))
        self.label_model_info.setText(text)

    def btn_select_dir_func(self):
        root = tkinter.Tk()
        root.withdraw()
        dir_path = filedialog.askdirectory(parent=root,initialdir="/",title='Please select a directory')
        self.dataset_dir = dir_path
        self.label_dir.setText("���: "+dir_path)
        self.lw_imgs.clear()
        imgs = glob(dir_path+"/*")
        for img in imgs:
            if img.split('.')[-1] in IMG_FORMATS or img.split('.')[-1] in VID_FORMATS:
                self.lw_imgs.addItem(img.split('\\')[1])

    def btn_load_dataset_func(self):
        if self.yolo.model == None :
            self.pop_error_msg("�����ͼ� ���� �Ұ�", "���� �������� �ʾҽ��ϴ�. ���� ���� ������ �ּ���.")
            return
        if self.lw_imgs.currentItem() == None:
            self.pop_error_msg("�����ͼ� ���� �Ұ�", "������ ������ �ּ���..")
            return
        source = self.dataset_dir + "/" +self.lw_imgs.currentItem().text()
        self.yolo.load_dataset(source=source)

    def btn_detect_func(self):
        if self.yolo.dataset == None:
            self.pop_error_msg("�м� �Ұ�", "�����ͼ��� �ε���� �ʾҽ��ϴ�.")
            return
        self.pop_error_msg("�м���", "�м� �Ϸ� �� �Ϸ� �޽����� �߻��մϴ�.\nȮ���� ������ �м��� ���۵˴ϴ�.")

        self.yolo.skipFrame = int(self.cb_skipFrame.currentText())
        self.yolo.detect()
        self.pop_error_msg("�м� �Ϸ�", "�м��� �Ϸ�ƽ��ϴ�.\nȮ���� �����ּ���.")

        self.lw_classes.clear()
        self.lw_results.clear()
        # print(self.yolo.results)
        classes = []
        for results in self.yolo.results:
            for result in results:
                classes.append(result[1])

        for class_ in set(classes):
            if type(class_)==int:
                self.lw_classes.addItem(CLASSES[class_])
    
    def lw_classes_doubleclicked_func(self):
        self.lw_results.clear()
        label = self.lw_classes.currentItem().text()
        target_class = CLASSES.index(label)
        for frame, xy, results in zip(self.yolo.frame, self.yolo.xys, self.yolo.results):
            for result in results:
                if result[1] == target_class:
                    self.lw_results.addItem("frame: "+str(frame) + " // label: "+ label)
                    break

    def lw_results_doubleclicked_func(self):
        index = int(self.lw_results.currentItem().text().split(':')[1].split('//')[0])
        img = self.yolo.curr_imgs[self.yolo.frame.index(index)]

        cv2.imshow("img", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()



    def pop_error_msg(self, title, inform):
        msgBox = QMessageBox()
        msgBox.setWindowTitle(title)
        msgBox.setIcon(QMessageBox.Critical)
        msgBox.setText(inform)
        msgBox.setDefaultButton(QMessageBox.Ok)
        msgBox.exec_()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QTextEdit,
    QVBoxLayout, QWidget)

from pyqtgraph import PlotWidget

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(800, 600)
        Widget.setMinimumSize(QSize(800, 600))
        self.graphicsViewTemperaturePlot = PlotWidget(Widget)
        self.graphicsViewTemperaturePlot.setObjectName(u"graphicsViewTemperaturePlot")
        self.graphicsViewTemperaturePlot.setGeometry(QRect(250, 10, 531, 411))
        self.groupBox = QGroupBox(Widget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 430, 771, 161))
        self.textEditStatusUpdate = QTextEdit(self.groupBox)
        self.textEditStatusUpdate.setObjectName(u"textEditStatusUpdate")
        self.textEditStatusUpdate.setGeometry(QRect(10, 30, 741, 121))
        self.groupBox_2 = QGroupBox(Widget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(10, 10, 231, 171))
        self.pushButtonInitialCheck = QPushButton(self.groupBox_2)
        self.pushButtonInitialCheck.setObjectName(u"pushButtonInitialCheck")
        self.pushButtonInitialCheck.setGeometry(QRect(10, 30, 211, 41))
        self.lineEditAPIKey = QLineEdit(self.groupBox_2)
        self.lineEditAPIKey.setObjectName(u"lineEditAPIKey")
        self.lineEditAPIKey.setGeometry(QRect(10, 130, 211, 31))
        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 100, 71, 31))
        self.layoutWidget = QWidget(self.groupBox_2)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 70, 211, 41))
        self.horizontalLayout = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_6 = QLabel(self.layoutWidget)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout.addWidget(self.label_6)

        self.lineEdit_DeviceName = QLineEdit(self.layoutWidget)
        self.lineEdit_DeviceName.setObjectName(u"lineEdit_DeviceName")

        self.horizontalLayout.addWidget(self.lineEdit_DeviceName)

        self.groupBox_3 = QGroupBox(Widget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(10, 180, 231, 241))
        self.layoutWidget1 = QWidget(self.groupBox_3)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(10, 180, 211, 71))
        self.horizontalLayout_2 = QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.pushButton_StartMeasurement = QPushButton(self.layoutWidget1)
        self.pushButton_StartMeasurement.setObjectName(u"pushButton_StartMeasurement")

        self.horizontalLayout_2.addWidget(self.pushButton_StartMeasurement)

        self.pushButton_StopMeasurement = QPushButton(self.layoutWidget1)
        self.pushButton_StopMeasurement.setObjectName(u"pushButton_StopMeasurement")

        self.horizontalLayout_2.addWidget(self.pushButton_StopMeasurement)

        self.layoutWidget2 = QWidget(self.groupBox_3)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(10, 30, 211, 168))
        self.horizontalLayout_3 = QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_2 = QLabel(self.layoutWidget2)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.label_3 = QLabel(self.layoutWidget2)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_2.addWidget(self.label_3)

        self.label_4 = QLabel(self.layoutWidget2)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_2.addWidget(self.label_4)

        self.label_5 = QLabel(self.layoutWidget2)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_2.addWidget(self.label_5)

        self.label_7 = QLabel(self.layoutWidget2)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout_2.addWidget(self.label_7)

        self.label_8 = QLabel(self.layoutWidget2)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout_2.addWidget(self.label_8)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lineEdit_T1 = QLineEdit(self.layoutWidget2)
        self.lineEdit_T1.setObjectName(u"lineEdit_T1")

        self.verticalLayout.addWidget(self.lineEdit_T1)

        self.lineEdit_T1PeriodMins = QLineEdit(self.layoutWidget2)
        self.lineEdit_T1PeriodMins.setObjectName(u"lineEdit_T1PeriodMins")

        self.verticalLayout.addWidget(self.lineEdit_T1PeriodMins)

        self.lineEdit_T2 = QLineEdit(self.layoutWidget2)
        self.lineEdit_T2.setObjectName(u"lineEdit_T2")

        self.verticalLayout.addWidget(self.lineEdit_T2)

        self.lineEdit_T2PeriodMins = QLineEdit(self.layoutWidget2)
        self.lineEdit_T2PeriodMins.setObjectName(u"lineEdit_T2PeriodMins")

        self.verticalLayout.addWidget(self.lineEdit_T2PeriodMins)

        self.lineEdit_TimeStepSizeMins = QLineEdit(self.layoutWidget2)
        self.lineEdit_TimeStepSizeMins.setObjectName(u"lineEdit_TimeStepSizeMins")

        self.verticalLayout.addWidget(self.lineEdit_TimeStepSizeMins)

        self.lineEdit_MeasurementTimePeriodMins = QLineEdit(self.layoutWidget2)
        self.lineEdit_MeasurementTimePeriodMins.setObjectName(u"lineEdit_MeasurementTimePeriodMins")

        self.verticalLayout.addWidget(self.lineEdit_MeasurementTimePeriodMins)


        self.horizontalLayout_3.addLayout(self.verticalLayout)


        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Temperature resoluiton tester", None))
        self.groupBox.setTitle(QCoreApplication.translate("Widget", u"Status update", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Widget", u"Sensibo API", None))
        self.pushButtonInitialCheck.setText(QCoreApplication.translate("Widget", u"Check avaiable Daikin devices.", None))
        self.lineEditAPIKey.setText(QCoreApplication.translate("Widget", u"bUBfc0Vz8bQF85dnwxIQw8PrVlZsA2", None))
        self.label.setText(QCoreApplication.translate("Widget", u"API Key", None))
        self.label_6.setText(QCoreApplication.translate("Widget", u"Device name", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Widget", u"Test parameters", None))
        self.pushButton_StartMeasurement.setText(QCoreApplication.translate("Widget", u"Start!", None))
        self.pushButton_StopMeasurement.setText(QCoreApplication.translate("Widget", u"Stop!", None))
        self.label_2.setText(QCoreApplication.translate("Widget", u"T1 (C)", None))
        self.label_3.setText(QCoreApplication.translate("Widget", u"Max Period for T1 (mins)", None))
        self.label_4.setText(QCoreApplication.translate("Widget", u"T2 (C)", None))
        self.label_5.setText(QCoreApplication.translate("Widget", u"Period for T2 (mins)", None))
        self.label_7.setText(QCoreApplication.translate("Widget", u"Time step size (mins)", None))
        self.label_8.setText(QCoreApplication.translate("Widget", u"Measurement time (mins)", None))
    # retranslateUi


import sys
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import pandas as pd
import os
from datetime import datetime, date
from initialization import init as initail
from windows.main_window import *
from windows.report_window import *
from windows.save_window import *
from windows.help_window import *


class SaveParams(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()
        self.mainwind = self.sender()
        print(self.mainwind, type(self.mainwind))
        self.prokuror = 'Jeka'
        self.setGeometry(300, 400, 300, 50)
        self.setWindowTitle('Сохраняем параметры')
        self.mainBox = QtWidgets.QVBoxLayout()

        self.datacheck = QtWidgets.QHBoxLayout()
        lbdatasave = QtWidgets.QLabel("Дата задачи", self)
        self.datacheckcol = QtWidgets.QDateEdit()
        self.datacheckcol.setDate(datetime.today())
        self.datacheckcol.setCalendarPopup(True)
        self.datacheck.addWidget(lbdatasave)
        self.datacheck.addWidget(self.datacheckcol)
        self.mainBox.addLayout(self.datacheck)

        self.testtype = QtWidgets.QHBoxLayout()
        lbtesttype = QtWidgets.QLabel("Выбери тип задачи", self)
        self.combotesttype = QtWidgets.QComboBox(self)
        self.combotesttype.addItems(initail.tasklist)
        self.testtype.addWidget(lbtesttype)
        self.testtype.addWidget(self.combotesttype)
        self.mainBox.addLayout(self.testtype)

        self.cmstype = QtWidgets.QHBoxLayout()
        lbcmstype = QtWidgets.QLabel("Выбери тип площадки", self)
        self.combocmstype = QtWidgets.QComboBox(self)
        self.combocmstype.addItems(initail.cmslist)
        self.cmstype.addWidget(lbcmstype)
        self.cmstype.addWidget(self.combocmstype)
        self.mainBox.addLayout(self.cmstype)

        self.horchechbox3 = QtWidgets.QHBoxLayout()
        lbl3 = QtWidgets.QLabel("Тестовая плащадка", self)
        self.checboxtest = QtWidgets.QCheckBox()
        self.horchechbox3.addWidget(lbl3)
        self.horchechbox3.addWidget(self.checboxtest)
        self.mainBox.addLayout(self.horchechbox3)

        self.mainBox.addWidget(QtWidgets.QLabel("-" * 75, self))

        self.testtime = QtWidgets.QHBoxLayout()
        lbtesttime = QtWidgets.QLabel("Введите кол-во часов", self)
        self.inputtesttime = QtWidgets.QLineEdit()
        self.inputtesttime.setText('0')
        self.inputtesttime.setMaximumWidth(147)
        self.testtime.addWidget(lbtesttime)
        self.testtime.addWidget(self.inputtesttime)
        self.mainBox.addLayout(self.testtime)

        self.tesknumber = QtWidgets.QHBoxLayout()
        lbtasknum = QtWidgets.QLabel("Номер задачи", self)
        self.tesknumberinp = QtWidgets.QLineEdit()
        self.tesknumberinp.setMaximumWidth(147)
        self.tesknumberinp.setText('0')
        self.tesknumber.addWidget(lbtasknum)
        self.tesknumber.addWidget(self.tesknumberinp)
        self.mainBox.addLayout(self.tesknumber)

        self.infomened = QtWidgets.QHBoxLayout()
        lbinfomened = QtWidgets.QLabel("Менеджер", self)
        self.comboinfomened = QtWidgets.QComboBox(self)
        self.comboinfomened.addItems(initail.worker_list(department=1, activat=1))
        self.infomened.addWidget(lbinfomened)
        self.infomened.addWidget(self.comboinfomened)
        self.mainBox.addLayout(self.infomened)

        self.infoverst = QtWidgets.QHBoxLayout()
        lbinfoverst = QtWidgets.QLabel("Верстальщик", self)
        self.comboinfoverst = QtWidgets.QComboBox(self)
        self.comboinfoverst.addItems(initail.worker_list(department=0, activat=1))
        self.infoverst.addWidget(lbinfoverst)
        self.infoverst.addWidget(self.comboinfoverst)
        self.mainBox.addLayout(self.infoverst)

        self.infoprog = QtWidgets.QHBoxLayout()
        lbinfoprog = QtWidgets.QLabel("Програмист", self)
        self.comboinfoprog = QtWidgets.QComboBox(self)
        self.comboinfoprog.addItems(initail.worker_list(department=2, activat=1))
        self.infoprog.addWidget(lbinfoprog)
        self.infoprog.addWidget(self.comboinfoprog)
        self.mainBox.addLayout(self.infoprog)

        self.iteration = QtWidgets.QHBoxLayout()
        lbiter = QtWidgets.QLabel("Итерация номер", self)
        self.iterationnum = QtWidgets.QLineEdit()
        self.iterationnum.setMaximumWidth(147)
        self.iterationnum.setText('1')
        self.iteration.addWidget(lbiter)
        self.iteration.addWidget(self.iterationnum)
        self.mainBox.addLayout(self.iteration)

        lbcoment = QtWidgets.QLabel("Что мы думаем о задаче:", self)
        self.mainBox.addWidget(lbcoment)

        self.testcoment = QtWidgets.QTextEdit()
        self.testcoment.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.mainBox.addWidget(self.testcoment)

        self.hbox = QtWidgets.QHBoxLayout()
        self.btnOK = QtWidgets.QPushButton("&OK")
        self.btnCancel = QtWidgets.QPushButton("&Cancel")
        self.btnOK.clicked.connect(self.accept)
        self.btnCancel.clicked.connect(self.reject)
        self.hbox.addWidget(self.btnOK)
        self.hbox.addWidget(self.btnCancel)
        self.mainBox.addLayout(self.hbox)
        self.setLayout(self.mainBox)

    def accept(self):
        print('do')
        initail.save_param_prodject(self.datacheckcol.date(), self.combotesttype.currentText(),
                                    self.combocmstype.currentText(), self.checboxtest.checkState(),
                                    self.inputtesttime.text(), self.tesknumberinp.text(),
                                    self.comboinfomened.currentText(), self.comboinfoverst.currentText(),
                                    self.comboinfoprog.currentText(), self.testcoment.toPlainText(), self.prokuror,
                                    self.iterationnum.text(), 0)
        print('posle')
        self.close()

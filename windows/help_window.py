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


class HelpWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        helpsave = QtWidgets.QAction('Сохранить изменения', self)
        helpsave.setShortcut('Ctrl+S')
        helpsave.triggered.connect(self.saveelpchange)
        self.menuBar().addAction(helpsave)
        self.helpText = initail.readhelp()
        self.setWindowTitle('Окно хелпа')
        self.helpBox = QtWidgets.QTextEdit()
        self.helpBox.setWordWrapMode(QtGui.QTextOption.WordWrap)
        self.helpBox.setFontPointSize(13)
        self.helpBox.setText(self.helpText)
        self.setCentralWidget(self.helpBox)
        self.setGeometry(400, 200, 400, 600)

    def saveelpchange(self):
        text = self.helpBox.toPlainText()
        initail.writehelp(text)


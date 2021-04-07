import sys
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import pandas as pd
import os
from datetime import datetime, date
from windows.main_window import *
from windows.report_window import *
from windows.save_window import *
from windows.help_window import *



def main():
    app = QtWidgets.QApplication(sys.argv)
    main_win = Main()
    main_win.show()
    sys.exit(app.exec_())



if __name__ == '__main__':
    main()

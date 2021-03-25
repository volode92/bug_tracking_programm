import sys
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import initialization as initail
import pandas as pd
import os
from datetime import datetime, date


class Main(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.testmodule = initail.uniq_module(initail.reader)  # считываем все модули
        self.testmoduleactiv = self.testmodule[0]  # в качестве основногго берем первый
        self.testcaselist = initail.test_case_list(initail.reader,
                                                   self.testmoduleactiv)  # считываем список юлоков в модуле
        self.errordeptype = None  # типы ошибок по отделу
        self.senderold = None
        self.testcaseactiv = None
        self.blockanable = None
        self.buglist = initail.read_errors_df()
        self.errcount = len(self.buglist)

        # добавляем верхнее меню
        profjectfile = QtWidgets.QAction('Добавить проект', self)
        profjectfile.setShortcut('Ctrl+R')
        profjectfile.triggered.connect(self.on_btnfile_clicked)
        browsefolder = QtWidgets.QAction('Выбор проекта', self)
        browsefolder.setShortcut('Ctrl+T')
        browsefolder.triggered.connect(self.on_browsefolder_clicked)
        errsee = QtWidgets.QAction('Просмотр отчета', self)
        errsee.setShortcut('Ctrl+U')
        errsee.triggered.connect(self.on_seeerror_clicked)
        errsave = QtWidgets.QAction('Сохранение ошибок с параметром', self)
        errsave.setShortcut('Ctrl+Y')
        errsave.triggered.connect(self.on_paramerrorsave_clicked)
        helpsee = QtWidgets.QAction('Вызвать хелп', self)
        helpsee.setShortcut('F1')
        helpsee.triggered.connect(self.call_help)
        wallposition = QtWidgets.QAction('Поверх окон', self)
        wallposition.setShortcut('Ctrl+F')
        wallposition.triggered.connect(self.flagchangetop)
        self.menuBar().addAction(profjectfile)
        self.menuBar().addAction(browsefolder)
        self.menuBar().addAction(errsave)
        self.menuBar().addAction(errsee)
        self.menuBar().addAction(helpsee)
        self.menuBar().addAction(wallposition)

        self.mainlayout = QtWidgets.QHBoxLayout(self)  # основной лайоут для накидывание на него полей
        self.leftlist = QtWidgets.QVBoxLayout(self)  # левый столбец
        self.layoutreport = QtWidgets.QVBoxLayout()  # правый столбец

        # левый столбец
        # создаем
        self.butandspis = QtWidgets.QHBoxLayout(self)
        self.adapterrlayout = QtWidgets.QVBoxLayout(self)
        self.inputerrorlayoyt = QtWidgets.QHBoxLayout(self)
        self.buttonSendErron = QtWidgets.QHBoxLayout()

        # формируем
        self.leftlist.addLayout(self.butandspis)
        self.leftlist.addLayout(self.adapterrlayout)
        self.leftlist.addLayout(self.inputerrorlayoyt)
        self.leftlist.addLayout(self.buttonSendErron)
        self.mainlayout.addLayout(self.leftlist)

        # добавляем элементы в штучки
        # парсер кнопок и списков
        self.butandspis.setSpacing(0)
        self.butnlist = QtWidgets.QGridLayout(self)
        self.butnlist.setSpacing(4)
        self.butnlist.setAlignment(QtCore.Qt.AlignTop)  # список сверху
        stroc, col = 0, 0
        for i in range(len(self.testmodule)):
            qbtn = QtWidgets.QPushButton(str(self.testmodule[i]), self)
            if str(self.testmodule[i]) == self.testmoduleactiv:
                qbtn.setStyleSheet(
                    " QPushButton {  font-weight: 700;  color: white;   border-radius: 3px;  background: rgb(64,199,129); } QPushButton::hover {background: rgb(53, 167, 110);} ")
                self.senderold = qbtn
            qbtn.clicked.connect(self.on_pushButton_clicked)
            qbtn.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
            qbtn.setFixedSize(QtCore.QSize(145, 30))
            self.butnlist.addWidget(qbtn, stroc, col)
            if col == 0:
                col += 1
            else:
                stroc += 1
                col = 0
        self.sizewidg = QtWidgets.QWidget(self)
        self.sizewidg.setLayout(self.butnlist)
        self.sizewidg.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        self.butandspis.addWidget(self.sizewidg)
        self.layoutblocks = QtWidgets.QVBoxLayout(self)
        self.qlist = QtWidgets.QListWidget(self)
        self.qlist.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        self.qlist.setMaximumSize(250, stroc * 37)
        self.qlist.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.qlist.itemChanged.connect(self.qlistitemchecked)
        self.qlist.setWordWrap(True)
        for i in range(len(self.testcaselist)):
            item = QtWidgets.QListWidgetItem()
            item.setText(self.testcaselist['test_case'][i])
            item.setData(QtCore.Qt.UserRole, self.testcaselist['test_case'][i])
            item.setCheckState(0)
            self.qlist.addItem(item)
        self.layoutblocks.addWidget(self.qlist)
        self.butandspis.addLayout(self.layoutblocks)
        # поле ввода ошибки
        self.inputerror = QtWidgets.QTextEdit()
        self.inputerror.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        self.inputerror.setMaximumSize(2000, 2000)
        self.inputerrorlayoyt.addWidget(self.inputerror)
        # галочка адапт ошибки
        self.adapterr = QtWidgets.QCheckBox("Кнопка адаптивной ошибки", self)
        self.adapterrlayout.addWidget(self.adapterr)
        # кнопки с ошибками
        self.buttonAddReportvers = QtWidgets.QPushButton('Верстальщики', self)
        self.buttonAddReportvers.setStyleSheet(
            " QPushButton {  font-weight: 700;  color: white;   border-radius: 3px;  background: rgb(64,199,129); } QPushButton::hover {background: rgb(53, 167, 110);} ")
        self.buttonAddReportvers.setMinimumSize(175, 40)
        self.buttonAddReportvers.clicked.connect(self.on_button_send_error_verst)
        self.buttonAddReportprog = QtWidgets.QPushButton('Програмисты', self)
        self.buttonAddReportprog.setStyleSheet(
            " QPushButton {  font-weight: 700;  color: white;   border-radius: 3px;  background: rgb(64,199,129); } QPushButton::hover {background: rgb(53, 167, 110);} ")
        self.buttonAddReportprog.setMinimumSize(175, 40)
        self.buttonAddReportprog.clicked.connect(self.on_button_send_error_prog)
        self.buttonAddReportmaned = QtWidgets.QPushButton('Менеджеры', self)
        self.buttonAddReportmaned.setStyleSheet(
            " QPushButton {  font-weight: 700;  color: white;   border-radius: 3px;  background: rgb(64,199,129); } QPushButton::hover {background: rgb(53, 167, 110);} ")
        self.buttonAddReportmaned.setMinimumSize(175, 40)
        self.buttonAddReportmaned.clicked.connect(self.on_button_send_error_maned)
        self.buttonSendErron.addWidget(self.buttonAddReportvers)
        self.buttonSendErron.addWidget(self.buttonAddReportprog)
        self.buttonSendErron.addWidget(self.buttonAddReportmaned)

        # правый столбец
        self.report = QtWidgets.QListWidget()
        self.botnparamlist = QtWidgets.QHBoxLayout()
        self.layoutreport.addWidget(self.report)
        self.layoutreport.addLayout(self.botnparamlist)
        self.mainlayout.addLayout(self.layoutreport)
        # наполняем правыйстолбец
        self.openreportlist = QtWidgets.QPushButton('Открыть файл', self)
        self.changeerrtype = QtWidgets.QPushButton('Изменить тип', self)
        self.delreportpoint = QtWidgets.QPushButton('Удалить', self)
        self.changeerrtypemodul = QtWidgets.QPushButton('Изменить модуль', self)
        self.botnparamlist.addWidget(self.changeerrtypemodul)
        self.botnparamlist.addWidget(self.delreportpoint)
        self.botnparamlist.addWidget(self.changeerrtype)
        self.botnparamlist.addWidget(self.openreportlist)
        self.report.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.report.setWordWrap(True)
        self.report.itemChanged.connect(self.editreport)
        self.updateReportList()

        # кнопки к баглисту
        self.delreportpoint.clicked.connect(self.delpointfromreport)
        self.changeerrtype.clicked.connect(self.editpointfromreport)
        self.openreportlist.clicked.connect(self.openreport)
        self.changeerrtypemodul.clicked.connect(self.editmodulfromreport)

        # делвем mainlayout основным на экране
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setLayout(self.mainlayout)
        self.setCentralWidget(self.centralwidget)

        # размеры и заголовок
        self.setGeometry(400, 200, 1000, 600)
        self.setWindowTitle(initail.file_name)

    def on_btnfile_clicked(self):
        """Создание папки проекта"""
        text, ok = QtWidgets.QInputDialog.getText(self, 'Создание проекта', 'Введи название проекта:')
        if ok:
            pathnew = str(initail.pathdirect) + '/' + str(text)
            if initail.check_directories(pathnew):
                result = QtWidgets.QMessageBox.question(self, 'Заголовок окна подтверждения повтора папки',
                                                        'Такая папка уже есть продолжить в ней?',
                                                        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                        QtWidgets.QMessageBox.No)
                if result == QtWidgets.QMessageBox.Yes:
                    initail.file_name = str(text)
                    initail.path = pathnew
                    self.setWindowTitle(initail.file_name)
                    initail.save_settings()
                else:
                    self.on_btnfile_clicked()
            else:
                initail.file_name = str(text)
                initail.create_directories(pathnew)
                initail.path = pathnew
                self.setWindowTitle(initail.file_name)
                initail.save_settings()
        self.buglist = initail.read_errors_df()
        self.errcount = len(self.buglist)
        self.updateUIlist()

    def on_browsefolder_clicked(self):
        """Выбираем папку кликом"""
        file_name = QtWidgets.QFileDialog.getExistingDirectory(self, 'Выберите папку', initail.pathdirect)
        # открыть диалог выбора директории и установить значение переменной
        # равной пути к выбранной директории
        if file_name:  # не продолжать выполнение, если пользователь не выбрал директорию
            file_name = file_name.split('/')
            initail.file_name = file_name[-1]
            initail.path = str(initail.pathdirect) + '/' + initail.file_name
            self.setWindowTitle(initail.file_name)
            initail.save_settings()
        self.buglist = initail.read_errors_df()
        self.errcount = len(self.buglist)
        self.updateUIlist()

    def updateUIlist(self):
        """Очистка полей от галочек и надписей, обновление листа ошибок"""
        self.qlist.clear()
        for i in range(len(self.testcaselist)):
            item = QtWidgets.QListWidgetItem()
            item.setText(self.testcaselist['test_case'][i])
            item.setData(QtCore.Qt.UserRole, self.testcaselist['test_case'][i])
            item.setCheckState(0)
            self.qlist.addItem(item)
            self.inputerror.setPlainText('')
        self.updateReportList()

    def call_help(self):
        """Вызов окна с хэлпом"""
        self.helpWindow = HelpWindow()
        self.helpWindow.show()

    def on_paramerrorsave_clicked(self):
        """Вызов окна сохранения"""
        self.saveparam = SaveParams()
        self.saveparam.show()

    def on_seeerror_clicked(self):
        """Вызов окна для просмотра багрепортов"""
        self.errorsee = ReportWindow()
        self.errorsee.setWindowTitle("Отчет по ошибкам")
        self.errorsee.show()

    def on_pushButton_clicked(self):
        """Изменение просматриваемого модуля"""
        sender = self.sender()
        if self.senderold is not None:
            self.senderold.setStyleSheet("")
        sender.setStyleSheet(
            " QPushButton {  font-weight: 700;  color: white;   border-radius: 3px;  background: rgb(64,199,129); } QPushButton::hover {background: rgb(53, 167, 110);} ")
        self.senderold = sender
        self.testmoduleactiv = sender.text()
        self.blockanable = None
        self.testcaselist = initail.test_case_list(initail.reader, self.testmoduleactiv)
        self.updateUIlist()

    def on_button_send_error_verst(self):
        """Ошибка верстальшика"""
        self.errordeptype = 'imposer'
        self.on_button_send_error()

    def on_button_send_error_prog(self):
        """Ошибка прогера"""
        self.errordeptype = 'programmer'
        self.on_button_send_error()

    def on_button_send_error_maned(self):
        """Ошибка менеджера"""
        self.errordeptype = 'manager'
        self.on_button_send_error()

    def on_button_send_error(self):
        """Добавление бага к листу"""
        if self.inputerror.toPlainText() == '':
            return
        # будем тут менять
        k = 0
        for index in range(self.qlist.count()):
            if self.qlist.item(index).checkState() == QtCore.Qt.Checked:
                self.testcaseactiv = self.qlist.item(index).text()
                k += 1
        if k == 0:
            self.testcaseactiv = 'необходимо уточнение'
        self.buglist.loc[len(self.buglist)] = [self.testmoduleactiv, self.testcaseactiv, self.inputerror.toPlainText(),
                                               self.errordeptype, 1, 1 if self.adapterr.checkState() else 0]
        self.errcount += 1
        self.inputerror.setPlainText('')
        initail.save_errors(self.buglist)
        self.updateReportList()

    def editreport(self):
        """Изменение пункта ошибки"""
        text = self.report.item(self.report.currentRow()).text()
        text = text.split('. ')
        id = int(text.pop(0)) - 1
        testerr = ". ".join(text)
        self.buglist.loc[id]['err_text'] = testerr
        initail.save_errors(self.buglist)
        self.updateReportList()

    def updateReportList(self):
        """Формирование списка с ошибками"""
        self.reporttext = 'Верстка: \n'
        self.report.clear()
        trp = QtWidgets.QListWidgetItem('Верстка:')
        self.report.addItem(trp)
        self.create_item_by_type('imposer')
        trp = QtWidgets.QListWidgetItem('-' * 40)
        self.reporttext += '-' * 40 + '\n'
        self.report.addItem(trp)
        trp = QtWidgets.QListWidgetItem('Менеджмент:')
        self.reporttext += 'Менеджмент:  \n'
        self.report.addItem(trp)
        self.create_item_by_type('manager')
        trp = QtWidgets.QListWidgetItem('-' * 40)
        self.reporttext += '-' * 40 + '\n'
        self.report.addItem(trp)
        trp = QtWidgets.QListWidgetItem('Программинг:')
        self.reporttext += 'Программинг:  \n'
        self.report.addItem(trp)
        self.create_item_by_type('programmer')
        initail.save_report(self.reporttext)

    def create_item_by_type(self, err_type):
        """Добавление ошибок по типу"""
        index_list = list(self.buglist[(self.buglist['err_type'] == err_type) & (self.buglist['activ_err'] == 1)].index)
        for ind in index_list:
            text = str(ind + 1) + '. ' + str(self.buglist.iloc[ind]['err_text'])
            self.reporttext += text + '\n'
            trp = QtWidgets.QListWidgetItem(text)
            trp.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable)
            self.report.addItem(trp)

    def delpointfromreport(self):
        """Удаление ошибок из списка"""
        if self.report.currentRow() != -1:
            result = QtWidgets.QMessageBox.question(self, 'Подтверждение удаления',
                                                    'Точно удаляем ' + str(
                                                        self.report.item(self.report.currentRow()).text()) + '?',
                                                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                    QtWidgets.QMessageBox.No)
            if result == QtWidgets.QMessageBox.Yes:
                id = int(self.report.item(self.report.currentRow()).text().split('. ')[0]) - 1
                self.buglist.loc[id]['activ_err'] = 0
        initail.save_errors(self.buglist)
        self.updateReportList()

    def editpointfromreport(self):
        """Изменение типа ошибки"""
        if self.report.currentRow() != -1:
            items = ("Верстка", "Менедмент", "Програминг")
            item, ok = QtWidgets.QInputDialog.getItem(self, "Изменение типа", 'На какой тип меняем ' + str(
                self.report.item(self.report.currentRow()).text()) + '?', items, 0, False)

            if ok and item:
                if item == 'Верстка':
                    self.errordeptype = 'imposer'
                elif item == 'Менедмент':
                    self.errordeptype = 'manager'
                else:
                    self.errordeptype = 'programmer'
                id = int(self.report.item(self.report.currentRow()).text().split('. ')[0]) - 1
                self.buglist.loc[id]['err_type'] = self.errordeptype
        initail.save_errors(self.buglist)
        self.updateReportList()

    def editmodulfromreport(self):
        if self.report.currentRow() != -1:
            id = int(self.report.item(self.report.currentRow()).text().split('. ')[0]) - 1
            test_module_err = self.buglist.loc[id].test_module
            test_case_err = self.buglist.loc[id].test_case
        self.changemodulwind = ChangeModul(str(test_module_err), str(test_case_err), id)
        self.changemodulwind.show()

    def change_err_modul(self, id, test_module, test_case, adapt_err):
        self.buglist.loc[id]['test_module'] = test_module
        self.buglist.loc[id]['test_case'] = test_case
        self.buglist.loc[id]['adapt_err'] = adapt_err
        initail.save_errors(self.buglist)
        self.updateReportList()

    def openreport(self):
        """Открыть файл с ошбкой"""
        os.startfile(initail.path)

    def flagchangetop(self):
        """окно будет поверх всех окон"""
        if bool(self.windowFlags() & QtCore.Qt.WindowStaysOnTopHint):
            self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint)
            self.show()
        else:
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            self.show()

    def qlistitemchecked(self, listaItem):
        """"""
        if self.blockanable == None:
            self.blockanable = listaItem
            return
        if self.blockanable == listaItem:
            self.blockanable = None
        else:
            self.blockanable.setCheckState(0)
            self.blockanable = listaItem

    def clean_list(self):
        pass


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


class SaveParams(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()
        self.mainwind = self.sender()
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
        initail.save_param_prodject(self.datacheckcol.date(), self.combotesttype.currentText(),
                                    self.combocmstype.currentText(), self.checboxtest.checkState(),
                                    self.inputtesttime.text(), self.tesknumberinp.text(),
                                    self.comboinfomened.currentText(), self.comboinfoverst.currentText(),
                                    self.comboinfoprog.currentText(), self.testcoment.toPlainText(), self.prokuror,
                                    self.iterationnum.text(), 0)
        self.close()


class ReportWindow(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 300, 50)
        self.setWindowTitle('Тут смотрим ошибки')
        self.dferr = []
        self.mainBox = QtWidgets.QVBoxLayout()
        self.bottonline = QtWidgets.QHBoxLayout()
        self.bottoncreatereport = QtWidgets.QPushButton('Сформировать отчет')
        self.bottoncreatereport.clicked.connect(self.updateerrlistall)
        self.bottoncreatereport.setFixedSize(QtCore.QSize(150, 25))
        self.bottonline.addWidget(self.bottoncreatereport)

        self.bottonfilter = QtWidgets.QPushButton('Фильтр')
        self.bottonfilter.clicked.connect(self.activfilt)
        self.bottonfilter.setFixedSize(QtCore.QSize(70, 25))
        self.bottonline.addWidget(self.bottonfilter)

        self.datestartchecbox = QtWidgets.QCheckBox()
        self.lbldatestart = QtWidgets.QLabel("c")
        self.datestartinput = QtWidgets.QDateEdit()
        self.datestartinput.setDate(date(2020, 10, 1))
        self.datestartinput.setCalendarPopup(True)
        self.bottonline.addWidget(self.datestartchecbox)
        self.bottonline.addWidget(self.lbldatestart)
        self.bottonline.addWidget(self.datestartinput)
        self.lbldateend = QtWidgets.QLabel("до")
        self.dateendinput = QtWidgets.QDateEdit()
        self.dateendinput.setCalendarPopup(True)
        self.dateendinput.setDate(date.today())
        self.bottonline.addWidget(self.lbldateend)
        self.bottonline.addWidget(self.dateendinput)
        self.bottonline.addWidget(QtWidgets.QLabel("|"))

        self.typetaskchecbox = QtWidgets.QCheckBox()
        self.lbltypetask = QtWidgets.QLabel("тип задачи")
        self.typecombo = QtWidgets.QComboBox(self)
        self.typecombo.addItems(initail.tasklist)
        self.bottonline.addWidget(self.typetaskchecbox)
        self.bottonline.addWidget(self.lbltypetask)
        self.bottonline.addWidget(self.typecombo)
        self.bottonline.addWidget(QtWidgets.QLabel("|"))

        self.typecmschecbox = QtWidgets.QCheckBox()
        lbltypecms = QtWidgets.QLabel("тип CMS")
        self.typecms = QtWidgets.QComboBox(self)
        self.typecms.addItems(initail.cmslist)
        self.bottonline.addWidget(self.typecmschecbox)
        self.bottonline.addWidget(lbltypecms)
        self.bottonline.addWidget(self.typecms)

        # вторая линия фильтра
        self.filterline = QtWidgets.QHBoxLayout()

        self.filterline.addWidget(QtWidgets.QLabel("|"))
        lbldeepdivisiob = QtWidgets.QLabel("углубленное деление")
        self.deepdivisionchecbox = QtWidgets.QCheckBox()
        self.filterline.addWidget(self.deepdivisionchecbox)
        self.filterline.addWidget(lbldeepdivisiob)

        self.sepcheckboxbymodyl = QtWidgets.QCheckBox()
        self.filterline.addWidget(self.sepcheckboxbymodyl)
        self.filterline.addWidget(QtWidgets.QLabel("деление по блокам"))

        self.filterline.addWidget(QtWidgets.QLabel("|"))
        lbldepartmenterr = QtWidgets.QLabel("Показывать ошибки:")
        self.filterline.addWidget(lbldepartmenterr)

        lbldepartmenterrimpos = QtWidgets.QLabel("Верстки")
        self.checkboximposererr = QtWidgets.QCheckBox()
        self.checkboximposererr.setCheckState(2)
        self.filterline.addWidget(self.checkboximposererr)
        self.filterline.addWidget(lbldepartmenterrimpos)

        lbldepartmenterrprog = QtWidgets.QLabel("Програм")
        self.checkboxprogramerr = QtWidgets.QCheckBox()
        self.checkboxprogramerr.setCheckState(2)
        self.filterline.addWidget(self.checkboxprogramerr)
        self.filterline.addWidget(lbldepartmenterrprog)

        lbldepartmenterrmanag = QtWidgets.QLabel("Манагер")
        self.checkboxmanagererr = QtWidgets.QCheckBox()
        self.checkboxmanagererr.setCheckState(2)
        self.filterline.addWidget(self.checkboxmanagererr)
        self.filterline.addWidget(lbldepartmenterrmanag)

        self.filterline.addWidget(QtWidgets.QLabel("|"))

        self.widgforbottonline2 = QtWidgets.QWidget()
        self.widgforbottonline2.setLayout(self.filterline)
        self.widgforbottonline2.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)

        # разные типы вывода
        self.outtypeline = QtWidgets.QHBoxLayout()
        self.alllist = QtWidgets.QPushButton('все ошибки')
        self.alllist.clicked.connect(self.alllistreport)
        self.alllist.setFixedSize(QtCore.QSize(150, 25))
        self.outtypeline.addWidget(self.alllist)

        self.separationchecbox = QtWidgets.QCheckBox()
        self.outtypeline.addWidget(self.separationchecbox)

        self.imposerlist = QtWidgets.QPushButton('Только верстальщики')
        self.imposerlist.clicked.connect(self.imposerlistreport)
        self.imposerlist.setFixedSize(QtCore.QSize(150, 25))
        self.outtypeline.addWidget(self.imposerlist)

        self.managerlist = QtWidgets.QPushButton('Только менеджеры')
        self.managerlist.clicked.connect(self.managerlistreport)
        self.managerlist.setFixedSize(QtCore.QSize(150, 25))
        self.outtypeline.addWidget(self.managerlist)

        self.programlist = QtWidgets.QPushButton('Только прогеры')
        self.programlist.clicked.connect(self.programlistreport)
        self.programlist.setFixedSize(QtCore.QSize(150, 25))
        self.outtypeline.addWidget(self.programlist)

        self.errtype = QtWidgets.QComboBox(self)
        tmp = list(initail.uniq_module(initail.reader))
        tmp.insert(0, 'Все')
        self.errtype.addItems(tmp)
        self.outtypeline.addWidget(self.errtype)

        self.widgforbottonline = QtWidgets.QWidget()
        self.widgforbottonline.setLayout(self.bottonline)
        self.widgforbottonline.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        self.mainBox.addWidget(self.widgforbottonline)
        self.mainBox.addWidget(self.widgforbottonline2)

        self.widgfortypeerr = QtWidgets.QWidget()
        self.widgfortypeerr.setLayout(self.outtypeline)
        self.widgfortypeerr.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        self.mainBox.addWidget(self.widgfortypeerr)

        self.graphline = QtWidgets.QHBoxLayout()

        self.directorieslist = initail.directlist(initail.pathdirect)
        self.qlist = QtWidgets.QTreeWidget(self)
        self.qlist.itemChanged.connect(self.set_checbox_parent)
        self.qlist.setColumnCount(1)
        self.qlist.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Expanding)
        self.qlist.setMaximumSize(200, 2000)
        self.qlist.setMinimumSize(200, 400)
        smesh = 1
        for i in range(len(self.directorieslist[0][1])):
            item = QtWidgets.QTreeWidgetItem()
            item.setData(0, QtCore.Qt.UserRole, 'direct')
            item.setText(0, self.directorieslist[0][1][i])
            item.setCheckState(0, 0)
            if self.directorieslist[i + smesh][1] != []:
                for k in range(len(self.directorieslist[i + smesh][1])):
                    child = QtWidgets.QTreeWidgetItem()
                    child.setText(0, "Тестовая" if str(self.directorieslist[i + smesh][1][k]) == "Test" else "Живая")
                    child.setData(0, QtCore.Qt.UserRole, 'direct')
                    # child.setText(0, self.directorieslist[i + smesh][1][k])
                    child.setCheckState(0, 0)
                    for j in range(len(self.directorieslist[i + smesh + k + 1][2])):
                        childfile = QtWidgets.QTreeWidgetItem()
                        wayf, tasktypef, cmstypef, datef, otherinfo = self.take_info_error_list(i, j, k, smesh)
                        childfile.setData(0, QtCore.Qt.UserRole, [wayf, tasktypef, cmstypef, datef, otherinfo])
                        childfile.setText(0, self.directorieslist[i + smesh + k + 1][2][j])
                        childfile.setBackground(0, QtCore.Qt.red)
                        childfile.setCheckState(0, 0)
                        child.addChild(childfile)
                    item.addChild(child)
                    self.qlist.expandItem(child)
            smesh += len(self.directorieslist[i + smesh][1])
            self.qlist.addTopLevelItem(item)

        self.qlist2 = QtWidgets.QListWidget(self)
        self.qlist2.itemDoubleClicked.connect(self.on_listdetail_clicked)

        self.qlist.setHeaderLabels(["Древо проектов"])

        self.horizforbuttontree = QtWidgets.QHBoxLayout(self)
        self.horizforbuttontree.setSpacing(0)
        self.openalltree = QtWidgets.QPushButton('открыть')
        self.openalltree.setMaximumSize(QtCore.QSize(55, 25))
        self.openalltree.clicked.connect(self.open_all_tree)
        self.horizforbuttontree.addWidget(self.openalltree)

        self.closealltree = QtWidgets.QPushButton('закрыть')
        self.closealltree.setMaximumSize(QtCore.QSize(55, 25))
        self.closealltree.clicked.connect(self.close_all_tree)
        self.horizforbuttontree.addWidget(self.closealltree)

        self.filteralltree = QtWidgets.QPushButton('по фильтру')
        self.filteralltree.setMaximumSize(QtCore.QSize(70, 25))
        self.filteralltree.clicked.connect(self.open_list_tree)
        self.horizforbuttontree.addWidget(self.filteralltree)

        self.horizforbuttontreeW = QtWidgets.QWidget()
        self.horizforbuttontreeW.setLayout(self.horizforbuttontree)

        self.vertforbut = QtWidgets.QVBoxLayout(self)
        self.vertforbut.addWidget(self.qlist)
        self.vertforbut.addWidget(self.horizforbuttontreeW)
        self.vertforbutW = QtWidgets.QWidget()
        self.vertforbutW.setLayout(self.vertforbut)
        self.graphline.addWidget(self.vertforbutW)
        self.graphline.addWidget(self.qlist2)
        self.widgforgraphline = QtWidgets.QWidget()
        self.widgforgraphline.setLayout(self.graphline)
        self.widgforgraphline.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.mainBox.addWidget(self.widgforgraphline)

        self.setLayout(self.mainBox)

    def open_all_tree(self):
        for i in range(self.qlist.topLevelItemCount()):
            for j in range(self.qlist.topLevelItem(i).childCount()):
                self.qlist.topLevelItem(i).child(j).setExpanded(1)
                self.qlist.topLevelItem(i).setExpanded(1)

    def close_all_tree(self):
        for i in range(self.qlist.topLevelItemCount()):
            for j in range(self.qlist.topLevelItem(i).childCount()):
                self.qlist.topLevelItem(i).child(j).setExpanded(0)
                self.qlist.topLevelItem(i).setExpanded(0)

    def on_Buttonsortparam_clicked(self):
        pass

    def activfilt(self):
        for i in range(self.qlist.topLevelItemCount()):
            for j in range(self.qlist.topLevelItem(i).childCount()):
                for k in range(self.qlist.topLevelItem(i).child(j).childCount()):
                    c = self.qlist.topLevelItem(i).child(j).child(k).data(0, QtCore.Qt.UserRole)
                    self.qlist.topLevelItem(i).child(j).child(k).setCheckState(0, 0)
                    if self.datestartchecbox.checkState() == 2:
                        if (c[3] < self.datestartinput.date()) or (c[3] > self.dateendinput.date()):
                            continue
                    if self.typetaskchecbox.checkState() == 2:
                        if c[1] != self.typecombo.currentText():
                            continue
                    if self.typecmschecbox.checkState() == 2:
                        if c[2] != self.typecms.currentText():
                            continue
                    self.qlist.topLevelItem(i).child(j).child(k).setCheckState(0, 2)

    def take_info_error_list(self, i, j, k, smesh):
        way = self.directorieslist[i + smesh][0] + "/" + self.directorieslist[i + smesh][1][k] + "/" + \
              self.directorieslist[i + smesh + k + 1][2][j]
        df = pd.read_csv(way)
        dates = date(df.year_save[0], df.month_save[0], df.day_save[0])
        cmstype = df.cmstype[0]
        tasktype = df.tasktype[0]
        otherinfo = [df.redmine_number[0], df.imposer[0], df.manager[0], df.programmer[0], df.prokuror[0],
                     df.iteration[0]]
        return way, tasktype, cmstype, dates, otherinfo

    def updateerrlist(self, task_type):
        # self.dferr = pd.DataFrame(
        #     columns=["Unnamed: 0", "test_module", "test_case", "err_text", "err_type", "activ_err", "datesave",
        #              "year_save",
        #              "month_save", "day_save", "tasktype", "cmstype", "checkbox_vers", "time_on_work", "redmine_number",
        #              "manager", "imposer", "programmer", "tester_coment", "prokuror", "iteration"])
        self.dferr = pd.DataFrame()
        for i in range(self.qlist.topLevelItemCount()):
            for j in range(self.qlist.topLevelItem(i).childCount()):
                for k in range(self.qlist.topLevelItem(i).child(j).childCount()):
                    if self.qlist.topLevelItem(i).child(j).child(k).checkState(0) == 2:
                        c = self.qlist.topLevelItem(i).child(j).child(k).data(0, QtCore.Qt.UserRole)
                        dffile = pd.read_csv(c[0])
                        self.dferr = pd.concat([self.dferr, dffile], ignore_index=True, sort=False)
        self.dferr = self.dferr[self.dferr.activ_err == 1]
        if task_type != 'Все':
            self.dferr = self.dferr[self.dferr.test_module == task_type]
        # self.updateerrlistall()

    def updateerrlistall(self):
        # self.dferr = pd.DataFrame(
        #     columns=["Unnamed: 0", "test_module", "test_case", "err_text", "err_type", "activ_err", "datesave",
        #              "year_save",
        #              "month_save", "day_save", "tasktype", "cmstype", "checkbox_vers", "time_on_work", "redmine_number",
        #              "manager", "imposer", "programmer", "tester_coment", "prokuror", "iteration"])
        self.dferr = pd.DataFrame()
        for i in range(self.qlist.topLevelItemCount()):
            for j in range(self.qlist.topLevelItem(i).childCount()):
                for k in range(self.qlist.topLevelItem(i).child(j).childCount()):
                    if self.qlist.topLevelItem(i).child(j).child(k).checkState(0) == 2:
                        c = self.qlist.topLevelItem(i).child(j).child(k).data(0, QtCore.Qt.UserRole)
                        dffile = pd.read_csv(c[0])
                        self.dferr = pd.concat([self.dferr, dffile], ignore_index=True, sort=False)
        self.dferr = self.dferr[self.dferr.activ_err == 1]
        self.printlist()

    def createList(self):
        pass

    def printlist(self):
        self.qlist2.clear()
        self.deepparam = 0
        if self.checkboximposererr.checkState() == 0:
            self.dferr = self.dferr[self.dferr['err_type'] != 'imposer']
        if self.checkboxmanagererr.checkState() == 0:
            self.dferr = self.dferr[self.dferr['err_type'] != 'manager']
        if self.checkboxprogramerr.checkState() == 0:
            self.dferr = self.dferr[self.dferr['err_type'] != 'programmer']
        if self.deepdivisionchecbox.checkState() == 2:
            self.deepparam = 1
            self.counterr = self.dferr.groupby(['test_module', 'test_case'])['err_text'].count().reset_index()
            self.counterr = self.counterr.sort_values('err_text', ascending=False).reset_index()
            if self.sepcheckboxbymodyl.checkState() == 0:
                for i in range(len(self.counterr)):
                    item = QtWidgets.QListWidgetItem()
                    item.setText(
                        str(self.counterr.loc[i]['err_text']) + ' ' + str(
                            self.counterr.loc[i]['test_module']) + " - " + str(
                            self.counterr.loc[i]['test_case']))
                    item.setData(QtCore.Qt.UserRole,
                                 [self.counterr.loc[i]['test_module'], self.counterr.loc[i]['test_case']])
                    self.qlist2.addItem(item)
            else:
                tmplistmod = self.dferr.groupby(['test_module'])['err_text'].count().reset_index()
                tmplistmod = tmplistmod.sort_values('err_text', ascending=False).reset_index()
                tmplistmod = tmplistmod['test_module'].unique()
                for el in tmplistmod:
                    item = QtWidgets.QListWidgetItem()
                    item.setText(str(el))
                    item.setData(QtCore.Qt.UserRole,
                                 [el, 0])
                    item.setForeground(QtCore.Qt.blue)
                    self.qlist2.addItem(item)
                    self.tmpdferr = self.dferr[self.dferr['test_module'] == el].groupby(['test_case'])[
                        'err_text'].count().reset_index()
                    self.tmpdferr = self.tmpdferr.sort_values('err_text', ascending=False).reset_index()
                    for j in range(len(self.tmpdferr)):
                        item = QtWidgets.QListWidgetItem()
                        item.setText(' ' +
                                     str(self.tmpdferr.loc[j]['err_text']) + '\t' + str(
                            self.tmpdferr.loc[j]['test_case']))
                        item.setData(QtCore.Qt.UserRole,
                                     [el, self.tmpdferr.loc[j]['test_case']])
                        self.qlist2.addItem(item)
                    # print(self.counterr.loc[i].size)
                    # print(self.counterr.loc[i])

        else:
            self.counterr = self.dferr.groupby(['test_module'])['err_text'].count().reset_index()
            self.counterr = self.counterr.sort_values('err_text', ascending=False).reset_index()
            for i in range(len(self.counterr)):
                item = QtWidgets.QListWidgetItem()
                item.setText(
                    str(self.counterr.loc[i]['err_text']) + ' ' + str(
                        self.counterr.loc[i]['test_module']))
                item.setData(QtCore.Qt.UserRole,
                             [self.counterr.loc[i]['test_module'], self.counterr.loc[i]['test_module']])
                self.qlist2.addItem(item)

    def on_listdetail_clicked(self, item):
        if item.data(QtCore.Qt.UserRole)[1] == 0:
            return
        if self.deepparam == 1:
            self.detailerrlist = self.dferr[(self.dferr['test_module'] == item.data(QtCore.Qt.UserRole)[0]) & (
                    self.dferr['test_case'] == item.data(QtCore.Qt.UserRole)[1])]
        else:
            self.detailerrlist = self.dferr[self.dferr['test_module'] == item.data(QtCore.Qt.UserRole)[0]]
        self.adderrinlist()
        # self.errordetail = QtWidgets.QWidget()
        # qlistdetaillist = QtWidgets.QVBoxLayout()
        # self.qlistdetail = QtWidgets.QListWidget()
        # self.qlistdetail.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # self.adderrinlist()
        # qlistdetaillist.addWidget(self.qlistdetail)
        # self.errordetail.setLayout(qlistdetaillist)
        # self.errordetail.show()
        # self.errordetail.setGeometry(300, 300, 600, 300)

    def adderrinlist(self):
        # self.qlistdetail.clear()
        # errtypelist = ['imposer', 'manager', 'programmer']
        # for type in errtypelist:
        #     dftype = self.detailerrlist[self.detailerrlist['err_type'] == type].reset_index()
        #     if len(dftype.index) != 0:
        #         if type == 'imposer':
        #             trp = QtWidgets.QListWidgetItem('Верстка:')
        #             self.qlistdetail.addItem(trp)
        #         elif type == 'manager':
        #             trp = QtWidgets.QListWidgetItem('Менеджмент:')
        #             self.qlistdetail.addItem(trp)
        #         else:
        #             trp = QtWidgets.QListWidgetItem('Программинг:')
        #             self.qlistdetail.addItem(trp)
        #         for i in range(len(self.detailerrlist[self.detailerrlist['err_type'] == type].index)):
        #             trp = QtWidgets.QListWidgetItem('-' + str(dftype.loc[i]['err_text']))
        #             self.qlistdetail.addItem(trp)
        #         trp = QtWidgets.QListWidgetItem('-' * 40)
        #         self.qlistdetail.addItem(trp)

        self.errdetWindow = DetailErrorListWidget(self.detailerrlist)
        self.errdetWindow.show()

    def alllistreport(self):
        self.updateerrlist(self.errtype.currentText())
        self.errallWindow = ErrorListWidget(self.dferr, self.separationchecbox.checkState(), -1)
        self.updateerrlistall()
        self.errallWindow.show()

    def imposerlistreport(self):
        self.updateerrlist(self.errtype.currentText())
        self.errallWindow = ErrorListWidget(self.dferr, self.separationchecbox.checkState(), 0)
        self.updateerrlistall()
        self.errallWindow.show()

    def managerlistreport(self):
        self.updateerrlist(self.errtype.currentText())
        self.errallWindow = ErrorListWidget(self.dferr, self.separationchecbox.checkState(), 1)
        self.updateerrlistall()
        self.errallWindow.show()

    def programlistreport(self):
        self.updateerrlist(self.errtype.currentText())
        self.errallWindow = ErrorListWidget(self.dferr, self.separationchecbox.checkState(), 2)
        self.updateerrlistall()
        self.errallWindow.show()

    def set_checbox_parent(self, item, column):
        if item.parent() == None:
            for i in range(item.childCount()):
                item.child(i).setCheckState(0, item.checkState(column))
                for j in range(item.child(i).childCount()):
                    item.child(i).child(j).setCheckState(0, item.checkState(column))
        elif item.childCount() != 0:
            for i in range(item.childCount()):
                item.child(i).setCheckState(0, item.checkState(column))
        else:
            pass

    def open_list_tree(self):
        for i in range(self.qlist.topLevelItemCount()):
            paramend = 0
            for j in range(self.qlist.topLevelItem(i).childCount()):
                for k in range(self.qlist.topLevelItem(i).child(j).childCount()):
                    if self.qlist.topLevelItem(i).child(j).child(k).checkState(0) == 2:
                        self.qlist.topLevelItem(i).child(j).setExpanded(1)
                        paramend = 1
                        break
                    self.qlist.topLevelItem(i).child(j).setExpanded(0)
            if paramend != 0:
                self.qlist.topLevelItem(i).setExpanded(1)
            else:
                self.qlist.topLevelItem(i).setExpanded(0)


class ErrorListWidget(QtWidgets.QWidget):
    def __init__(self, param, separ, buttype=-1):
        super().__init__()
        self.param = param
        self.buttype = buttype
        self.separation = 1 if separ else 0
        self.setGeometry(300, 300, 1350, 700)

        self.setWindowTitle('Тут смотрим ошибки')
        self.mainBox = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainBox)

        # строчка с заданиями
        # self.task_number_w = QtWidgets.QWidget()
        # self.task_number = QtWidgets.QHBoxLayout()
        # self.task_number_w.setLayout(self.task_number)
        # lbiter = QtWidgets.QLabel("Используемые задачи", self)
        # self.task_number.addWidget(lbiter)
        # self.mainBox.addWidget(self.task_number_w)
        # for i in range(self.param.redmine_number.nunique()):
        #     qbtn = QtWidgets.QPushButton(str(self.param.redmine_number.unique()[i]), self)
        #     qbtn.clicked.connect(self.on_button_num_task_clic)
        #     qbtn.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        #     qbtn.setFixedSize(QtCore.QSize(110, 20))
        #     self.task_number.addWidget(qbtn)
        if self.buttype == -1:
            if self.separation:
                # верстальщики
                self.imposer_block = QtWidgets.QWidget()
                lbvers = QtWidgets.QLabel("лажи верстальщиков", self)
                self.imposer_block_w_l = QtWidgets.QVBoxLayout()
                self.imposer_block_w_l.addWidget(lbvers)
                self.imposer_block.setLayout(self.imposer_block_w_l)
                self.mainBox.addWidget(self.imposer_block)
                self.qlistimp = QtWidgets.QListWidget(self)
                self.imposer_block_w_l.addWidget(self.qlistimp)
                self.qlistimp.itemClicked.connect(self.on_listdetail_clicked)
                self.add_item_list('imposer')
                # менеджеры
                self.manager_block = QtWidgets.QWidget()
                lbvers = QtWidgets.QLabel("лажи менеджеров", self)
                self.manager_block_w_l = QtWidgets.QVBoxLayout()
                self.manager_block_w_l.addWidget(lbvers)
                self.manager_block.setLayout(self.manager_block_w_l)
                self.mainBox.addWidget(self.manager_block)
                self.qlistman = QtWidgets.QListWidget(self)
                self.manager_block_w_l.addWidget(self.qlistman)
                self.qlistman.itemClicked.connect(self.on_listdetail_clicked)
                self.add_item_list('manager')
                # прогеры
                self.prog_block = QtWidgets.QWidget()
                lbvers = QtWidgets.QLabel("лажи прогеров", self)
                self.prog_block_w_l = QtWidgets.QVBoxLayout()
                self.prog_block_w_l.addWidget(lbvers)
                self.prog_block.setLayout(self.prog_block_w_l)
                self.mainBox.addWidget(self.prog_block)
                self.qlistprog = QtWidgets.QListWidget(self)
                self.prog_block_w_l.addWidget(self.qlistprog)
                self.qlistprog.itemClicked.connect(self.on_listdetail_clicked)
                self.add_item_list('programmer')
            else:
                self.all_block = QtWidgets.QWidget()
                lbvers = QtWidgets.QLabel("вcе ошибки", self)
                self.all_block_w_l = QtWidgets.QVBoxLayout()
                self.all_block_w_l.addWidget(lbvers)
                self.all_block.setLayout(self.all_block_w_l)
                self.mainBox.addWidget(self.all_block)
                self.qlistall = QtWidgets.QListWidget(self)
                self.all_block_w_l.addWidget(self.qlistall)
                self.qlistall.itemClicked.connect(self.on_listdetail_clicked)
                self.add_item_list('all')
        elif self.buttype == 0:
            self.imposer_block = QtWidgets.QWidget()
            lbvers = QtWidgets.QLabel("лажи верстальщиков", self)
            self.imposer_block_w_l = QtWidgets.QVBoxLayout()
            self.imposer_block_w_l.addWidget(lbvers)
            self.imposer_block.setLayout(self.imposer_block_w_l)
            self.mainBox.addWidget(self.imposer_block)
            self.qlistimp = QtWidgets.QListWidget(self)
            self.imposer_block_w_l.addWidget(self.qlistimp)
            self.qlistimp.itemDoubleClicked.connect(self.on_listdetail_clicked)
            self.add_item_list('imposer')
        elif self.buttype == 1:
            self.manager_block = QtWidgets.QWidget()
            lbvers = QtWidgets.QLabel("лажи менеджеров", self)
            self.manager_block_w_l = QtWidgets.QVBoxLayout()
            self.manager_block_w_l.addWidget(lbvers)
            self.manager_block.setLayout(self.manager_block_w_l)
            self.mainBox.addWidget(self.manager_block)
            self.qlistman = QtWidgets.QListWidget(self)
            self.manager_block_w_l.addWidget(self.qlistman)
            self.qlistman.itemDoubleClicked.connect(self.on_listdetail_clicked)
            self.add_item_list('manager')
        else:
            self.prog_block = QtWidgets.QWidget()
            lbvers = QtWidgets.QLabel("лажи прогеров", self)
            self.prog_block_w_l = QtWidgets.QVBoxLayout()
            self.prog_block_w_l.addWidget(lbvers)
            self.prog_block.setLayout(self.prog_block_w_l)
            self.mainBox.addWidget(self.prog_block)
            self.qlistprog = QtWidgets.QListWidget(self)
            self.prog_block_w_l.addWidget(self.qlistprog)
            self.qlistprog.itemDoubleClicked.connect(self.on_listdetail_clicked)
            self.add_item_list('programmer')

    def on_button_num_task_clic(self):
        sender = self.sender()
        QtGui.QDesktopServices.openUrl(QtCore.QUrl('https://redmine.twinscom.ru/issues/' + str(sender.text())))

    def on_listdetail_clicked(self, item):
        QtGui.QDesktopServices.openUrl(
            QtCore.QUrl('https://redmine.twinscom.ru/issues/' + str(item.data(QtCore.Qt.UserRole)[0])))

    def add_item_list(self, param):
        if param == 'imposer':
            self.qlistimp.clear()
            self.counterr = self.param[self.param.err_type == param].reset_index()
            if self.counterr.sitename.nunique():
                for site in self.counterr.sitename.unique():
                    tmp = self.counterr[self.counterr.sitename == site].reset_index()
                    item = QtWidgets.QListWidgetItem()
                    item.setForeground(QtCore.Qt.blue)
                    item.setText(
                        str(site))
                    item.setData(QtCore.Qt.UserRole, [tmp.loc[0]['redmine_number']])
                    self.qlistimp.addItem(item)
                    for i in range(len(tmp)):
                        item = QtWidgets.QListWidgetItem()
                        item.setText('   ' +
                                     str(tmp.loc[i]['err_text']))
                        item.setData(QtCore.Qt.UserRole, [tmp.loc[i]['redmine_number']])
                        self.qlistimp.addItem(item)
        elif param == 'manager':
            self.qlistman.clear()
            self.counterr = self.param[self.param.err_type == param].reset_index()
            if self.counterr.sitename.nunique():
                for site in self.counterr.sitename.unique():
                    tmp = self.counterr[self.counterr.sitename == site].reset_index()
                    item = QtWidgets.QListWidgetItem()
                    item.setForeground(QtCore.Qt.blue)
                    item.setText(
                        str(site))
                    item.setData(QtCore.Qt.UserRole, [tmp.loc[0]['redmine_number']])
                    self.qlistman.addItem(item)
                    for i in range(len(tmp)):
                        item = QtWidgets.QListWidgetItem()
                        item.setText('   ' +
                                     str(tmp.loc[i]['err_text']))
                        item.setData(QtCore.Qt.UserRole, [tmp.loc[i]['redmine_number']])
                        self.qlistman.addItem(item)
        elif param == 'programmer':
            self.qlistprog.clear()
            self.counterr = self.param[self.param.err_type == param].reset_index()
            if self.counterr.sitename.nunique():
                for site in self.counterr.sitename.unique():
                    tmp = self.counterr[self.counterr.sitename == site].reset_index()
                    item = QtWidgets.QListWidgetItem()
                    item.setForeground(QtCore.Qt.blue)
                    item.setText(
                        str(site))
                    item.setData(QtCore.Qt.UserRole, [tmp.loc[0]['redmine_number']])
                    self.qlistprog.addItem(item)
                    for i in range(len(tmp)):
                        item = QtWidgets.QListWidgetItem()
                        item.setText('   ' +
                                     str(tmp.loc[i]['err_text']))
                        item.setData(QtCore.Qt.UserRole, [tmp.loc[i]['redmine_number']])
                        self.qlistprog.addItem(item)
        else:
            self.qlistall.clear()
            self.counterr = self.param.reset_index()
            if self.counterr.sitename.nunique():
                for site in self.counterr.sitename.unique():
                    tmp = self.counterr[self.counterr.sitename == site].reset_index()
                    item = QtWidgets.QListWidgetItem()
                    item.setForeground(QtCore.Qt.blue)
                    item.setText(
                        str(site))
                    item.setData(QtCore.Qt.UserRole, [tmp.loc[0]['redmine_number']])
                    self.qlistall.addItem(item)
                    for i in range(len(tmp)):
                        item = QtWidgets.QListWidgetItem()
                        item.setText('   ' +
                                     str(tmp.loc[i]['err_text']))
                        item.setData(QtCore.Qt.UserRole, [tmp.loc[i]['redmine_number']])
                        self.qlistall.addItem(item)


class DetailErrorListWidget(QtWidgets.QWidget):
    def __init__(self, param):
        super().__init__()
        self.param = param
        self.setGeometry(300, 300, 1350, 700)
        self.setWindowTitle('Тут смотрим ошибки')
        self.mainBox = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainBox)

        # строчка с заданиями
        # self.task_number_w = QtWidgets.QWidget()
        # self.task_number = QtWidgets.QHBoxLayout()
        # self.task_number_w.setLayout(self.task_number)
        # lbiter = QtWidgets.QLabel("Используемые задачи", self)
        # self.task_number.addWidget(lbiter)
        # self.mainBox.addWidget(self.task_number_w)
        #
        # #заготовка под названия всемто номера
        # # quest = pd.unique(self.param[['sitename', 'redmine_number']].values.ravel())
        # # but_arr = []
        # # i=0
        # # while i<(len(quest)):
        # #     tmp = [quest[i],quest[i+1]]
        # #     but_arr.append(tmp)
        # #     i+=2
        # for i in range(self.param.redmine_number.nunique()):
        #     qbtn = QtWidgets.QPushButton(str(self.param.redmine_number.unique()[i]), self)
        #     qbtn.clicked.connect(self.on_button_num_task_clic)
        #     qbtn.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        #     qbtn.setFixedSize(QtCore.QSize(110, 20))
        #     self.task_number.addWidget(qbtn)

        # верстальщики
        if len(self.param[self.param['err_type'] == 'imposer']) != 0:
            self.imposer_block = QtWidgets.QWidget()
            lbvers = QtWidgets.QLabel("лажи верстальщиков", self)
            self.imposer_block_w_l = QtWidgets.QVBoxLayout()
            self.imposer_block_w_l.addWidget(lbvers)
            self.imposer_block.setLayout(self.imposer_block_w_l)
            self.mainBox.addWidget(self.imposer_block)
            self.qlistimp = QtWidgets.QListWidget(self)
            self.imposer_block_w_l.addWidget(self.qlistimp)
            self.qlistimp.itemDoubleClicked.connect(self.on_listdetail_clicked)
            self.add_item_list('imposer')
        # менеджеры
        if len(self.param[self.param['err_type'] == 'manager']) != 0:
            self.manager_block = QtWidgets.QWidget()
            lbvers = QtWidgets.QLabel("лажи менеджеров", self)
            self.manager_block_w_l = QtWidgets.QVBoxLayout()
            self.manager_block_w_l.addWidget(lbvers)
            self.manager_block.setLayout(self.manager_block_w_l)
            self.mainBox.addWidget(self.manager_block)
            self.qlistman = QtWidgets.QListWidget(self)
            self.manager_block_w_l.addWidget(self.qlistman)
            self.qlistman.itemDoubleClicked.connect(self.on_listdetail_clicked)
            self.add_item_list('manager')
        # прогеры
        if len(self.param[self.param['err_type'] == 'programmer']) != 0:
            self.prog_block = QtWidgets.QWidget()
            lbvers = QtWidgets.QLabel("лажи прогеров", self)
            self.prog_block_w_l = QtWidgets.QVBoxLayout()
            self.prog_block_w_l.addWidget(lbvers)
            self.prog_block.setLayout(self.prog_block_w_l)
            self.mainBox.addWidget(self.prog_block)
            self.qlistprog = QtWidgets.QListWidget(self)
            self.prog_block_w_l.addWidget(self.qlistprog)
            self.qlistprog.itemDoubleClicked.connect(self.on_listdetail_clicked)
            self.add_item_list('programmer')

    def on_button_num_task_clic(self):
        sender = self.sender()
        QtGui.QDesktopServices.openUrl(QtCore.QUrl('https://redmine.twinscom.ru/issues/' + str(sender.text())))

    def on_listdetail_clicked(self, item):
        QtGui.QDesktopServices.openUrl(
            QtCore.QUrl('https://redmine.twinscom.ru/issues/' + str(item.data(QtCore.Qt.UserRole)[0])))

    def add_item_list(self, param):
        if param == 'imposer':
            self.qlistimp.clear()
            self.counterr = self.param[self.param.err_type == param].reset_index()
            if self.counterr.sitename.nunique():
                for site in self.counterr.sitename.unique():
                    tmp = self.counterr[self.counterr.sitename == site].reset_index()
                    item = QtWidgets.QListWidgetItem()
                    item.setForeground(QtCore.Qt.blue)
                    item.setText(
                        str(site))
                    item.setData(QtCore.Qt.UserRole, [tmp.loc[0]['redmine_number']])
                    self.qlistimp.addItem(item)
                    for i in range(len(tmp)):
                        item = QtWidgets.QListWidgetItem()
                        item.setText('   ' +
                                     str(tmp.loc[i]['err_text']))
                        item.setData(QtCore.Qt.UserRole, [tmp.loc[i]['redmine_number']])
                        self.qlistimp.addItem(item)
        elif param == 'manager':
            self.qlistman.clear()
            self.counterr = self.param[self.param.err_type == param].reset_index()
            if self.counterr.sitename.nunique():
                for site in self.counterr.sitename.unique():
                    tmp = self.counterr[self.counterr.sitename == site].reset_index()
                    item = QtWidgets.QListWidgetItem()
                    item.setForeground(QtCore.Qt.blue)
                    item.setText(
                        str(site))
                    item.setData(QtCore.Qt.UserRole, [tmp.loc[0]['redmine_number']])
                    self.qlistman.addItem(item)
                    for i in range(len(tmp)):
                        item = QtWidgets.QListWidgetItem()
                        item.setText('   ' +
                                     str(tmp.loc[i]['err_text']))
                        item.setData(QtCore.Qt.UserRole, [tmp.loc[i]['redmine_number']])
                        self.qlistman.addItem(item)
        elif param == 'programmer':
            self.qlistprog.clear()
            self.counterr = self.param[self.param.err_type == param].reset_index()
            if self.counterr.sitename.nunique():
                for site in self.counterr.sitename.unique():
                    tmp = self.counterr[self.counterr.sitename == site].reset_index()
                    item = QtWidgets.QListWidgetItem()
                    item.setForeground(QtCore.Qt.blue)
                    item.setText(
                        str(site))
                    item.setData(QtCore.Qt.UserRole, [tmp.loc[0]['redmine_number']])
                    self.qlistprog.addItem(item)
                    for i in range(len(tmp)):
                        item = QtWidgets.QListWidgetItem()
                        item.setText('   ' +
                                     str(tmp.loc[i]['err_text']))
                        item.setData(QtCore.Qt.UserRole, [tmp.loc[i]['redmine_number']])
                        self.qlistprog.addItem(item)
        else:
            self.qlistall.clear()
            self.counterr = self.param.reset_index()
            if self.counterr.sitename.nunique():
                for site in self.counterr.sitename.unique():
                    tmp = self.counterr[self.counterr.sitename == site].reset_index()
                    item = QtWidgets.QListWidgetItem()
                    item.setForeground(QtCore.Qt.blue)
                    item.setText(
                        str(site))
                    item.setData(QtCore.Qt.UserRole, [tmp.loc[0]['redmine_number']])
                    self.qlistall.addItem(item)
                    for i in range(len(tmp)):
                        item = QtWidgets.QListWidgetItem()
                        item.setText('   ' +
                                     str(tmp.loc[i]['err_text']))
                        item.setData(QtCore.Qt.UserRole, [tmp.loc[i]['redmine_number']])
                        self.qlistall.addItem(item)


class ChangeModul(QtWidgets.QMainWindow):
    def __init__(self, test_modul, test_bloc, id):
        super().__init__()
        self.mainlayout_w = QtWidgets.QVBoxLayout(self)
        self.butandspis_w = QtWidgets.QHBoxLayout(self)
        self.adapterrlayout_w = QtWidgets.QHBoxLayout(self)
        self.buttonSendErron_w = QtWidgets.QHBoxLayout()

        self.mainlayout_w.addLayout(self.butandspis_w)
        self.mainlayout_w.addLayout(self.adapterrlayout_w)
        self.mainlayout_w.addLayout(self.buttonSendErron_w)

        self.id_w = id
        self.testmodule_w = initail.uniq_module(initail.reader)  # считываем все модули
        self.testmoduleactiv_w = test_modul  # в качестве основногго берем первый
        self.testcaselist_w = initail.test_case_list(initail.reader,
                                                     self.testmoduleactiv_w)  # считываем список юлоков в модуле
        self.butandspis_w.setSpacing(0)
        self.butnlist_w = QtWidgets.QGridLayout(self)
        self.butnlist_w.setSpacing(4)
        self.butnlist_w.setAlignment(QtCore.Qt.AlignTop)  # список сверху
        stroc, col = 0, 0
        for i in range(len(self.testmodule_w)):
            qbtn = QtWidgets.QPushButton(str(self.testmodule_w[i]), self)
            if str(self.testmodule_w[i]) == self.testmoduleactiv_w:
                qbtn.setStyleSheet(
                    " QPushButton {  font-weight: 700;  color: white;   border-radius: 3px;  background: rgb(64,199,129); } QPushButton::hover {background: rgb(53, 167, 110);} ")
                self.senderold_w = qbtn
            qbtn.clicked.connect(self.on_pushButton_clicked_w)
            qbtn.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
            qbtn.setFixedSize(QtCore.QSize(145, 30))
            self.butnlist_w.addWidget(qbtn, stroc, col)
            if col == 0:
                col += 1
            else:
                stroc += 1
                col = 0
        self.sizewidg_w = QtWidgets.QWidget(self)
        self.sizewidg_w.setLayout(self.butnlist_w)
        self.sizewidg_w.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        self.butandspis_w.addWidget(self.sizewidg_w)
        self.layoutblocks_w = QtWidgets.QVBoxLayout(self)
        self.qlist_w = QtWidgets.QListWidget(self)
        self.qlist_w.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        self.qlist_w.setMaximumSize(250, stroc * 37)
        self.qlist_w.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.qlist_w.itemChanged.connect(self.qlistitemchecked_w)
        self.qlist_w.setWordWrap(True)
        self.blockanable_w = None
        for i in range(len(self.testcaselist_w)):
            item = QtWidgets.QListWidgetItem()
            item.setText(self.testcaselist_w['test_case'][i])
            item.setData(QtCore.Qt.UserRole, self.testcaselist_w['test_case'][i])
            item.setCheckState(0)
            if str(self.testcaselist_w['test_case'][i]) == test_bloc:
                self.blockanable_w = item
                item.setCheckState(2)
            self.qlist_w.addItem(item)

        self.layoutblocks_w.addWidget(self.qlist_w)
        self.butandspis_w.addLayout(self.layoutblocks_w)
        self.adapterr_w = QtWidgets.QCheckBox("Кнопка адаптивной ошибки", self)
        self.adapterrlayout_w.addWidget(self.adapterr_w)

        self.buttonAddReport_w = QtWidgets.QPushButton('сохранить с новым модулем', self)
        self.buttonAddReport_w.setStyleSheet(
            " QPushButton {  font-weight: 700;  color: white;   border-radius: 3px;  background: rgb(64,199,129); } QPushButton::hover {background: rgb(53, 167, 110);} ")
        self.buttonAddReport_w.setMinimumSize(175, 40)
        self.buttonAddReport_w.clicked.connect(self.on_button_send_error_modul_w)
        self.buttonSendErron_w.addWidget(self.buttonAddReport_w)

        self.centralwidget_w = QtWidgets.QWidget()
        self.centralwidget_w.setLayout(self.mainlayout_w)
        self.setCentralWidget(self.centralwidget_w)

        # размеры и заголовок
        self.setGeometry(400, 200, 600, 400)
        self.setWindowTitle(initail.file_name)

    def on_button_send_error_modul_w(self):
        k = 0
        for index in range(self.qlist_w.count()):
            if self.qlist_w.item(index).checkState() == QtCore.Qt.Checked:
                testcaseactiv = self.qlist_w.item(index).text()
                k += 1
        if k == 0:
            testcaseactiv = 'необходимо уточнение'
        adapt_err = 1 if self.adapterr_w.checkState() else 0
        Main.change_err_modul(Main(), self.id_w, self.testmoduleactiv_w, testcaseactiv, adapt_err)
        self.close()

    def qlistitemchecked_w(self):
        pass

    def on_pushButton_clicked_w(self):
        """Изменение просматриваемого модуля"""
        sender = self.sender()
        if self.senderold_w is not None:
            self.senderold_w.setStyleSheet("")
        sender.setStyleSheet(
            " QPushButton {  font-weight: 700;  color: white;   border-radius: 3px;  background: rgb(64,199,129); } QPushButton::hover {background: rgb(53, 167, 110);} ")
        self.senderold_w = sender
        self.testmoduleactiv_w = sender.text()
        self.blockanable_w = None
        self.testcaselist_w = initail.test_case_list(initail.reader, self.testmoduleactiv_w)
        self.updateUIlist_w()

    def updateUIlist_w(self):
        self.qlist_w.clear()
        for i in range(len(self.testcaselist_w)):
            item = QtWidgets.QListWidgetItem()
            item.setText(self.testcaselist_w['test_case'][i])
            item.setData(QtCore.Qt.UserRole, self.testcaselist_w['test_case'][i])
            item.setCheckState(0)
            self.qlist_w.addItem(item)


def main():
    app = QtWidgets.QApplication(sys.argv)
    main_win = Main()
    # main = ChangeModul('Адаптивка','необходимо уточнение', 0)
    # print(main.testmodule_w)
    # main_win = ReportWindow()
    main_win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

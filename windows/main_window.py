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
from lshmodel.lsh import *

class Main(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.testmodule = initail.uniq_module(initail.reader)  # считываем все модули
        self.testmoduleactiv = self.testmodule[0]  # в качестве основного берем первый
        self.testcaselist = initail.test_case_list(initail.reader,
                                                   self.testmoduleactiv)  # считываем список блоков в модуле
        self.errordeptype = None  # типы ошибок по отделу
        self.senderold = None
        self.testcaseactiv = None
        self.blockanable = None
        self.buglist = initail.read_errors_df()
        self.errcount = len(self.buglist)
        self.shifterr = 1

        self.create_interface()
        self.find_forwst = Forest_search()
        self.setWindowIcon(QtGui.QIcon(initail.work_spase + r'\files\favicon.png'))


    def create_interface(self):
        # добавляем верхнее меню
        self.create_up_menu()

        self.mainlayout = QtWidgets.QHBoxLayout(self)  # основной лайоут для накидывание на него полей
        self.leftlist = QtWidgets.QVBoxLayout(self)  # левый столбец
        self.layoutreport = QtWidgets.QVBoxLayout()  # правый столбец

        # левый столбец
        self.left_colms()

        # правый столбец
        self.right_colums()

        # делвем mainlayout основным на экране
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setLayout(self.mainlayout)
        self.setCentralWidget(self.centralwidget)

        # размеры и заголовок
        self.setGeometry(400, 200, 1000, 600)
        self.setWindowTitle(initail.file_name)

    def create_up_menu(self):
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
        featuresMenu = QtWidgets.QMenu("Допплюшки", self)
        wallposition = QtWidgets.QAction('Поверх окон', self)
        wallposition.setShortcut('Ctrl+F')
        wallposition.triggered.connect(self.flagchangetop)
        featuresMenu.addAction(wallposition)
        shiftErrInd = QtWidgets.QAction('Добавление сдвига', self)
        shiftErrInd.triggered.connect(self.add_shift_ind)
        featuresMenu.addAction(shiftErrInd)
        self.menuBar().addAction(profjectfile)
        self.menuBar().addAction(browsefolder)
        self.menuBar().addAction(errsave)
        self.menuBar().addAction(errsee)
        self.menuBar().addAction(helpsee)
        self.menuBar().addMenu(featuresMenu)

    def left_colms(self):
        # создаем
        self.butandspis = QtWidgets.QHBoxLayout(self)
        self.adapterrlayout = QtWidgets.QVBoxLayout(self)
        self.inputerrorlayoyt = QtWidgets.QVBoxLayout(self)
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
        self.inputerror.textChanged.connect(self.text_change)
        self.inputerror.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        self.inputerror.setMaximumSize(570, 104)
        self.inputerror.setMinimumSize(560, 104)
        self.inputerrorlayoyt.addWidget(self.inputerror)

        self.helpline = QtWidgets.QListWidget()
        self.inputerrorlayoyt.addWidget(self.helpline)
        self.helpline.setMaximumSize(570, 2000)
        self.helpline.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Expanding)
        self.helpline.setWordWrap(True)
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

    def right_colums(self):
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

    def text_change(self):
        text = self.inputerror.toPlainText()
        if len(text.split()) < 2:
            list_tmp = ['надо ввести еще что то']
        else:
            list_tmp = self.find_forwst.predict(text)
            #list_tmp = set(list_tmp)
        self.print_help(list_tmp)

    def print_help(self, list_help):
        self.helpline.clear()
        for el in list_help:
            trp = QtWidgets.QListWidgetItem(el)
            trp.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable)
            self.helpline.addItem(trp)

    def on_browsefolder_clicked(self):
        """Выбираем папку кликом"""
        file_name = QtWidgets.QFileDialog.getExistingDirectory(self, 'Выберите папку', initail.pathdirect)
        # открыть диалог выбора директории и установить значение переменной
        # равной пути к выбранной директории
        if file_name:  # не продолжать выполнение, если пользователь не выбрал директорию
            file_name = file_name.split('/')
            print(file_name)
            if file_name[-1] in ['Test','Live']:
                file_name.pop()
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
        id = int(text.pop(0)) - self.shifterr
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
            text = str(ind + self.shifterr) + '. ' + str(self.buglist.iloc[ind]['err_text'])
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
                id = int(self.report.item(self.report.currentRow()).text().split('. ')[0]) - self.shifterr
                if id == self.buglist.shape[0]-1:
                    self.buglist = self.buglist.drop([id])
                else:
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
                id = int(self.report.item(self.report.currentRow()).text().split('. ')[0]) - self.shifterr
                self.buglist.loc[id]['err_type'] = self.errordeptype
        initail.save_errors(self.buglist)
        self.updateReportList()

    def editmodulfromreport(self):
        if self.report.currentRow() != -1:
            id = int(self.report.item(self.report.currentRow()).text().split('. ')[0]) - self.shifterr
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

    def add_shift_ind(self):
        text, ok = QtWidgets.QInputDialog.getText(self, 'Смещение ошибок', 'Введи с какой ошибки начинать:')
        if ok:
            if int(text) > 0:
                self.shifterr = int(text)
            else:
                self.shifterr = 1
        self.updateUIlist()
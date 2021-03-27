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
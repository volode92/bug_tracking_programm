import pandas as pd
import csv
import os
import configparser
from datetime import datetime, date
import shutil

config = configparser.ConfigParser()
config.read('settings.ini')

#project_list = config.get("Settings", "path_proj")
path = config.get("Settings", "path")
pathdirect = config.get("Settings", "pathdirect")  # для тест листа(d ,wlw
file_name = config.get("Settings", "file_name")
tests_list = config.get("Settings", "tests_list")
work_spase = config.get("Settings", "work_spase")
file_obj = work_spase + tests_list
reader = pd.read_csv(file_obj)
tasklist = list(pd.read_csv('files/tasklist.csv', encoding='UTF-8')['task_type'])
cmslist = list(pd.read_csv('files/cmslist.csv', encoding='UTF-8')['name_cms'])


def uniq_module(reader):
    """Загрузка уникальных модулей для отображении на кнопоках"""
    x = reader.test_module.unique()
    return x


def test_case_list(reader, test_module):
    x = reader[reader.test_module == test_module]['test_case'].reset_index()
    return x


def save_report(text):
    a = datetime.today()
    with open(path + '/report' + str(datetime.date(a)) + '.txt', "w", encoding='UTF8') as file:
        file.write(text)


def save_errors(testerror):
    a = datetime.today()
    name_file_save = path + '/' + str(datetime.date(a)) + '.csv'
    testerror.to_csv(name_file_save)

def read_errors_df():
    a = datetime.today()
    name_file_save = path + '/' + str(datetime.date(a)) + '.csv'
    if os.path.exists(name_file_save):
        buglist = pd.DataFrame(columns=['test_module', 'test_case', 'err_text', 'err_type', 'activ_err', 'adapt_err'])
        buglist1 = pd.read_csv(name_file_save)
        for i in range(len(buglist1)):
            buglist.loc[i] = buglist1.loc[i]
    else:
        buglist = pd.DataFrame(columns=['test_module', 'test_case', 'err_text', 'err_type','activ_err', 'adapt_err'])
    return buglist


def send_errors_hard(array):
    a = datetime.today()
    with open(path + '/' + str(datetime.date(a)) + '.txt', "w", encoding='UTF8') as file:
        for i in range(len(array)):
            file.write(array[i])


def save_errors_hard(testerror):
    a = datetime.today()
    with open(path + '/' + str(datetime.date(a)) + '.txt', "w", encoding='UTF8') as file:
        file.write(testerror)


def read_report():
    a = datetime.today()
    if os.path.exists(path + '/' + str(datetime.date(a)) + '.txt'):
        file = open(path + '/' + str(datetime.date(a)) + '.txt', encoding='UTF8')
        text = file.readlines()
        return text
    else:
        return ''


def check_directories(direct):
    if os.path.exists(direct):
        return True
    return False


def create_directories(direct):
    os.makedirs(direct)


def save_settings():
    config.set("Settings", "path", path)
    config.set("Settings", "pathdirect", pathdirect)
    config.set("Settings", "file_name", file_name)


    with open('settings.ini', "w") as config_file:
        config.write(config_file)


def save_param_prodject(datesave, tasktype, cmstype, checkbox_vers, time_on_work, redmine_number, manager, imposer, programmer, tester_coment, prokuror, iteration, frontenddevop):
    #self.datacheckcol.date(), self.combotesttype.currentText(), self.combocmstype.currentText(), self.checboxtest.checkState(),
    # self.inputtesttime.text(), self.tesknumberinp.text(), self.comboinfomened.currentText(),
    # self.comboinfoverst.currentText(), self.comboinfoprog.currentText(), self.testcoment.text(), self.prokuror, self.iterationnum.text()
    # дописывание строчки с параметрами в файл
    a = datetime.today()
    name_file_load = path + '/' + str(datetime.date(a)) + '.csv'
    name_file_save = path + '/' + str(datesave.year()) + '-' + str(datesave.month()) + '-' + str(datesave.day()) + '.csv'
    df_for_save = pd.read_csv(name_file_load)
    df_for_save = df_for_save[df_for_save['activ_err'] == 1]
    df_for_save['datesave'] = date(datesave.year(),datesave.month(),datesave.day())
    df_for_save['year_save'] = datesave.year()
    df_for_save['month_save'] = datesave.month()
    df_for_save['day_save'] = datesave.day()
    df_for_save['tasktype'] = tasktype
    df_for_save['cmstype'] = cmstype
    df_for_save['checkbox_vers'] = checkbox_vers
    df_for_save['time_on_work'] = time_on_work
    df_for_save['redmine_number'] = redmine_number
    df_for_save['manager'] = manager
    df_for_save['imposer'] = imposer
    df_for_save['programmer'] = programmer
    df_for_save['tester_coment'] = tester_coment
    df_for_save['prokuror'] = prokuror
    df_for_save['iteration'] = iteration
    df_for_save['frontenddevop'] = frontenddevop
    df_for_save['sitename'] = path.split('/')[1]
    del df_for_save['Unnamed: 0']
    df_for_save.to_csv(name_file_save, encoding="utf-8")

    if checkbox_vers == 0:
        if not os.path.exists(path + '\Live'):
            os.makedirs(path + '\Live')
        shutil.move(name_file_save, path + '\Live')
    else:
        if not os.path.exists(path + '\Test'):
            os.makedirs(path + '\Test')
        shutil.move(name_file_save, path + '\Test')
    if name_file_save != name_file_load:
        os.remove(name_file_load)


def directlist(pathdirect):
    tree = os.walk(pathdirect)
    sp = []
    for i in tree:
        sp.append(i)
    return sp


def writehelp(help):
    with open(work_spase + '/files/help.txt', "w", encoding='UTF8') as file:
        file.write(help)


def readhelp():
    with open(work_spase + '/files/help.txt', "r", encoding='UTF8') as file:
        help = file.read()
    return help

def worker_list(department, activat=1):
    if department == 0:
        df = pd.read_csv(work_spase + r'/files/imposer.csv', encoding='UTF-8')
        if activat:
            df = df[df.activ == 1]
        return df.name.unique()
    elif department == 1:
        df = pd.read_csv(work_spase + r'/files/manager.csv', encoding='UTF-8')
        if activat:
            df = df[df.activ == 1]
        return df.name.unique()
    else:
        df = pd.read_csv(work_spase + r'/files/proger.csv', encoding='UTF-8')
        if activat:
            df = df[df.activ == 1]
        return df.name.unique()

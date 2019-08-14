# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Thimble.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread
import json
import time
from datetime import datetime, timedelta, date
import organ
import os, subprocess
import sys
import winsound
from gtts import gTTS
import calendar
from threading import Thread
import re

alarm_times = {}
my_date = date.today()
day = calendar.day_name[my_date.weekday()]
language = 'en'

class ExternalFunctions:
    def interval(start_hour, start_minute, end_hour, end_minute, period1_time, period1_message, period2_time, period2_message):
        start = datetime.strptime(str(start_hour) + ":" + str(start_minute), "%H:%M")
        end = datetime.strptime(str(end_hour) + ":" + str(end_minute), "%H:%M")
        x = [period1_time, period2_time]
        y = [period1_message, period2_message]

        for i in range(50):
            ad = x[i % 2]
            if start > (end + timedelta(minutes=1)):
                break
            else:
                alarm_times[start.strftime("%I:%M %p")] = y[i % 2]
                start += timedelta(minutes=ad)

    def prse(string):
        l = string.split(",")

        start_hour = int(l[0])
        start_minute = int(l[1])
        end_hour = int(l[2])
        end_minute = int(l[3])
        period1_time = int(l[4])
        period1_message = l[5]
        period2_time = int(l[6])
        period2_message = l[7]

        ExternalFunctions.interval(start_hour, start_minute, end_hour, end_minute, period1_time, period1_message, period2_time, period2_message)

class Alarm(QThread):

    def __init__(self, display_lines):
        QThread.__init__(self)
        self.lines = display_lines

    def __del__(self):
        self.wait()

    def run(self):
        while True:
            now = datetime.now().strftime("%I:%M %p")

            if now in alarm_times.keys():
                Ui_MainWindow().signal_look(self.lines, now)
                print(f"ALARM AT {now}")
                winsound.Beep(400, 500)

                myobj = gTTS(text=alarm_times[now], lang=language, slow=False)
                myobj.save("announcement.mp3")
                load = [r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe", r"C:\Users\Adam\Desktop\python_projects\scripts\Projects\GUI\Main\announcement.mp3"]
                p = subprocess.Popen(load)

                time.sleep(5)
                p.terminate()
                time.sleep(55)
            else:
                time.sleep(2)

class Ui_MainWindow(object):

    def __init__(self):
        self.input_lines = {}
        self.display_lines = {}
        self.input_line_count = 0

    def remove(self):
        for button in list(self.input_lines.items()):
            if "input_buttondelete_right_" in button[0] and button[1].isChecked():
                but_id = button[0][-2:].strip("_")

                self.input_lines[button[0]].setChecked(False)

                button[1].deleteLater()
                self.input_lines["input_timeedit_left_" + but_id].deleteLater()
                self.input_lines["input_actionedit_right_" + but_id].deleteLater()
                self.input_lines["input_buttondelete_right_" + but_id].deleteLater()
                self.input_lines["input_frame_left_" + but_id].deleteLater()
                self.input_lines["input_frame_right_" + but_id].deleteLater()

                del self.input_lines["input_timeedit_left_" + but_id]
                del self.input_lines["input_actionedit_right_" + but_id]
                del self.input_lines["input_buttondelete_right_" + but_id]
                del self.input_lines["input_frame_left_" + but_id]
                del self.input_lines["input_frame_right_" + but_id]
                del self.input_lines["input_gridlayout_left" + but_id]
                del self.input_lines["input_horizontallayout_right_" + but_id]

            else:
                pass

    def add_input_line(self, t=False, d=False, p=False):
        _translate = QtCore.QCoreApplication.translate

        input_frame_left = "input_frame_left_" + str(self.input_line_count)
        input_gridlayout_left = "input_gridlayout_left" + str(self.input_line_count)
        input_timeedit_left = "input_timeedit_left_" + str(self.input_line_count)
        input_frame_right = "input_frame_right_" + str(self.input_line_count)
        input_horizontallayout_right = "input_horizontallayout_right_" + str(self.input_line_count)
        input_actionedit_right = "input_actionedit_right_" + str(self.input_line_count)
        input_buttondelete_right = "input_buttondelete_right_" + str(self.input_line_count)
        icon = QtGui.QIcon()

        icon.addPixmap(QtGui.QPixmap(r"C:\Users\Adam\Desktop\organ photos\download.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.input_lines[input_frame_left] = QtWidgets.QFrame(self.settings_add_items_scroll_area_contents) # FRAME FOR TIME INPUT
        self.input_lines[input_frame_left].setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.input_lines[input_frame_left].setFrameShadow(QtWidgets.QFrame.Raised)
        self.input_lines[input_frame_left].setObjectName(input_frame_left)

        self.input_lines[input_gridlayout_left] = QtWidgets.QGridLayout(self.input_lines[input_frame_left]) # GRID LAYOUT FOR TIME INPUT
        self.input_lines[input_gridlayout_left].setObjectName(input_gridlayout_left)

        self.input_lines[input_timeedit_left] = QtWidgets.QLineEdit(self.input_lines[input_frame_left])
        #if p == True:
            #self.input_lines[input_timeedit_left].setEnabled(False)
        #else:
        self.input_lines[input_timeedit_left].setEnabled(True)
        self.input_lines[input_timeedit_left].setStyleSheet("color: rgb(194, 194, 194);\n" + "background-color: rgb(76, 76, 76);")
        self.input_lines[input_timeedit_left].setText("")
        self.input_lines[input_timeedit_left].setAlignment(QtCore.Qt.AlignCenter)
        self.input_lines[input_timeedit_left].setClearButtonEnabled(False)
        self.input_lines[input_timeedit_left].setObjectName(input_timeedit_left)
        if p == True:
            self.input_lines[input_timeedit_left].setText(_translate("MainWindow", "PERIOD"))
        else:
            self.input_lines[input_timeedit_left].setPlaceholderText(_translate("MainWindow", "Time"))
        self.input_lines[input_gridlayout_left].addWidget(self.input_lines[input_timeedit_left], 0, 0, 1, 1)

        self.formLayout.setWidget(self.input_line_count, QtWidgets.QFormLayout.LabelRole, self.input_lines[input_frame_left])

        ###

        self.input_lines[input_frame_right] = QtWidgets.QFrame(self.settings_add_items_scroll_area_contents)
        self.input_lines[input_frame_right].setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.input_lines[input_frame_right].setFrameShadow(QtWidgets.QFrame.Raised)
        self.input_lines[input_frame_right].setObjectName(input_frame_right)

        self.input_lines[input_horizontallayout_right] = QtWidgets.QHBoxLayout(self.input_lines[input_frame_right])
        self.input_lines[input_horizontallayout_right].setObjectName(input_horizontallayout_right)

        self.input_lines[input_actionedit_right] = QtWidgets.QLineEdit(self.input_lines[input_frame_right])
        #if p == True:
            #self.input_lines[input_actionedit_right].setEnabled(False)
        #else:
        self.input_lines[input_actionedit_right].setEnabled(True)
        self.input_lines[input_actionedit_right].setFocusPolicy(QtCore.Qt.StrongFocus)
        self.input_lines[input_actionedit_right].setStyleSheet("color: rgb(194, 194, 194);\n" + "background-color: rgb(76, 76, 76);")
        self.input_lines[input_actionedit_right].setText("")
        self.input_lines[input_actionedit_right].setAlignment(QtCore.Qt.AlignCenter)
        self.input_lines[input_actionedit_right].setClearButtonEnabled(False)
        self.input_lines[input_actionedit_right].setObjectName(input_actionedit_right)

        if p == True:
            breakaway = []
            start_hour = self.settings_extra_settings_set_period_start_time_input_hour.text()
            start_minute = self.settings_extra_settings_set_period_start_time_input_minute.text()
            end_hour = self.lineEdit_54.text()
            end_minute = self.lineEdit_55.text()
            period_1_length = self.lineEdit_56.text()
            period_1_message = self.lineEdit_52.text()
            period_2_length = self.settings_extra_settings_set_period_period2_input_length.text()
            period_2_message = self.settings_extra_settings_set_period_period2_input_message.text()
            breakaway.extend((start_hour, start_minute, end_hour, end_minute, period_1_length, period_1_message, period_2_length, period_2_message))

            if all(len(i) > 0 for i in breakaway):
                message = f"{start_hour},{start_minute},{end_hour},{end_minute},{period_1_length},{period_1_message},{period_2_length},{period_2_message}"
                self.input_lines[input_actionedit_right].setText(_translate("MainWindow", message))
            else:
                self.input_lines[input_actionedit_right].setText(_translate("MainWindow", "ERROR: PERIOD NOT VALID"))

        else:
            self.input_lines[input_actionedit_right].setPlaceholderText(_translate("MainWindow", "Action"))

        self.input_lines[input_horizontallayout_right].addWidget(self.input_lines[input_actionedit_right])

        self.input_lines[input_buttondelete_right] = QtWidgets.QPushButton(self.input_lines[input_frame_right])
        self.input_lines[input_buttondelete_right].setCheckable(True)
        self.input_lines[input_buttondelete_right].setText("")
        self.input_lines[input_buttondelete_right].setIcon(icon)
        self.input_lines[input_buttondelete_right].setFlat(True)
        self.input_lines[input_buttondelete_right].setObjectName(input_buttondelete_right)
        self.input_lines[input_buttondelete_right].clicked.connect(self.remove)
        self.input_lines[input_horizontallayout_right].addWidget(self.input_lines[input_buttondelete_right])

        self.formLayout.setWidget(self.input_line_count, QtWidgets.QFormLayout.FieldRole, self.input_lines[input_frame_right])

        if t != False:
            self.input_lines[input_timeedit_left].setText(t)
        if d != False:
            self.input_lines[input_actionedit_right].setText(d)

        self.input_line_count += 1

    def add_period(self):
        self.add_input_line(p=True)

    def save(self):
        save_dict = {}
        l = []
        for key, value in list(self.input_lines.items()):
            if value.__class__.__name__ == "QLineEdit":
                if "timeedit" in key:
                    l.append(key[-2:].strip("_"))
                    l.append(value.text())
                if "actionedit" in key:
                    l.append(value.text())

        for i in range(0, len(l), 3):
            if len(l[i+1]) == 0 or len(l[i+2]) == 0:
                pass
            else:
                save_dict[l[i]] = (l[i+1], l[i+2])

        with open('main_save.json', 'w') as f:
            f.write(json.dumps(save_dict))

    def load(self):
        if len(self.input_lines) > 0:
            for button in list(self.input_lines.items()):
                if "input_buttondelete_right_" in button[0]:
                    button[1].click()

        with open('main_save.json', 'r') as f:
            data = json.load(f)
            for k, v in list(data.items()):
                if v[0] == "PERIOD":
                    self.add_input_line(t=v[0], d=v[1], p=True)
                else:
                    self.add_input_line(t=v[0], d=v[1])

    def commit(self):
        print("ALARM ACTIVE")
        if len(alarm_times) > 0:
            alarm_times.clear()

        for key, value in list(self.input_lines.items()):
            idx = key[-2:].strip("_")
            if value.__class__.__name__ == "QLineEdit" and value.text() != "PERIOD":
                alarm_times[self.input_lines[f"input_timeedit_left_{idx}"].text()] = self.input_lines[f"input_actionedit_right_{idx}"].text()
            if value.__class__.__name__ == "QLineEdit" and value.text() == "PERIOD":
                ExternalFunctions.prse(self.input_lines[f"input_actionedit_right_{idx}"].text())
        try:
            del alarm_times["PERIOD"]
        except:
            pass

        with open('alarm_times.json', 'w') as f:
            f.write(json.dumps(alarm_times))

        self.settings_commit_button.setEnabled(False)
        self.settings_commit_button.setStyleSheet("color: rgb(194, 194, 194);background-color: rgb(100, 50, 50)")

        self.display()

    def display(self):
        left = "display_left_" + str(self.input_line_count)
        right = "display_right_" + str(self.input_line_count)

        if len(self.display_lines) > 0:
            for k, v in list(self.display_lines.items()):
                v.deleteLater()
                del self.display_lines[k]

        _translate = QtCore.QCoreApplication.translate

        for k, v in list(alarm_times.items()):
            left = "display_left_" + str(self.input_line_count)
            right = "display_right_" + str(self.input_line_count)

            self.display_lines[left] = QtWidgets.QLineEdit(self.DisplayScrollAreaContents)
            self.display_lines[left].setEnabled(False)
            self.display_lines[left].setStyleSheet("color: rgb(194, 194, 194);")
            self.display_lines[left].setAlignment(QtCore.Qt.AlignCenter)
            self.display_lines[left].setObjectName(left)
            self.formLayout_4.setWidget(self.input_line_count, QtWidgets.QFormLayout.LabelRole, self.display_lines[left])
            self.display_lines[left].setText(_translate("MainWindow", k))

            self.display_lines[right] = QtWidgets.QLineEdit(self.DisplayScrollAreaContents)
            self.display_lines[right].setEnabled(False)
            self.display_lines[right].setStyleSheet("color: rgb(194, 194, 194);")
            self.display_lines[right].setAlignment(QtCore.Qt.AlignCenter)
            self.display_lines[right].setObjectName(right)
            self.formLayout_4.setWidget(self.input_line_count, QtWidgets.QFormLayout.FieldRole, self.display_lines[right])
            self.display_lines[right].setText(_translate("MainWindow", v))

            self.input_line_count += 1

        self.alarm = Alarm(self.display_lines)
        self.alarm.start()

    def signal_look(self, lines, now): ############################################################################################################################################################################################################
        self.display_lines = lines

        for k, v in list(self.display_lines.items()):
            if re.match(r"\d\d:\d\d", v.text()) and v.text() == now:
                num = k[-2:].strip("_")

                self.display_lines[f'display_left_{num}'].setStyleSheet("color: rgb(194, 194, 194);background-color: rgb(50, 100, 50)")
                self.display_lines[f'display_right_{num}'].setStyleSheet("color: rgb(194, 194, 194);background-color: rgb(50, 100, 50)")

            if re.match(r"\d\d:\d\d", v.text()) and v.text() != now:
                num = k[-2:].strip("_")

                self.display_lines[f'display_left_{num}'].setStyleSheet("color: rgb(194, 194, 194);")
                self.display_lines[f'display_right_{num}'].setStyleSheet("color: rgb(194, 194, 194);")

    def lock_save_check(self):
        if self.settings_extra_settings_customize_lock_checkbox.isChecked():
            self.settings_save.setEnabled(False)
            self.settings_save.setStyleSheet("background-color: rgb(100, 50, 50)")
        else:
            self.settings_save.setEnabled(True)
            self.settings_save.setStyleSheet("background-color: rgb(58, 58, 58)")

    def setupUi(self, MainWindow):
        print("WARNING: DO NOT PRESS COMMIT MORE THAN ONCE. IF YOU HAVE TO REDO A TIME BLOCK, SAVE, EXIT, THEN LOAD.")

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
        MainWindow.setMouseTracking(False)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("background-color: rgb(58, 58, 58);\n"
"color: rgb(255, 255, 255);")
        MainWindow.setDocumentMode(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.MainTabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.MainTabWidget.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setBold(True)
        font.setWeight(75)
        self.MainTabWidget.setFont(font)
        self.MainTabWidget.setStyleSheet("color: rgb(58, 58, 58);\n"
"\n"
"")
        self.MainTabWidget.setTabPosition(QtWidgets.QTabWidget.West)
        self.MainTabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.MainTabWidget.setDocumentMode(True)
        self.MainTabWidget.setMovable(False)
        self.MainTabWidget.setObjectName("MainTabWidget")
        self.Home = QtWidgets.QWidget()
        self.Home.setObjectName("Home")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.Home)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.home_screen = QtWidgets.QTextBrowser(self.Home)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(75)
        self.home_screen.setFont(font)
        self.home_screen.setStyleSheet("border-color: rgb(58, 58, 58);")
        self.home_screen.setObjectName("home_screen")
        self.gridLayout_2.addWidget(self.home_screen, 0, 0, 1, 1)
        self.MainTabWidget.addTab(self.Home, "")
        self.Alarms = QtWidgets.QWidget()
        self.Alarms.setObjectName("Alarms")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.Alarms)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.SubTabWidget = QtWidgets.QTabWidget(self.Alarms)
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setBold(True)
        font.setWeight(75)
        self.SubTabWidget.setFont(font)
        self.SubTabWidget.setStyleSheet("color: rgb(58, 58, 58);\n"
"\n"
"")
        self.SubTabWidget.setDocumentMode(True)
        self.SubTabWidget.setTabBarAutoHide(False)
        self.SubTabWidget.setObjectName("SubTabWidget")
        self.Display = QtWidgets.QWidget()
        self.Display.setObjectName("Display")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.Display)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.DisplayScrollArea = QtWidgets.QScrollArea(self.Display)
        self.DisplayScrollArea.setFrameShape(QtWidgets.QFrame.Box)
        self.DisplayScrollArea.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.DisplayScrollArea.setWidgetResizable(True)
        self.DisplayScrollArea.setObjectName("DisplayScrollArea")
        self.DisplayScrollAreaContents = QtWidgets.QWidget()
        self.DisplayScrollAreaContents.setGeometry(QtCore.QRect(0, 0, 1001, 607))
        self.DisplayScrollAreaContents.setObjectName("DisplayScrollAreaContents")
        self.formLayout_4 = QtWidgets.QFormLayout(self.DisplayScrollAreaContents)
        self.formLayout_4.setObjectName("formLayout_4")


#################################################################################################################################

#################################################################################################################################

        self.DisplayScrollArea.setWidget(self.DisplayScrollAreaContents)
        self.gridLayout_4.addWidget(self.DisplayScrollArea, 1, 0, 1, 1)
        self.SubTabWidget.addTab(self.Display, "")
        self.Settings = QtWidgets.QWidget()
        self.Settings.setObjectName("Settings")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.Settings)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.settings_main_settings_frame = QtWidgets.QGroupBox(self.Settings)
        self.settings_main_settings_frame.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.settings_main_settings_frame.setStyleSheet("color: rgb(194, 194, 194);")
        self.settings_main_settings_frame.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.settings_main_settings_frame.setFlat(True)
        self.settings_main_settings_frame.setObjectName("settings_main_settings_frame")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.settings_main_settings_frame)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.settings_add_buttons_frame = QtWidgets.QFrame(self.settings_main_settings_frame)
        self.settings_add_buttons_frame.setAcceptDrops(False)
        self.settings_add_buttons_frame.setStyleSheet("border-color: rgb(194, 194, 194);")
        self.settings_add_buttons_frame.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.settings_add_buttons_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.settings_add_buttons_frame.setObjectName("settings_add_buttons_frame")
        self.gridLayout_12 = QtWidgets.QGridLayout(self.settings_add_buttons_frame)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.settings_add_single = QtWidgets.QPushButton(self.settings_add_buttons_frame)
        self.settings_add_single.setObjectName("settings_add_single")
        self.gridLayout_12.addWidget(self.settings_add_single, 0, 0, 1, 1, QtCore.Qt.AlignHCenter)

        self.settings_add_period = QtWidgets.QPushButton(self.settings_add_buttons_frame)
        self.settings_add_period.setObjectName("settings_add_period")
        self.settings_add_period.clicked.connect(self.add_period)
        self.gridLayout_12.addWidget(self.settings_add_period, 2, 0, 1, 1)
        self.gridLayout_10.addWidget(self.settings_add_buttons_frame, 0, 1, 1, 1)

        ################################################################################
        self.settings_save = QtWidgets.QPushButton(self.settings_add_buttons_frame)
        self.settings_save.setObjectName("settings_save")
        self.settings_save.clicked.connect(self.save)
        self.gridLayout_12.addWidget(self.settings_save, 3, 0, 1, 1)
        self.settings_save.setStyleSheet("background-color: rgb(100, 50, 50)")

        self.settings_save.setEnabled(False)

        self.settings_load = QtWidgets.QPushButton(self.settings_add_buttons_frame)
        self.settings_load.setObjectName("settings_load")
        self.settings_load.clicked.connect(self.load)
        self.gridLayout_12.addWidget(self.settings_load, 4, 0, 1, 1)
        ################################################################################

        self.settings_add_items_frame = QtWidgets.QFrame(self.settings_main_settings_frame)
        self.settings_add_items_frame.setStyleSheet("border-color: rgb(194, 194, 194);")
        self.settings_add_items_frame.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.settings_add_items_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.settings_add_items_frame.setObjectName("settings_add_items_frame")
        self.gridLayout_50 = QtWidgets.QGridLayout(self.settings_add_items_frame)
        self.gridLayout_50.setObjectName("gridLayout_50")
        self.settings_add_items_scroll_area = QtWidgets.QScrollArea(self.settings_add_items_frame)
        self.settings_add_items_scroll_area.setWidgetResizable(True)
        self.settings_add_items_scroll_area.setObjectName("settings_add_items_scroll_area")
        self.settings_add_items_scroll_area_contents = QtWidgets.QWidget()
        self.settings_add_items_scroll_area_contents.setGeometry(QtCore.QRect(0, 0, 860, 233))
        self.settings_add_items_scroll_area_contents.setObjectName("settings_add_items_scroll_area_contents")
        self.formLayout = QtWidgets.QFormLayout(self.settings_add_items_scroll_area_contents)
        self.formLayout.setObjectName("formLayout")

        ###

        self.settings_add_items_scroll_area.setWidget(self.settings_add_items_scroll_area_contents)
        self.gridLayout_50.addWidget(self.settings_add_items_scroll_area, 0, 0, 1, 1)
        self.gridLayout_10.addWidget(self.settings_add_items_frame, 0, 0, 1, 1)
        self.gridLayout_5.addWidget(self.settings_main_settings_frame, 0, 0, 1, 1)
        self.settings_commit_button = QtWidgets.QPushButton(self.Settings)
        self.settings_commit_button.setAutoFillBackground(False)
        self.settings_commit_button.setStyleSheet("color: rgb(194, 194, 194);\n"
"background-color: rgb(89, 89, 89);")
        self.settings_commit_button.setCheckable(False)
        self.settings_commit_button.setChecked(False)
        self.settings_commit_button.setAutoDefault(False)
        self.settings_commit_button.setFlat(False)
        self.settings_commit_button.setObjectName("settings_commit_button")
        self.settings_commit_button.clicked.connect(self.commit)
        self.gridLayout_5.addWidget(self.settings_commit_button, 2, 0, 1, 1)
        self.settings_extra_settings_frame = QtWidgets.QGroupBox(self.Settings)
        self.settings_extra_settings_frame.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.settings_extra_settings_frame.setStyleSheet("color: rgb(194, 194, 194);")
        self.settings_extra_settings_frame.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.settings_extra_settings_frame.setFlat(True)
        self.settings_extra_settings_frame.setCheckable(False)
        self.settings_extra_settings_frame.setChecked(False)
        self.settings_extra_settings_frame.setObjectName("settings_extra_settings_frame")
        self.gridLayout_13 = QtWidgets.QGridLayout(self.settings_extra_settings_frame)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.settings_extra_settings_set_period_frame = QtWidgets.QGroupBox(self.settings_extra_settings_frame)
        self.settings_extra_settings_set_period_frame.setStyleSheet("color: rgb(194, 194, 194);")
        self.settings_extra_settings_set_period_frame.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.settings_extra_settings_set_period_frame.setFlat(False)
        self.settings_extra_settings_set_period_frame.setObjectName("settings_extra_settings_set_period_frame")
        self.gridLayout_49 = QtWidgets.QGridLayout(self.settings_extra_settings_set_period_frame)
        self.gridLayout_49.setObjectName("gridLayout_49")
        self.frame_39 = QtWidgets.QFrame(self.settings_extra_settings_set_period_frame)
        self.frame_39.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_39.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_39.setObjectName("frame_39")
        self.gridLayout_45 = QtWidgets.QGridLayout(self.frame_39)
        self.gridLayout_45.setObjectName("gridLayout_45")
        self.label_8 = QtWidgets.QLabel(self.frame_39)
        self.label_8.setStyleSheet("color: rgb(194, 194, 194);")
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout_45.addWidget(self.label_8, 0, 0, 1, 1)
        self.gridLayout_49.addWidget(self.frame_39, 1, 0, 1, 1)
        self.settings_extra_settings_set_period_period2_frame_right = QtWidgets.QFrame(self.settings_extra_settings_set_period_frame)
        self.settings_extra_settings_set_period_period2_frame_right.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.settings_extra_settings_set_period_period2_frame_right.setFrameShadow(QtWidgets.QFrame.Raised)
        self.settings_extra_settings_set_period_period2_frame_right.setObjectName("settings_extra_settings_set_period_period2_frame_right")
        self.gridLayout_39 = QtWidgets.QGridLayout(self.settings_extra_settings_set_period_period2_frame_right)
        self.gridLayout_39.setObjectName("gridLayout_39")
        self.settings_extra_settings_set_period_period2_input_message = QtWidgets.QLineEdit(self.settings_extra_settings_set_period_period2_frame_right)
        self.settings_extra_settings_set_period_period2_input_message.setStyleSheet("color: rgb(194, 194, 194);")
        self.settings_extra_settings_set_period_period2_input_message.setText("")
        self.settings_extra_settings_set_period_period2_input_message.setAlignment(QtCore.Qt.AlignCenter)
        self.settings_extra_settings_set_period_period2_input_message.setObjectName("settings_extra_settings_set_period_period2_input_message")
        self.gridLayout_39.addWidget(self.settings_extra_settings_set_period_period2_input_message, 0, 1, 1, 1)
        self.settings_extra_settings_set_period_period2_input_length = QtWidgets.QLineEdit(self.settings_extra_settings_set_period_period2_frame_right)
        self.settings_extra_settings_set_period_period2_input_length.setStyleSheet("color: rgb(194, 194, 194);")
        self.settings_extra_settings_set_period_period2_input_length.setText("")
        self.settings_extra_settings_set_period_period2_input_length.setAlignment(QtCore.Qt.AlignCenter)
        self.settings_extra_settings_set_period_period2_input_length.setObjectName("settings_extra_settings_set_period_period2_input_length")
        self.gridLayout_39.addWidget(self.settings_extra_settings_set_period_period2_input_length, 0, 0, 1, 1)
        self.gridLayout_49.addWidget(self.settings_extra_settings_set_period_period2_frame_right, 2, 1, 1, 1)
        self.frame_32 = QtWidgets.QFrame(self.settings_extra_settings_set_period_frame)
        self.frame_32.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_32.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_32.setObjectName("frame_32")
        self.gridLayout_38 = QtWidgets.QGridLayout(self.frame_32)
        self.gridLayout_38.setObjectName("gridLayout_38")
        self.lineEdit_52 = QtWidgets.QLineEdit(self.frame_32)
        self.lineEdit_52.setStyleSheet("color: rgb(194, 194, 194);")
        self.lineEdit_52.setText("")
        self.lineEdit_52.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_52.setObjectName("lineEdit_52")
        self.gridLayout_38.addWidget(self.lineEdit_52, 0, 1, 1, 1)
        self.lineEdit_56 = QtWidgets.QLineEdit(self.frame_32)
        self.lineEdit_56.setStyleSheet("color: rgb(194, 194, 194);")
        self.lineEdit_56.setText("")
        self.lineEdit_56.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_56.setObjectName("lineEdit_56")
        self.gridLayout_38.addWidget(self.lineEdit_56, 0, 0, 1, 1)
        self.gridLayout_49.addWidget(self.frame_32, 1, 1, 1, 1)
        self.settings_extra_settings_set_period_start_time_frame_right = QtWidgets.QFrame(self.settings_extra_settings_set_period_frame)
        self.settings_extra_settings_set_period_start_time_frame_right.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.settings_extra_settings_set_period_start_time_frame_right.setFrameShadow(QtWidgets.QFrame.Raised)
        self.settings_extra_settings_set_period_start_time_frame_right.setObjectName("settings_extra_settings_set_period_start_time_frame_right")
        self.gridLayout_36 = QtWidgets.QGridLayout(self.settings_extra_settings_set_period_start_time_frame_right)
        self.gridLayout_36.setObjectName("gridLayout_36")
        self.settings_extra_settings_set_period_start_time_input_hour = QtWidgets.QLineEdit(self.settings_extra_settings_set_period_start_time_frame_right)
        self.settings_extra_settings_set_period_start_time_input_hour.setStyleSheet("color: rgb(194, 194, 194);")
        self.settings_extra_settings_set_period_start_time_input_hour.setText("")
        self.settings_extra_settings_set_period_start_time_input_hour.setAlignment(QtCore.Qt.AlignCenter)
        self.settings_extra_settings_set_period_start_time_input_hour.setObjectName("settings_extra_settings_set_period_start_time_input_hour")
        self.gridLayout_36.addWidget(self.settings_extra_settings_set_period_start_time_input_hour, 0, 0, 1, 1)
        self.settings_extra_settings_set_period_start_time_input_minute = QtWidgets.QLineEdit(self.settings_extra_settings_set_period_start_time_frame_right)
        self.settings_extra_settings_set_period_start_time_input_minute.setStyleSheet("color: rgb(194, 194, 194);")
        self.settings_extra_settings_set_period_start_time_input_minute.setText("")
        self.settings_extra_settings_set_period_start_time_input_minute.setAlignment(QtCore.Qt.AlignCenter)
        self.settings_extra_settings_set_period_start_time_input_minute.setObjectName("settings_extra_settings_set_period_start_time_input_minute")
        self.gridLayout_36.addWidget(self.settings_extra_settings_set_period_start_time_input_minute, 0, 1, 1, 1)
        self.gridLayout_49.addWidget(self.settings_extra_settings_set_period_start_time_frame_right, 0, 1, 1, 1)
        self.settings_extra_settings_set_period_start_time_frame_left = QtWidgets.QFrame(self.settings_extra_settings_set_period_frame)
        self.settings_extra_settings_set_period_start_time_frame_left.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.settings_extra_settings_set_period_start_time_frame_left.setFrameShadow(QtWidgets.QFrame.Raised)
        self.settings_extra_settings_set_period_start_time_frame_left.setObjectName("settings_extra_settings_set_period_start_time_frame_left")
        self.gridLayout_47 = QtWidgets.QGridLayout(self.settings_extra_settings_set_period_start_time_frame_left)
        self.gridLayout_47.setObjectName("gridLayout_47")
        self.settings_extra_settings_set_period_start_time_display = QtWidgets.QLabel(self.settings_extra_settings_set_period_start_time_frame_left)
        self.settings_extra_settings_set_period_start_time_display.setStyleSheet("color: rgb(194, 194, 194);")
        self.settings_extra_settings_set_period_start_time_display.setAlignment(QtCore.Qt.AlignCenter)
        self.settings_extra_settings_set_period_start_time_display.setObjectName("settings_extra_settings_set_period_start_time_display")
        self.gridLayout_47.addWidget(self.settings_extra_settings_set_period_start_time_display, 0, 0, 1, 1)
        self.gridLayout_49.addWidget(self.settings_extra_settings_set_period_start_time_frame_left, 0, 0, 1, 1)
        self.settings_extra_settings_set_period_period2_frame_left = QtWidgets.QFrame(self.settings_extra_settings_set_period_frame)
        self.settings_extra_settings_set_period_period2_frame_left.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.settings_extra_settings_set_period_period2_frame_left.setFrameShadow(QtWidgets.QFrame.Raised)
        self.settings_extra_settings_set_period_period2_frame_left.setObjectName("settings_extra_settings_set_period_period2_frame_left")
        self.gridLayout_48 = QtWidgets.QGridLayout(self.settings_extra_settings_set_period_period2_frame_left)
        self.gridLayout_48.setObjectName("gridLayout_48")
        self.settings_extra_settings_set_period_period2_display = QtWidgets.QLabel(self.settings_extra_settings_set_period_period2_frame_left)
        self.settings_extra_settings_set_period_period2_display.setStyleSheet("color: rgb(194, 194, 194);")
        self.settings_extra_settings_set_period_period2_display.setAlignment(QtCore.Qt.AlignCenter)
        self.settings_extra_settings_set_period_period2_display.setObjectName("settings_extra_settings_set_period_period2_display")
        self.gridLayout_48.addWidget(self.settings_extra_settings_set_period_period2_display, 0, 0, 1, 1)
        self.gridLayout_49.addWidget(self.settings_extra_settings_set_period_period2_frame_left, 2, 0, 1, 1)
        self.frame_40 = QtWidgets.QFrame(self.settings_extra_settings_set_period_frame)
        self.frame_40.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_40.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_40.setObjectName("frame_40")
        self.gridLayout_46 = QtWidgets.QGridLayout(self.frame_40)
        self.gridLayout_46.setObjectName("gridLayout_46")
        self.label_9 = QtWidgets.QLabel(self.frame_40)
        self.label_9.setStyleSheet("color: rgb(194, 194, 194);")
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.gridLayout_46.addWidget(self.label_9, 0, 0, 1, 1)
        self.gridLayout_49.addWidget(self.frame_40, 3, 0, 1, 1)
        self.frame_34 = QtWidgets.QFrame(self.settings_extra_settings_set_period_frame)
        self.frame_34.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_34.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_34.setObjectName("frame_34")
        self.gridLayout_40 = QtWidgets.QGridLayout(self.frame_34)
        self.gridLayout_40.setObjectName("gridLayout_40")
        self.lineEdit_54 = QtWidgets.QLineEdit(self.frame_34)
        self.lineEdit_54.setStyleSheet("color: rgb(194, 194, 194);")
        self.lineEdit_54.setText("")
        self.lineEdit_54.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_54.setObjectName("lineEdit_54")
        self.gridLayout_40.addWidget(self.lineEdit_54, 0, 0, 1, 1)
        self.lineEdit_55 = QtWidgets.QLineEdit(self.frame_34)
        self.lineEdit_55.setStyleSheet("color: rgb(194, 194, 194);")
        self.lineEdit_55.setText("")
        self.lineEdit_55.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_55.setObjectName("lineEdit_55")
        self.gridLayout_40.addWidget(self.lineEdit_55, 0, 1, 1, 1)
        self.gridLayout_49.addWidget(self.frame_34, 3, 1, 1, 1)
        self.gridLayout_13.addWidget(self.settings_extra_settings_set_period_frame, 3, 0, 2, 1, QtCore.Qt.AlignLeft)
        self.settings_extra_settings_customize_frame = QtWidgets.QGroupBox(self.settings_extra_settings_frame)
        self.settings_extra_settings_customize_frame.setStyleSheet("color: rgb(194, 194, 194);")
        self.settings_extra_settings_customize_frame.setAlignment(QtCore.Qt.AlignCenter)
        self.settings_extra_settings_customize_frame.setObjectName("settings_extra_settings_customize_frame")
        self.formLayout_2 = QtWidgets.QFormLayout(self.settings_extra_settings_customize_frame)
        self.formLayout_2.setObjectName("formLayout_2")
        self.settings_extra_settings_customize_tts_checkbox = QtWidgets.QCheckBox(self.settings_extra_settings_customize_frame)
        self.settings_extra_settings_customize_tts_checkbox.setStyleSheet("color: rgb(194, 194, 194);")
        self.settings_extra_settings_customize_tts_checkbox.setChecked(True)
        self.settings_extra_settings_customize_tts_checkbox.setObjectName("settings_extra_settings_customize_tts_checkbox")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.settings_extra_settings_customize_tts_checkbox)

        self.settings_extra_settings_customize_beep_checkbox = QtWidgets.QCheckBox(self.settings_extra_settings_customize_frame)
        self.settings_extra_settings_customize_beep_checkbox.setStyleSheet("color: rgb(194, 194, 194);")
        self.settings_extra_settings_customize_beep_checkbox.setChecked(True)
        self.settings_extra_settings_customize_beep_checkbox.setObjectName("settings_extra_settings_customize_beep_checkbox")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.settings_extra_settings_customize_beep_checkbox)

        self.settings_extra_settings_customize_lock_checkbox = QtWidgets.QCheckBox(self.settings_extra_settings_customize_frame)
        self.settings_extra_settings_customize_lock_checkbox.setStyleSheet("color: rgb(194, 194, 194);")
        self.settings_extra_settings_customize_lock_checkbox.setChecked(True)
        self.settings_extra_settings_customize_lock_checkbox.setObjectName("settings_extra_settings_customize_lock_checkbox")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.settings_extra_settings_customize_lock_checkbox)

        self.settings_extra_settings_customize_lock_checkbox.clicked.connect(self.lock_save_check)

        self.gridLayout_13.addWidget(self.settings_extra_settings_customize_frame, 3, 1, 1, 1, QtCore.Qt.AlignRight)
        self.gridLayout_5.addWidget(self.settings_extra_settings_frame, 1, 0, 1, 1)
        self.SubTabWidget.addTab(self.Settings, "")
        self.gridLayout_3.addWidget(self.SubTabWidget, 0, 0, 1, 1)
        self.MainTabWidget.addTab(self.Alarms, "")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.tab_6)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.scrollArea_5 = QtWidgets.QScrollArea(self.tab_6)
        self.scrollArea_5.setWidgetResizable(True)
        self.scrollArea_5.setObjectName("scrollArea_5")
        self.scrollAreaWidgetContents_5 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_5.setGeometry(QtCore.QRect(0, 0, 1021, 650))
        self.scrollAreaWidgetContents_5.setObjectName("scrollAreaWidgetContents_5")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_5)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.textEdit = QtWidgets.QTextEdit(self.scrollAreaWidgetContents_5)
        self.textEdit.setStyleSheet("color: rgb(194, 194, 194);")
        self.textEdit.setObjectName("textEdit")
        self.gridLayout_11.addWidget(self.textEdit, 0, 0, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.scrollAreaWidgetContents_5)
        self.pushButton_3.setAutoFillBackground(False)
        self.pushButton_3.setStyleSheet("color: rgb(194, 194, 194);\n"
"background-color: rgb(89, 89, 89);")
        self.pushButton_3.setCheckable(False)
        self.pushButton_3.setChecked(False)
        self.pushButton_3.setAutoDefault(False)
        self.pushButton_3.setFlat(False)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout_11.addWidget(self.pushButton_3, 1, 0, 1, 1)
        self.scrollArea_5.setWidget(self.scrollAreaWidgetContents_5)
        self.gridLayout_7.addWidget(self.scrollArea_5, 0, 0, 1, 1)
        self.MainTabWidget.addTab(self.tab_6, "")
        self.gridLayout.addWidget(self.MainTabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1082, 21))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionOverview = QtWidgets.QAction(MainWindow)
        self.actionOverview.setObjectName("actionOverview")
        self.actionChecklist = QtWidgets.QAction(MainWindow)
        self.actionChecklist.setObjectName("actionChecklist")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionLoad = QtWidgets.QAction(MainWindow)
        self.actionLoad.setCheckable(False)
        self.actionLoad.setObjectName("actionLoad")
        self.menuMenu.addAction(self.actionLoad)
        self.menuMenu.addAction(self.actionSave)
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionOverview)
        self.menuHelp.addAction(self.actionChecklist)
        self.menubar.addAction(self.menuMenu.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.MainTabWidget.setCurrentIndex(0)
        self.SubTabWidget.setCurrentIndex(0)
        self.actionQuit.triggered.connect(MainWindow.close)
        self.pushButton_3.clicked.connect(self.textEdit.clear)
        self.settings_add_single.clicked.connect(self.add_input_line)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        if open("main_save.json", "r"):
            self.load()
            #self.commit()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Thimble"))
        self.home_screen.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Arial\'; font-size:8.25pt; font-weight:600; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:48pt; font-weight:400; color:#c2c2c2;\">Welcome!</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:48pt; font-weight:400; color:#c2c2c2;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:24pt; font-weight:400; color:#c2c2c2;\">This is my first GUI program, attempted in PyQt. Please, feel free to browse around. If you need help, simply press the &quot;help&quot; menu option at the top.</span></p></body></html>"))
        self.MainTabWidget.setTabText(self.MainTabWidget.indexOf(self.Home), _translate("MainWindow", "Home"))
        self.SubTabWidget.setTabText(self.SubTabWidget.indexOf(self.Display), _translate("MainWindow", "Display"))
        self.settings_main_settings_frame.setTitle(_translate("MainWindow", "Main Settings"))
        self.settings_add_single.setText(_translate("MainWindow", "Add Single"))
        self.settings_add_period.setText(_translate("MainWindow", "Add Period"))
        self.settings_save.setText(_translate("MainWindow", "Save"))
        self.settings_load.setText(_translate("MainWindow", "Load"))
        self.settings_extra_settings_frame.setTitle(_translate("MainWindow", "Extra Settings"))
        self.settings_extra_settings_set_period_frame.setTitle(_translate("MainWindow", "Set Period"))
        self.label_8.setText(_translate("MainWindow", "Period 1"))
        self.settings_extra_settings_set_period_period2_input_message.setPlaceholderText(_translate("MainWindow", "Message"))
        self.settings_extra_settings_set_period_period2_input_length.setPlaceholderText(_translate("MainWindow", "Length (minutes)"))
        self.lineEdit_52.setPlaceholderText(_translate("MainWindow", "Message"))
        self.lineEdit_56.setPlaceholderText(_translate("MainWindow", "Length (minutes)"))
        self.settings_extra_settings_set_period_start_time_input_hour.setPlaceholderText(_translate("MainWindow", "Hour"))
        self.settings_extra_settings_set_period_start_time_input_minute.setPlaceholderText(_translate("MainWindow", "Minute"))
        self.settings_extra_settings_set_period_start_time_display.setText(_translate("MainWindow", "Start Time"))
        self.settings_extra_settings_set_period_period2_display.setText(_translate("MainWindow", "Period 2"))
        self.label_9.setText(_translate("MainWindow", "End Time"))
        self.lineEdit_54.setPlaceholderText(_translate("MainWindow", "Hour"))
        self.lineEdit_55.setPlaceholderText(_translate("MainWindow", "Minute"))
        self.settings_extra_settings_customize_frame.setTitle(_translate("MainWindow", "Customize"))
        self.settings_extra_settings_customize_tts_checkbox.setText(_translate("MainWindow", "TTS Alarm Sounds"))
        self.settings_extra_settings_customize_beep_checkbox.setText(_translate("MainWindow", "Beep sound"))
        self.settings_extra_settings_customize_lock_checkbox.setText(_translate("MainWindow", "Lock Save"))
        self.SubTabWidget.setTabText(self.SubTabWidget.indexOf(self.Settings), _translate("MainWindow", "Settings"))
        self.MainTabWidget.setTabText(self.MainTabWidget.indexOf(self.Alarms), _translate("MainWindow", "Alarms"))
        self.settings_commit_button.setText(_translate("MainWindow", "Compile"))
        self.pushButton_3.setText(_translate("MainWindow", "Log Entry"))
        self.MainTabWidget.setTabText(self.MainTabWidget.indexOf(self.tab_6), _translate("MainWindow", "Log"))
        self.menuMenu.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionOverview.setText(_translate("MainWindow", "Overview"))
        self.actionChecklist.setText(_translate("MainWindow", "Checklist"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionLoad.setText(_translate("MainWindow", "Load"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

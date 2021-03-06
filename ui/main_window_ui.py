# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 5.15.5
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1347, 563)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.actionOpen_Bulletin = QAction(MainWindow)
        self.actionOpen_Bulletin.setObjectName(u"actionOpen_Bulletin")
        icon = QIcon()
        icon.addFile(u"ui/resources/file-open.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionOpen_Bulletin.setIcon(icon)
        self.actionOpen_Bulletin.setVisible(False)
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        icon1 = QIcon()
        icon1.addFile(u"ui/resources/help-content.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionAbout.setIcon(icon1)
        self.action_Quit = QAction(MainWindow)
        self.action_Quit.setObjectName(u"action_Quit")
        icon2 = QIcon()
        icon2.addFile(u"ui/resources/file-exit.png", QSize(), QIcon.Normal, QIcon.Off)
        self.action_Quit.setIcon(icon2)
        self.actionConnection = QAction(MainWindow)
        self.actionConnection.setObjectName(u"actionConnection")
        self.actionBulletin = QAction(MainWindow)
        self.actionBulletin.setObjectName(u"actionBulletin")
        self.actionCatalog = QAction(MainWindow)
        self.actionCatalog.setObjectName(u"actionCatalog")
        self.action_NAS_bulletin = QAction(MainWindow)
        self.action_NAS_bulletin.setObjectName(u"action_NAS_bulletin")
        self.action_ArcGIS = QAction(MainWindow)
        self.action_ArcGIS.setObjectName(u"action_ArcGIS")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setLayoutDirection(Qt.LeftToRight)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setAlignment(Qt.AlignCenter)
        self.horizontalLayout_7 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.verticalLayout_3.addWidget(self.label)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.from_dateTime = QDateTimeEdit(self.groupBox)
        self.from_dateTime.setObjectName(u"from_dateTime")
        self.from_dateTime.setMaximumSize(QSize(194, 16777215))
        self.from_dateTime.setDate(QDate(2020, 2, 1))
        self.from_dateTime.setTime(QTime(0, 0, 0))
        self.from_dateTime.setMinimumDateTime(QDateTime(QDate(1752, 9, 14), QTime(0, 0, 0)))
        self.from_dateTime.setCalendarPopup(False)

        self.horizontalLayout_2.addWidget(self.from_dateTime)

        self.to_dateTime = QDateTimeEdit(self.groupBox)
        self.to_dateTime.setObjectName(u"to_dateTime")
        self.to_dateTime.setMaximumSize(QSize(194, 16777215))
        self.to_dateTime.setDate(QDate(2020, 10, 20))
        self.to_dateTime.setTime(QTime(0, 0, 0))
        self.to_dateTime.setCalendarPopup(False)

        self.horizontalLayout_2.addWidget(self.to_dateTime)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)


        self.horizontalLayout_5.addLayout(self.verticalLayout_3)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.from_Mag = QDoubleSpinBox(self.groupBox)
        self.from_Mag.setObjectName(u"from_Mag")
        self.from_Mag.setFrame(True)
        self.from_Mag.setDecimals(1)
        self.from_Mag.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)
        self.from_Mag.setValue(0.000000000000000)

        self.horizontalLayout_3.addWidget(self.from_Mag)

        self.to_Mag = QDoubleSpinBox(self.groupBox)
        self.to_Mag.setObjectName(u"to_Mag")
        self.to_Mag.setFrame(True)
        self.to_Mag.setDecimals(1)
        self.to_Mag.setStepType(QAbstractSpinBox.DefaultStepType)
        self.to_Mag.setValue(9.000000000000000)

        self.horizontalLayout_3.addWidget(self.to_Mag)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)


        self.horizontalLayout_5.addLayout(self.verticalLayout_2)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_7 = QLabel(self.groupBox)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_7, 0, 0, 1, 1)

        self.label_8 = QLabel(self.groupBox)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_8, 1, 0, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.comment_line = QLineEdit(self.groupBox)
        self.comment_line.setObjectName(u"comment_line")

        self.gridLayout_2.addWidget(self.comment_line, 0, 0, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.sta_line = QLineEdit(self.groupBox)
        self.sta_line.setObjectName(u"sta_line")
        self.sta_line.setMaximumSize(QSize(45, 16777215))

        self.horizontalLayout_4.addWidget(self.sta_line)

        self.horizontalSpacer = QSpacerItem(138, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)


        self.gridLayout_2.addLayout(self.horizontalLayout_4, 1, 0, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 1, 1, 1)


        self.horizontalLayout_5.addLayout(self.gridLayout_3)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.search_events_button = QPushButton(self.groupBox)
        self.search_events_button.setObjectName(u"search_events_button")

        self.horizontalLayout.addWidget(self.search_events_button)

        self.select_all_button = QPushButton(self.groupBox)
        self.select_all_button.setObjectName(u"select_all_button")

        self.horizontalLayout.addWidget(self.select_all_button)

        self.save_as_button = QPushButton(self.groupBox)
        self.save_as_button.setObjectName(u"save_as_button")

        self.horizontalLayout.addWidget(self.save_as_button)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.progressBar = QProgressBar(self.groupBox)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(24)

        self.verticalLayout_4.addWidget(self.progressBar)


        self.horizontalLayout_5.addLayout(self.verticalLayout_4)


        self.horizontalLayout_7.addLayout(self.horizontalLayout_5)


        self.verticalLayout_5.addWidget(self.groupBox)

        self.tableWidget = QTableWidget(self.centralwidget)
        if (self.tableWidget.columnCount() < 9):
            self.tableWidget.setColumnCount(9)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, __qtablewidgetitem8)
        self.tableWidget.setObjectName(u"tableWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(5)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy1)
        self.tableWidget.setMinimumSize(QSize(150, 0))
        self.tableWidget.setBaseSize(QSize(0, 0))
        self.tableWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(50)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(120)
        self.tableWidget.horizontalHeader().setProperty("showSortIndicator", True)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setProperty("showSortIndicator", False)

        self.verticalLayout_5.addWidget(self.tableWidget)


        self.verticalLayout.addLayout(self.verticalLayout_5)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1347, 30))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuSettings = QMenu(self.menuFile)
        self.menuSettings.setObjectName(u"menuSettings")
        self.menu_Save_as = QMenu(self.menuFile)
        self.menu_Save_as.setObjectName(u"menu_Save_as")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setEnabled(True)
        self.statusbar.setMouseTracking(False)
        self.statusbar.setAutoFillBackground(False)
        MainWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.from_dateTime, self.to_dateTime)
        QWidget.setTabOrder(self.to_dateTime, self.from_Mag)
        QWidget.setTabOrder(self.from_Mag, self.to_Mag)
        QWidget.setTabOrder(self.to_Mag, self.comment_line)
        QWidget.setTabOrder(self.comment_line, self.sta_line)
        QWidget.setTabOrder(self.sta_line, self.search_events_button)
        QWidget.setTabOrder(self.search_events_button, self.select_all_button)
        QWidget.setTabOrder(self.select_all_button, self.save_as_button)
        QWidget.setTabOrder(self.save_as_button, self.tableWidget)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.menu_Save_as.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionOpen_Bulletin)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.menuSettings.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.action_Quit)
        self.menuSettings.addAction(self.actionConnection)
        self.menu_Save_as.addAction(self.actionBulletin)
        self.menu_Save_as.addAction(self.actionCatalog)
        self.menu_Save_as.addAction(self.action_NAS_bulletin)
        self.menu_Save_as.addAction(self.action_ArcGIS)
        self.menuHelp.addAction(self.actionAbout)

        self.retranslateUi(MainWindow)
        self.select_all_button.clicked.connect(self.tableWidget.selectAll)
        self.action_Quit.triggered.connect(MainWindow.close)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"getquakes", None))
        self.actionOpen_Bulletin.setText(QCoreApplication.translate("MainWindow", u"&Open Bulletin...", None))
#if QT_CONFIG(shortcut)
        self.actionOpen_Bulletin.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About...", None))
        self.action_Quit.setText(QCoreApplication.translate("MainWindow", u"&Quit", None))
#if QT_CONFIG(shortcut)
        self.action_Quit.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Q", None))
#endif // QT_CONFIG(shortcut)
        self.actionConnection.setText(QCoreApplication.translate("MainWindow", u"Connection", None))
        self.actionBulletin.setText(QCoreApplication.translate("MainWindow", u"&Bulletin (*.txt)", None))
        self.actionCatalog.setText(QCoreApplication.translate("MainWindow", u"&Catalog (*.xlsx)", None))
        self.action_NAS_bulletin.setText(QCoreApplication.translate("MainWindow", u"&NAS bulletin (*.bltn)", None))
        self.action_ArcGIS.setText(QCoreApplication.translate("MainWindow", u"Arc&GIS (*.txt)", None))
        self.groupBox.setTitle("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">Date time</p></body></html>", None))
        self.from_dateTime.setDisplayFormat(QCoreApplication.translate("MainWindow", u"yyyy-MM-dd HH:mm:ss", None))
        self.to_dateTime.setDisplayFormat(QCoreApplication.translate("MainWindow", u"yyyy-MM-dd HH:mm:ss", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Magnitude", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Comment", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"STA", None))
        self.sta_line.setText(QCoreApplication.translate("MainWindow", u"ALL", None))
        self.search_events_button.setText(QCoreApplication.translate("MainWindow", u"Search for events", None))
        self.select_all_button.setText(QCoreApplication.translate("MainWindow", u"Select all", None))
        self.save_as_button.setText(QCoreApplication.translate("MainWindow", u"Save as...", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"ID", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Origin Time", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Lat", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Lon", None));
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Depth", None));
        ___qtablewidgetitem5 = self.tableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"ML", None));
        ___qtablewidgetitem6 = self.tableWidget.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"MPSP", None));
        ___qtablewidgetitem7 = self.tableWidget.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"Region", None));
        ___qtablewidgetitem8 = self.tableWidget.horizontalHeaderItem(8)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"STA, Ph, time", None));
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuSettings.setTitle(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.menu_Save_as.setTitle(QCoreApplication.translate("MainWindow", u"&Save as...", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'db_conn.ui'
##
## Created by: Qt User Interface Compiler version 5.15.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(346, 212)
        self.horizontalLayout_7 = QHBoxLayout(Dialog)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.host_line = QLineEdit(Dialog)
        self.host_line.setObjectName(u"host_line")

        self.horizontalLayout.addWidget(self.host_line)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_2.addWidget(self.label_4)

        self.port_line = QLineEdit(Dialog)
        self.port_line.setObjectName(u"port_line")

        self.horizontalLayout_2.addWidget(self.port_line)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_4.addWidget(self.label_2)

        self.user_line = QLineEdit(Dialog)
        self.user_line.setObjectName(u"user_line")

        self.horizontalLayout_4.addWidget(self.user_line)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_5.addWidget(self.label_3)

        self.password_line = QLineEdit(Dialog)
        self.password_line.setObjectName(u"password_line")

        self.horizontalLayout_5.addWidget(self.password_line)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_5 = QLabel(Dialog)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_3.addWidget(self.label_5)

        self.db_name_line = QLineEdit(Dialog)
        self.db_name_line.setObjectName(u"db_name_line")

        self.horizontalLayout_3.addWidget(self.db_name_line)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.horizontalLayout_6.addLayout(self.verticalLayout)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Vertical)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.horizontalLayout_6.addWidget(self.buttonBox)


        self.horizontalLayout_7.addLayout(self.horizontalLayout_6)

        QWidget.setTabOrder(self.host_line, self.port_line)

        self.retranslateUi(Dialog)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Database connection settings", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Host:", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Port:", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"User:", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Password:", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Database:", None))
    # retranslateUi


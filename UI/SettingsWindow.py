# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SettingsWindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_setWin(object):
    def setupUi(self, setWin):
        if not setWin.objectName():
            setWin.setObjectName(u"setWin")
        setWin.resize(784, 383)
        self.gridLayout = QGridLayout(setWin)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_12)

        self.label = QLabel(setWin)
        self.label.setObjectName(u"label")

        self.horizontalLayout_10.addWidget(self.label)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_13)


        self.verticalLayout_3.addLayout(self.horizontalLayout_10)

        self.lstCandidates = QListWidget(setWin)
        self.lstCandidates.setObjectName(u"lstCandidates")
        self.lstCandidates.setSelectionMode(QAbstractItemView.SingleSelection)

        self.verticalLayout_3.addWidget(self.lstCandidates)

        self.splitter = QSplitter(setWin)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.btnAddC = QPushButton(self.splitter)
        self.btnAddC.setObjectName(u"btnAddC")
        self.splitter.addWidget(self.btnAddC)
        self.btnRemoveC = QPushButton(self.splitter)
        self.btnRemoveC.setObjectName(u"btnRemoveC")
        self.btnRemoveC.setEnabled(False)
        self.splitter.addWidget(self.btnRemoveC)

        self.verticalLayout_3.addWidget(self.splitter)

        self.splitter_2 = QSplitter(setWin)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Horizontal)
        self.btnGet = QPushButton(self.splitter_2)
        self.btnGet.setObjectName(u"btnGet")
        self.splitter_2.addWidget(self.btnGet)
        self.btnClear = QPushButton(self.splitter_2)
        self.btnClear.setObjectName(u"btnClear")
        self.btnClear.setEnabled(False)
        self.splitter_2.addWidget(self.btnClear)

        self.verticalLayout_3.addWidget(self.splitter_2)


        self.horizontalLayout_16.addLayout(self.verticalLayout_3)

        self.station = QVBoxLayout()
        self.station.setObjectName(u"station")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)

        self.label_3 = QLabel(setWin)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_4.addWidget(self.label_3)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_5)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_8 = QLabel(setWin)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_3.addWidget(self.label_8)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.txtAccount = QLineEdit(setWin)
        self.txtAccount.setObjectName(u"txtAccount")

        self.horizontalLayout_3.addWidget(self.txtAccount)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_9 = QLabel(setWin)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_2.addWidget(self.label_9)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.txtPort = QLineEdit(setWin)
        self.txtPort.setObjectName(u"txtPort")

        self.horizontalLayout_2.addWidget(self.txtPort)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_10 = QLabel(setWin)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout.addWidget(self.label_10)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.spIntervalUi = QSpinBox(setWin)
        self.spIntervalUi.setObjectName(u"spIntervalUi")
        self.spIntervalUi.setMinimum(1)
        self.spIntervalUi.setMaximum(99999)

        self.horizontalLayout.addWidget(self.spIntervalUi)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.label_13 = QLabel(setWin)
        self.label_13.setObjectName(u"label_13")

        self.horizontalLayout_13.addWidget(self.label_13)

        self.horizontalSpacer_18 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_18)

        self.spIntervalWorker = QSpinBox(setWin)
        self.spIntervalWorker.setObjectName(u"spIntervalWorker")
        self.spIntervalWorker.setMinimum(30)
        self.spIntervalWorker.setMaximum(99999)

        self.horizontalLayout_13.addWidget(self.spIntervalWorker)


        self.verticalLayout.addLayout(self.horizontalLayout_13)


        self.station.addLayout(self.verticalLayout)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_17)

        self.label_12 = QLabel(setWin)
        self.label_12.setObjectName(u"label_12")

        self.horizontalLayout_12.addWidget(self.label_12)

        self.horizontalSpacer_16 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_16)


        self.verticalLayout_5.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.tmTechFrom = QTimeEdit(setWin)
        self.tmTechFrom.setObjectName(u"tmTechFrom")

        self.horizontalLayout_11.addWidget(self.tmTechFrom)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_14)

        self.label_11 = QLabel(setWin)
        self.label_11.setObjectName(u"label_11")

        self.horizontalLayout_11.addWidget(self.label_11)

        self.horizontalSpacer_15 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_15)

        self.tmTechTo = QTimeEdit(setWin)
        self.tmTechTo.setObjectName(u"tmTechTo")

        self.horizontalLayout_11.addWidget(self.tmTechTo)


        self.verticalLayout_5.addLayout(self.horizontalLayout_11)


        self.station.addLayout(self.verticalLayout_5)

        self.chbxUiDebug = QCheckBox(setWin)
        self.chbxUiDebug.setObjectName(u"chbxUiDebug")

        self.station.addWidget(self.chbxUiDebug)

        self.chbxAutostart = QCheckBox(setWin)
        self.chbxAutostart.setObjectName(u"chbxAutostart")

        self.station.addWidget(self.chbxAutostart)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.station.addItem(self.verticalSpacer_2)


        self.horizontalLayout_16.addLayout(self.station)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_7)

        self.label_2 = QLabel(setWin)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_9.addWidget(self.label_2)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_6)


        self.verticalLayout_2.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_4 = QLabel(setWin)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_8.addWidget(self.label_4)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_8)

        self.spProfit = QSpinBox(setWin)
        self.spProfit.setObjectName(u"spProfit")

        self.horizontalLayout_8.addWidget(self.spProfit)


        self.verticalLayout_2.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_6 = QLabel(setWin)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_7.addWidget(self.label_6)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_9)

        self.spTrail = QSpinBox(setWin)
        self.spTrail.setObjectName(u"spTrail")

        self.horizontalLayout_7.addWidget(self.spTrail)


        self.verticalLayout_2.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_5 = QLabel(setWin)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_6.addWidget(self.label_5)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_10)

        self.spLoss = QSpinBox(setWin)
        self.spLoss.setObjectName(u"spLoss")
        self.spLoss.setMinimum(-99)
        self.spLoss.setMaximum(0)

        self.horizontalLayout_6.addWidget(self.spLoss)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_7 = QLabel(setWin)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_5.addWidget(self.label_7)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_11)

        self.spBulck = QSpinBox(setWin)
        self.spBulck.setObjectName(u"spBulck")
        self.spBulck.setMinimum(1)
        self.spBulck.setMaximum(10000)

        self.horizontalLayout_5.addWidget(self.spBulck)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalSpacer_19 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_19)

        self.label_14 = QLabel(setWin)
        self.label_14.setObjectName(u"label_14")

        self.horizontalLayout_14.addWidget(self.label_14)

        self.horizontalSpacer_20 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_20)


        self.verticalLayout_2.addLayout(self.horizontalLayout_14)

        self.chbxUseServer = QCheckBox(setWin)
        self.chbxUseServer.setObjectName(u"chbxUseServer")

        self.verticalLayout_2.addWidget(self.chbxUseServer)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label_15 = QLabel(setWin)
        self.label_15.setObjectName(u"label_15")

        self.horizontalLayout_15.addWidget(self.label_15)

        self.horizontalSpacer_21 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_15.addItem(self.horizontalSpacer_21)

        self.txtServerUrl = QLineEdit(setWin)
        self.txtServerUrl.setObjectName(u"txtServerUrl")

        self.horizontalLayout_15.addWidget(self.txtServerUrl)


        self.verticalLayout_2.addLayout(self.horizontalLayout_15)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.horizontalLayout_16.addLayout(self.verticalLayout_2)


        self.verticalLayout_4.addLayout(self.horizontalLayout_16)

        self.buttonBox = QDialogButtonBox(setWin)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout_4.addWidget(self.buttonBox)


        self.gridLayout.addLayout(self.verticalLayout_4, 0, 0, 1, 1)


        self.retranslateUi(setWin)
        self.buttonBox.accepted.connect(setWin.accept)
        self.buttonBox.rejected.connect(setWin.reject)

        QMetaObject.connectSlotsByName(setWin)
    # setupUi

    def retranslateUi(self, setWin):
        setWin.setWindowTitle(QCoreApplication.translate("setWin", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("setWin", u"Stocks to track", None))
        self.btnAddC.setText(QCoreApplication.translate("setWin", u"Add", None))
        self.btnRemoveC.setText(QCoreApplication.translate("setWin", u"Remove", None))
        self.btnGet.setText(QCoreApplication.translate("setWin", u"Download", None))
        self.btnClear.setText(QCoreApplication.translate("setWin", u"Clear", None))
        self.label_3.setText(QCoreApplication.translate("setWin", u"AlgoTrader settings", None))
        self.label_8.setText(QCoreApplication.translate("setWin", u"Account", None))
        self.label_9.setText(QCoreApplication.translate("setWin", u"Port", None))
        self.label_10.setText(QCoreApplication.translate("setWin", u"UI refresh (sec)", None))
        self.label_13.setText(QCoreApplication.translate("setWin", u"Worker interval (sec)", None))
        self.label_12.setText(QCoreApplication.translate("setWin", u"Technical breack", None))
        self.label_11.setText(QCoreApplication.translate("setWin", u"to", None))
#if QT_CONFIG(tooltip)
        self.chbxUiDebug.setToolTip(QCoreApplication.translate("setWin", u"UI only no any data loaded for Development", None))
#endif // QT_CONFIG(tooltip)
        self.chbxUiDebug.setText(QCoreApplication.translate("setWin", u"UI only (debug)", None))
#if QT_CONFIG(tooltip)
        self.chbxAutostart.setToolTip(QCoreApplication.translate("setWin", u"Automatically start positions processing when all data loaded", None))
#endif // QT_CONFIG(tooltip)
        self.chbxAutostart.setText(QCoreApplication.translate("setWin", u"Auto start processing", None))
        self.label_2.setText(QCoreApplication.translate("setWin", u"Algorithm settings", None))
        self.label_4.setText(QCoreApplication.translate("setWin", u"Profit", None))
        self.label_6.setText(QCoreApplication.translate("setWin", u"Trail %", None))
        self.label_5.setText(QCoreApplication.translate("setWin", u"Stop Loss", None))
        self.label_7.setText(QCoreApplication.translate("setWin", u"Bulk size USD", None))
        self.label_14.setText(QCoreApplication.translate("setWin", u"Server settings", None))
        self.chbxUseServer.setText(QCoreApplication.translate("setWin", u"use Algotrader server", None))
        self.label_15.setText(QCoreApplication.translate("setWin", u"URL", None))
    # retranslateUi


# Form implementation generated from reading ui file 'config/src/mainConfig.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.
import sys
import os
import json

from src.config import config

from PyQt6 import QtCore, QtGui, QtWidgets
#TODO: Added these Additional Imports
from PyQt6.QtWidgets import QFileDialog, QWidget, QMessageBox, QMainWindow


#TODO: Changed parent window to QMainWindow from object
class Ui_MainWindow(QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(724, 561)
        #TODO: Added this next line
        self._parent = MainWindow
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(parent=self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_directoryconfig = QtWidgets.QWidget()
        self.tab_directoryconfig.setObjectName("tab_directoryconfig")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_directoryconfig)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_addJSON = QtWidgets.QPushButton(parent=self.tab_directoryconfig)
        self.pushButton_addJSON.setObjectName("pushButton_addJSON")
        self.gridLayout.addWidget(self.pushButton_addJSON, 4, 2, 1, 1)
        self.label = QtWidgets.QLabel(parent=self.tab_directoryconfig)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(parent=self.tab_directoryconfig)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(parent=self.tab_directoryconfig)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 5, 0, 1, 1)
        self.lstJSONLocation = QtWidgets.QListWidget(parent=self.tab_directoryconfig)
        self.lstJSONLocation.setObjectName("lstJSONLocation")
        self.gridLayout.addWidget(self.lstJSONLocation, 3, 0, 1, 3)
        self.pushButton_ProfileLocation = QtWidgets.QPushButton(parent=self.tab_directoryconfig)
        self.pushButton_ProfileLocation.setObjectName("pushButton_ProfileLocation")
        self.gridLayout.addWidget(self.pushButton_ProfileLocation, 1, 2, 1, 1, QtCore.Qt.AlignmentFlag.AlignTop)
        self.lstXMLLocation = QtWidgets.QListWidget(parent=self.tab_directoryconfig)
        self.lstXMLLocation.setObjectName("lstXMLLocation")
        self.gridLayout.addWidget(self.lstXMLLocation, 6, 0, 1, 3)
        self.pushButton_removeXML = QtWidgets.QPushButton(parent=self.tab_directoryconfig)
        self.pushButton_removeXML.setObjectName("pushButton_removeXML")
        self.gridLayout.addWidget(self.pushButton_removeXML, 7, 1, 1, 1)
        self.pushButton_addXML = QtWidgets.QPushButton(parent=self.tab_directoryconfig)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_addXML.sizePolicy().hasHeightForWidth())
        self.pushButton_addXML.setSizePolicy(sizePolicy)
        self.pushButton_addXML.setObjectName("pushButton_addXML")
        self.gridLayout.addWidget(self.pushButton_addXML, 7, 2, 1, 1)
        self.pushButton_removeJSON = QtWidgets.QPushButton(parent=self.tab_directoryconfig)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_removeJSON.sizePolicy().hasHeightForWidth())
        self.pushButton_removeJSON.setSizePolicy(sizePolicy)
        self.pushButton_removeJSON.setObjectName("pushButton_removeJSON")
        self.gridLayout.addWidget(self.pushButton_removeJSON, 4, 1, 1, 1)
        self.lnProfileLocation = QtWidgets.QLineEdit(parent=self.tab_directoryconfig)
        self.lnProfileLocation.setObjectName("lnProfileLocation")
        self.gridLayout.addWidget(self.lnProfileLocation, 1, 0, 1, 2)
        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_directoryconfig, "")
        self.tab_marketinformation = QtWidgets.QWidget()
        self.tab_marketinformation.setObjectName("tab_marketinformation")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.tab_marketinformation)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.pushButton_tradersdirectory = QtWidgets.QPushButton(parent=self.tab_marketinformation)
        self.pushButton_tradersdirectory.setObjectName("pushButton_tradersdirectory")
        self.gridLayout_4.addWidget(self.pushButton_tradersdirectory, 3, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(parent=self.tab_marketinformation)
        self.label_5.setObjectName("label_5")
        self.gridLayout_4.addWidget(self.label_5, 2, 0, 1, 1)
        self.lnMarketDirectory = QtWidgets.QLineEdit(parent=self.tab_marketinformation)
        self.lnMarketDirectory.setObjectName("lnMarketDirectory")
        self.gridLayout_4.addWidget(self.lnMarketDirectory, 1, 0, 1, 1)
        self.pushButton_marketdirectory = QtWidgets.QPushButton(parent=self.tab_marketinformation)
        self.pushButton_marketdirectory.setObjectName("pushButton_marketdirectory")
        self.gridLayout_4.addWidget(self.pushButton_marketdirectory, 1, 1, 1, 1)
        self.lnTraderDirectory = QtWidgets.QLineEdit(parent=self.tab_marketinformation)
        self.lnTraderDirectory.setObjectName("lnTraderDirectory")
        self.gridLayout_4.addWidget(self.lnTraderDirectory, 3, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(parent=self.tab_marketinformation)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_4.setObjectName("label_4")
        self.gridLayout_4.addWidget(self.label_4, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout_4.addItem(spacerItem, 4, 0, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_4, 0, 2, 1, 1)
        self.tabWidget.addTab(self.tab_marketinformation, "")
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.pushButton_Close = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_Close.setObjectName("pushButton_Close")
        self.gridLayout_2.addWidget(self.pushButton_Close, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 724, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        # TODO: Added All the Push Button Responses
        self.pushButton_ProfileLocation.clicked['bool'].connect(self._getProfileLocation)  # type: ignore
        self.pushButton_marketdirectory.clicked['bool'].connect(self._getMarketLocation)  # type: ignore
        self.pushButton_tradersdirectory.clicked['bool'].connect(self._getTraderLocation)  # type: ignore
        self.pushButton_addJSON.clicked['bool'].connect(self._addJSONLocation)  # type: ignore
        self.pushButton_removeJSON.clicked['bool'].connect(self._removeJSONLocation)  # type: ignore
        self.pushButton_addXML.clicked['bool'].connect(self._addXMLLocation)  # type: ignore
        self.pushButton_removeXML.clicked['bool'].connect(self._removeXMLLocation)  # type: ignore
        self.pushButton_Close.clicked['bool'].connect(self._closeform)  # type: ignore

        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        # TODO: Changed Name of Main Window
        MainWindow.setWindowTitle(_translate("MainWindow", "DayZ Admin Tools Config Editor"))
        self.pushButton_addJSON.setText(_translate("MainWindow", "+"))
        self.label.setText(_translate("MainWindow", "DayZ Profile Location"))
        self.label_2.setText(_translate("MainWindow", "DayZ JSON File Location(s)"))
        self.label_3.setText(_translate("MainWindow", "DayZ XML File Location(s)"))
        self.pushButton_ProfileLocation.setText(_translate("MainWindow", "..."))
        self.pushButton_removeXML.setText(_translate("MainWindow", "-"))
        self.pushButton_addXML.setText(_translate("MainWindow", "+"))
        self.pushButton_removeJSON.setText(_translate("MainWindow", "-"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_directoryconfig), _translate("MainWindow", "Core Directory Info"))
        self.pushButton_tradersdirectory.setText(_translate("MainWindow", "..."))
        self.label_5.setText(_translate("MainWindow", "Traders Directory"))
        self.pushButton_marketdirectory.setText(_translate("MainWindow", "..."))
        self.label_4.setText(_translate("MainWindow", "Market Directory"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_marketinformation), _translate("MainWindow", "Market Information"))
        self.pushButton_Close.setText(_translate("MainWindow", "&Close"))



        #TODO: Added All the code down to if __name__=="__main__"
        profile_dir, market_dir, trader_dir, json_dir, xml_dir = config.loadConfig()

        self.lnProfileLocation.setText(profile_dir)
        self.lnMarketDirectory.setText(market_dir)
        self.lnTraderDirectory.setText(trader_dir)

        for path in json_dir:
            self.lstJSONLocation.addItem(path)

        for path in xml_dir:
            self.lstXMLLocation.addItem(path)

    def getDirectory(self, title: str, start_dir: str):

        return QFileDialog.getExistingDirectory(self, caption=title,
                                                directory=start_dir)

    def _getMarketLocation(self, status: bool):
        fileName = self.getDirectory("Locate Expansion Market Directory", self.lnProfileLocation.text())
        if fileName:
            self.lnMarketDirectory.setText(fileName)
        else:
            self.lnMarketDirectory.setText("")
        return

    def _getTraderLocation(self, status: bool):

        fileName = self.getDirectory("Locate Expansion Trader Directory", self.lnProfileLocation.text())
        if fileName:
            self.lnTraderDirectory.setText(fileName)
        else:
            self.lnTraderDirectory.setText("")
        return

    def _getProfileLocation(self, status: bool):
        fileName = self.getDirectory("Locate DayZ Profile Directory", self.lnProfileLocation.text())
        if fileName:
            self.lnProfileLocation.setText(fileName)
        else:
            self.lnProfileLocation.setText("")
        return

    def _addJSONLocation(self):
        fileName = self.getDirectory("Locate JSON Directory", self.lnProfileLocation.text())
        if fileName:
            self.lstJSONLocation.addItem(fileName)
        return

    def _removeJSONLocation(self):

        for item in self.lstJSONLocation.selectedItems():
            current_item = self.lstJSONLocation.takeItem(
                self.lstJSONLocation.indexFromItem(item).row())
            del current_item

            return

    def _addXMLLocation(self):
        fileName = self.getDirectory("Locate XML Directory", self.lnProfileLocation.text())
        if fileName:
            self.lstXMLLocation.addItem(fileName)

        return

    def _removeXMLLocation(self):

        for item in self.lstXMLLocation.selectedItems():
            current_item = self.lstXMLLocation.takeItem(
                self.lstXMLLocation.indexFromItem(item).row())
            del current_item

        return

    def _closeform(self):
        # Save Configuration File Info
        if self.lnProfileLocation.text() == "":
            return

        self.saveConfig()
        self._parent.close()

        return

    def saveConfig(self):

        json_items, xml_items = [], []

        for index in range(self.lstJSONLocation.count()):
            json_items.append(str(self.lstJSONLocation.item(index).text()))

        for index in range(self.lstXMLLocation.count()):
            xml_items.append(str(self.lstXMLLocation.item(index).text()))

        config.saveConfig(self.lnProfileLocation.text(),
                          self.lnMarketDirectory.text(),
                          self.lnTraderDirectory.text(),
                          json_items,
                          xml_items)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
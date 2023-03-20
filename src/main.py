from PyQt6 import QtCore, QtGui, QtWidgets
#TODO: Added these Additional Imports
from PyQt6.QtWidgets import QFileDialog, QWidget, QMessageBox, QMainWindow
from src.forms import mainUI

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = mainUI.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
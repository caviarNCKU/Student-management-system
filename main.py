# !/usr/bin/python
# coding:utf-8
from PyQt5 import QtWidgets, QtSql
from mainForm import MainUi   # 讀入我們設計的Main Window
import sys
    
if __name__ == "__main__":
    def run_app():
        app = QtWidgets.QApplication(sys.argv)
        window = MainUi()
        window.show()
        app.exec_()
    run_app()

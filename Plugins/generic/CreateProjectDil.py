from generic import PyQt6, os

QtWidgets = PyQt6.QtWidgets
QtCore = PyQt6.QtCore
QtGui = PyQt6.QtGui

if False: # IDE Only
    import os
    import PyQt6
    from PyQt6 import QtWidgets, QtCore, QtGui


class createProjectDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.v = QtWidgets.QFormLayout(self)

        self.lblPath = QtWidgets.QLabel("Select path")


from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5 import uic
import sys


class UI(QMainWindow):
    global grid
    grid = QGridLayout()
    grid.setSpacing(0)

    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi("gui.ui", self)
        self.button = self.findChild(QCommandLinkButton, "next")
        self.clearbtn = self.findChild(QCommandLinkButton, "clear")
        self.process_info_group = self.findChild(QGroupBox, "process_info")
        self.no_process = self.findChild(QComboBox, "no_process")
        self.algorithm = self.findChild(QComboBox, "algorithm")
        self.plot = QCommandLinkButton("Plot")
        self.plot.setFixedSize(101,50)
        self.process_info_group.setFixedSize(500,300)
        self.clearbtn.clicked.connect(self.clear_button)
        self.button.clicked.connect(self.next_button)
        self.show()

    def clear_button(self):
        for i in reversed(range(grid.count())):
            grid.itemAt(i).widget().setParent(None)

    def next_button(self):
        num_processes = int(self.no_process.currentText())
        algorithm_type = str(self.algorithm.currentText())
        process_num_label = QLabel("#", width="101", height="13")
        arrival_label = QLabel("Arrival Time", width="101", height="13")
        burst_label = QLabel("Burst Time", width="101", height="13")
        priority_label = False
        if "Priority" in algorithm_type:
            priority_label = QLabel("Prority", width="101", height="13")

        grid.addWidget(process_num_label, 0, 0)
        grid.addWidget(arrival_label, 0, 1)
        grid.addWidget(burst_label, 0, 2)
        if(priority_label):
            
            grid.addWidget(priority_label, 0, 3)
        for i in range(num_processes):
            if(priority_label):
                grid.addWidget(QLineEdit(name="priority{}".format(i)), i+1, 3)
            grid.addWidget(QLineEdit(name="process{}".format(i)), i+1, 0)
            grid.addWidget(QLineEdit(name="arrival{}".format(i)), i+1, 1)
            grid.addWidget(QLineEdit(name="burst{}".format(i)), i+1, 2)
        grid.addWidget(self.plot, 0, 5)
        self.process_info_group.setLayout(grid)
        self.process_info_group.setVisible(True)


app = QApplication(sys.argv)
UIWindow = UI()

app.exec_()

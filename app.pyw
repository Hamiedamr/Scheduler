from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5 import uic
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from Slot import Slot
from Slot import drawSlots
from collections import OrderedDict


class UI(QMainWindow):

    def __init__(self):
        # UI Load
        super(UI, self).__init__()
        uic.loadUi("gui.ui", self)

        # Upper section
        self.next_button = self.findChild(QCommandLinkButton, "next")
        self.clear_button = self.findChild(QCommandLinkButton, "clear")
        self.no_process_list = self.findChild(QComboBox, "no_process")
        self.algorithm_list = self.findChild(QComboBox, "algorithm")
        self.clear_button.clicked.connect(self.clear_action)
        self.next_button.clicked.connect(self.next_action)

        # Lower Section
        self.process_info_group = self.findChild(QGroupBox, "process_info")
        self.plot_button = QCommandLinkButton("Plot")
        self.plot_button.setFixedSize(101, 50)
        self.process_info_group.setFixedSize(500, 300)
        self.process_data = dict()
        self.plot_button.clicked.connect(self.plot_action)

        # Globals

        global grid
        # Create Grid Layout
        grid = QGridLayout()
        grid.setSpacing(0)

        # MainWindow Show
        self.show()

    def clear_action(self):
        for i in reversed(range(grid.count())):
            grid.itemAt(i).widget().setParent(None)
        self.next_action()

    def next_action(self):
        global num_processes
        num_processes = int(self.no_process_list.currentText())

        # Fetch the values of algorithm and number of processes

        algorithm_type = str(self.algorithm_list.currentText())

        # Initialize procecess data dictionary with process keys ex: first proces key is p1 and zero values
        self.process_data = {i: {} for i in range(1, num_processes+1)}

        # Processes information labels(name,arrival,brust,[optional]prority,[optional]quantum)
        process_num_label = QLabel("#", width="101", height="13")
        arrival_label = QLabel("Arrival Time", width="101", height="13")
        burst_label = QLabel("Brust Time", width="101", height="13")
        priority_label = False
        quantum_label = False
        if "Priority" in algorithm_type:
            priority_label = QLabel("Prority", width="101", height="13")
        elif "Round Robin" in algorithm_type:
            quantum_label = QLabel("Quantum")
        grid.addWidget(process_num_label, 0, 0)
        grid.addWidget(arrival_label, 0, 1)
        grid.addWidget(burst_label, 0, 2)
        if(priority_label):
            grid.addWidget(priority_label, 0, 3)

        # Draw textboxes
        for i in range(1, num_processes+1):
            self.process_data[i]['priority'] = False
            self.process_data[i]['quantum'] = False
            # Priority textbox
            if(priority_label):
                priority_input = QLineEdit()
                priority_input.setObjectName("priority{}".format(i))
                grid.addWidget(priority_input, i, 3)
                self.process_data[i]['priority'] = priority_input

            # Quantum textbox
            elif(quantum_label):
                quantum_input = QLineEdit()
                quantum_input.setObjectName("quantum{}".format(i))
                grid.addWidget(quantum_input, i, 3)
                self.process_data[i]['quantum'] = quantum_input

            # Process name textbox
            process_name_input = QLineEdit()
            process_name_input.setObjectName("process-name{}".format(i))
            grid.addWidget(process_name_input, i, 0)
            self.process_data[i]['process-name'] = process_name_input

            # Arrival time textbox
            arrival_time_input = QLineEdit()
            arrival_time_input.setObjectName("arrival{}".format(i))
            grid.addWidget(arrival_time_input, i, 1)
            self.process_data[i]['arrival'] = arrival_time_input

            # Burst time textbox
            burst_time_input = QLineEdit()
            burst_time_input.setObjectName("brust{}".format(i))
            grid.addWidget(burst_time_input, i, 2)
            self.process_data[i]['brust'] = burst_time_input

        grid.addWidget(self.plot_button, 0, 5)
        self.process_info_group.setLayout(grid)
        self.process_info_group.setVisible(True)

    def plot_action(self):
        # slots = [Slot("as", 0, 24),Slot("as", 24, 10),Slot("as", 34, 65)]
        # drawSlots(slots)
        try:

            for i in range(1, num_processes+1):
                self.process_data[i]['process-name'] = self.process_data[i]['process-name'].text()
                self.process_data[i]['arrival'] = float(self.process_data[i]['arrival'].text(
                ))
                self.process_data[i]['brust'] = float(self.process_data[i]['brust'].text(
                ))
                if(self.process_data[i]['priority']):
                    self.process_data[i]['priority'] = float(self.process_data[i]['priority'].text(
                    ))
                elif(self.process_data[i]['quantum']):
                    self.process_data[i]['quantum'] = float(self.process_data[i]['quantum'].text(
                    ))
            if str(self.algorithm_list.currentText()) == ("FCFS"):
                slots = self.calc_fcfsEnhanced(self.process_data)
            elif str(self.algorithm_list.currentText()) == ("Non Preemptive SJF"):
                slots = self.calc_SJFEnhanced(self.process_data)

            elif str(self.algorithm_list.currentText()) == ("Non Preemptive Priority"):
                slots = self.calc_priorityEnhanced(self.process_data)

            drawSlots(slots)

            self.clear_action()

        except Exception as e:
            print(e)
            self.clear_action()

    def calc_fcfsEnhanced(self, process_data):
        n = num_processes
        brust_time = np.array([float(process_data[i]['brust'])
                               for i in process_data])
        arrival_time = np.array(
            [float(process_data[i]['arrival']) for i in process_data])
        process_names = np.array(
            [process_data[i]['process-name'] for i in process_data])

        slots = []
        begin = 0
        for i in range(n):
            if i != 0:
                begin += brust_time[i-1]
            slots.append(Slot(process_names[i], begin, brust_time[i]))

        return slots

    def calc_SJFEnhanced(self, process_data):
        x = sorted(process_data.items(
        ), key=lambda d:(d[1]['arrival'], d[1]['brust']))
        process_data=OrderedDict(x)

        n = num_processes
        brust_time = np.array([float(process_data[i]['brust'])
                               for i in process_data])
        arrival_time = np.array(
            [float(process_data[i]['arrival']) for i in process_data])
        process_names = np.array(
            [process_data[i]['process-name'] for i in process_data])

        slots = []
        begin = 0
        for i in range(n):
            if i != 0:
                begin += brust_time[i-1]
            slots.append(Slot(process_names[i], begin, brust_time[i]))

        return slots

    def calc_priorityEnhanced(self, process_data):
        process_data = OrderedDict(sorted(process_data.items(
        ), key=lambda d: (d[1]['arrival'], d[1]['priority'])))
        n = num_processes
        brust_time = np.array([float(process_data[i]['brust'])
                               for i in process_data])
        arrival_time = np.array(
            [float(process_data[i]['arrival']) for i in process_data])
        process_names = np.array(
            [process_data[i]['process-name'] for i in process_data])

        slots = []
        begin = 0
        for i in range(n):
            if i != 0:
                begin += brust_time[i-1]
            slots.append(Slot(process_names[i], begin, brust_time[i]))

        return slots


app = QApplication(sys.argv)
UIWindow = UI()

app.exec_()

from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5 import uic
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


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
        # self.next_action()

    def next_action(self):
        global num_processes
        num_processes = int(self.no_process_list.currentText())

        # Fetch the values of algorithm and number of processes
        global algorithm_type
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
        elif(quantum_label):
            grid.addWidget(quantum_label,0,3)

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
        try:
            for i in range(1, num_processes+1):
                self.process_data[i]['process-name'] = self.process_data[i]['process-name'].text()
                self.process_data[i]['arrival'] = self.process_data[i]['arrival'].text(
                )
                self.process_data[i]['brust'] = self.process_data[i]['brust'].text(
                )
                if(self.process_data[i]['priority']):
                    self.process_data[i]['priority'] = self.process_data[i]['priority'].text(
                    )
                elif(self.process_data[i]['quantum']):
                    self.process_data[i]['quantum'] = self.process_data[i]['quantum'].text(
                    )
            if algorithm_type == "FCFS":
                self.calc_fcfs(self.process_data)
            self.clear_action()

        except Exception as e:
            print(e)
            self.clear_action()

    def calc_fcfs(self, process_data):
        n = num_processes
        brust_time = np.array([float(process_data[i]['brust'])
                               for i in process_data])
        arrival_time = np.array(
            [float(process_data[i]['arrival']) for i in process_data])
        departure_time = np.array([brust_time[0], 0])
        for i in range(1, n):
            departure_time[i] = brust_time[i] + departure_time[i-1]
        average_turn_around_time = np.sum(departure_time - arrival_time) / n
        average_wait_time = np.sum(
            departure_time - arrival_time-brust_time) / n

        fig = plt.figure()
        for i in range(n):
            p = patches.Rectangle((i*0.1, 0.2), brust_time[i]*0.1, 0.5, label="p"+str(i),color="red",fill=0)
            fig.add_artist(p)
        plt.show()


app = QApplication(sys.argv)
UIWindow = UI()

app.exec_()

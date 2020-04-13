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

    def drawSlots_sjf(self, slots):
        fig = plt.figure()
        left = .1
        bottom, height = .2, .5
        widthRange = .01
        xScale = 0.01
        width = [0]
        start = [0]
        processBegin = [0]
        frist = True
        i = 1
        for s in slots:
            start.insert(i, [s.slotStart][0] * xScale)
            width.insert(i, [s.slotTime][0] * widthRange)
            processBegin.insert(i, [s.arrival_time][0])
            slotName = [s.processName][0]
            if processBegin[i] <= processBegin[i - 1] + (width[i - 1] * 100):
                start[i] = (
                    (processBegin[i - 1] + (width[i - 1] * 100)) * xScale)
                processBegin[i] = start[i] * 100

                p = patches.Rectangle(
                    (start[i], bottom), width[i], height, label="p", color="red", fill=0)
                # start time of the process
                fig.text(start[i], bottom, str(int((start[i] * 100))), horizontalalignment='left',
                          verticalalignment='top')
                # proces name
                fig.text(start[i], height / 2 + bottom, slotName,
                         horizontalalignment='left', verticalalignment='top')
                fig.add_artist(p)
                # process end time
                fig.text(start[i] + width[i], bottom, str(int((start[i] * 100) + s.slotTime)),
                          horizontalalignment='left',
                          verticalalignment='top')

                fig.add_artist(p)
            else:

                p = patches.Rectangle(
                    (start[i], bottom), width[i], height, label="p", color="red", fill=0)
                # start time of the process
                fig.text(start[i], bottom, str(int(processBegin[i])), horizontalalignment='left',
                          verticalalignment='top')
                # proces name
                fig.text(start[i], height / 2 + bottom, slotName,
                         horizontalalignment='left', verticalalignment='top')
                fig.add_artist(p)
                # process end time
                fig.text(start[i] + width[i], bottom, str(int(processBegin[i] + s.slotTime)),
                          horizontalalignment='left',
                          verticalalignment='top')
                fig.add_artist(p)
            i += 1

        plt.show()

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
        self.process_data = {i: {} for i in range(1, num_processes + 1)}

        # Processes information labels(name,arrival,brust,[optional]prority,[optional]quantum)
        process_num_label = QLabel("#", width="101", height="13")
        arrival_label = QLabel("Arrival Time", width="101", height="13")
        burst_label = QLabel("Brust Time", width="101", height="13")
        priority_label = False
        quantum_label = False
        global quantum_input
        if "Priority" in algorithm_type:  # Priority label
            priority_label = QLabel("Prority", width="101", height="13")
            grid.addWidget(priority_label, 0, 3)
        elif "Round Robin" in algorithm_type:  # Quantum textbox and label
            quantum_label = QLabel("Quantum")
            quantum_input = QLineEdit()
            grid.addWidget(quantum_label, 0, 3)
            grid.addWidget(quantum_input, 1, 3)

        grid.addWidget(process_num_label, 0, 0)
        grid.addWidget(arrival_label, 0, 1)
        grid.addWidget(burst_label, 0, 2)

        # Draw textboxes
        for i in range(1, num_processes + 1):
            self.process_data[i]['priority'] = False
            self.process_data[i]['quantum'] = False
            # Priority textbox
            if (priority_label):
                priority_input = QLineEdit()
                priority_input.setObjectName("priority{}".format(i))
                grid.addWidget(priority_input, i, 3)
                self.process_data[i]['priority'] = priority_input

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

            for i in range(1, num_processes + 1):
                self.process_data[i]['process-name'] = self.process_data[i]['process-name'].text()
                self.process_data[i]['arrival'] = float(self.process_data[i]['arrival'].text(
                ))
                self.process_data[i]['brust'] = float(self.process_data[i]['brust'].text(
                ))
                if (self.process_data[i]['priority']):
                    self.process_data[i]['priority'] = float(self.process_data[i]['priority'].text(
                    ))
                elif (self.process_data[i]['quantum']):
                    self.process_data[i]['quantum'] = float(self.process_data[i]['quantum'].text(
                    ))
            if str(self.algorithm_list.currentText()) == ("FCFS"):
                slots = self.calc_fcfsEnhanced(self.process_data)

            elif str(self.algorithm_list.currentText()) == ("Non Preemptive Priority"):
                slots = self.calc_priorityEnhanced(self.process_data)
            elif str(self.algorithm_list.currentText()) == ("Round Robin"):
                slots = self.calc_roundRobinEnhanced(self.process_data)
            elif str(self.algorithm_list.currentText()) == ("Preemptive Priority"):
                slots = self.calc_priority_pree(self.process_data)
            elif str(self.algorithm_list.currentText()) == ("Preemptive SJF"):
                slots = self.calc_sjf_pree(self.process_data)

            elif str(self.algorithm_list.currentText()) == ("Non Preemptive SJF"):
                slots_1 = self.calc_SJFEnhanced(self.process_data)

            if str(self.algorithm_list.currentText()) == (
                "Non Preemptive SJF"): self.drawSlots_sjf(slots_1)
            else:  # drawSlots( slots )
                self.drawSlots_sjf(slots)
            self.clear_action()

        except Exception as e:
            print(e)
            self.clear_action()

    def calc_fcfsEnhanced(self, process_data):
        x = sorted(process_data.items(
        ), key=lambda d: d[1]['arrival'])
        process_data = OrderedDict(x)
        n = num_processes
        brust_time = np.array([float(process_data[i]['brust'])
                                for i in process_data])
        arrival_time = np.array(
            [float(process_data[i]['arrival']) for i in process_data])
        process_names = np.array(
            [process_data[i]['process-name'] for i in process_data])

        slots = []
        begin = arrival_time[0]
        for i in range(n):
            if i != 0:
                begin += brust_time[i - 1]
            slots.append(
                Slot(process_names[i], begin, brust_time[i], arrival_time[i]))

        return slots

    def calc_SJFEnhanced(self, process_data):
        x = sorted(process_data.items(
        ), key=lambda d: (d[1]['arrival'], d[1]['brust']))
        process_data = OrderedDict(x)

        n = num_processes
        brust_time = np.array([float(process_data[i]['brust'])
                                for i in process_data])
        arrival_time = np.array(
            [float(process_data[i]['arrival']) for i in process_data])
        process_names = np.array(
            [process_data[i]['process-name'] for i in process_data])

        slots_1 = []
        begin = arrival_time[0]
        for i in range(n):
            # lzam abtdy mn arrival bt3y lw akber mn el begin bt3 el process  el ably
            if i != 0 and arrival_time[i] >= begin:
                begin = arrival_time[i]
            slots_1.append(
                Slot(process_names[i], begin, brust_time[i], arrival_time[i]))

        return slots_1

    def calc_priorityEnhanced(self, process_data):
        process_data = OrderedDict(sorted(process_data.items(
        ), key=lambda d: (d[1]['arrival'], d[1]['priority'])))
       # print(process_data)
        n = num_processes
        brust_time = np.array([float(process_data[i]['brust'])
                                for i in process_data])
        arrival_time = np.array(
            [float(process_data[i]['arrival']) for i in process_data])
        process_names = np.array(
            [process_data[i]['process-name'] for i in process_data])
        priorities = np.array([float(process_data[i]['priority'])
                              for i in process_data])

        slots = []
        begin = arrival_time[0]
        i = 0
        while i < n:

            if i != 0:
                begin += brust_time[i - 1]
                if begin < arrival_time[i]:
                    continue
                elif begin == arrival_time[i]:
                    indx = i
                    priorities[indx] = 9999
                    slots.append(
                        Slot(process_names[i], begin, brust_time[i], arrival_time[i]))

                else:
                     indx = np.argmin(priorities)
                     priorities[indx] = 9999
                     slots.append( Slot( process_names[indx], begin, brust_time[indx] ,arrival_time[indx]) )
                    

            else:
                indx = i
                priorities[indx] = 9999
                slots.append( Slot( process_names[indx], begin, brust_time[indx] ,arrival_time[indx]) )
            i += 1
        return slots
    def calc_sjf_pree(self, process_data):
        process_data = OrderedDict(sorted(process_data.items(
        ), key=lambda d: (d[1]['arrival'], d[1]['brust'])))
       # print(process_data)
        n = num_processes
        brust_time = np.array([float(process_data[i]['brust'])
                                for i in process_data])
        arrival_time = np.array(
            [float(process_data[i]['arrival']) for i in process_data])
        process_names = np.array(
            [process_data[i]['process-name'] for i in process_data])

        slots = []
        begin = arrival_time[0]
        i = 0
        while i < n:

            if i != 0:
                begin += brust_time[i - 1]
                if begin < arrival_time[i]:
                    continue
                elif begin == arrival_time[i]:
                    indx = i
                    brust_time[indx] -= begin
                    slots.append(
                        Slot(process_names[i], begin, brust_time[i], arrival_time[i]))

                else:
                     indx = np.argmin(brust_time)
                     brust_time[indx]-= begin
                     slots.append( Slot( process_names[indx], begin, brust_time[indx] ,arrival_time[indx]) )
                    

            else:
                indx = i
                brust_time[indx] -= begin
                slots.append( Slot( process_names[indx], begin, arrival_time[indx+1] ,arrival_time[indx]) )
            i += 1
        return slots

    
    
    
    def calc_roundRobinEnhanced(self, process_data):
        Q = float( quantum_input.text() )
        process_data = OrderedDict( sorted( process_data.items(
        ), key=lambda d: d[1]['arrival'] ) )
        n = num_processes
        brust_time = np.array( [float( process_data[i]['brust'] )
                                for i in process_data] )
        arrival_time = np.array(
            [float( process_data[i]['arrival'] ) for i in process_data] )
        process_names = np.array(
            [process_data[i]['process-name'] for i in process_data] )

        slots = []
        begin = arrival_time[0] # anta btbtdy mn el arrival time bt3 awl wa7dah mesh zero
        total_slots = int( sum( brust_time ) - (n - Q - 1) )
        i = 0
        for j in range( total_slots ):
            if sum( brust_time ) == 0:
                break
            while i < n :
                if brust_time[i] != 0:
                    if begin < arrival_time[i]:
                        begin += Q
                        continue
                    brust_time[i] -= Q
                    slots.append( Slot(process_names[i], begin,  Q,arrival_time[i]))# nta kont bt add begin 3la Q w da 8lat anta  el solt  el brust bt3o Q bas
                    begin += Q
                i += 1
            i = 0

        return slots

    def get_current_pri(self, process_data, time):
        min = 10000000000
        minindex = 0
        x= len(process_data)
        thereIsProcess = 0
        for i in range(1, x+1 ):
            if time >= process_data[i]['arrival'] and int(process_data[i]['brust']) != 0:
                if int(process_data[i]['priority']) <= min:
                    min = int(process_data[i]['priority'])
                    minindex = i
                    thereIsProcess=1

        if(thereIsProcess>0):
            return minindex
        else:
            return -1

    def calc_priority_pree(self, process_data):
        x = sorted( process_data.items(
        ), key=lambda d: (d[1]['arrival']) )
        process_data = OrderedDict( x )
        n = num_processes
        brust_time = np.array( [float( process_data[i]['brust'] )
                                for i in process_data] )
        arrival_time = np.array(
            [float( process_data[i]['arrival'] ) for i in process_data] )
        process_names = np.array(
            [process_data[i]['process-name'] for i in process_data] )

        slots = []
        begin = 0
        full_time = sum( brust_time )
        current_process = 0
        previvous_process = -2
        # i = arrival_time[0]
        for i in range(int(full_time+arrival_time[0])):
            current_process = self.get_current_pri( process_data, i )-1

            if(current_process <0):
                begin += 1
                continue
            if current_process != previvous_process :
                previvous_process = current_process
                slots.append( Slot( process_names[current_process], begin, 1 ) )
            else:
                i=0
                for s in slots:
                   if(i==len(slots)-1):
                       s.slotTime+=1
                   i+=1



            begin+=1
            process_data[current_process+1]['brust'] -= 1

        return slots


app = QApplication( sys.argv )
UIWindow = UI()

app.exec_()

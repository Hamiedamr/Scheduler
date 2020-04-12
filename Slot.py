import matplotlib
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5 import uic
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
matplotlib.rcParams.update({'font.size': 7})

def drawSlots(slots):
    fig = plt.figure()
    left = .1
    bottom, height = .2, .5
    widthRange = .01
    xScale = 0.01

    start = 0
    frist = True
    for s in slots:
        start = [s.slotStart][0] * xScale
        width = [s.slotTime][0] * widthRange
        processBegin = [s.slotStart][0]
        slotName = [s.processName][0]
        p = patches.Rectangle( (start, bottom), width, height, label="p", color="red", fill=0 )
        # start time of the process
        fig.text( start, bottom, str( int( processBegin ) ), horizontalalignment='left', verticalalignment='top' )
        # proces name
        fig.text( start, height / 2 + bottom, slotName, horizontalalignment='left', verticalalignment='top' )
        fig.add_artist( p )
    frist = False
    if frist == False:
        fig.text( start + width, bottom, str( int( processBegin + s.slotTime ) ), horizontalalignment='left',
                  verticalalignment='top' )
        fig.add_artist( p )

    plt.show()
class Slot:
    def __init__(self, processName, slotStart,slotTime ):
        self.processName = processName
        self.slotStart = float(slotStart)
        self.slotTime = float(slotTime)






#!/usr/bin/env python
## used to parse files more easily
#from __future__ import with_statement
import time
#
from pylab import *
from scipy import *
# os
import os
# Numpy module
import numpy as np
# for command-line arguments
import sys
# Qt4 bindings for core Qt functionalities (non-GUI)
from PyQt4 import QtCore
# Python Qt4 bindings for GUI objects
from PyQt4 import QtGui
# import the MainWindow widget from the converted .ui files
from qtdesigner import Ui_MplMainWindow
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
class DesignerMainWindow(QtGui.QMainWindow, Ui_MplMainWindow):
  """Customization for Qt Designer created window"""
  def __init__(self, parent = None):
    # initialization of the superclass
    super(DesignerMainWindow, self).__init__(parent)
    # setup the GUI --> function generated by pyuic4
    self.setupUi(self)

  def clear(self):
    self.mpl.canvas.ax.clear()
    self.mpl.canvas.draw()

  def plotrm(self):
    self.mpl.canvas.ax.clear()
    self.mpl.canvas.ax.plot(range(len(self.rm)), self.rm, 'o-')
    self.mpl.canvas.ax.set_xlim(0, len(self.rm) )
    self.mpl.canvas.ax.set_ylim(0, max(self.rm))
    self.mpl.canvas.draw()

  def plottheo(self):
    self.mpl.canvas.ax.plot(range(len(self.rm)), sqrt(range(len(self.rm))), 'r', lw=2)
    self.mpl.canvas.draw()

  def run(self):
    self.mpl.canvas.ax.clear()
    self.npart = int(self.lineEdit_npart.text())
    self.niter = int(self.lineEdit_niter.text())
    self.Lbox  = int(self.lineEdit_Lbox.text())
    self.drawcircle = self.checkBox_drawcircle.isChecked()
    self.plottrajectory = self.checkBox_plottrajectory.isChecked()
    self.rm = [0.]
    if self.radioButton_pointsource.isChecked():
      xo = zeros(self.npart)
      yo = zeros(self.npart)
    elif self.radioButton_leftfront.isChecked():
      xo = self.Lbox*(2*random.rand(self.npart)-2) 
      yo = self.Lbox*(4*random.rand(self.npart)-2)
    l = 1.
    self.mpl.canvas.ax.set_xlim(-self.Lbox,self.Lbox)
    self.mpl.canvas.ax.set_ylim(-self.Lbox,self.Lbox)
    myplot, = self.mpl.canvas.ax.plot(xo,yo,'o', zorder=1)
    circ = Circle((0,0), radius=0, fc='None', lw=2, color='red', zorder=2)
    self.mpl.canvas.ax.add_patch(circ)
    self.mpl.canvas.draw()
    self.t = -1
    while self.t<self.niter:
      self.t = self.t+1
      r = random.rand(self.npart)
      theta = 2*pi*r
      x = xo + cos(theta)*l
      y = yo + sin(theta)*l
      if self.plottrajectory:
        self.mpl.canvas.ax.plot([xo, x], [yo, y], '-b')
      myplot.set_data(x, y)
      self.mpl.canvas.draw()
      xo = x
      yo = y
      self.rm.append(sqrt(mean(x**2+y**2)))
      if self.drawcircle:
        circ.set_radius(self.rm[self.t])
        #self.mpl.canvas.ax.add_patch(circ)
      QtCore.QCoreApplication.processEvents()
  def stop(self):
    self.t = self.niter

# create the GUI application
app = QtGui.QApplication(sys.argv)
# instantiate the main window
dmw = DesignerMainWindow()
# show it
dmw.show()
# start the Qt main loop execution, exiting from this script
# with the same return code of Qt application
sys.exit(app.exec_())


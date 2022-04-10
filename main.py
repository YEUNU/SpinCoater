# changelog : preset save load by internal file, os.chdir test

# if you want to make pyinstall use the code
# try:
#     os.chdir(sys._MEIPASS)
#     print(sys._MEIPASS)
# except:
#     os.chdir(os.getcwd())

# os.chdir("/home/pi/spincoater")
# print(os.getcwd())

#library
import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from PyQt5 import QtCore
from pyqtgraph import PlotWidget, plot
import time
import pyqtgraph as pg
import sys  
import os
import serial
from keypad_dialog import keypadClass

#check COM port 
def check_port():
    global real_port
    port_list =["/dev/ttyACM0","/dev/ttyUSB0","COM4","COM9","COM7","COM3","COM5"] # ttyACM0,ttyUSB0 is for raspberry
    for i in range((len(port_list))):
        try:
            ser = serial.Serial(port = port_list[i],baudrate = 115200) # port is in port_list baudrate is 115200
            real_port = port_list[i]
            print(real_port)
        except:
            print("no")
check_port()

# #arduino connect 
ser = serial.Serial(
    port= real_port,
    baudrate=115200
)

#wait for arduino connection
time.sleep(5)

#pyqt ui file 
main_uiFile = './main.ui'

#class for pyqt
class gui(QMainWindow):
    def __init__(self):
        super().__init__() # __init__ is parent class
        self.vaccum = 0 # 0 : vaccum off, 1 : vaccum on 
        self.check_click = 0 # check vaccum button is clicked
        self.xlist = [] # x axis list for drawed graph
        self.ylist = [] # y axis list for drawed graph
        self.copy_ylist =[] # y axis list for following graph 
        self.copy_xlist = [] # x axis list for following graph 
        self.copy_count = 0 # count for following graph
        self.run_status = 0 # 0 : not running motor 1 : running motor 2 : user set rpm over 9000 
        self.update_value = [0] # list for transport to arduino [run_status , vaccum , w value , r value , t value,....]
        self.preset1 = [] # list for preset1
        self.preset2 = [] # list for preset2
        self.preset3 = [] # list for preset3
        self.preset4 = [] # list for preset4
        self.x1 = [] # list for w1,r1,t1 [w1,r1,t1]
        self.x2 = [] # list for w2,r2,t2 [w2,r2,t2]
        self.x3 = [] # list for w3,r3,t3 [w3,r3,t3]
        self.x4 = [] # list for w4,r4,t4 [w4,r4,t4]
        self.x5 = [] # list for w5,r5,t5 [w5,r5,t5]
        self.x6 = [] # list for w6,r6,t6 [w6,r6,t6]
        self.x7 = [] # list for w7,r7,t7 [w7,r7,t7]
        self.x8 = [] # list for w8,r8,t8 [w8,r8,t8]
        self.x9 = [] # list for w9,r9,t9 [w9,r9,t9]
        self.x10 = [] # list for w10,r10,t10 [w10,r10,t10]
        self.mx=[1,1,1,1,1,1,1,1,1,1] # check list for missed x value
        self.graphwidget = pg.PlotWidget() # main graph tab 
        self.timer = QTimer(self) # main graph timer
        pg.setConfigOptions(background = 'w') # make pyqtgraph background white
        uic.loadUi(main_uiFile, self) # load the ui file 
        self.UIinit() # style sheet etc function
        self.pen = pg.mkPen(color=(255, 0, 0),width=4) # drawed main graph color(red),width(4)
        self.pen_1 = pg.mkPen(color=(0, 255, 0),width=4) # following main graph color(green),width(4)
        self.timer.timeout.connect(self.copy_calc) # if timer passed following main graph function connect

    def plot(self, time, rpm): # function for drawed main graph 
        self.graphwidget.showGrid(x=True,y=True) # grid on
        self.graphwidget.plot(time, rpm ,pen=self.pen) # set x, y axis 

    def plot_1(self, time, rpm): # function for follwing main graph 
        self.graphwidget.showGrid(x=True,y=True) # grid on
        self.graphwidget.plot(time, rpm ,pen=self.pen_1) # set x, y axis 

    def arduino(self): # function for data transport to arduino
        self.update_value = str(self.run_status) + ',' + str(self.vaccum)  
        if self.mx[0] == 1:
            self.update_value = \
                self.update_value\
                + "," + self.w1_num.text()\
                + "," + self.r1_num.text()\
                + "," + self.t1_num.text()

        if self.mx[1] == 1:
            self.update_value = \
                self.update_value\
                + "," + self.w2_num.text()\
                + "," + self.r2_num.text()\
                + "," + self.t2_num.text()

        if self.mx[2] == 1:
            self.update_value = \
                self.update_value\
                + "," + self.w3_num.text()\
                + "," + self.r3_num.text()\
                + "," + self.t3_num.text()

        if self.mx[3] == 1:
            self.update_value = \
                self.update_value\
                + "," + self.w4_num.text()\
                + "," + self.r4_num.text()\
                + "," + self.t4_num.text()

        if self.mx[4] == 1:
            self.update_value = \
                self.update_value\
                + "," + self.w5_num.text()\
                + "," + self.r5_num.text()\
                + "," + self.t5_num.text()

        if self.mx[5] == 1:
            self.update_value = \
                self.update_value\
                + "," + self.w6_num.text()\
                + "," + self.r6_num.text()\
                + "," + self.t6_num.text()

        if self.mx[6] == 1:
            self.update_value = \
                self.update_value\
                + "," + self.w7_num.text()\
                + "," + self.r7_num.text()\
                + "," + self.t7_num.text()

        if self.mx[7] == 1:
            self.update_value = \
                self.update_value\
                + "," + self.w8_num.text()\
                + "," + self.r8_num.text()\
                + "," + self.t8_num.text()

        if self.mx[8] == 1:
            self.update_value = \
                self.update_value\
                + "," + self.w9_num.text()\
                + "," + self.r9_num.text()\
                + "," + self.t9_num.text()

        if self.mx[9] == 1:
            self.update_value = \
                self.update_value\
                + "," + self.w10_num.text()\
                + "," + self.r10_num.text()\
                + "," + self.t10_num.text()
        temp = str(self.update_value) # make string combined data(update_value)
        trans =temp.encode('utf-8') # encode local variable to utf-8 for arduino can read
        print(trans)
        ser.write(trans) # write data to arduino

    def vaccum_arduino(self): # function for activate vaccum 
        if self.vaccum == 0: # if vaccum button is not pushed
            if self.run_status == 1:
                temp = "1,0\n" # data [1,0]
            if self.run_status == 0:
                temp = "0,0\n" # data [0,0]
        if self.vaccum == 1: # if vaccum button is pushed
            if self.run_status ==1: # if motor is running 
                temp = "1,1\n" # data [1,1]
            if self.run_status ==0: # if motor is not running 
                temp = "0,1\n" # data [0,1]

        trans =temp.encode('utf-8')
        print(trans)
        ser.write(trans)
        
    def run(self): # running function 
        self.setvalue() # setvalue for user not pushed check button
        if self.run_status == 2: # if user set rpm over 9000
            self.change_page(1) # set view page(1) : setting page
            
        if self.run_status == 0: # if run_status = 0
            self.change_page(2) # set view page(2) : graph page
            self.run_status = 1 # set run_status = 1
            self.arduino() # trans data to arduino by arduino function
            self.timer.start(1000) # run main timer 1sec
 
    def stop(self):
        self.copy_count=0 # clear
        self.count = 0 # clear
        self.update_value = 0, # clear
        self.run_status =0 # clear
        self.rpm_indicator.display(str(0)) # display clear
        print("update_value",str(self.update_value))
        self.arduino() # trans stop data to arduino transported data is (0)

    def check(self):
        self.run_status = 0
        try:
            if int(self.w1_num.text()) > 9000: # if user set rpm over 9000
                QMessageBox.about(self,'ERROR',"RPM must be under 9000") # error message occur
                self.run_status = 2 # set run_status =2
        except:
            print("w1 is under 9000") 
        try:
            if int(self.w2_num.text()) > 9000: # if user set rpm over 9000
                QMessageBox.about(self,'ERROR',"RPM must be under 9000") # error message occur
                self.run_status = 2 # set run_status =2
        except:
            print("w2 is under 9000")
        try:
            if int(self.w3_num.text()) > 9000: # if user set rpm over 9000
                QMessageBox.about(self,'ERROR',"RPM must be under 9000") # error message occur
                self.run_status = 2 # set run_status =2
        except:
            print("w3 is under 9000")
        try:
            if int(self.w4_num.text()) > 9000: # if user set rpm over 9000
                QMessageBox.about(self,'ERROR',"RPM must be under 9000") # error message occur
                self.run_status = 2 # set run_status =2
        except:
            print("w4 is under 9000")
        try:
            if int(self.w5_num.text()) > 9000: # if user set rpm over 9000
                QMessageBox.about(self,'ERROR',"RPM must be under 9000") # error message occur
                self.run_status = 2 # set run_status =2
        except:
            print("w5 is under 9000")
        try:
            if int(self.w6_num.text()) > 9000: # if user set rpm over 9000
                QMessageBox.about(self,'ERROR',"RPM must be under 9000") # error message occur
                self.run_status = 2 # set run_status =2
        except:
            print("w6 is under 9000")
        try:
            if int(self.w7_num.text()) > 9000: # if user set rpm over 9000
                QMessageBox.about(self,'ERROR',"RPM must be under 9000") # error message occur
                self.run_status = 2 # set run_status =2
        except:
            print("w7 is under 9000")
        try:
            if int(self.w8_num.text()) > 9000: # if user set rpm over 9000
                QMessageBox.about(self,'ERROR',"RPM must be under 9000") # error message occur
                self.run_status = 2 # set run_status =2
        except:
            print("w8 is under 9000")
        try:
            if int(self.w9_num.text()) > 9000: # if user set rpm over 9000
                QMessageBox.about(self,'ERROR',"RPM must be under 9000") # error message occur
                self.run_status = 2 # set run_status =2
        except:
            print("w9 is under 9000")
        try:
            if int(self.w10_num.text()) > 9000: # if user set rpm over 9000
                QMessageBox.about(self,'ERROR',"RPM must be under 9000") # error message occur
                self.run_status = 2 # set run_status =2
        except:
            print("w10 is under 9000")

    def setvalue(self): # if check button clicked setvalue function operate
        self.check() # run check function to check rpm
        if self.run_status ==2: # if rpm is over 9000
            print("ERROR") # function ended
        if self.run_status == 0: # if run_status =0 (motor is not running )
            self.copy_xlist = [] # clear following graph x list
            self.copy_ylist = [] # clear following graph y list
            self.graphwidget.clear() # clear visual graph
            self.mx = [1,1,1,1,1,1,1,1,1,1] # clear mx list(check the missed value) 1 : value inserted, 0 : value not inserted
            self.update_value = str(self.run_status) + "," + str(self.vaccum)
            try:
                self.x1 = [float(self.w1_num.text()),int(self.r1_num.text()),int(self.t1_num.text())]
                print("x1",self.x1)
            except:
                self.mx[0] = 0
                print("x1 no")
            try:
                self.x2 = [float(self.w2_num.text()),int(self.r2_num.text()),int(self.t2_num.text())]
                print("x2",self.x2)
            except:
                self.mx[1] = 0
                print("x2 no")
            try:
                self.x3 = [float(self.w3_num.text()),int(self.r3_num.text()),int(self.t3_num.text())]
                print("x3",self.x3)
            except:
                self.mx[2] = 0
                print("x3 no")
            try:
                self.x4 = [float(self.w4_num.text()),int(self.r4_num.text()),int(self.t4_num.text())]
                print("x4",self.x4)
            except:
                self.mx[3] = 0
                print("x4 no")
            try:
                self.x5 = [float(self.w5_num.text()),int(self.r5_num.text()),int(self.t5_num.text())]
                print("x5",self.x5)
            except:
                self.mx[4] = 0
                print("x5 no")
            try:
                self.x6 = [float(self.w6_num.text()),int(self.r6_num.text()),int(self.t6_num.text())]
                print("x6",self.x6)
            except:
                self.mx[5] = 0
                print("x6 no")
            try:
                self.x7 = [float(self.w7_num.text()),int(self.r7_num.text()),int(self.t7_num.text())]
                print("x7",self.x7)
            except:
                self.mx[6] = 0
                print("x7 no")
            try:
                self.x8 = [float(self.w8_num.text()),int(self.r8_num.text()),int(self.t8_num.text())]
                print("x8",self.x8)
            except:
                self.mx[7] = 0
                print("x8 no")
            try:
                self.x9 = [float(self.w9_num.text()),int(self.r9_num.text()),int(self.t9_num.text())]
                print("x9",self.x9)
            except:
                self.mx[8] = 0
                print("x9 no")
            try:
                self.x10 = [float(self.w10_num.text()),int(self.r10_num.text()),int(self.t10_num.text())]
                print("x10",self.x10)
            except:
                self.mx[9] = 0
                print("x10 no") 
            self.calc() # draw main graph
        print("update_value :",self.update_value)

    def preset_save(self,num): # preset save function
        self.setvalue() # setvalue function for user whom not pressed check button

        if num == 1: # if preset1 save is pressed
            self.preset1 = [] # clear preset1 list
            self.preset1.append(self.x1) # append x1
            self.preset1.append(self.x2) # append x2
            self.preset1.append(self.x3) # append x3
            self.preset1.append(self.x4) # append x4
            self.preset1.append(self.x5) # append x5
            self.preset1.append(self.x6) # append x6
            self.preset1.append(self.x7) # append x7
            self.preset1.append(self.x8) # append x8
            self.preset1.append(self.x9) # append x9
            self.preset1.append(self.x10) # append x10
            f = open("preset1.txt","w")
            f.write(str(self.preset1))
            f.close()
            print("preset1",self.preset1)

        if num == 2: # if preset2 save is pressed
            self.preset2 = [] # clear preset2 list
            self.preset2.append(self.x1) # append x1
            self.preset2.append(self.x2) # append x2
            self.preset2.append(self.x3) # append x3
            self.preset2.append(self.x4) # append x4
            self.preset2.append(self.x5) # append x5
            self.preset2.append(self.x6) # append x6
            self.preset2.append(self.x7) # append x7
            self.preset2.append(self.x8) # append x8
            self.preset2.append(self.x9) # append x9
            self.preset2.append(self.x10) # append x10
            f = open("preset2.txt","w")
            f.write(str(self.preset2))
            f.close()
            print("preset2",self.preset2)

        if num == 3: # if preset3 save is pressed
            self.preset3 = [] # clear preset3 list
            self.preset3.append(self.x1) # append x1
            self.preset3.append(self.x2) # append x2
            self.preset3.append(self.x3) # append x3
            self.preset3.append(self.x4) # append x4
            self.preset3.append(self.x5) # append x5
            self.preset3.append(self.x6) # append x6
            self.preset3.append(self.x7) # append x7
            self.preset3.append(self.x8) # append x8
            self.preset3.append(self.x9) # append x9
            self.preset3.append(self.x10) # append x10
            f = open("preset3.txt","w")
            f.write(str(self.preset3))
            f.close()
            print("preset3",self.preset3)

        if num == 4: # if preset4 save is pressed
            self.preset4 = [] # clear preset4 list
            self.preset4.append(self.x1) # append x1
            self.preset4.append(self.x2) # append x2
            self.preset4.append(self.x3) # append x3
            self.preset4.append(self.x4) # append x4
            self.preset4.append(self.x5) # append x5
            self.preset4.append(self.x6) # append x6
            self.preset4.append(self.x7) # append x7
            self.preset4.append(self.x8) # append x8
            self.preset4.append(self.x9) # append x9
            self.preset4.append(self.x10) # append x10
            f = open("preset4.txt","w")
            f.write(str(self.preset4))
            f.close()
            print("preset4",self.preset4)

        message = "Preset "+str(num) + " saved" # local variable for visual text message
        QMessageBox.about(self,'Saved',message) # message event

    def preset_load(self,num): # preset load function
        self.empty(2)
        if num == 1: # if user pressed preset1 load
            try:
                try:
                    f = open("preset1.txt", 'r')
                    lines = f.readline()
                    lines = lines.replace('[',"").replace(']',"").split(",")
                    self.preset1 = []
                    temp = []
                    count = 0
                    list_count = 0
                    for i in lines:
                        count += 1
                        temp.append(i)
                        if count == 3:
                            self.preset1.append(temp)
                            count = 0
                            temp = []
                    
                except:
                    message = "Preset " + str(num) + "is not saved"
                    QMessageBox.about(self,'Failed',message)
                f.close()

                self.w1_num.setText(str(self.preset1[0][0])) #[[v],[],[]]
                self.r1_num.setText(str(self.preset1[0][1])) #[[],[v],[]]
                self.t1_num.setText(str(self.preset1[0][2])) #[[],[],[v]]
                self.w2_num.setText(str(self.preset1[1][0])) 
                self.r2_num.setText(str(self.preset1[1][1])) 
                self.t2_num.setText(str(self.preset1[1][2]))
                self.w3_num.setText(str(self.preset1[2][0]))
                self.r3_num.setText(str(self.preset1[2][1]))
                self.t3_num.setText(str(self.preset1[2][2]))
                self.w4_num.setText(str(self.preset1[3][0]))
                self.r4_num.setText(str(self.preset1[3][1]))
                self.t4_num.setText(str(self.preset1[3][2]))
                self.w5_num.setText(str(self.preset1[4][0]))
                self.r5_num.setText(str(self.preset1[4][1]))
                self.t5_num.setText(str(self.preset1[4][2]))
                self.w6_num.setText(str(self.preset1[5][0]))
                self.r6_num.setText(str(self.preset1[5][1]))
                self.t6_num.setText(str(self.preset1[5][2]))
                self.w7_num.setText(str(self.preset1[6][0]))
                self.r7_num.setText(str(self.preset1[6][1]))
                self.t7_num.setText(str(self.preset1[6][2]))
                self.w8_num.setText(str(self.preset1[7][0]))
                self.r8_num.setText(str(self.preset1[7][1]))
                self.t8_num.setText(str(self.preset1[7][2]))
                self.w9_num.setText(str(self.preset1[8][0]))
                self.r9_num.setText(str(self.preset1[8][1]))
                self.t9_num.setText(str(self.preset1[8][2]))
                self.w10_num.setText(str(self.preset1[9][0]))
                self.r10_num.setText(str(self.preset1[9][1]))
                self.t10_num.setText(str(self.preset1[9][2]))

            except IndexError:
                print("Index error")

        if num == 2: # if user pressed preset2 load
            try:
                try:
                    f = open("preset2.txt", 'r')
                    lines = f.readline()
                    lines = lines.replace('[',"").replace(']',"").split(",")
                    self.preset1 = []
                    temp = []
                    count = 0
                    list_count = 0
                    for i in lines:
                        count += 1
                        temp.append(i)
                        if count == 3:
                            self.preset1.append(temp)
                            count = 0
                            temp = []
                    
                except:
                    message = "Preset " + str(num) + " is not saved"
                    QMessageBox.about(self,'Failed',message)
                f.close()

                self.w1_num.setText(str(self.preset2[0][0])) #[[v],[],[]]
                self.r1_num.setText(str(self.preset2[0][1])) #[[],[v],[]]
                self.t1_num.setText(str(self.preset2[0][2])) #[[],[],[v]]
                self.w2_num.setText(str(self.preset2[1][0]))
                self.r2_num.setText(str(self.preset2[1][1]))
                self.t2_num.setText(str(self.preset2[1][2]))
                self.w3_num.setText(str(self.preset2[2][0]))
                self.r3_num.setText(str(self.preset2[2][1]))
                self.t3_num.setText(str(self.preset2[2][2]))
                self.w4_num.setText(str(self.preset2[3][0]))
                self.r4_num.setText(str(self.preset2[3][1]))
                self.t4_num.setText(str(self.preset2[3][2]))
                self.w5_num.setText(str(self.preset2[4][0]))
                self.r5_num.setText(str(self.preset2[4][1]))
                self.t5_num.setText(str(self.preset2[4][2]))
                self.w6_num.setText(str(self.preset2[5][0]))
                self.r6_num.setText(str(self.preset2[5][1]))
                self.t6_num.setText(str(self.preset2[5][2]))
                self.w7_num.setText(str(self.preset2[6][0]))
                self.r7_num.setText(str(self.preset2[6][1]))
                self.t7_num.setText(str(self.preset2[6][2]))
                self.w8_num.setText(str(self.preset2[7][0]))
                self.r8_num.setText(str(self.preset2[7][1]))
                self.t8_num.setText(str(self.preset2[7][2]))
                self.w9_num.setText(str(self.preset2[8][0]))
                self.r9_num.setText(str(self.preset2[8][1]))
                self.t9_num.setText(str(self.preset2[8][2]))
                self.w10_num.setText(str(self.preset2[9][0]))
                self.r10_num.setText(str(self.preset2[9][1]))
                self.t10_num.setText(str(self.preset2[9][2]))

            except IndexError:
                print("index error")

        if num == 3: # if user pressed preset3 load
            try:
                try:
                    f = open("preset3.txt", 'r')
                    lines = f.readline()
                    lines = lines.replace('[',"").replace(']',"").split(",")
                    self.preset1 = []
                    temp = []
                    count = 0
                    list_count = 0
                    for i in lines:
                        count += 1
                        temp.append(i)
                        if count == 3:
                            self.preset1.append(temp)
                            count = 0
                            temp = []
                    
                except:
                    message = "Preset " + str(num) + "is not saved"
                    QMessageBox.about(self,'Failed',message)
                f.close()

                self.w1_num.setText(str(self.preset3[0][0])) #[[v],[],[]]
                self.r1_num.setText(str(self.preset3[0][1])) #[[],[v],[]]
                self.t1_num.setText(str(self.preset3[0][2])) #[[],[],[v]]
                self.w2_num.setText(str(self.preset3[1][0]))
                self.r2_num.setText(str(self.preset3[1][1]))
                self.t2_num.setText(str(self.preset3[1][2]))
                self.w3_num.setText(str(self.preset3[2][0]))
                self.r3_num.setText(str(self.preset3[2][1]))
                self.t3_num.setText(str(self.preset3[2][2]))
                self.w4_num.setText(str(self.preset3[3][0]))
                self.r4_num.setText(str(self.preset3[3][1]))
                self.t4_num.setText(str(self.preset3[3][2]))
                self.w5_num.setText(str(self.preset3[4][0]))
                self.r5_num.setText(str(self.preset3[4][1]))
                self.t5_num.setText(str(self.preset3[4][2]))
                self.w6_num.setText(str(self.preset3[5][0]))
                self.r6_num.setText(str(self.preset3[5][1]))
                self.t6_num.setText(str(self.preset3[5][2]))
                self.w7_num.setText(str(self.preset3[6][0]))
                self.r7_num.setText(str(self.preset3[6][1]))
                self.t7_num.setText(str(self.preset3[6][2]))
                self.w8_num.setText(str(self.preset3[7][0]))
                self.r8_num.setText(str(self.preset3[7][1]))
                self.t8_num.setText(str(self.preset3[7][2]))
                self.w9_num.setText(str(self.preset3[8][0]))
                self.r9_num.setText(str(self.preset3[8][1]))
                self.t9_num.setText(str(self.preset3[8][2]))
                self.w10_num.setText(str(self.preset3[9][0]))
                self.r10_num.setText(str(self.preset3[9][1]))
                self.t10_num.setText(str(self.preset3[9][2]))

            except IndexError:
                print("index error")

        if num == 4: # if user pressed preset4 load
            try:
                try:
                    f = open("preset4.txt", 'r')
                    lines = f.readline()
                    lines = lines.replace('[',"").replace(']',"").split(",")
                    self.preset1 = []
                    temp = []
                    count = 0
                    list_count = 0
                    for i in lines:
                        count += 1
                        temp.append(i)
                        if count == 3:
                            self.preset1.append(temp)
                            count = 0
                            temp = []
                    
                except:
                    message = "Preset " + str(num) + "is not saved"
                    QMessageBox.about(self,'Failed',message)
                f.close()

                self.w1_num.setText(str(self.preset4[0][0])) #[[v],[],[]]
                self.r1_num.setText(str(self.preset4[0][1])) #[[],[v],[]]
                self.t1_num.setText(str(self.preset4[0][2])) #[[],[],[v]]
                self.w2_num.setText(str(self.preset4[1][0]))
                self.r2_num.setText(str(self.preset4[1][1]))
                self.t2_num.setText(str(self.preset4[1][2]))
                self.w3_num.setText(str(self.preset4[2][0]))
                self.r3_num.setText(str(self.preset4[2][1]))
                self.t3_num.setText(str(self.preset4[2][2]))
                self.w4_num.setText(str(self.preset4[3][0]))
                self.r4_num.setText(str(self.preset4[3][1]))
                self.t4_num.setText(str(self.preset4[3][2]))
                self.w5_num.setText(str(self.preset4[4][0]))
                self.r5_num.setText(str(self.preset4[4][1]))
                self.t5_num.setText(str(self.preset4[4][2]))
                self.w6_num.setText(str(self.preset4[5][0]))
                self.r6_num.setText(str(self.preset4[5][1]))
                self.t6_num.setText(str(self.preset4[5][2]))
                self.w7_num.setText(str(self.preset4[6][0]))
                self.r7_num.setText(str(self.preset4[6][1]))
                self.t7_num.setText(str(self.preset4[6][2]))
                self.w8_num.setText(str(self.preset4[7][0]))
                self.r8_num.setText(str(self.preset4[7][1]))
                self.t8_num.setText(str(self.preset4[7][2]))
                self.w9_num.setText(str(self.preset4[8][0]))
                self.r9_num.setText(str(self.preset4[8][1]))
                
                self.t9_num.setText(str(self.preset4[8][2]))
                self.w10_num.setText(str(self.preset4[9][0]))
                self.r10_num.setText(str(self.preset4[9][1]))
                self.t10_num.setText(str(self.preset4[9][2]))

            except IndexError:
                print("index error")

        message = "Preset "+str(num) + " loaded" # local variable for preset load message
        QMessageBox.about(self,'Saved',message) # message occur

    def copy_calc(self): # function for following graph
        self.graphwidget.clear() # displayed graph clear

        if self.run_status == 1: # if running 
            try:
                self.copy_ylist.append(round(self.ylist[self.copy_count],2)) # append following ylist round 2 
                self.rpm_indicator.display(str(round(self.ylist[self.copy_count],2))) # display present main graph tab rpm indicator 
                self.copy_xlist.append(self.copy_count) # append following xlist

            except IndexError:
                print("list index out of range")

            self.plot(self.xlist,self.ylist) # draw main graph by appended value list
            self.plot_1(self.copy_xlist,self.copy_ylist) # draw following graph by appended value list
            self.copy_count += 1 # add count

            if self.copy_count >= len(self.xlist): # if count length = xlist length 
                self.run_status = 0 # run_status clear
                self.count = 0 # count clear
                self.copy_count = 0 # count copy_clear
                self.update_value = 0 # update_value clear
                self.rpm_indicator.display('0') # clear main graph rpm indicator
                self.timer.stop() # main graph timer stop

        else : # if run_status =! 1
            self.timer.stop() # timer stop for not make error

    def calc(self): # function for draw main graph
        self.xlist = [0] # graph need to start in 0,0 
        self.ylist = [0] # graph need to start in 0,0
        count = 1 # 0,0 is already added, so count starts 1
        self.copy_ylist = [] 

        if self.mx[0] == 1: # if x1 is not missing
            rpm = self.x1[0] # [[v],[],[]]
            speed_time = self.x1[1] # [[],[v],[]]
            maintain_time = self.x1[2] # [[],[],[v]]
            self.update_value = self.update_value + ',' + str(rpm) + ',' + str(speed_time) + ',' + str(maintain_time) + ','
            try:
                add = rpm/speed_time # inclination (y = 'a'x graph) add is for 'a'
            except ZeroDivisionError: # if speed_time is zero
                QMessageBox.about(self,'Warning',"R value is 0 \n it must be upper than 0") # error message occur

            for i in range(1,speed_time+1):
                self.ylist.append(add*i) # y = ax graph
                self.xlist.append(count)
                count += 1
            for i in range(1,maintain_time+1): # maintain graph y = rpm graph
                self.ylist.append(rpm)
                self.xlist.append(count)
                count += 1

        if self.mx[1] == 1: # if x2 is not missing
            update_rpm = self.x2[0] # [[v],[],[]]
            speed_time = self.x2[1] # [[],[v],[]]
            maintain_time = self.x2[2] # [[],[],[v]]
            self.update_value = self.update_value + str(rpm) + ',' + str(speed_time) + ',' + str(maintain_time) + ','
            try:
                add = (update_rpm-rpm)/speed_time # inclination (y = 'a'x + b graph) add is for 'a'
            except ZeroDivisionError: # if speed_time is zero
                QMessageBox.about(self,'Warning',"R value is 0 \n it must be upper than 0") # error message occur
            
            for i in range(1,speed_time+1):
                self.ylist.append(rpm + add) # y = ax + b graph
                self.xlist.append(count)
                rpm += add
                count += 1
            for i in range(1,maintain_time+1): # maintain graph y = rpm graph
                self.ylist.append(update_rpm)
                self.xlist.append(count)
                count += 1

        if self.mx[2] == 1: # if x3 is not missing
            update_rpm = self.x3[0] # [[v],[],[]]
            speed_time = self.x3[1] # [[],[v],[]]
            maintain_time = self.x3[2] # [[],[],[v]]
            self.update_value = self.update_value + str(rpm) + ',' + str(speed_time) + ',' + str(maintain_time) + ','
            try:
                add = (update_rpm-rpm)/speed_time # inclination (y = 'a'x + b graph) add is for 'a'
            except ZeroDivisionError: # if speed_time is zero
                QMessageBox.about(self,'Warning',"R value is 0 \n it must be upper than 0") # error message occur
            for i in range(1,speed_time+1):
                self.ylist.append(rpm + add) # y = ax + b graph
                self.xlist.append(count)
                rpm += add
                count += 1
            for i in range(1,maintain_time+1): # maintain graph y = rpm graph
                self.ylist.append(update_rpm)
                self.xlist.append(count)
                count += 1

        if self.mx[3] == 1: # if x4 is not missing
            update_rpm = self.x4[0] # [[v],[],[]]
            speed_time = self.x4[1] # [[],[v],[]]
            maintain_time = self.x4[2] # [[],[],[v]]
            self.update_value = self.update_value + str(rpm) + ',' + str(speed_time) + ',' + str(maintain_time) + ','
            try:
                add = (update_rpm-rpm)/speed_time # inclination (y = 'a'x + b graph) add is for 'a'
            except ZeroDivisionError: # if speed_time is zero
                QMessageBox.about(self,'Warning',"R value is 0 \n it must be upper than 0") # error message occur
            
            for i in range(1,speed_time+1):
                self.ylist.append(rpm + add) # y = ax + b graph
                self.xlist.append(count)
                rpm += add
                count += 1
            for i in range(1,maintain_time+1): # maintain graph y = rpm graph
                self.ylist.append(update_rpm)
                self.xlist.append(count)
                count += 1

        if self.mx[4] == 1: # if x5 is not missing
            update_rpm = self.x5[0] # [[v],[],[]]
            speed_time = self.x5[1] # [[],[v],[]]
            maintain_time = self.x5[2] # [[],[],[v]]
            self.update_value = self.update_value + str(rpm) + ',' + str(speed_time) + ',' + str(maintain_time) + ','
            try:
                add = (update_rpm-rpm)/speed_time # inclination (y = 'a'x + b graph) add is for 'a'
            except ZeroDivisionError: # if speed_time is zero
                QMessageBox.about(self,'Warning',"R value is 0 \n it must be upper than 0") # error message occur
            for i in range(1,speed_time+1):
                self.ylist.append(rpm + add) # y = ax + b graph
                self.xlist.append(count)
                rpm += add
                count += 1
            for i in range(1,maintain_time+1): # maintain graph y = rpm graph
                self.ylist.append(update_rpm)
                self.xlist.append(count)
                count += 1

        if self.mx[5] == 1: # if x6 is not missing
            update_rpm = self.x6[0] # [[v],[],[]]
            speed_time = self.x6[1] # [[],[v],[]]
            maintain_time = self.x6[2] # [[],[],[v]]
            self.update_value = self.update_value + str(rpm) + ',' + str(speed_time) + ',' + str(maintain_time) + ','
            try:
                add = (update_rpm-rpm)/speed_time # inclination (y = 'a'x + b graph) add is for 'a'
            except ZeroDivisionError: # if speed_time is zero
                QMessageBox.about(self,'Warning',"R value is 0 \n it must be upper than 0") # error message occur
            
            for i in range(1,speed_time+1):
                self.ylist.append(rpm + add) # y = ax + b graph
                self.xlist.append(count)
                rpm += add
                count += 1
            for i in range(1,maintain_time+1): # maintain graph y = rpm graph
                self.ylist.append(update_rpm)
                self.xlist.append(count)
                count += 1

        if self.mx[6] == 1: # if x7 is not missing
            update_rpm = self.x7[0] # [[v],[],[]]
            speed_time = self.x7[1] # [[],[v],[]]
            maintain_time = self.x7[2] # [[],[],[v]]
            self.update_value = self.update_value + str(rpm) + ',' + str(speed_time) + ',' + str(maintain_time) + ','
            try:
                add = (update_rpm-rpm)/speed_time # inclination (y = 'a'x + b graph) add is for 'a'
            except ZeroDivisionError: # if speed_time is zero
                QMessageBox.about(self,'Warning',"R value is 0 \n it must be upper than 0") # error message occur
            for i in range(1,speed_time+1):
                self.ylist.append(rpm + add) # y = ax + b graph
                self.xlist.append(count)
                rpm += add
                count += 1
            for i in range(1,maintain_time+1): # maintain graph y = rpm graph
                self.ylist.append(update_rpm)
                self.xlist.append(count)
                count += 1

        if self.mx[7] == 1: # if x8 is not missing
            update_rpm = self.x8[0] # [[v],[],[]]
            speed_time = self.x8[1] # [[],[v],[]]
            maintain_time = self.x8[2] # [[],[],[v]]
            self.update_value = self.update_value + str(rpm) + ',' + str(speed_time) + ',' + str(maintain_time) + ','
            try:
                add = (update_rpm-rpm)/speed_time # inclination (y = 'a'x + b graph) add is for 'a'
            except ZeroDivisionError:
                QMessageBox.about(self,'Warning',"R value is 0 \n it must be upper than 0") # error message occur
            
            for i in range(1,speed_time+1):
                self.ylist.append(rpm + add) # y = ax + b graph
                self.xlist.append(count)
                rpm += add
                count += 1
            for i in range(1,maintain_time+1): # maintain graph y = rpm graph
                self.ylist.append(update_rpm)
                self.xlist.append(count)
                count += 1

        if self.mx[8] == 1: # if x9 is not missing
            update_rpm = self.x9[0] # [[v],[],[]]
            speed_time = self.x9[1] # [[],[v],[]]
            maintain_time = self.x9[2] # [[],[],[v]]
            self.update_value = self.update_value + str(rpm) + ',' + str(speed_time) + ',' + str(maintain_time) + ','
            try:
                add = (update_rpm-rpm)/speed_time # inclination (y = 'a'x + b graph) add is for 'a'
            except ZeroDivisionError:
                QMessageBox.about(self,'Warning',"R value is 0 \n it must be upper than 0") # error message occur
            
            for i in range(1,speed_time+1):
                self.ylist.append(rpm + add) # y = ax + b graph
                self.xlist.append(count)
                rpm += add
                count += 1
            for i in range(1,maintain_time+1): # maintain graph y = rpm graph
                self.ylist.append(update_rpm)
                self.xlist.append(count)
                count += 1

        if self.mx[9] == 1: # if x10 is not missing
            update_rpm = self.x10[0] # [[v],[],[]]
            speed_time = self.x10[1] # [[],[v],[]]
            maintain_time = self.x10[2] # [[],[],[v]]
            self.update_value = self.update_value + str(rpm) + ',' + str(speed_time) + ',' + str(maintain_time) + ','
            try:
                add = (update_rpm-rpm)/speed_time # inclination (y = 'a'x + b graph) add is for 'a'
            except ZeroDivisionError:
                QMessageBox.about(self,'Warning',"R value is 0 \n it must be upper than 0") # error message occur

            for i in range(1,speed_time+1):
                self.ylist.append(rpm + add) # y = ax + b graph
                self.xlist.append(count)
                rpm += add
                count += 1
            for i in range(1,maintain_time+1): # maintain graph y = rpm graph
                self.ylist.append(update_rpm)
                self.xlist.append(count)
                count += 1

        self.plot(self.xlist,self.ylist) # draw main graph

    def change_page(self, num): # function for change page

        if num == 0:
            self.stackedWidget.setCurrentIndex(2) # sample
        if num == 1:
            self.stackedWidget.setCurrentIndex(0) # setting
        if num == 2:
            self.stackedWidget.setCurrentIndex(1) # graph

    def info(self): # function for version display
        #info message
        QMessageBox.about(self,"Program Information", "SpinCoater Ver.1\n\n<Hardware Version>\n  - Raspberry Pi 3 Model B ver1.2\n\n<Sofrware Version>\n  - Python_Version: 3.7.3\n  - PyQt5_Version: 5.11.3 \n\n\n http://teraleader.com")
        
    def empty(self, num): # function for empty value
        if num == 1: # make x[i] list empty
            self.x1 = []
            self.x2 = []
            self.x3 = []
            self.x4 = []
            self.x5 = []
            self.x6 = []
            self.x7 = []
            self.x8 = []
            self.x9 = []
            self.x10 = []
            print("xilist will be empty")

        if num == 2: # make w[i],r[i],t[i] empty
            self.w1_num.setText("")
            self.w2_num.setText("")
            self.w3_num.setText("")
            self.w4_num.setText("")
            self.w5_num.setText("")
            self.w6_num.setText("")
            self.w7_num.setText("")
            self.w8_num.setText("")
            self.w9_num.setText("")
            self.w10_num.setText("")
            self.r1_num.setText("")
            self.r2_num.setText("")
            self.r3_num.setText("")
            self.r4_num.setText("")
            self.r5_num.setText("")
            self.r6_num.setText("")
            self.r7_num.setText("")
            self.r8_num.setText("")
            self.r9_num.setText("")
            self.r10_num.setText("")
            self.t1_num.setText("")
            self.t2_num.setText("")
            self.t3_num.setText("")
            self.t4_num.setText("")
            self.t5_num.setText("")
            self.t6_num.setText("")
            self.t7_num.setText("")
            self.t8_num.setText("")
            self.t9_num.setText("")
            self.t10_num.setText("")
            print("w,r,t value will be empty")

        if num == 0: # run empty 1,2
            self.empty(1)
            self.empty(2)

    def widget(self, button): # function for keypad widget
        dlg = keypadClass() # local variable for get keypadclass
        r = dlg.showmodal() # keypadclass showmodal function

        if r: # == if true
            text = dlg.keypad_val.text() # text = keypad_val(is combined in keypad_dialog global variable)
            if button == "w1_num": 
                self.w1_num.setText(text) 
            if button == "r1_num":
                self.r1_num.setText(text)
            if button == "t1_num":
                self.t1_num.setText(text)

            if button == "w2_num":
                self.w2_num.setText(text)
            if button == "r2_num":
                self.r2_num.setText(text)
            if button == "t2_num":
                self.t2_num.setText(text)

            if button == "w3_num":
                self.w3_num.setText(text)
            if button == "r3_num":
                self.r3_num.setText(text)
            if button == "t3_num":
                self.t3_num.setText(text)
            
            if button == "w4_num":
                self.w4_num.setText(text)
            if button == "r4_num":
                self.r4_num.setText(text)
            if button == "t4_num":
                self.t4_num.setText(text)
        
            if button == "w5_num":
                self.w5_num.setText(text)
            if button == "r5_num":
                self.r5_num.setText(text)
            if button == "t5_num":
                self.t5_num.setText(text)

            if button == "w5_num":
                self.w5_num.setText(text)
            if button == "r5_num":
                self.r5_num.setText(text)
            if button == "t5_num":
                self.t5_num.setText(text)

            if button == "w6_num":
                self.w6_num.setText(text)
            if button == "r6_num":
                self.r6_num.setText(text)
            if button == "t6_num":
                self.t6_num.setText(text)

            if button == "w7_num":
                self.w7_num.setText(text)
            if button == "r7_num":
                self.r7_num.setText(text)
            if button == "t7_num":
                self.t7_num.setText(text)

            if button == "w8_num":
                self.w8_num.setText(text)
            if button == "r8_num":
                self.r8_num.setText(text)
            if button == "t8_num":
                self.t8_num.setText(text)

            if button == "w9_num":
                self.w9_num.setText(text)
            if button == "r9_num":
                self.r9_num.setText(text)
            if button == "t9_num":
                self.t9_num.setText(text)

            if button == "w10_num":
                self.w10_num.setText(text)
            if button == "r10_num":
                self.r10_num.setText(text)
            if button == "t10_num":
                self.t10_num.setText(text)
    
    def vaccum_event(self, event): # vaccum flash effect
        self.check_click += 1 # count for on/off
        self.movie = QMovie('./pic/push.gif', QByteArray(), self) # pyqt QMovie gif setting
        self.movie.setCacheMode(QMovie.CacheAll) # movie file set cache
        self.vaccum_label.setMovie(self.movie) # set movie file in qlabel
        self.movie.start() # animation start
        self.vaccum = 1 # vaccum on
        print("vaccum",self.vaccum)
        self.vaccum_arduino() # transport data to arduino

        if self.check_click % 2 == 0: # when count is even
            self.movie.stop() # animation stop
            self.vaccum = 0 # vaccum off
            print("vaccum",self.vaccum)
            self.vaccum_arduino() # transport data to arduino

    def closeEvent(self, event): 
        reply = QMessageBox.question(self, 'Message',
            "Exit the program", QMessageBox.Yes | QMessageBox.Cancel)

        if reply == QMessageBox.Yes:
            sys.exit()

    def UIinit(self):
        QScroller.grabGesture(self.scrollArea, QScroller.LeftMouseButtonGesture) # touch scroll event
        
        self.power_button.clicked.connect(self.closeEvent)
        self.setting_button.clicked.connect(lambda:self.change_page(1))
        self.graph_button.clicked.connect(lambda:self.change_page(2))
        self.vaccum_label.mouseReleaseEvent = self.vaccum_event
        self.info_button.clicked.connect(self.info)
        
        self.set_button.clicked.connect(self.setvalue)
        self.set_button_2.clicked.connect(self.setvalue)
        
        self.run_button.clicked.connect(self.run)
        self.run_button_2.clicked.connect(self.run)
        
        self.stop_button.clicked.connect(self.stop)
        self.stop_button_2.clicked.connect(self.stop)
       
        self.reset_button.clicked.connect(lambda:self.empty(0))

        self.w1_num.clicked.connect(lambda:self.widget("w1_num"))
        self.r1_num.clicked.connect(lambda:self.widget("r1_num"))
        self.t1_num.clicked.connect(lambda:self.widget("t1_num"))

        self.w2_num.clicked.connect(lambda:self.widget("w2_num"))
        self.r2_num.clicked.connect(lambda:self.widget("r2_num"))
        self.t2_num.clicked.connect(lambda:self.widget("t2_num"))

        self.w3_num.clicked.connect(lambda:self.widget("w3_num"))
        self.r3_num.clicked.connect(lambda:self.widget("r3_num"))
        self.t3_num.clicked.connect(lambda:self.widget("t3_num"))

        self.w4_num.clicked.connect(lambda:self.widget("w4_num"))
        self.r4_num.clicked.connect(lambda:self.widget("r4_num"))
        self.t4_num.clicked.connect(lambda:self.widget("t4_num"))

        self.w5_num.clicked.connect(lambda:self.widget("w5_num"))
        self.r5_num.clicked.connect(lambda:self.widget("r5_num"))
        self.t5_num.clicked.connect(lambda:self.widget("t5_num"))

        self.w6_num.clicked.connect(lambda:self.widget("w6_num"))
        self.r6_num.clicked.connect(lambda:self.widget("r6_num"))
        self.t6_num.clicked.connect(lambda:self.widget("t6_num"))

        self.w7_num.clicked.connect(lambda:self.widget("w7_num"))
        self.r7_num.clicked.connect(lambda:self.widget("r7_num"))
        self.t7_num.clicked.connect(lambda:self.widget("t7_num"))

        self.w8_num.clicked.connect(lambda:self.widget("w8_num"))
        self.r8_num.clicked.connect(lambda:self.widget("r8_num"))
        self.t8_num.clicked.connect(lambda:self.widget("t8_num"))

        self.w9_num.clicked.connect(lambda:self.widget("w9_num"))
        self.r9_num.clicked.connect(lambda:self.widget("r9_num"))
        self.t9_num.clicked.connect(lambda:self.widget("t9_num"))

        self.w10_num.clicked.connect(lambda:self.widget("w10_num"))
        self.r10_num.clicked.connect(lambda:self.widget("r10_num"))
        self.t10_num.clicked.connect(lambda:self.widget("t10_num")) 

        self.p1_save.clicked.connect(lambda:self.preset_save(1))
        self.p2_save.clicked.connect(lambda:self.preset_save(2))
        self.p3_save.clicked.connect(lambda:self.preset_save(3))
        self.p4_save.clicked.connect(lambda:self.preset_save(4))

        self.p1_load.clicked.connect(lambda:self.preset_load(1))
        self.p2_load.clicked.connect(lambda:self.preset_load(2))
        self.p3_load.clicked.connect(lambda:self.preset_load(3))
        self.p4_load.clicked.connect(lambda:self.preset_load(4))

        # style sheet
        self.power_button.setStyleSheet(
            '''
            QPushButton{border:0px; image:url(./pic/power.png); background-color: rgb(3, 86, 161);}
            QPushButton:pressed{border:2px; background-color: rgb(3, 86, 130);}
            '''
        )

        self.setting_button.setStyleSheet(
            '''
            QPushButton{border:0px; background-color: rgb(3, 86, 161); color: rgb(255, 255, 255);border-width: 2px; border-radius: 10px; }
            QPushButton:pressed{border:0px; background-color: rgb(3, 86, 130);}
            '''
        )
        self.graph_button.setStyleSheet(
            '''
            QPushButton{border:0px; background-color: rgb(3, 86, 161); color: rgb(255, 255, 255);border-width: 2px; border-radius: 10px; }
            QPushButton:pressed{border:0px; background-color: rgb(3, 86, 130);}
            '''
        )
        self.vaccum_label.setPixmap(QPixmap("./pic/nopush.png"))

        self.info_button.setStyleSheet(
            '''
            QPushButton{border:0px; background-color: rgb(3, 86, 161); color: rgb(255, 255, 255);border-width: 2px; border-radius: 10px; }
            QPushButton:pressed{border:0px; background-color: rgb(3, 86, 130);}
            '''
        )

        self.run_button.setStyleSheet(
            '''
            QPushButton{image:url(./pic/run.png); border:0px; }
            QPushButton:pressed{image:url(./pic/c_run.png); border:0px; }
            '''
        )
        self.run_button_2.setStyleSheet(
            '''
            QPushButton{image:url(./pic/run.png); border:0px; }
            QPushButton:pressed{image:url(./pic/c_run.png); border:0px; }
            '''
        )

        self.set_button.setStyleSheet(
            '''
            QPushButton{image:url(./pic/check.png); border:0px; }
            QPushButton:pressed{image:url(./pic/c_check.png); border:0px;}
            '''
        )
        self.set_button_2.setStyleSheet(
            '''
            QPushButton{image:url(./pic/check.png); border:0px; }
            QPushButton:pressed{image:url(./pic/c_check.png); border:0px;}
            '''
        )

        self.stop_button.setStyleSheet(
            '''
            QPushButton{image:url(./pic/stop.png); border:0px;}
            QPushButton:pressed{image:url(./pic/c_stop.png); border:0px;}
            '''
        )
        self.stop_button_2.setStyleSheet(
            '''
            QPushButton{image:url(./pic/stop.png); border:0px;}
            QPushButton:pressed{image:url(./pic/c_stop.png); border:0px;}
            '''
        )

        self.reset_button.setStyleSheet(
            '''
            QPushButton{image:url(./pic/empty.png); border:0px;background-color: rgba(255, 255, 255, 0); }
            QPushButton:pressed{image:url(./pic/c_empty.png); border:0px;}
            '''
        )
        self.p1_save.setStyleSheet(
            '''
            QPushButton{color: rgb(0, 0, 0); border-width: 2px; border-radius: 10px;}
            QPushButton:pressed{color: rgb(3, 86, 161);background-color: rgba(3, 86, 161, 30);border-width: 2px; border-radius: 10px; }
            '''
        )
        self.p1_load.setStyleSheet(
            '''
            QPushButton{color: rgb(0, 0, 0); border-width: 2px; border-radius: 10px;}
            QPushButton:pressed{color: rgb(161, 86, 3);background-color: rgba(161, 86, 3, 30);border-width: 2px; border-radius: 10px; }
            '''
        )
        self.p2_save.setStyleSheet(
            '''
            QPushButton{border:0px; color: rgb(0, 0, 0); border-width: 2px; border-radius: 10px;}
            QPushButton:pressed{color: rgb(3, 86, 161);background-color: rgba(3, 86, 161, 30);border-width: 2px; border-radius: 10px; }
            '''
        )
        self.p2_load.setStyleSheet(
            '''
            QPushButton{border:0px; color: rgb(0, 0, 0); border-width: 2px; border-radius: 10px;}
            QPushButton:pressed{color: rgb(161, 86, 3);background-color: rgba(161, 86, 3, 30);border-width: 2px; border-radius: 10px; }
            '''
        )
    
        self.p3_save.setStyleSheet(
            '''
            QPushButton{border:0px; color: rgb(0, 0, 0); border-width: 2px; border-radius: 10px;}
            QPushButton:pressed{color: rgb(3, 86, 161);background-color: rgba(3, 86, 161, 30);border-width: 2px; border-radius: 10px; }
            '''
        )
        self.p3_load.setStyleSheet(
            '''
            QPushButton{border:0px; color: rgb(0, 0, 0); border-width: 2px; border-radius: 10px;}
            QPushButton:pressed{color: rgb(161, 86, 3);background-color: rgba(161, 86, 3, 30);border-width: 2px; border-radius: 10px; }
            '''
        )
        self.p4_save.setStyleSheet(
            '''
            QPushButton{border:0px; color: rgb(0, 0, 0); border-width: 2px; border-radius: 10px;}
            QPushButton:pressed{color: rgb(3, 86, 161);background-color: rgba(3, 86, 161, 30);border-width: 2px; border-radius: 10px; }
            '''
        )
        self.p4_load.setStyleSheet(
            '''
            QPushButton{border:0px; color: rgb(0, 0, 0); border-width: 2px; border-radius: 10px;}
            QPushButton:pressed{color: rgb(161, 86, 3);background-color: rgba(161, 86, 3, 30);border-width: 2px; border-radius: 10px; }
            '''
        )
        self.w1_num.setStyleSheet(
            '''
            QPushButton{image:url(./pic/text.png); border:0px; }
            QPushButton:pressed{image:url(./pic/c_text.png); border:0px;}
            '''
        )
        self.w2_num.setStyleSheet(
            '''
            QPushButton{image:url(./pic/text.png); border:0px; }
            QPushButton:pressed{image:url(./pic/c_text.png); border:0px;}
            '''
        )
        self.w3_num.setStyleSheet(
            '''
            QPushButton{image:url(./pic/text.png); border:0px; }
            QPushButton:pressed{image:url(./pic/c_text.png); border:0px;}
            '''
        )
        self.w4_num.setStyleSheet(
            '''
            QPushButton{image:url(./pic/text.png); border:0px; }
            QPushButton:pressed{image:url(./pic/c_text.png); border:0px;}
            '''
        )
        self.w5_num.setStyleSheet(
            '''
            QPushButton{image:url(./pic/text.png); border:0px; }
            QPushButton:pressed{image:url(./pic/c_text.png); border:0px;}
            '''
        )
        self.w6_num.setStyleSheet(
            '''
            QPushButton{image:url(./pic/text.png); border:0px; }
            QPushButton:pressed{image:url(./pic/c_text.png); border:0px;}
            '''
        )
        self.w7_num.setStyleSheet(
            '''
            QPushButton{image:url(./pic/text.png); border:0px; }
            QPushButton:pressed{image:url(./pic/c_text.png); border:0px;}
            '''
        )
        self.w8_num.setStyleSheet(
            '''
            QPushButton{image:url(./pic/text.png); border:0px; }
            QPushButton:pressed{image:url(./pic/c_text.png); border:0px;}
            ''')
        self.w9_num.setStyleSheet(
            '''
            QPushButton{image:url(./pic/text.png); border:0px; }
            QPushButton:pressed{image:url(./pic/c_text.png); border:0px;}
            ''')
        self.w10_num.setStyleSheet(
            '''
            QPushButton{image:url(./pic/text.png); border:0px; }
            QPushButton:pressed{image:url(./pic/c_text.png); border:0px;}
            ''')

        self.t1_num.setStyleSheet(
            '''
            QPushButton{image:url(./pic/text.png); border:0px; }
            QPushButton:pressed{image:url(./pic/c_text.png); border:0px;}
            ''')
        self.t2_num.setStyleSheet(
            '''
            QPushButton{image:url(./pic/text.png); border:0px; }
            QPushButton:pressed{image:url(./pic/c_text.png); border:0px;}
            ''')
        self.t3_num.setStyleSheet(
            '''
            QPushButton{image:url(./pic/text.png); border:0px; }
            QPushButton:pressed{image:url(./pic/c_text.png); border:0px;}
            ''')
        self.t4_num.setStyleSheet(
            '''
            QPushButton{image:url(./pic/text.png); border:0px; }
            QPushButton:pressed{image:url(./pic/c_text.png); border:0px;}
            ''')
        self.t5_num.setStyleSheet(
            '''
            QPushButton{image:url(./pic/text.png); border:0px; }
            QPushButton:pressed{image:url(./pic/c_text.png); border:0px;}
            ''')
        self.t6_num.setStyleSheet(
            '''
            QPushButton{image:url(./pic/text.png); border:0px; }
            QPushButton:pressed{image:url(./pic/c_text.png); border:0px;}
            ''')
        self.t7_num.setStyleSheet(
            '''
            QPushButton{image:url(./pic/text.png); border:0px; }
            QPushButton:pressed{image:url(./pic/c_text.png); border:0px;}
            ''')
        self.t8_num.setStyleSheet(
            '''
            QPushButton{image:url(./pic/text.png); border:0px; }
            QPushButton:pressed{image:url(./pic/c_text.png); border:0px;}
            ''')
        self.t9_num.setStyleSheet(
            '''
            QPushButton{image:url(./pic/text.png); border:0px; }
            QPushButton:pressed{image:url(./pic/c_text.png); border:0px;}
            ''')
        self.t10_num.setStyleSheet(
            '''
            QPushButton{image:url(./pic/text.png); border:0px; }
            QPushButton:pressed{image:url(./pic/c_text.png); border:0px;}
            ''')

        self.r1_num.setStyleSheet(
            '''
            QPushButton{image:url(./pic/text.png); border:0px; }
            QPushButton:pressed{image:url(./pic/c_text.png); border:0px;}
            ''')
        self.r2_num.setStyleSheet(
            '''
            QPushButton{image:url(./pic/text.png); border:0px; }
            QPushButton:pressed{image:url(./pic/c_text.png); border:0px;}
            ''')
        self.r3_num.setStyleSheet(
            '''
            QPushButton{image:url(./pic/text.png); border:0px; }
            QPushButton:pressed{image:url(./pic/c_text.png); border:0px;}
            ''')
        self.r4_num.setStyleSheet(
            '''
            QPushButton{image:url(./pic/text.png); border:0px; }
            QPushButton:pressed{image:url(./pic/c_text.png); border:0px;}
            ''')
        self.r5_num.setStyleSheet(
            '''
            QPushButton{image:url(./pic/text.png); border:0px; }
            QPushButton:pressed{image:url(./pic/c_text.png); border:0px;}
            ''')
        self.r6_num.setStyleSheet(
            '''
            QPushButton{image:url(./pic/text.png); border:0px; }
            QPushButton:pressed{image:url(./pic/c_text.png); border:0px;}
            ''')
        self.r7_num.setStyleSheet(
            '''
            QPushButton{image:url(./pic/text.png); border:0px; }
            QPushButton:pressed{image:url(./pic/c_text.png); border:0px;}
            ''')
        self.r8_num.setStyleSheet(
            '''
            QPushButton{image:url(./pic/text.png); border:0px; }
            QPushButton:pressed{image:url(./pic/c_text.png); border:0px;}
            ''')
        self.r9_num.setStyleSheet(
            '''
            QPushButton{image:url(./pic/text.png); border:0px; }
            QPushButton:pressed{image:url(./pic/c_text.png); border:0px;}
            ''')
        self.r10_num.setStyleSheet(
            '''
            QPushButton{image:url(./pic/text.png); border:0px; }
            QPushButton:pressed{image:url(./pic/c_text.png); border:0px;}
            ''')
        # Tera Logo Image
        self.logo_label.setPixmap(QPixmap("./pic/tera.png"))
    
app = QApplication(sys.argv)
myWindow = gui() 
myWindow.showFullScreen() # FullScreen Mode
sys.exit(app.exec_())
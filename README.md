# Make Spincoater by Raspberrypi, Arduino 

## 1. Outline

I was internship in Teraleader by 2021.03 ~ 2021.12.

This is my first Python Project in Teraleader (http://teraleader.co.kr).


## 2. Goal

Spin coater : https://en.wikipedia.org/wiki/Spin_coating

Goal RPM : 9000 (with accuracy 99%)

## 3. Component

Raspberry Pi (Raspberry Pi 3 Model B)
Raspberry Pi Touch Display (7 inch)
Arudino nano
Stepper Motor IHSV57 (https://www.jmc-motor.com/product/901.html)
Pulley Gear Ratio (1 : 3 = motor rpm : real rpm)

## 4. WorkFlow


## 5. Explanation

### Used Library

PyQt5, pyqtgraph, Pyserial

### X Values

x1 ~ x10 are the list, including W,R,T values.

W : target RPM

R : target Time

T : hold time

### Signal Rules

update_value is the list, including [run_status , vaccum , w value , r value , t value, ....]

run_status : 0 (Not working), 1 (Working), 2 (Error)

vaccum_status : 0 (Not working), 1 (Working)

### Function Explanation

plot(self, time, rpm): # function for drawed main graph 

arduino(self): # function for data transport to arduino

setvalue(self): # if check button clicked setvalue function operate

preset_save(self,num): # preset save function

preset_load(self,num): # preset load function

calc(self): # function for draw main graph

copy_calc(self): # function for following graph

widget(self, button): # function for keypad widget


## 6. Points to add

Qthread

too many useless value

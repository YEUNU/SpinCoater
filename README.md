# Python PyQt를 이용한 GUI 프로그램 제작

1. 개요

(주)테라리더에서 진행한 첫번째 PyQt프로젝트

나의 첫 PyQt프로그램


2. 목표

파이썬과 아두이노간의 통신을 통해 파이썬 GUI로 아두이노를 활용한다.

아두이노가 아두이노에 연결된 하드웨어에 명령을 처리하며 원하는 결과를 가져온다.


3. 사용한 라이브러리

PyQt5, pyqtgraph, Pyserial


4. 변수설명


vaccum = 0 # 0 : vaccum off, 1 : vaccum on 

check_click = 0 # check vaccum button is clicked

xlist = [] # x axis list for drawed graph

ylist = [] # y axis list for drawed graph

copy_ylist =[] # y axis list for following graph 

copy_xlist = [] # x axis list for following graph 

copy_count = 0 # count for following graph

run_status = 0 # 0 : not running motor 1 : running motor 2 : user set rpm over 9000 

update_value = [0] # list for transport to arduino [run_status , vaccum , w value , r value , t value,....]

preset1 = [] # list for preset1

preset2 = [] # list for preset2

preset3 = [] # list for preset3

preset4 = [] # list for preset4

x1 = [] # list for w1,r1,t1 [w1,r1,t1]

x2 = [] # list for w2,r2,t2 [w2,r2,t2]

x3 = [] # list for w3,r3,t3 [w3,r3,t3]

x4 = [] # list for w4,r4,t4 [w4,r4,t4]

x5 = [] # list for w5,r5,t5 [w5,r5,t5]

x6 = [] # list for w6,r6,t6 [w6,r6,t6]

x7 = [] # list for w7,r7,t7 [w7,r7,t7]

x8 = [] # list for w8,r8,t8 [w8,r8,t8]

x9 = [] # list for w9,r9,t9 [w9,r9,t9]

x10 = [] # list for w10,r10,t10 [w10,r10,t10]

mx=[1,1,1,1,1,1,1,1,1,1] # check list for missed x value


5. 함수설명

plot(self, time, rpm): # function for drawed main graph 

arduino(self): # function for data transport to arduino

setvalue(self): # if check button clicked setvalue function operate

preset_save(self,num): # preset save function

preset_load(self,num): # preset load function

calc(self): # function for draw main graph

copy_calc(self): # function for following graph

widget(self, button): # function for keypad widget


6. 아쉬운점

아직 미숙한 프로그래밍으로 인한 더러운 코드 관리

Qthread를 사용하여 더욱 효과적인 프로그래밍이 부족했다.

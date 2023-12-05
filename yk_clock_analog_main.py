import tkinter
import time
from datetime import datetime as dt
import platform
import os
import sys
import math

print("finish reading packages")

os.chdir(os.path.abspath(os.path.dirname(__file__)))
MachineOS = platform.system()
print("OS:",MachineOS)

def windowdestroy():
    global app_0
    app_0.after_cancel(show_time_censec)
    app_0.after_cancel(show_time_second)
    #app_0.after_cancel(show_time_minute)
    #app_0.after_cancel(show_time_hour)
    #app_0.destroy()
    print("Windowdestroy")
    exit()

def gettime():
    hour = dt.now().hour
    minute = dt.now().minute
    second = dt.now().second
    censec = dt.now().microsecond // 10000
    return [hour,minute,second,censec]

def calangle(timearray : list):
    #timearray : [hour,minute,second,censec]
    angle_h = (timearray[0] % 12) * 30 + timearray[1] * 0.5
    angle_m = timearray[1] * 6
    angle_s = timearray[2] * 6 #+ timearray[3] * 0.06
    angle_c = timearray[3] * 3.6
    outlist = [angle_h,angle_m,angle_s,angle_c]
    return outlist

def calcoord(offset : list,degree : float,outradius : float,inradius = 0.0):
    angle_radian = degree * math.pi / 180
    coord0 = [inradius * math.sin(angle_radian) + offset[0],-inradius * math.cos(angle_radian) + offset[1]]
    coord1 = [outradius * math.sin(angle_radian) + offset[0],-outradius * math.cos(angle_radian) + offset[1]]
    outcoord = list(map(int,coord0 + coord1))
    return outcoord

timearray = gettime()
fpscount = 0
flag0 = True
maxfps = 120 #1 ~ 1000
mininterval = int(1000/maxfps)
censecswitch = True
secondswitch = True
soundswitch = False

if sys.argv[-1].isdecimal():
    windowheight = int(sys.argv[-1])
else:
    windowheight = 400

zoomrate = windowheight / 360
windowwidth = windowheight #int(1660 * zoomrate)

fontname = ['system','Yu Gothic','Terminal'][1]
defaultfontsize = 10

app_0 = tkinter.Tk()
app_0.title("clock_yk")# アプリのタイトル
app_0.geometry(str(windowwidth) + "x" + str(windowheight))# アプリ画面のサイズ

canvas_mainback = tkinter.Canvas(app_0,width = windowwidth, height = windowheight,bg = "#ffffff")
canvas_mainback.place(x = 0,y = 0)

R0 = 0
R1 = windowheight * 0.60 * 0.5
R2 = windowheight * 0.80 * 0.5
R3 = windowheight * 0.85 * 0.5
R4 = windowheight * 0.90 * 0.5
R5 = windowheight * 0.95 * 0.5
R6 = windowheight * 1.00 * 0.5
coordoffset = [windowheight * 0.5] * 2

#目盛り描写
id_measures = []
for mind in range(60):
    if mind % 5 == 0:
        R_in = R3
        linewidth = 3
        tag = "measurebold"
    else:
        R_in = R4
        linewidth = 1
        tag = "measuresharp"
    coord = calcoord(coordoffset,mind * 6,R6,R_in)
    id_measures.append(canvas_mainback.create_line(coord,width=linewidth,tags=tag))

#短針・長針・秒針描写
id_hpin = canvas_mainback.create_line(calcoord(coordoffset,90,R1,R0),width=8,fill="#666666")
id_mpin = canvas_mainback.create_line(calcoord(coordoffset,0,R2,R0),width=4,fill="#333333")
id_spin = canvas_mainback.create_line(calcoord(coordoffset,0,R5,R0),width=2,fill="#000000")

beforesec = 0
def timerenew_second():
    global app_0
    global show_time_second
    global flag0
    global fpscount
    global beforesec
    func_interval = max(5,mininterval)
    show_time_second = app_0.after(
        func_interval,
        timerenew_second
    )
    
    timearray = gettime()
    angles = calangle(timearray)
    canvas_mainback.coords(id_hpin,calcoord(coordoffset,angles[0],R1,R0))
    canvas_mainback.coords(id_mpin,calcoord(coordoffset,angles[1],R2,R0))
    if secondswitch:
        canvas_mainback.coords(id_spin,calcoord(coordoffset,angles[2],R5,R0))
    else:
        canvas_mainback.coords(id_spin,calcoord(coordoffset,angles[2],R0,R0))
    flag0 = bool(beforesec == dt.now().second % 10)
    fpscount += 1
    beforesec = dt.now().second % 10
timerenew_second()

def timerenew_censec():
    T0 = time.time()
    global app_0
    global show_time_censec
    global fpscount
    global flag0
    func_interval = max(1,mininterval)
    show_time_censec = app_0.after(
        func_interval,
        timerenew_censec
    )
    
    if flag0:
        fpscount += 1
    else:
        fpscount = 0
        flag0 = True
timerenew_censec()

def switchchange_second(dummy = False):
    global secondswitch
    global app_0
    secondswitch = not(secondswitch)
canvas_mainback.bind('<Button-1>',switchchange_second)

app_0.protocol("WM_DELETE_WINDOW", windowdestroy)
print("Window ready")
app_0.mainloop()
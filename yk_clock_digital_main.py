import tkinter
from tkinter import StringVar, font
import tkinter.ttk as ttk
import time
import datetime
from datetime import datetime as dt
import platform
import os
import sys
import subprocess as sp



print("finish reading packages")

os.chdir(os.path.abspath(os.path.dirname(__file__)))
MachineOS = platform.system()
print("OS:",MachineOS)

def windowdestroy():
    global app_0
    #app_0.after_cancel(showarrow)
    app_0.after_cancel(show_time_censec)
    app_0.after_cancel(show_time_second)
    app_0.after_cancel(show_time_minute)
    app_0.after_cancel(show_time_hour)
    app_0.destroy()
    print("Windowdestroy")
    exit()

def gettime():
    hour = datetime.datetime.now().hour
    minute = datetime.datetime.now().minute
    second = datetime.datetime.now().second
    censec = datetime.datetime.now().microsecond // 10000
    return [hour,minute,second,censec]

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
    windowheight = 240

zoomrate = windowheight / 360
windowwidth = int(1660 * zoomrate)
Leftmargin = int(50 * zoomrate)
Topmargin_num = int(-20 * zoomrate)
Topmargin_colon = int(-50 * zoomrate)
#numimg:150x360
interval_num = int(150 * zoomrate)
#colonimg:120x360
interval_colon = int(120 * zoomrate)

def cal_interval(colon,num):
    return Leftmargin + interval_colon * colon + interval_num * num


fontname = ['system','Yu Gothic','Terminal'][1]
defaultfontsize = 10

app_0 = tkinter.Tk()
app_0.geometry(
    #"1660x360" # アプリ画面のサイズ
    str(windowwidth) + "x" + str(windowheight)
)

app_0.title("clock_mm" )# アプリのタイトル
imgheight = 720
imgzoomrate = windowheight / imgheight
imgfolderpath = "ImgFiles/" + str(imgheight) + "p"#os.path.abspath("ImgFiles/" + str(imgheight) + "p")
tmpimgfolderpath = "ImgFiles/tmp"#os.path.abspath("ImgFiles/tmp")
if not(os.path.isdir(tmpimgfolderpath)):
    os.mkdir(tmpimgfolderpath)
adjustedimgobjs = []

print("loading and dealing with image files...")

prclist = []
for ind0 in range(10):
    inimgpath = imgfolderpath + "/" + str(imgheight) + "p_" + str(ind0) + ".png"
    outimgpath = tmpimgfolderpath + "/tmp_" + str(ind0) + ".png"
    com = ["python3","imgzoom.py","-i",inimgpath,"-o",outimgpath,"-h",str(windowheight)]
    prclist.append(sp.Popen(com))
incolonimgpath = imgfolderpath + "/" + str(imgheight) + "p_colon.png"
outcolonimgpath = tmpimgfolderpath + "/tmp_colon.png"
com_colon = ["python3","imgzoom.py","-i",incolonimgpath,"-o",outcolonimgpath,"-h",str(windowheight)]
inwhiteimgpath = imgfolderpath + "/" + str(imgheight) + "p_white.png"
outwhiteimgpath = tmpimgfolderpath + "/tmp_white.png"
com_white = ["python3","imgzoom.py","-i",inwhiteimgpath,"-o",outwhiteimgpath,"-h",str(windowheight)]
prclist.append(sp.Popen(com_colon))
prclist.append(sp.Popen(com_white))

for ind1 in range(len(prclist)):
    prclist[ind1].wait()

for ind3 in range(10):
    #adjustedimgobjs += [tkinter.PhotoImage(file = imgfolderpath + "/" + str(imgheight) + "p_" + str(a) + ".png").zoom(int(50 * imgzoomrate)).subsample(50)]
    readimgfile = tmpimgfolderpath + "/tmp_" + str(ind3) + ".png"
    adjustedimgobjs += [tkinter.PhotoImage(file = readimgfile)]
    print(readimgfile)

#colon_adjustedimgobj = tkinter.PhotoImage(file = imgfolderpath + "/" + str(imgheight) + "p_colon.png").zoom(int(50 * imgzoomrate)).subsample(50)
colon_adjustedimgobj = tkinter.PhotoImage(file = outcolonimgpath)
print(outcolonimgpath)

#white_adjustedimgobj = tkinter.PhotoImage(file = imgfolderpath + "/" + str(imgheight) + "p_white.png").zoom(int(50 * imgzoomrate)).subsample(50)
white_adjustedimgobj = tkinter.PhotoImage(file = outwhiteimgpath)
print(outwhiteimgpath)

print("finish loading and dealing with image files")

canvas_mainback = tkinter.Canvas(
    app_0, # キャンバスの作成先アプリ
    width = windowwidth, # キャンバスの横サイズ
    height = windowheight, # キャンバスの縦サイズ
    bg = "#ffffff" # キャンバスの色
)

# キャンバスの配置
canvas_mainback.place(
    x = 0, # キャンバスの配置先座標x
    y = 0 # キャンバスの配置先座標y
)
"""
canvas_second = tkinter.Canvas(
    app_0, # キャンバスの作成先アプリ
    width = cal_interval(2,6) - cal_interval(2,4), # キャンバスの横サイズ
    height = windowheight, # キャンバスの縦サイズ
    bg = "#ffffff" # キャンバスの色 ffeeee
)

# キャンバスの配置
canvas_second.place(
    x = cal_interval(2,4), # キャンバスの配置先座標x
    y = 0 # キャンバスの配置先座標y
)

canvas_censec = tkinter.Canvas(
    app_0, # キャンバスの作成先アプリ
    width = cal_interval(3,8) - cal_interval(3,6), # キャンバスの横サイズ
    height = windowheight, # キャンバスの縦サイズ
    bg = "#eeeeee" # キャンバスの色 eeffee
)

# キャンバスの配置
canvas_censec.place(
    x = cal_interval(3,6), # キャンバスの配置先座標x
    y = 0 # キャンバスの配置先座標y
)
"""
label_dummy = tkinter.Label(
    app_0,
    font = (fontname, defaultfontsize),
    text = "0",
    foreground = '#ffffff',
    background = "#ffffff"
)
label_dummy.place(
    x = 0,
    y = 0
)

truefontsize = defaultfontsize
label_hour_x0 = tkinter.Label(
    app_0,
    font = (fontname, truefontsize),
    image = adjustedimgobjs[timearray[0] // 10],
    foreground = '#000000',
    background = "#ffffff"
)
label_hour_x0.place(
    x = cal_interval(0,0),
    y = Topmargin_num
)

label_hour_0x = tkinter.Label(
    app_0,
    font = (fontname, truefontsize),
    image = adjustedimgobjs[timearray[0] % 10],
    foreground = '#000000',
    background = "#ffffff"
)
label_hour_0x.place(
    x = cal_interval(0,1),
    y = Topmargin_num
)

label_minute_x0 = tkinter.Label(
    app_0,
    font = (fontname, truefontsize),
    image = adjustedimgobjs[timearray[1] // 10],
    foreground = '#000000',
    background = "#ffffff"
)
label_minute_x0.place(
    x = cal_interval(1,2),
    y = Topmargin_num
)

label_minute_0x = tkinter.Label(
    app_0,
    font = (fontname, truefontsize),
    image = adjustedimgobjs[timearray[1] % 10],
    foreground = '#000000',
    background = "#ffffff"
)
label_minute_0x.place(
    x = cal_interval(1,3),
    y = Topmargin_num
)

label_second_x0 = tkinter.Label(
    app_0,
    font = (fontname, truefontsize),
    image = adjustedimgobjs[timearray[2] // 10],
    foreground = '#000000',
    background = "#ffffff"
)
label_second_x0.place(
    x = cal_interval(2,4),
    y = Topmargin_num
)

label_second_0x = tkinter.Label(
    app_0,
    font = (fontname, truefontsize),
    image = adjustedimgobjs[timearray[2] % 10],
    foreground = '#000000',
    background = "#ffffff"
)
label_second_0x.place(
    x = cal_interval(2,5),
    y = Topmargin_num
)

label_censec_x0 = tkinter.Label(
    app_0,
    font = (fontname, truefontsize),
    image = adjustedimgobjs[timearray[3] // 10],
    foreground = '#000000',
    background = "#ffffff"
)
label_censec_x0.place(
    x = cal_interval(3,6),
    y = Topmargin_num
)

label_censec_0x = tkinter.Label(
    app_0,
    font = (fontname, truefontsize),
    image = adjustedimgobjs[timearray[3] % 10],
    foreground = '#000000',
    background = "#ffffff"
)
label_censec_0x.place(
    x = cal_interval(3,7),
    y = Topmargin_num
)

label_colon0 = tkinter.Label(
    app_0,
    font = (fontname, truefontsize),
    image=colon_adjustedimgobj,
    foreground = '#000000',
    background = "#ffffff"
)
label_colon0.place(
    x = cal_interval(0,2),
    y = Topmargin_colon
)

label_colon1 = tkinter.Label(
    app_0,
    font = (fontname, truefontsize),
    image=colon_adjustedimgobj,
    foreground = '#000000',
    background = "#ffffff"
)
label_colon1.place(
    x = cal_interval(1,4),
    y = Topmargin_colon
)

label_colon2 = tkinter.Label(
    app_0,
    font = (fontname, truefontsize),
    image=colon_adjustedimgobj,
    foreground = '#000000',
    background = "#ffffff"
)
label_colon2.place(
    x = cal_interval(2,6),
    y = Topmargin_colon
)

label_fpsmonitor = tkinter.Label(
    app_0,
    font = (fontname, int(truefontsize * zoomrate)),
    text = str(fpscount),
    foreground = '#000000',
    background = "#ffffff"
)
label_fpsmonitor.place(
    x = 0,
    y = windowheight
    #y = 0
)

def timerenew_hour():
    global app_0
    global show_time_hour
    global fpscount
    if dt.now().minute >= 54:
        func_interval = max(5,mininterval)
    else:
        func_interval = 1000 * 300
    show_time_hour = app_0.after(
        func_interval,
        timerenew_hour
    )
    label_hour_x0["image"] = adjustedimgobjs[dt.now().hour // 10],
    label_hour_0x["image"] = adjustedimgobjs[dt.now().hour % 10],
    fpscount += 1
timerenew_hour()

def timerenew_minute():
    global app_0
    global show_time_minute
    global fpscount
    if dt.now().second >= 54:
        func_interval = max(5,mininterval)
    else:
        func_interval = 1000 * 5
    show_time_minute = app_0.after(
        func_interval,
        timerenew_minute
    )
    label_minute_x0["image"] = adjustedimgobjs[dt.now().minute // 10]
    label_minute_0x["image"] = adjustedimgobjs[dt.now().minute % 10]
    fpscount += 1
timerenew_minute()
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
    if secondswitch:
        label_second_x0["image"] = adjustedimgobjs[dt.now().second // 10]
        label_second_0x["image"] = adjustedimgobjs[dt.now().second % 10]
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
    if censecswitch and secondswitch:
        label_censec_x0["image"] = adjustedimgobjs[dt.now().microsecond // 100000]
        label_censec_0x["image"] = adjustedimgobjs[(dt.now().microsecond // 10000) % 10]
        
    else:
        pass
    if flag0:
        fpscount += 1
    else:
        label_fpsmonitor["text"] = str(fpscount) + " " + str(time.time() - T0)
        fpscount = 0
        flag0 = True
        if MachineOS == "Windows" and soundswitch:
            
            if dt.now().second > 56:
                sp.Popen(["python","BeepSound500Hz.py"],shell=True)
            elif dt.now().second % 10 == 0:
                sp.Popen(["python","BeepSound1000Hz.py"],shell=True)
            else:
                sp.Popen(["python","BeepSound2000Hz.py"],shell=True)


timerenew_censec()

def switchchange_second(dummy = False):
    global secondswitch
    global label_second_x0
    global label_second_0x
    global label_censec_x0
    global label_censec_0x
    global label_colon1
    global label_colon2
    global button_change_second
    secondswitch = not(secondswitch)
    if secondswitch:
        label_second_x0["foreground"] = label_second_0x["foreground"] = label_colon1["foreground"] = "#000000"
        label_colon1["image"] = colon_adjustedimgobj
        #button_change_second["text"] = "非表示"
        if censecswitch:
            label_censec_x0["foreground"] = label_censec_0x["foreground"] = label_colon2["foreground"] = "#000000"
            label_colon2["image"] = colon_adjustedimgobj
    else:
        #button_change_second["text"] = "表示"
        label_second_x0["foreground"] = label_second_0x["foreground"] = label_colon1["foreground"] = "#ffffff"
        label_second_x0["image"] = label_second_0x["image"] = label_colon1["image"] = white_adjustedimgobj
        label_censec_x0["foreground"] = label_censec_0x["foreground"] = label_colon2["foreground"] = "#ffffff"
        label_censec_x0["image"] = label_censec_0x["image"] = label_colon2["image"] = white_adjustedimgobj
        
def switchchange_censec(dummy = False):
    global censecswitch
    global label_censec_x0
    global label_censec_0x
    global label_colon2
    global button_change_censec
    censecswitch = not(censecswitch)
    if censecswitch:
        label_censec_x0["foreground"] = label_censec_0x["foreground"] = label_colon2["foreground"] = "#000000"
        #button_change_censec["text"] = "非表示"
        if secondswitch:
            label_colon2["image"] = colon_adjustedimgobj
    else:
        label_censec_x0["foreground"] = label_censec_0x["foreground"] = label_colon2["foreground"] = "#ffffff"
        label_censec_x0["image"] = label_censec_0x["image"] = label_colon2["image"] = white_adjustedimgobj
        #button_change_censec["text"] = "表示"

"""
button_change_second = tkinter.Button(
    app_0, # ボタンの作成先アプリ
    text = "非表示", # ボタンに表示するテキスト
    font = (fontname,8),
    command = switchchange_second, # ボタンクリック時に実行する関数
    height = 1

)
# ボタンの配置
button_change_second.place(
    x = cal_interval(2,4), # ボタンの配置先座標x
    y = 0, # ボタンの配置先座標y
)
"""

label_second_x0.bind('<Button-1>',switchchange_second)
label_second_0x.bind('<Button-1>',switchchange_second)
label_colon1.bind('<Button-1>',switchchange_second)
#canvas_second.bind('<Button-1>',switchchange_second)
"""
button_change_censec = tkinter.Button(
    app_0, # ボタンの作成先アプリ
    text = "非表示", # ボタンに表示するテキスト
    font = (fontname,8),
    command = switchchange_censec, # ボタンクリック時に実行する関数
    height = 1

)

# ボタンの配置
button_change_censec.place(
    x = cal_interval(3,6), # ボタンの配置先座標x
    y = 0, # ボタンの配置先座標y
)
"""
label_censec_x0.bind('<Button-1>',switchchange_censec)
label_censec_0x.bind('<Button-1>',switchchange_censec)
label_colon2.bind('<Button-1>',switchchange_censec)
#canvas_censec.bind('<Button-1>',switchchange_censec)


def soundswitchcange():
    global soundswitch
    global button_change_sound
    soundswitch = not(soundswitch)
    if soundswitch:
        button_change_sound["text"] = "音無"
    else:
        button_change_sound["text"] = "音有"

button_change_sound = tkinter.Button(
    app_0, # ボタンの作成先アプリ
    text = "音有", # ボタンに表示するテキスト
    font = (fontname,8),
    command = soundswitchcange, # ボタンクリック時に実行する関数
    height = 1

)
# ボタンの配置
button_change_sound.place(
    x = cal_interval(1,2), # ボタンの配置先座標x
    y = windowheight * 2, # ボタンの配置先座標y
)


app_0.protocol("WM_DELETE_WINDOW", windowdestroy)
print("Window ready")
app_0.mainloop()
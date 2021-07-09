#!/usr/bin/python
import os
from os import close, system, name
import time
import tkinter as tk
from tkinter import *
from ctypes import windll
from pyglet import *
from pyglet.gl import *
from tkinter.ttk import *
import time
import random
from PyQt5 import QtWidgets, QtCore, QtGui
from PIL import ImageTk, Image, ImageDraw
import numpy as np
from PIL import ImageGrab
import cv2
import tkinter.ttk as tkk
import math

# Snip tool script was used from https://github.com/harupy/snipping-tool with small changes made by myself
class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        global snipRoot
        super().__init__()
        snipRoot = tk.Tk()
        screen_width = snipRoot.winfo_screenwidth()
        screen_height = snipRoot.winfo_screenheight()
        self.setGeometry(0, 0, screen_width, screen_height)
        self.setWindowTitle(' ')
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.setWindowOpacity(0.3)
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.CrossCursor)
        )
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        print('Capture the screen...')
        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor('black'), 3))
        qp.setBrush(QtGui.QColor(128, 128, 255, 128))
        qp.drawRect(QtCore.QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.close()

        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())

        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        img.save('capture.png')
        img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)

        snipRoot.destroy()

#region Functions

# Closes the menu
def contract():
    global count
    global size
    global openMenu

    if count <= 64 and count > 2 and openMenu == True:
        size -= 2
        leftFrame.config(width=size)
        count -= 1
        root.after(10, contract)
        
    elif count == 2:
        openMenu = False
        menuText.config(text="")
        homeText.config(text="")  
        passGenText.config(text="")  
        passVaultText.config(text="")  
        TypingText.config(text="")  
        cameraText.config(text="")  

# Opens the menu
def expand():
    global count
    global size
    global openMenu

    if openMenu == True:
        contract()

    if openMenu == False:
        if count < 64:    
            size += 2
            leftFrame.config(width=size)
            count += 1
            root.after(10, expand)  

            menuText.config(text="Menu")       
            homeText.config(text="Home")       
            passGenText.config(text="Password Generator")       
            passVaultText.config(text="Password Vault")       
            TypingText.config(text="Typing Test")       
            cameraText.config(text="Camera")       

        elif count == 64:
            openMenu = True

# Saves the click position
def save_last_click_pos(event):
    global lastClickX, lastClickY
    lastClickX = event.x
    lastClickY = event.y

# Allows the user to drag the custom title bar
def dragging(event):
    x, y = event.x - lastClickX + root.winfo_x(), event.y - lastClickY + root.winfo_y()
    root.geometry("+%s+%s" % (x , y))

# Highlights the close button to red
def change_on_hovering(event):
    global close_button
    close_button['bg'] = 'red'

# Returns the original colour back to the button
def return_to_normal_state(event):
   global close_button
   close_button['bg'] = '#1E1E1E'

# Minimise to tray
def minimise():
    root.protocol("WM_DELETE_WINDOW", root.iconify)

# Due to removing the use of overrideredirect, we need to make a function which allows the user to see the program on the windows task bar
def set_appwindow(root):
    hwnd = windll.user32.GetParent(root.winfo_id())
    style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    style = style & ~WS_EX_TOOLWINDOW
    style = style | WS_EX_APPWINDOW
    res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
    # re-assert the new window style
    root.wm_withdraw()
    root.after(10, lambda: root.wm_deiconify())

# Detects key press
def key_pressed(event):
    global imge
    global imgX
    global imgY

    global image1
    global newImage
    global imageCount
    global imgCheck
    global imgCount

    nextPageBtn = tk.Button(root_dir_img, command=load_next_page_img, image=nextIcon, background="#2D2D2D", activebackground="#2D2D2D", borderwidth=0)

    app = QtWidgets.QApplication(sys.argv)
    window = MyWidget()
    app.aboutToQuit.connect(app.deleteLater)
    app.exit(app.exec_())
    if os.path.isfile("capture.png"): 
        image_tk = Image.open("capture.png")
        newImage = tk.PhotoImage(file="capture.png")
        originalImage.append(newImage)
        save_image(exec("%s = %d" % ("cameraImage",imge)))

        image_tk.save("imageFolder\\cameraImage" + str(imageCount) + ".png", "png")

        rezied = image_tk.resize((150, 100), Image.ANTIALIAS)
        new_pic = ImageTk.PhotoImage(rezied)
        image1.configure(image=new_pic)
        images.append(image1)
        imageSlots.append(new_pic)

        file = open('images.txt','a')
        file.write("cameraImage" + str(imageCount) + ".png" + '\n')
        file.close()

        imge += 1
        imgX += 0.239
        imageCount += 1
        imgCheck += 1

        if imgX == 1.096:
            imgX = 0.14
            imgY = 0.6
            if imgCheck == 8:
                imgCount += 1
                make_new_page_img(exec("%s = %d" % ("camFrameP",imgCount)), exec("%s = %d" % ("camLayoutP",imgCount)))
                nextPageBtn.place(relx=0.55, rely=0.91)
                imgX = 0.14
                imgY = 0.2
                imgCheck = 0

        canvas.create_image(20,20, anchor=NW)
    
# Toggles the home panel
def show_home():
    global frameName
    global run_once

    frameWindow.config(text="Home")

    for page in buttons:
        page.place_forget()

    for page in pageAr:
        page.place_forget()
            
    homeFrame.place(relx=0.035, rely=0.109)

    if textLabel.winfo_ismapped() == 0:
        if countDa != None:
            root.after_cancel(countDa)
            secondsText.config(text="")
            run_once = 0

# Toggles the password gen panel
def show_pass_gen():
    global frameName
    global run_once

    frameWindow.config(text="Password Generator")

    for page in buttons:
        page.place_forget()
    
    for page in pageAr:
        page.place_forget()

    passFrame.place(relx=0.035, rely=0.109)

    if textLabel.winfo_ismapped() == 0:
        if countDa != None:
            root.after_cancel(countDa)
            secondsText.config(text="")
            run_once = 0

# Toggles the password vault panel
def show_pass_vault():
    global frameName
    global iPage
    global pageCount
    global run_once

    iPage = 0
    pageCount = 1

    frameWindow.config(text="Password Vault")

    for page in buttons:
        page.place_forget()
    
    for page in pageAr:
        page.place_forget()

    passVaFrame.place(relx=0.035, rely=0.109)

    if textLabel.winfo_ismapped() == 0:
        if countDa != None:
            root.after_cancel(countDa)
            secondsText.config(text="")
            run_once = 0

# Toggles the typing panel
def show_type():
    global frameName

    frameWindow.config(text="Typing Test")

    for page in buttons:
        page.place_forget()
    
    for page in pageAr:
        page.place_forget()

    typeFrame.place(relx=0.035, rely=0.109)
    textLabel.focus_set()

    textLabel.bind("<Key>", type_check)

    generate_words()

# Toggles the camera panel
def show_camera():
    global frameName
    global cPage
    global imgPageCount
    global run_once
    
    cPage = 0
    imgPageCount = 1

    frameWindow.config(text="Camera")

    for page in buttons:
        page.place_forget()
    
    for page in pageAr:
        page.place_forget()

    cameraFrame.place(relx=0.035, rely=0.109)

    if textLabel.winfo_ismapped() == 0:
        if countDa != None:
            root.after_cancel(countDa)
            secondsText.config(text="")
            run_once = 0
            
# Sets the password stength to low
def set_pass_low():
    med.set(0)
    high.set(0)
    
# Sets the password stength to medium
def set_pass_med():
    low.set(0)
    high.set(0)
    
# Sets the password stength to high
def set_pass_high():
    med.set(0)
    low.set(0)
    
# Generates the password
def gen_password():
    
    password = ""
    
    length = var1.get()

    if low.get() == 1:
        for i in range(0, length):
            password = password + random.choice(lowStrengh)
        return password
    elif med.get() == 1:
        for i in range(0, length):
            password = password + random.choice(mediumStrengh)
        return password
    elif high.get() == 1:
        for i in range(0, length):
            password = password + random.choice(highStrengh)
        return password
    else:
        print("Strength is not selected.")

# Calls the generatre password function
def call_gen():
    global pass1

    password1 = gen_password()
    passLabel.config(text=password1)

    pass1 = password1

# Opens the save menu panel
def open_save():
    if pass1 == "":
        print("No password can be saved.")
    else:
        saveFrame.place(relx=0.295, rely=0.3)

# Closes the save menu panel
def close_save():
    saveFrame.place_forget()

# Saves the password to the vault
def save_pass():
    global passY
    global check
    global test

    nextPageBtn = tk.Button(root_dir, command=load_next_page, image=nextIcon, background="#2D2D2D", activebackground="#2D2D2D", borderwidth=0)

    passVault = tk.Entry(root_dir,relief='flat',bd=0,takefocus=0,highlightthickness=0, font=("Louis George Cafe", 10))
    passVault.place(relx=0.11, rely=passY, relheight=0.084, relwidth=0.773)
    passVault.insert('end', siteEnter.get() + " : " + pass1)
    passVault.config(state="readonly", readonlybackground="#232323", fg="white", justify=CENTER)

    saveFrame.place_forget()
    passLabel.config(text="")
    siteEnter.delete(0, "end")

    passY += 0.15

    file = open('passwords.txt','a+')
    file.write(passVault.get() + '\n')
    file.close()

    if passY == 0.8500000000000001 and check == test:
        make_new_page(exec("%s = %d" % ("passVaFrameP",check + 1)), exec("%s = %d" % ("passVaLayoutP",check + 1)))
        nextPageBtn.place(relx=0.55, rely=0.91)
        check += 1
        test += 1

# Creates a new password page once it is complete
def make_new_page(passFrame, pageLayout):
    global root_dir
    global passY
    global page

    page += 1
    passY = 0.1

    passFrame = tk.Frame(root)
    pageLayout = tk.Frame(passFrame, height=430, width=825, bg="#2D2D2D")
    pageLayout.pack()

    pageText = tk.Label(passFrame, text="Page " + str(page), font=("Louis George Cafe", 10), bg="#2D2D2D", fg="white")
    pageText.place(relx=0.465, rely=0.91)

    root_dir = passFrame
    pageAr.append(passFrame)

def make_new_page_img(camFrame, camLayout):
    global root_dir_img
    global passY
    global page

    page += 1
    passY = 0.1

    camFrame = tk.Frame(root)
    camLayout = tk.Frame(camFrame, height=430, width=825, bg="#2D2D2D")
    camLayout.pack()

    pageText = tk.Label(camFrame, text="Page " + str(page), font=("Louis George Cafe", 10), bg="#2D2D2D", fg="white")
    pageText.place(relx=0.465, rely=0.91)

    root_dir_img = camFrame
    pageCam.append(camFrame)

# Loads the saved passwords
def load_pass():
    global passY
    global root_dir
    global test2
    
    page = 1

    file = open('passwords.txt', 'a+')
    file = open('images.txt','a')
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, r'imageFolder')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)
    file = open('passwords.txt', 'r')
    Lines = file.readlines()

    nextPageBtn = tk.Button(root_dir, command=load_next_page, image=nextIcon, background="#2D2D2D", activebackground="#2D2D2D", borderwidth=0)

    count = 0

    pageAr.append(passVaFrame)
    for line in Lines:
        count += 1

        passVault = tk.Entry(root_dir,relief='flat',bd=0,takefocus=0,highlightthickness=0, font=("Louis George Cafe", 10))
        passVault.place(relx=0.11, rely=passY, relheight=0.084, relwidth=0.773)
        passVault.insert('end', line.strip())
        passVault.config(state="readonly", readonlybackground="#232323", fg="white", justify=CENTER)

        passY += 0.15
        if passY == 0.8500000000000001 and page == test2:
            make_new_page(exec("passVaFrameP" + str(check + 1)), exec("passVaLayoutP" + str(check + 1)))
            nextPageBtn.place(relx=0.55, rely=0.91)
            page += 1
            test2 += 1

# Loads the next page for the passwords
def load_next_page():
    global iPage
    global imgPageCount

    previousPageBtn = tk.Button(pageAr[iPage + 1], command=load_previous_page, image=previousIcon, background="#2D2D2D", activebackground="#2D2D2D", borderwidth=0)
    nextPageBtn = tk.Button(pageAr[iPage + 1], command=load_next_page, image=nextIcon, background="#2D2D2D", activebackground="#2D2D2D", borderwidth=0)

    pageAr[iPage].place_forget()

    iPage += 1
    imgPageCount += 1

    pageAr[iPage].place(relx=0.035, rely=0.109)

    if len(pageAr) > imgPageCount:
        nextPageBtn.place(relx=0.55, rely=0.91)
        previousPageBtn.place(relx=0.411, rely=0.91)
    if len(pageAr) == imgPageCount:
        previousPageBtn.place(relx=0.411, rely=0.91)

#
def load_next_page_img():
    global cPage
    global imgPageCount

    previousPageBtn = tk.Button(pageCam[cPage + 1], command=load_previous_page_img, image=previousIcon, background="#2D2D2D", activebackground="#2D2D2D", borderwidth=0)
    nextPageBtn = tk.Button(pageCam[cPage + 1], command=load_next_page_img, image=nextIcon, background="#2D2D2D", activebackground="#2D2D2D", borderwidth=0)

    pageCam[cPage].place_forget()

    cPage += 1
    imgPageCount += 1

    pageCam[cPage].place(relx=0.035, rely=0.109)

    if len(pageCam) > imgPageCount:
        nextPageBtn.place(relx=0.55, rely=0.91)
        previousPageBtn.place(relx=0.411, rely=0.91)
    if len(pageCam) == imgPageCount:
        previousPageBtn.place(relx=0.411, rely=0.91)
        pass

# Loads the previous page for the passwords
def load_previous_page():
    global iPage
    global pageCount

    previousPageBtn = tk.Button(pageAr[iPage - 1], command=load_previous_page, image=previousIcon, background="#2D2D2D", activebackground="#2D2D2D", borderwidth=0)

    pageAr[iPage].place_forget()

    iPage -= 1
    pageCount -= 1

    pageAr[iPage].place(relx=0.035, rely=0.109)

    if len(pageAr) <= pageCount:
        previousPageBtn.place(relx=0.411, rely=0.91)        

#
def load_previous_page_img():
    global cPage
    global imgPageCount

    previousPageBtn = tk.Button(pageCam[cPage - 1], command=load_previous_page_img, image=previousIcon, background="#2D2D2D", activebackground="#2D2D2D", borderwidth=0)

    pageCam[cPage].place_forget()

    cPage -= 1
    imgPageCount -= 1

    pageCam[cPage].place(relx=0.035, rely=0.109)

    if len(pageCam) <= imgPageCount:
        previousPageBtn.place(relx=0.411, rely=0.91)  

# Saves the image
def save_image(imageName):
    global image1
    global imgCheck
    imageName = tk.Button(root_dir_img, command=lambda b=("%s = %d" % ("cameraImage",imge)): make_newwindow(b))   
    imageName.place(relx=imgX, rely=imgY, anchor=CENTER)  
    image1 = imageName

# Loads the image   
def load_image():   
    for image in images:
        for imageSlot in imageSlots:
            image.configure(image=imageSlot)

# Loads the images once the program has started
def start_load_images():
    global imge
    global imgX
    global imgY
    global imageCount
    global imgCount
    global imgCheck

    nextPageBtn = tk.Button(root_dir_img, command=load_next_page_img, image=nextIcon, background="#2D2D2D", activebackground="#2D2D2D", borderwidth=0)

    if os.path.isfile("images.txt"): 
        with open('images.txt','rb') as f:
            os.chdir("imageFolder")
            img = ['%s/%s'%(os.getcwd(),line.strip()) for line in f]

        for image in img:
            image_tk = Image.open("cameraImage" + str(imageCount) + ".png")
            newImage = tk.PhotoImage(file="cameraImage" + str(imageCount) + ".png")
            originalImage.append(newImage)

            save_image(exec("%s = %d" % ("cameraImage",imge)))

            rezied = image_tk.resize((150, 100), Image.ANTIALIAS)
            new_pic = ImageTk.PhotoImage(rezied)
            image1.configure(image=new_pic)
            images.append(image1)
            imageSlots.append(new_pic)

            imge += 1
            imgX += 0.239

            imageCount += 1
            imgCheck += 1

            if imgX == 1.096:
                imgX = 0.14
                imgY = 0.6
                if imgCheck == 8:
                    imgCount += 1
                    make_new_page_img(exec("%s = %d" % ("camFrameP",imgCount)), exec("%s = %d" % ("camLayoutP",imgCount)))
                    nextPageBtn.place(relx=0.55, rely=0.91)
                    imgX = 0.14
                    imgY = 0.2
                    imgCheck = 0
    else:
        print("File has not been created yet.")

    if f.closed:
        os.chdir('..')

# Creates a new window when you click on an image
def make_newwindow(button):
    global newwindow
    newwindow = tk.Toplevel()
    newwindow.title('Image')
    newwindow.resizable(False, False)
    btnString = button[-1:]
    newimage = Label(newwindow, image=originalImage[int(btnString)])
    newimage.pack()

# Generates a random set of words
def generate_words():
    global word
    global chars
    global y
    global u
    global o
    global b

    textLabel.configure(state=NORMAL)

    word = ""
    lst = []
    i = 0
    y = 0
    u = 0
    b = 0
    o = 0

    chars = []
    
    for line in open("words.txt").read().split():
        lst.append(line)

    while i < len(lst):
        word += random.choice(lst) + " "
        i += 1

    textLabel.place(relx=0.5, rely=0.6, anchor=CENTER)
    textLabel.delete("1.0", END)
    textLabel.insert(END, word)
    textLabel.configure(state=DISABLED, borderwidth=0)

    chars = list(word)  
    
# Checks to see if the words that the user types are the same as the ones given in the text
def type_check(event):
    global y
    global u
    global chars
    global run_once
    global characters
    global countDa
    global timee
    global b
    global o
    global word
    global totalChar

    if textLabel.winfo_ismapped() == 1:
        totalChar += 1
        if event.keysym == "Tab":
            generate_words()
            if countDa != None:
                root.after_cancel(countDa)
            secondsText.config(text="")
            run_once = 0
            return "break"
        if countdownTime != 0:
            secondsText.place(relx=0.125, rely=0.3, anchor=CENTER)
            if textLabel.count("1.0", "1." + str(b+1), "displaylines") == (1,):
                textLabel.config(state=NORMAL)
                textLabel.delete("1.0", "1." + str(b))
                b = 0
                y = 0
                u = 0
                textLabel.delete("1.0", "1.1")
                if chars[o].isspace() == True:
                    o += 1
                return "break"
            elif chars[o].isspace() == True:
                if event.keysym == "space":
                    y += 1
                    textLabel.tag_add("correct", '1.' + str(u), '1.' + str(y))
                    u += 1
                    textLabel.tag_config("correct", background="green")
                    if run_once == 0:
                        countdown(countdownTime)
                        run_once = 1
                    characters += 1
                    b += 1
                    o += 1
                    return "break"
                else:
                    y += 1
                    textLabel.tag_add("incorrect", '1.' + str(u), '1.' + str(y))
                    u += 1
                    textLabel.tag_config("incorrect", background="red")
                    if run_once == 0:
                        countdown(countdownTime)
                        run_once = 1
                    b += 1
                    o += 1
                    return "break"
            elif event.keysym == "BackSpace":
                return "break"
            elif event.keysym == chars[o]:
                y += 1
                textLabel.tag_add("correct", '1.' + str(u), '1.' + str(y))
                u += 1
                textLabel.tag_config("correct", background="green")
                if run_once == 0:
                    countdown(countdownTime)
                    run_once = 1
                characters += 1
                b += 1
                o += 1
                return "break"
            else:
                y += 1
                textLabel.tag_add("incorrect", '1.' + str(u), '1.' + str(y))
                u += 1
                textLabel.tag_config("incorrect", background="red")
                if run_once == 0:
                    countdown(countdownTime)
                    run_once = 1
                b += 1
                o += 1
                return "break"

# Calculates the countdown time, also the WPM
def countdown(seconds):
    global countDa
    global characters
    global isTyping
    global run_once

    wpm = 0
    acc = 0
    wholeAcc = 0
    secondsText.config(text=str(seconds) + " sec", background="#2D2D2D", fg="white")
    if seconds > 0:
        countDa = root.after(1000, countdown, seconds-1)
    if seconds == 0:
        wpm = (characters / 5) / (timee / 60)
        acc = (characters / totalChar) * 100
        wholeAcc = math.trunc(acc)
        if countDa != None:
            root.after_cancel(countDa)
        secondsText.config(text="")
        generate_words()
        run_once = 0
        characters = 0
        typeFrame.place_forget()
        statsFrame.place(relx=0.035, rely=0.109)
        wpmText.config(text=wpm)
        accText.config(text=str(wholeAcc) + "%")
        wpm = 0
        acc = 0

# Sets the base time for the countdown timer
def get_value(time):
    global timee
    global countdownTime
    countdownTime = 0
    timee = time
    countdownTime = time

    if time == 15:
        button15s.config(fg="#8bcce8")
        button30s.config(fg="white")
        button60s.config(fg="white")
        button120s.config(fg="white")
    elif time == 30:
        button15s.config(fg="white")
        button30s.config(fg="#8bcce8")
        button60s.config(fg="white")
        button120s.config(fg="white")
    elif time == 60:
        button15s.config(fg="white")
        button30s.config(fg="white")
        button60s.config(fg="#8bcce8")
        button120s.config(fg="white")
    elif time == 120:
        button15s.config(fg="white")
        button30s.config(fg="white")
        button60s.config(fg="white")
        button120s.config(fg="#8bcce8")
    else:
        pass
    
def close_stats():
    statsFrame.place_forget()
    typeFrame.place(relx=0.035, rely=0.109)
#endregion

#region Variables

images = []
originalImage = []
imageSlots = []
char = []

characters = 0

password1 = ""

pass1 = ""

pageCam = []

lowStrengh = "abcdefghijklmnopqrstuvwxyz"
mediumStrengh = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
highStrengh = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 !@#$%^&*()"

title_window = ""
frameName = "Home"

pyglet.font.add_file("Louis George Cafe.ttf")

width_of_window = 854
height_of_window = 480

imgX = 0.14
imgY = 0.2

page = 1
pageCount = 1
imgPageCount = 1
count = 0
size = 26
iPage = 0
cPage = 0
check = 1
imgCheck = 0
imge = 0

imgCount = 0

countdownTime = 0

openMenu = False
isTyping = False
countDa = None
totalChar = 0

run_once = 0

test = 1
test2 = 1
y = 0
u = 0
b = 0
o = 0

imageCount = 0

passY = 0.1

GWL_EXSTYLE=-20
WS_EX_APPWINDOW=0x00040000
WS_EX_TOOLWINDOW=0x00000080

current_time = time.strftime("%H:%M")

root = tk.Tk()

root.winfo_toplevel()

low = tk.IntVar()
med = tk.IntVar()
high = tk.IntVar()

var1 = IntVar()

combostyle = Style()

combostyle.theme_create('combostyle', parent='alt',
                         settings = {'TCombobox':
                                     {'configure':
                                      {'selectbackground': '#232323',
                                       'fieldbackground': '#232323',
                                       'background': 'white',
                                       'foreground': 'white',
                                       'highlightthickness': 0,
                                       'borderwidth': 0
                                       }}}
                        )

combostyle.theme_use('combostyle') 

menuIcon = tk.PhotoImage(file = "menuIcon.png")
lockIcon = tk.PhotoImage(file = "lockIcon.png")
vaultIcon = tk.PhotoImage(file = "vault.png")
houseIcon = tk.PhotoImage(file = "houseIcon.png")
clipboard = tk.PhotoImage(file = "clipboard.png")
checkmark = tk.PhotoImage(file = "checkmark.png")
nextIcon = tk.PhotoImage(file = "nextIcon.png")
previousIcon = tk.PhotoImage(file = "previousIcon.png")
keyboardIcon = tk.PhotoImage(file = "keyboard.png")
cameraIcon = tk.PhotoImage(file = "cameraIcon.png")

#endregion

#region Home

homeFrame = tk.Frame(root)
homeLayout = tk.Frame(homeFrame, height=430, width=825, bg="#2D2D2D")
homeLayout.pack()

userTime = tk.Label(homeFrame, text=current_time, bg="#2D2D2D", fg="#ffffff", font=("Louis George Cafe", 13))
userTime.place(relx=0.93, rely=0.01)

#endregion

#region Password Generator

passFrame = tk.Frame(root)
passLayout = tk.Frame(passFrame, height=430, width=825, bg="#2D2D2D")
passLayout.pack()

passLabel = tk.Label(passFrame, text=password1, height=2, width=79, bg="#232323", font=("Louis George Cafe", 10), fg="white")
passLabel.place(relx=0.11, rely=0.1)

genBtn = tk.Button(passFrame, text="Generate password", font=("Louis George Cafe", 14), fg="#ffffff",height=1, width=20, bg="#232323", borderwidth=0, activebackground="#212121", activeforeground="white", command=call_gen)
genBtn.place(relx=0.537, rely=0.26)

saveBtn = tk.Button(passFrame, text="Save password", font=("Louis George Cafe", 14), fg="#ffffff",height=1, width=20, bg="#232323", borderwidth=0, activebackground="#212121", activeforeground="white", command=open_save)
saveBtn.place(relx=0.537, rely=0.38)

lowCheck = tk.Checkbutton(passFrame, text="Low strength", font=("Louis George Cafe", 14), selectcolor="#2D2D2D", bg="#2D2D2D", activebackground="#2D2D2D", fg="white", activeforeground="white",variable=low, onvalue=1, offvalue=0, command=set_pass_low)
lowCheck.place(relx=0.18, rely=0.26)

medCheck = tk.Checkbutton(passFrame, text="Medium strength", font=("Louis George Cafe", 14), selectcolor="#2D2D2D", bg="#2D2D2D", activebackground="#2D2D2D", fg="white", activeforeground="white",variable=med, onvalue=1, offvalue=0, command=set_pass_med)
medCheck.place(relx=0.18, rely=0.38)

highCheck = tk.Checkbutton(passFrame, text="High strength", font=("Louis George Cafe", 14), selectcolor="#2D2D2D", bg="#2D2D2D", activebackground="#2D2D2D", fg="white", activeforeground="white",variable=high, onvalue=1, offvalue=0, command=set_pass_high)
highCheck.place(relx=0.18, rely=0.50)

combo = Combobox(passFrame, textvariable=var1, state="readonly")

combo['values'] = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                   17, 18, 19, 20, 21, 22, 23, 24, 25,      
                   26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
                   41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55,
                   56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70)

combo.current(0)
combo.configure(font=("Louis George Cafe", 14))
combo.bind('<<ComboboxSelected>>')
combo.place(relx=0.18, rely=0.62)

#endregion

#region Save

saveFrame = tk.Frame(root)
saveLayout = tk.Frame(saveFrame, height=160, width=350, bg="#1E1E1E")
saveLayout.pack()

tk.Label(saveFrame, text="Enter site", font=("Louis George Cafe", 10), bg="#1E1E1E", fg="white").place(relx=0.41, rely=0.02)

siteEnter = tk.Entry(saveFrame,font=("Louis George Cafe", 14))
siteEnter.place(relx=0.18, rely=0.2)

saveBtn = tk.Button(saveFrame, text="Save", font=("Louis George Cafe", 14), fg="#ffffff",height=1, width=12, bg="#232323", borderwidth=0, activebackground="#212121", activeforeground="white", command=save_pass)
saveBtn.place(relx=0.55, rely=0.7)

closeBtn = tk.Button(saveFrame, text="Close", font=("Louis George Cafe", 14), fg="#ffffff",height=1, width=12, bg="#232323", borderwidth=0, activebackground="#212121", activeforeground="white", command=close_save)
closeBtn.place(relx=0.05, rely=0.7)

#endregion

#region Password Vault

#region Page 1
passVaFrame = tk.Frame(root)
passVaLayout = tk.Frame(passVaFrame, height=430, width=825, bg="#2D2D2D")
passVaLayout.pack()

root_dir = passVaFrame

pageText = tk.Label(passVaFrame, text="Page 1", font=("Louis George Cafe", 10), bg="#2D2D2D", fg="white")
pageText.place(relx=0.465, rely=0.91)

#endregion

#region Page 2

passVaFrameP2 = tk.Frame(root)
passVaLayoutP2 = tk.Frame(passVaFrameP2, height=430, width=825, bg="#2D2D2D")
passVaLayoutP2.pack()

pageText = tk.Label(passVaFrameP2, text="Page 2", font=("Louis George Cafe", 10), bg="#2D2D2D", fg="white")
pageText.place(relx=0.465, rely=0.91)

#endregion

pageAr = []

#endregion

#region Type

typeFrame = tk.Frame(root)
typeLayout = tk.Frame(typeFrame, height=430, width=825, bg="#2D2D2D")
typeLayout.pack()

textLabel = tk.Text(typeFrame, font=("Louis George Cafe", 15), bg="#2D2D2D", fg="white", width=60, height=10, wrap=WORD)

secondsText = tk.Label(typeFrame, font=("Louis George Cafe", 10))

button15s = tk.Button(typeFrame, text="15", background="#2D2D2D", fg="white", borderwidth=0, font=("Louis George Cafe", 10), activebackground="#2D2D2D", activeforeground="white", command=lambda *args: get_value(15))
button15s.place(relx=0.82, rely=0.05)

button30s = tk.Button(typeFrame, text="30", background="#2D2D2D", fg="white", borderwidth=0, font=("Louis George Cafe", 10), activebackground="#2D2D2D", activeforeground="white", command=lambda *args: get_value(30))
button30s.place(relx=0.85, rely=0.05)

button60s = tk.Button(typeFrame, text="60", background="#2D2D2D", fg="white", borderwidth=0, font=("Louis George Cafe", 10), activebackground="#2D2D2D", activeforeground="white", command=lambda *args: get_value(60))
button60s.place(relx=0.88, rely=0.05)

button120s = tk.Button(typeFrame, text="120", background="#2D2D2D", fg="white", borderwidth=0, font=("Louis George Cafe", 10), activebackground="#2D2D2D", activeforeground="white", command=lambda *args: get_value(120))
button120s.place(relx=0.91, rely=0.05) 

#region Stats

statsFrame = tk.Frame(root)
statsLayout = tk.Frame(statsFrame, height=430, width=825, bg="#2D2D2D")
statsLayout.pack()

statsCloseBtn = tk.Button(statsFrame, text="x", background="#2D2D2D", fg="white", borderwidth=0, font=("Louis George Cafe", 17), activebackground="#2D2D2D", activeforeground="white", command=close_stats)
statsCloseBtn.place(relx=0.95, rely=0.025) 

wpmWordText = tk.Label(statsFrame, text="wpm", font=("Louis George Cafe", 17), background="#2D2D2D", fg="white")
wpmWordText.place(relx=0.05, rely=0.025) 

wpmText = tk.Label(statsFrame, font=("Louis George Cafe", 30), background="#2D2D2D", fg="white")
wpmText.place(relx=0.075, rely=0.1) 

accWordText = tk.Label(statsFrame, text="acc", font=("Louis George Cafe", 17), background="#2D2D2D", fg="white")
accWordText.place(relx=0.05, rely=0.225) 

accText = tk.Label(statsFrame, font=("Louis George Cafe", 30), background="#2D2D2D", fg="white")
accText.place(relx=0.075, rely=0.3) 

#endregion

#endregion

#region Camera

cameraFrame = tk.Frame(root)
cameraLayout = tk.Frame(cameraFrame, height=430, width=825, bg="#2D2D2D")
cameraLayout.pack() 

root_dir_img = cameraFrame

camPageText = tk.Label(cameraFrame, text="Page 1", font=("Louis George Cafe", 10), bg="#2D2D2D", fg="white")
camPageText.place(relx=0.465, rely=0.91)

pageCam.append(cameraFrame)

#endregion

#region Base GUI

homeFrame.place(relx=0.035, rely=0.109)

root.resizable(False, False)

root.configure(background="#2D2D2D")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_coordinate = (screen_width/2) - (width_of_window/2)
y_coordinate = (screen_height/2) - (height_of_window/2)

root.overrideredirect(True)
root.geometry('%dx%d+%d+%d' % (width_of_window, height_of_window, x_coordinate, y_coordinate))

title_bar = tk.Frame(root, bg='#1E1E1E', relief='raised', bd=2, borderwidth=0)
title_bar.pack(fill=X)

title_name = tk.Label(title_bar, text=title_window, bg="#1E1E1E", fg="white", justify=CENTER)
title_name.pack(side=LEFT)

close_button = tk.Button(title_bar, text='X', bg="#1E1E1E", foreground="white", command=root.destroy, borderwidth=0, width=2)
close_button.pack(side=RIGHT)

title_bar.bind('<Button-1>', save_last_click_pos)
title_name.bind('<B1-Motion>', dragging)
title_name.bind('<Button-1>', save_last_click_pos)
title_bar.bind('<B1-Motion>', dragging)
close_button.bind('<Enter>', change_on_hovering)
close_button.bind('<Leave>', return_to_normal_state)

frameWindow = tk.Label(root, text=frameName, font=("Louis George Cafe", 15),bg="#232323", fg="white")
frameWindow.place(relx=0., rely=0.045, width=854)

leftFrame = tk.Frame(root, height=480, width=30, bg="#1E1E1E")
leftFrame.pack(side=LEFT)

menuText = tk.Label(leftFrame, text="", bg="#1E1E1E", fg="#ffffff", font=("Louis George Cafe", 9))
menuText.place(relx=0.2, rely=0.005)
homeText = tk.Label(leftFrame, text="", bg="#1E1E1E", fg="#ffffff", font=("Louis George Cafe", 9))
homeText.place(relx=0.2, rely=0.085)
passGenText = tk.Label(leftFrame, text="", bg="#1E1E1E", fg="#ffffff", font=("Louis George Cafe", 9))
passGenText.place(relx=0.2, rely=0.165)
passVaultText = tk.Label(leftFrame, text="", bg="#1E1E1E", fg="#ffffff", font=("Louis George Cafe", 9))
passVaultText.place(relx=0.2, rely=0.245)
TypingText = tk.Label(leftFrame, text="", bg="#1E1E1E", fg="#ffffff", font=("Louis George Cafe", 9))
TypingText.place(relx=0.2, rely=0.325)
cameraText = tk.Label(leftFrame, text="", bg="#1E1E1E", fg="#ffffff", font=("Louis George Cafe", 9))
cameraText.place(relx=0.2, rely=0.405)
 
menuButton = tk.Button(root, command=expand, image=menuIcon, background="#1E1E1E", activebackground="#1E1E1E", borderwidth=0)
menuButton.place(relx=0.005, rely=0.050)

homeButton = tk.Button(root, command=show_home, image=houseIcon, background="#1E1E1E", activebackground="#1E1E1E", borderwidth=0)
homeButton.place(relx=0.005, rely=0.125)

lockButton = tk.Button(root, command=show_pass_gen, image=lockIcon, background="#1E1E1E", activebackground="#1E1E1E", borderwidth=0)
lockButton.place(relx=0.005, rely=0.2)

lock2Button = tk.Button(root, command=show_pass_vault, image=vaultIcon, background="#1E1E1E", activebackground="#1E1E1E", borderwidth=0)
lock2Button.place(relx=0.005, rely=0.275)

typeButton = tk.Button(root, command=show_type, image=keyboardIcon, background="#1E1E1E", activebackground="#1E1E1E", borderwidth=0)
typeButton.place(relx=0.005, rely=0.35)

cameraButton = tk.Button(root, command=show_camera, image=cameraIcon, background="#1E1E1E", activebackground="#1E1E1E", borderwidth=0)
cameraButton.place(relx=0.005, rely=0.425)

buttons = [homeFrame, passFrame, passVaFrame, typeFrame, cameraFrame]

root.bind("<Control-x>",  key_pressed)
root.unbind_all("<<NextWindow>>")
    
root.after(10, lambda: set_appwindow(root))
root.after(10, lambda: load_pass())
root.after(10, lambda: load_image())
if os.path.isfile("capture.png"): 
    root.after(10, lambda: start_load_images())
root.mainloop()    
#endregion
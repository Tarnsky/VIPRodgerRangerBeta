# grabscreen.py
import datetime
import time

import pyscreenshot as ImageGrab
from pynput.mouse import Listener
import sys
import tkinter as tk
from PIL import Image

from datetime import datetime
import pytesseract

'''
        Grab a text from an image
        grabbed clicking on the left top corner
        and right down corner of the part of the screen
        with the text.
        It returns it in the console, replaces the text in Print.txt, 
        appends to text in Log.txt,
        saves image to Images folder,

'''


# Takes cords from clicks and takes an image
def grab(x, y, w, h, loop):
    global a, b, c, d
    if loop == False:
        a = x
        b = y
        c = w
        d = h
        im = ImageGrab.grab(bbox=(a, b, c, d))
        saveim(im)
        ocr()
    else:
        im = ImageGrab.grab(bbox=(a, b, c, d))
        saveim(im)
        ocr()


# Send Print.txt for printing
def sendToPrinter():
    pass


# Takes the result from the screen grab and adds text to a permanent txt file called Log.txt
def printToLog(ocr_result):
    f = open("Log.txt", "a")
    print(str(datetime.now().strftime('%Y_%m_%d-%I_%M-%S-%f')[:-3]), file=f)
    f = open("Log.txt", "a")
    print(ocr_result, file=f)
    f = open("Log.txt", "a")


# Takes the result from the screen grab and adds text to a temporary txt file called Print.txt
def printOutPut(ocr_result, x, y):
    f = open("Print.txt", "w")
    print(str(datetime.now().strftime('%Y_%m_%d-%I_%M-%S-%f')[:-3]), file=f)
    f = open("Print.txt", "a")
    print(ocr_result, file=f)
    f = open("Print.txt", "a")
    print("---------------------------------", file=f)
    # print to a Log which won't delete with new message
    printToLog(ocr_result)
    sendToPrinter()
    # Start Loop
    ##time.sleep(60)  # Delay for 1 minute (60 seconds).
    ##grab(x1, y1, x, y, True)


# Reads result of the ocr() function
def readImage(im):
    im_file = "im.png"

    img = Image.open(im_file)
    ocr_result = pytesseract.image_to_string(img)
    ## print(ocr_result)
    printOutPut(ocr_result, 0, 0)


# Saves screen grab as a temp image
def saveim(im):
    im.save('im.png')

    # os.startfile('im.png')
    readImage(im)
    saveGrabCopy(im)


# Saves copy of the screen grab if the image folder with a time stamp
def saveGrabCopy(im):
    image_name = f"MissionX-{str(datetime.now().strftime('%Y_%m_%d_%I-%M-%S-%f')[:-3])}.png"
    filepath = f"Images/{image_name}"
    ## print(filepath)
    im.save(filepath)


# Transcribe the screen grab to text
def ocr():
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
    print(pytesseract.image_to_string(r'im.png'))


click1 = 0
x1 = 0
y1 = 0


# gets cords of clicks to set capture area
def on_click(x, y, button, pressed):
    global click1, x1, y1, listener, a, b

    if pressed:
        if click1 == 0:
            x1 = x
            y1 = y
            click1 = 1

        else:

            grab(x1, y1, x, y, False)
            listener.stop()
            sys.exit()


def start():
    global listener

    root.destroy()
    print("Click once on top left and once on bottom right")
    # with Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
    with Listener(on_click=on_click) as listener:
        listener.join()
        # listener.stop()
        # sys.exit()
    print(x1, y1)


root = tk.Tk()

button = tk.Button(root, text="Calibrate", command=start)
button.pack()

root.mainloop()

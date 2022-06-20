from tkinter import *
import os
import time

# Make window
root = Tk()
root.title('Timer App')
root.geometry("275x100")
root.resizable(False, False) # Two bools for width and height

runTime = False
savedTime = 0

def formatTime(t):
    return f"{int(t/60)}:{str(t%60)[:4]}"

def startTimer():
    stopButton["state"] = "normal"
    timerButton["state"] = "disabled"
    resetButton["state"] = "normal"
    global runTime
    runTime = True
    global savedTime
    while runTime:
        root.update()
        time.sleep(0.1)
        savedTime += 0.1
        timerLabel.config(text=formatTime(savedTime))

def stopTimer():
    global runTime
    runTime = False
    timerButton["state"] = "normal"
    stopButton["state"] = "disabled"

def resetTimer():
    timerButton["state"] = "normal"
    stopButton["state"] = "disabled"
    resetButton["state"] = "disabled"
    global savedTime
    global runTime
    savedTime = 0
    runTime = False
    timerLabel.config(text=formatTime(savedTime))
    

timerButton = Button(root, text="Start", font=("Courier", 12), command=startTimer)
timerButton.grid(row=0, column = 0)

stopButton = Button(root, text="Stop", font=("Courier", 12), command=stopTimer)
stopButton["state"] = "disabled"
stopButton.grid(row=0, column = 1)

resetButton = Button(root, text="Reset", font=("Courier", 12), command=resetTimer)
resetButton["state"] = "disabled"
resetButton.grid(row=0, column = 2)

timerLabel = Label(text="00:00", font=("Courier New", 30))
timerLabel.grid(row=1, column=1)



root.mainloop()
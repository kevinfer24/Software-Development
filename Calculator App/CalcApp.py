from functools import partial
from tkinter import *
import pyperclip

# Make window
root = Tk()
root.title('Calculator')
root.geometry("350x370")
root.resizable(False, False) # Two bools for width and height

# If true, calc will start retyping
copied = False

# Accumulated value
accumulator = 0

# Current Operation to be exeuted once Equals is pressed
currentOp = None

# Key inputs
def typeNums(key):
    currentText = C.itemcget(output, 'text')
    if key.char.isnumeric():
        addNum(key.char)
    elif key.char == "." and "." not in currentText:
        addNum(".")

    # Back space    
    elif key.keycode == 8 and currentText != "" and float(currentText) != 0:
        try:
            C.itemconfig(output, text=currentText[0:-1])
            if C.itemcget(output, 'text') == "": C.itemconfig(output, text="0")
        except:
            C.itemconfig(output, text="0")

# Add number to the end of the displayed number
def addNum(num):
    global copied
    if not copied:
        currentText = C.itemcget(output, 'text')
        if len(currentText) < 9:
            if float(currentText) == 0 and "." not in currentText and num != ".":
                C.itemconfig(output, text="")
                currentText = ""
            if num != "." and num != "-": C.itemconfig(output, text=currentText + str(num))
            elif num == "." and "." not in currentText: C.itemconfig(output, text=currentText + str(num))
            elif num == "-" and "-" not in currentText: C.itemconfig(output, text="-"+currentText)
    else:
        copied = False
        global accumulator
        temp = accumulator
        clearNum()
        accumulator = temp
        addNum(num)

def setOp(op):
    global copied
    global accumulator
    global currentOp  
    
    if accumulator == 0:
        currentOp = op
        equals(True)
    else:
        equals()
        currentOp = op
    copied = True
 # Computes the calculation
def equals(first = False):
    global accumulator
    global copied
    result = 0
    if currentOp == "+":
        result = accumulator + float(C.itemcget(output, 'text'))
    elif currentOp == "-":
        result = float(C.itemcget(output, 'text')) if accumulator == 0 else accumulator - float(C.itemcget(output, 'text'))
    elif currentOp == "x":
        result = (1 if accumulator == 0 else accumulator) * float(C.itemcget(output, 'text'))
    elif currentOp == "/":
        result = float(C.itemcget(output, 'text')) if accumulator == 0 else accumulator/float(C.itemcget(output, 'text'))
    elif currentOp == "mod":
        result = float(C.itemcget(output, 'text')) if accumulator == 0 else accumulator % float(C.itemcget(output, 'text'))
    accumulator = result
    C.itemconfig(output, text=str(float(result)))
    
# Deletes most recently entered digit
def backSpace():
    currentText = C.itemcget(output, 'text')
    if currentText != "0":
        try:
            C.itemconfig(output, text=currentText[0:-1])
            if C.itemcget(output, 'text') == "": C.itemconfig(output, text="0")
        except:
            C.itemconfig(output, text="0")
# Clears the calculator and the accumulator
def clearNum():
    global accumulator
    accumulator = 0
    C.itemconfig(output, text="0")
# Copies to clipboard
def copyNum():
    pyperclip.copy(C.itemcget(output, 'text'))

# Creates the number buttons
def createNumButtons():
    butts = [Button(text = "0", font=("Arial", 25), command = lambda: addNum(0))]
    butts[-1].place(x=47, y=295)
    xPos, yPos = 0, 100
    for i in range(1, 10):
        butts.append(Button(text = str(i), font=("Arial", 25), command = partial(addNum, i)))
        butts[-1].place(x=xPos, y=yPos)
        # Change position
        xPos += 47
        if xPos > 47 * 2:
            xPos = 0
            yPos += 65
    # Decimal point
    butts.append(Button(text = " .", font=("Arial", 25), command = partial(addNum, ".")))
    butts[-1].place(x=47*2, y=295)

def createFunctionButtons():
    funcButts = []
    # ADD
    funcButts.append(Button(text = "+", font=("Arial", 25), command = partial(setOp, "+")))
    funcButts[-1].place(x=47*3, y=100)
    
    # SUB
    funcButts.append(Button(text = "- ", font=("Arial", 25), command = partial(setOp, "-")))
    funcButts[-1].place(x=47*3, y=165)
    # MULT
    funcButts.append(Button(text = "×", font=("Arial", 25), command = partial(setOp, "x")))
    funcButts[-1].place(x=47*3, y=230)
    # DIV
    funcButts.append(Button(text = "÷", font=("Arial", 25), command = partial(setOp, "/")))
    funcButts[-1].place(x=47*3, y=295)

    # MOD
    funcButts.append(Button(text = "mod", font=("Arial", 16), width = 4, height=2,command = partial(setOp, "mod")))
    funcButts[-1].place(x=47*4 + 60, y=100)

    # NEG
    funcButts.append(Button(text = "(-)", font=("Arial", 16), width = 4, height=2,command = partial(addNum, "-")))
    funcButts[-1].place(x=47*4, y=100)

    # COPY
    funcButts.append(Button(text = "Copy", font=("Arial", 25), width = 8, height=1,command = copyNum, bg="blue"))
    funcButts[-1].place(x=47*4 + 1, y=165)

    # CLEAR
    funcButts.append(Button(text = "Clear", font=("Arial", 25), width = 8, height=1,command = clearNum, bg="red"))
    funcButts[-1].place(x=47*4 + 1, y=230)

    # EQUALS
    funcButts.append(Button(text = "=", font=("Arial", 25), width = 8, height=1,command = equals, bg="green"))
    funcButts[-1].place(x=47*4 + 1, y=295)

    # BACKSPACE
    funcButts.append(Button(text = "Bksp", font=("Arial", 12), width=4,height=3,command = backSpace, bg="yellow"))
    funcButts[-1].place(x=0, y=295)

# Canvas
C = Canvas(root, width= 350, height=100, background="white")
output = C.create_text(350,65, anchor="e", text="0", fill="black", font=["Courier", 45])
C.place(x=0,y=0)

# Call the functions to draw the buttons and operators
createNumButtons()
createFunctionButtons()

root.bind("<KeyPress>", typeNums)
root.mainloop()

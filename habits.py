from datetime import date, timedelta, datetime
from cmu_graphics import*
from PIL import Image

def drawHabits(app):
    drawLabel('Habits', 98, 39, size=35, align='left', font='DM Sans 36pt')
    drawLine(78, 78, 1366, 78, fill=rgb(217, 217, 217))
    button = Image.open('Images/button.png') # Icon is element from https://www.canva.com/
    drawImage(CMUImage(button), 1224, 13, height=52, width=128)
    drawLabel('New Habit', 1298, 39, size=19, align='center', font='DM Sans 36pt')
    drawLabel('+', 1243, 41, size=28, font='DM Sans 36pt')

def drawHabitsPopUp(habitName, startTime, endTime, selectedDays, rect3Fill, rect4Fill):
    popUpMenu = Image.open('Images/popupmenu.png') # Image is shape from https://docs.google.com/presentation/u/1/
    drawImage(CMUImage(popUpMenu), 789, 13, width=422, height=385)
    drawLine(793, 78, 1207, 78, fill=rgb(217, 217, 217))
    drawLine(793, 333, 1207, 333, fill=rgb(217, 217, 217))
    drawLabel(habitName, 810, 46, align='left', size=35, font='DM Sans')
    drawLabel('Cancel', 1050, 364, fill=rgb(167, 173, 173), size=17, font='DM Sans')
    button = Image.open('Images/button.png') # Icon is element from https://www.canva.com/
    drawImage(CMUImage(button), 1095, 344, height=40, width=98)
    drawLabel('Add', 1144, 364, size=17, font='DM Sans')
    drawLabel('Duration', 810, 105, align='left', size=25, font='DM Sans', fill=rgb(167, 173, 173))
    drawRect(806, 121, 130, 40, fill=rect3Fill)
    drawLabel(startTime, 870, 142, size=30, font='DM Sans')
    drawLabel('to', 955, 143, size=30, fill=rgb(167, 173, 173), font='DM Sans')
    drawRect(975, 121, 130, 40, fill=rect4Fill)
    drawLabel(endTime, 1040, 142, size=30, font='DM Sans')
    drawLabel('Days', 810, 189, align='left', size=25, font='DM Sans', fill=rgb(167, 173, 173))
    drawDateButtons(810, 211, selectedDays)

def checkHabitStartEndTimePresses(app, mouseX, mouseY):
    if 806 <= mouseX <= 936 and 121 <= mouseY <= 161:
        app.rect3TextField = True
    else:
        app.rect3TextField = False
    if 975 <= mouseX <= 1105 and 121 <= mouseY <= 161:
        app.rect4TextField = True
    else:
        app.rect4TextField = False

def drawDateButtons(startX, startY, selectedDays):
    x = startX
    y = startY
    dayList = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    for days in dayList:
        if days in selectedDays:
            drawRect(x, y, 90, 50, fill=rgb(167, 173, 173), border=gradient(rgb(140, 82, 255), rgb(255, 145, 77), start='left'), borderWidth=4)
        else:
            drawRect(x, y, 90, 50, fill=rgb(167, 173, 173))
        drawLabel(days, x+45, y+25, fill='white', size=14, font='DM Sans')
        x += 95
        if x == 1190:
            x = startX
            y += 55

def isLegalHabitTime(app):
    startTime = app.habitStartTime.replace('|', '')
    endTime = app.habitEndTime.replace('|', '')
    ### strptime from https://www.programiz.com/python-programming/datetime/strptime ###
    startTime = datetime.strptime(startTime, '%I:%M%p')
    endTime = datetime.strptime(endTime,'%I:%M%p')
    ####################################################################################
    return startTime.time() < endTime.time()

def checkMultiDayButtonPresses(app, mouseX, mouseY, coords):
    days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    buttonValue = 0
    for (x, y) in coords:
        if x <= mouseX <= x+90:
            if y <= mouseY <= y+50:
                if days[buttonValue] not in app.selectedHabitDays:
                    app.selectedHabitDays.add(days[buttonValue])
                else:
                    app.selectedHabitDays.remove(days[buttonValue])
        buttonValue += 1

class Habit:

    def __init__(self, name, days, startTime, endTime):
        self.name = name
        self.days = days
        self.startTime = startTime
        self.endTime = endTime
        self.fill = "30, 33, 54" # Color sourced from https://i.pinimg.com/736x/af/34/ec/af34ec62e403206b0c9fce24051f9160.jpg
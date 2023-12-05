from datetime import date, timedelta, datetime
from cmu_graphics import*
from PIL import Image
from calendarScreen import*
import csv

def drawHabits(app):
    drawLabel('Habits', 98, 39, size=35, align='left', font='DM Sans 36pt')
    drawLine(78, 78, 1366, 78, fill=rgb(217, 217, 217))
    button = Image.open('Images/button.png') # Icon is element from https://www.canva.com/
    drawImage(CMUImage(button), 1224, 13, height=52, width=128)
    drawLabel('New Habit', 1298, 39, size=19, align='center', font='DM Sans 36pt')
    drawLabel('+', 1243, 41, size=28, font='DM Sans 36pt')
    drawHabitsWidgets(app)

def drawHabitsPopUp(habitName, startTime, endTime, rect1Fill, rect2Fill):
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
    drawRect(806, 121, 130, 40, fill=rect1Fill)
    drawLabel(startTime, 870, 142, size=30, font='DM Sans')
    drawLabel('to', 955, 143, size=30, fill=rgb(167, 173, 173), font='DM Sans')
    drawRect(975, 121, 130, 40, fill=rect2Fill)
    drawLabel(endTime, 1040, 142, size=30, font='DM Sans')
    drawLabel('Days', 810, 189, align='left', size=25, font='DM Sans', fill=rgb(167, 173, 173))
    drawDateButtons(app.habitsDayButtonList)

def drawHabitsWidgets(app):
    yValue = 98
    habitsList = list(app.habitsSet)
    for habits in habitsList[0+app.habitsIndex:app.habitsIndex+7]:
        drawRect(98, yValue, 1248, 78, fill='white', border=rgb(167, 173, 173), borderWidth=1)
        drawLabel(habits.name, 112, yValue+24, font='DM Sans', align='left', size=30)
        dayOrder = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        if isinstance(habits.days, str):
            habitDays = habits.days
            habitDays = habitDays.replace("'", '')
            habitDays = habitDays.replace('{', '')
            habitDays = habitDays.replace('}', '')
            habitDays = habitDays.replace(' ', '')
            daysList = habitDays.split(',')
            daysList = sorted(daysList, key=dayOrder.index) # Code from https://dev.to/abdulla783/sort-weekdays-in-python-example-wed-tues-sat-sun-fri-thurs-mon-5b3o
        else:
            habitDays = list(habits.days)
            daysList = sorted(habitDays, key=dayOrder.index) # Code from https://dev.to/abdulla783/sort-weekdays-in-python-example-wed-tues-sat-sun-fri-thurs-mon-5b3o
        dayString = ''
        for days in daysList:
            dayString += days
            dayString += ','
            dayString += ' '
        drawLabel(dayString[:-2], 112, yValue+57, font='DM Sans 36pt', align='left', size=20, fill=rgb(167, 173, 173))
        drawLabel(str(habits.startTime.strftime("%-I:%M")) + (str(habits.startTime.strftime("%p"))).lower() + ' to ' + str(habits.endTime.strftime("%-I:%M")) + (str(habits.endTime.strftime("%p"))).lower(), 1335, yValue+57, align='right', size=20, fill=rgb(167, 173, 173), font='DM Sans 36pt')
        trash = Image.open('Images/bin.png') # Icon from https://www.flaticon.com/free-icon/bin_484662?term=trash+can&page=1&position=1&origin=tag&related_id=484662
        drawImage(CMUImage(trash), 1315, yValue+12, height=20, width=20)
        app.habitWidgetCoords[habits] = (1315, yValue+12)
        yValue += 98

def checkForHabitTrashPress(app, mouseX, mouseY):
    for habits in app.habitWidgetCoords:
        (xCoord, yCoord) = app.habitWidgetCoords[habits]
        if xCoord <= mouseX <= xCoord+20 and yCoord <= mouseY <= yCoord+20:
            app.habitsSet.remove(habits)
            app.habitWidgetCoords = dict()
            removeHabitData(habits)
            break

### Code from https://stackoverflow.com/questions/56987312/how-to-delete-only-one-row-from-a-csv-file-with-python ###

def removeHabitData(habit):
    lines = []
    with open('habitData.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            lines.append(row)
            if row[0] == habit.name:
                lines.remove(row)
    with open('habitData.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)

#####################################################################################################################

def drawDateButtons(buttonList):
    for buttons in buttonList:
        if buttons.selected:
            drawRect(buttons.x, buttons.y, buttons.width, buttons.height, fill=rgb(167, 173, 173), border=gradient(rgb(140, 82, 255), rgb(255, 145, 77), start='left'), borderWidth=4)
        else:
            drawRect(buttons.x, buttons.y, buttons.width, buttons.height, fill=rgb(167, 173, 173))
        if isinstance(buttons.value, str):
            label = buttons.value
            drawLabel(label, buttons.x+45, buttons.y+25, fill='white', size=12, font='DM Sans')
        else:
            label = str(buttons.value.month) + '/' + str(buttons.value.day)
            drawLabel(label, buttons.x+45, buttons.y+25, fill='white', size=15, font='DM Sans')

def isLegalHabitTime(app):
    startTime = app.habitStartTime.replace('|', '')
    endTime = app.habitEndTime.replace('|', '')
    ### strptime from https://www.programiz.com/python-programming/datetime/strptime ###
    startTime = datetime.strptime(startTime, '%I:%M%p')
    endTime = datetime.strptime(endTime,'%I:%M%p')
    ####################################################################################
    return startTime.time() < endTime.time()

class Habit:

    def __init__(self, name, days, startTime, endTime):
        self.name = name
        self.days = days
        self.startTime = startTime
        self.endTime = endTime
        self.fill = "61, 66, 107" # Color sourced from https://www.color-name.com/color-image?c=3D426B&desktop
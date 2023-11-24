from datetime import date, timedelta
from cmu_graphics import*
from PIL import Image

def drawCalendar(currentDate, dateList):
    drawLabel(getCurrentMonth(dateList[0].month) + " " + str(dateList[0].year), 98, 39, size=35, align='left')
    drawRect(78, 156, 98, 624, fill=rgb(238, 241, 247))
    drawRect(78, 78, 1366, 78, fill=rgb(238, 241, 247))
    drawLine(78, 78, 1366, 78, fill=rgb(217, 217, 217))
    drawLine(78, 156, 1366, 156, fill=rgb(217, 217, 217))
    for y in range(234, 769, 78):
        drawLine(158, y, 1366, y, fill=rgb(217, 217, 217))
    for x in range(176, 1200, 170):
        drawLine(x, 78, x, 780, fill=rgb(217, 217, 217))
    x = 91
    for dates in dateList:
        x += 170
        if dates == currentDate:
            drawLabel(getCurrentDay(dates.weekday()) + " " + str(dates.day), x, 117, fill=rgb(25, 25, 25), size=27, bold=True)
        else:
            drawLabel(getCurrentDay(dates.weekday()) + " " + str(dates.day), x, 117, fill=rgb(92, 92, 93), size=27)
    button = Image.open('Images/button.png')
    drawImage(CMUImage(button), 1224, 13, height=52, width=128)
    drawLabel('New Task', 1298, 39, size=19, align='center')
    drawLabel('+', 1243, 41, size=28)

def drawTaskPopUp(taskName):
    popUpMenu = Image.open('Images/popupmenu.png')
    drawImage(CMUImage(popUpMenu), 789, 13, width=422, height=385)
    drawLine(793, 78, 1207, 78, fill=rgb(217, 217, 217))
    drawLine(793, 333, 1207, 333, fill=rgb(217, 217, 217))
    drawLabel(taskName, 810, 46, align='left', size=35, bold=True)
    drawLabel('Cancel', 1050, 364, fill=rgb(167, 173, 173), size=17, bold=True)
    button = Image.open('Images/button.png')
    drawImage(CMUImage(button), 1095, 344, height=40, width=98)
    drawLabel('Schedule', 1144, 364, size=17, bold=True)
    drawLabel('Single event', 840, 105, align='left', size=20, bold=True, fill=rgb(167, 173, 173))

def drawCheckBox(boxChecked):
    if boxChecked:
        drawRect(810, 95, 20, 20, fill=gradient(rgb(140, 82, 255), rgb(255, 145, 77), start='left'))
        check = Image.open('Images/check.png')
        drawImage(CMUImage(check), 820, 105, height=18, width=18, align='center')
    else:
        drawRect(810, 95, 20, 20, fill=None, border=rgb(217, 217, 217))

def drawSingleEventMenu(startTime, endTime, currentDate, buttonNum, rect1Opacity, rect2Opacity):
    drawRect(810, 135, 130, 40, fill=rgb(238, 241, 247), opacity=rect1Opacity)
    drawLabel(startTime, 875, 155, size=30, bold=True)
    drawLabel('to', 960, 155, size=30, fill=rgb(167, 173, 173), bold=True)
    drawRect(980, 135, 130, 40, fill=rgb(238, 241, 247), opacity=rect2Opacity)
    drawLabel(endTime, 1045, 155, size=30, bold=True)
    drawLabel('on', 1134, 159, size=30, fill=rgb(167, 173, 173), bold=True)
    drawDateButtons(810, 195, currentDate, buttonNum)

def drawDateButtons(startX, startY, currentDate, buttonNum):
    x = startX
    y = startY
    for nums in range(0, 8):
        if nums == buttonNum:
            drawRect(x, y, 90, 50, fill=rgb(167, 173, 173), border=gradient(rgb(140, 82, 255), rgb(255, 145, 77), start='left'), borderWidth=4)
        else:
            drawRect(x, y, 90, 50, fill=rgb(167, 173, 173))
        nextDate = currentDate + timedelta(days=nums)
        drawLabel(str(nextDate.month) + '/' + str(nextDate.day), x+45, y+25, fill='white', size=15)
        x += 95
        if x == 1190:
            x = startX
            y += 55

def drawMultipleEventsMenu():
    pass

def getCurrentDay(number):
    if number == 0:
        return 'Mon'
    elif number == 1:
        return 'Tue'
    elif number == 2:
        return 'Wed'
    elif number == 3:
        return 'Thu'
    elif number == 4:
        return 'Fri'
    elif number == 5:
        return 'Sat'
    else:
        return 'Sun'
    
def getCurrentMonth(number):
    if number == 1:
        return 'January'
    elif number == 2:
        return 'February'
    elif number == 3:
        return 'March'
    elif number == 4:
        return 'April'
    elif number == 5:
        return 'May'
    elif number == 6:
        return 'June'
    elif number == 7:
        return 'July'
    elif number == 8:
        return 'August'
    elif number == 9:
        return 'September'
    elif number == 10:
        return 'October'
    elif number == 11:
        return 'November'
    else:
        return 'December'
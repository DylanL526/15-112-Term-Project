from datetime import date, timedelta, datetime
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

def drawSingleEventMenu(startTime, endTime, currentDate, buttonNum, rect1Fill, rect2Fill):
    drawRect(810, 135, 130, 40, fill=rect1Fill)
    drawLabel(startTime, 875, 155, size=30, bold=True)
    drawLabel('to', 960, 155, size=30, fill=rgb(167, 173, 173), bold=True)
    drawRect(980, 135, 130, 40, fill=rect2Fill)
    drawLabel(endTime, 1045, 155, size=30, bold=True)
    drawLabel('on', 1134, 159, size=30, fill=rgb(167, 173, 173), bold=True)
    drawDateButtons(810, 195, currentDate, buttonNum)

def checkDayButtonPresses(app, mouseX, mouseY):
    buttonCoords = [(810, 195), (905, 195), (1000, 195), (1095, 195), (810, 250), (905, 250), (1000, 250), (1095, 250)]
    buttonValue = 0
    for (x, y) in buttonCoords:
        if x <= mouseX <= x+90:
            if y <= mouseY <= y+50:
                if app.clickedDayButton == buttonValue:
                    app.clickedDayButton = 9
                else:
                    app.clickedDayButton = buttonValue
        buttonValue += 1

def checkStartEndTimePresses(app, mouseX, mouseY):
    if 810 <= mouseX <= 940:
        if 135 <= mouseY <= 175:
            app.rect1TextField = True
        else:
            app.rect1TextField = False
    else:
        app.rect1TextField = False
    if 980 <= mouseX <= 1115:
        if 135 <= mouseY <= 175:
            app.rect2TextField = True
        else:
            app.rect2TextField = False
    else:
        app.rect2TextField = False

def checkTextFieldLegality(app):
    if '|' in app.startTime:
        timeFormat = '%I:%M%p|'
    else:
        timeFormat = '%I:%M%p'
    try:
        currentTime = datetime.strptime(app.startTime, timeFormat)
    except ValueError:
        app.rect1Fill = rgb(255, 204, 203)
    if '|' in app.endTime:
        timeFormat = '%I:%M%p|'
    else:
        timeFormat = '%I:%M%p'
    try:
        currentTime = datetime.strptime(app.endTime, timeFormat)
    except ValueError:
        app.rect2Fill = rgb(255, 204, 203)

def isLegalTime(app):
    startTime = app.startTime.replace('|', '')
    endTime = app.endTime.replace('|', '')
    startTime = datetime.strptime(startTime[:-2], '%I:%M')
    endTime = datetime.strptime(endTime[:-2],'%I:%M')
    if app.selectedDate == app.currentDate:
        if startTime.time() >= app.currentTime.time() and endTime.time() > app.currentTime.time():
            return True
        return False
    else:
        return startTime.time() < endTime.time()

def checkInTextField(app):
    if app.taskNameTextField:
        if app.cursorTimer == 8 and (app.taskName == '' or app.taskName[-1] != '|'):
            app.taskName += '|'
        app.cursorTimer += 1
        if app.cursorTimer == 16:
            app.cursorTimer = 0
            app.taskName = app.taskName.replace('|', '')
    else:
        if 8 <= app.cursorTimer <= 15 and '|' in app.taskName:
            app.taskName = app.taskName[:-1]
            app.cursorTimer = 0
    if app.singleEventChecked:
        if app.rect1TextField:
            app.rect1Fill = rgb(238, 241, 247)
            if app.cursorTimer == 8 and (app.startTime == '' or app.startTime[-1] != '|'):
                app.startTime += "|"
            app.cursorTimer += 1
            if app.cursorTimer == 16:
                app.cursorTimer = 0
                app.startTime = app.startTime.replace('|', '')
        else:
            if app.startTime != '' and app.startTime[-1] == '|':
                app.startTime = app.startTime[:-1]
                app.cursorTimer = 0
        if app.rect2TextField:
            app.rect2Fill = rgb(238, 241, 247)
            if app.cursorTimer == 8 and (app.endTime == '' or app.endTime[-1] != '|'):
                app.endTime += "|"
            app.cursorTimer += 1
            if app.cursorTimer == 16:
                app.cursorTimer = 0
                app.endTime = app.endTime.replace('|', '')
        else:
            if app.endTime != '' and app.endTime[-1] == '|':
                app.cursorTimer = 0
                app.endTime = app.endTime[:-1]

def drawDateButtons(startX, startY, currentDate, buttonNum):
    x = startX
    y = startY
    if type(buttonNum) == int:
        for nums in range(0, 8):
            if nums == buttonNum:
                drawRect(x, y, 90, 50, fill=rgb(167, 173, 173), border=gradient(rgb(140, 82, 255), rgb(255, 145, 77), start='left'), borderWidth=4)
            else:
                drawRect(x, y, 90, 50, fill=rgb(167, 173, 173))
            nextDate = currentDate + timedelta(days=nums)
            if nextDate not in app.dayButtonList:
                app.dayButtonList.append(nextDate)
            drawLabel(str(nextDate.month) + '/' + str(nextDate.day), x+45, y+25, fill='white', size=15)
            x += 95
            if x == 1190:
                x = startX
                y += 55
    else:
        for nums in range(0, 8):
            if nums in buttonNum:
                drawRect(x, y, 90, 50, fill=rgb(167, 173, 173), border=gradient(rgb(140, 82, 255), rgb(255, 145, 77), start='left'), borderWidth=4)
            else:
                drawRect(x, y, 90, 50, fill=rgb(167, 173, 173))
            nextDate = currentDate + timedelta(days=nums)
            if nextDate not in app.dayButtonList:
                app.dayButtonList.append(nextDate)
            drawLabel(str(nextDate.month) + '/' + str(nextDate.day), x+45, y+25, fill='white', size=15)
            x += 95
            if x == 1190:
                x = startX
                y += 55

def drawMultipleEventsMenu(deadline, duration, currentDate, buttonNums, deadlineFill):
    drawLabel('Duration', 810, 142, fill=rgb(167, 173, 173), size=25, align='left', bold=True)
    drawRect(993, 142, 150, 30, fill=None, border=rgb(217, 217, 217), align='center')
    drawLabel(duration, 993, 142, align='center', size=17)
    drawDateButtons(810, 211, currentDate, buttonNums)
    drawLabel('Deadline', 810, 185, fill=rgb(167, 173, 173), size=25, align='left', bold=True)
    drawRect(973, 185, 110, 35, align='center', fill=deadlineFill)
    drawLabel(deadline, 973, 185, align='center', size=25, bold=True)
    drawLabel('on', 1035, 188, align='left', fill=rgb(167, 173, 173), size=25, bold=True)

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
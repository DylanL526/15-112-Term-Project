from datetime import date, timedelta, datetime, time
from cmu_graphics import*
from PIL import Image
from habits import*
import copy

def drawCalendar(app, currentDate, dateList):
    drawLabel(getCurrentMonth(dateList[0].month) + " " + str(dateList[0].year), 98, 39, size=35, align='left', font='DM Sans 36pt')
    drawRect(78, 156, 98, 624, fill=rgb(238, 241, 247))
    drawRect(78, 78, 1366, 78, fill=rgb(238, 241, 247))
    drawLine(78, 78, 1366, 78, fill=rgb(217, 217, 217))
    drawLine(78, 156, 1366, 156, fill=rgb(217, 217, 217))
    for y in range(234, 769, 78):
        drawLine(158, y, 1366, y, fill=rgb(217, 217, 217))
    drawCalendarEvents(app)
    for x in range(176, 1200, 170):
        drawLine(x, 78, x, 780, fill=rgb(217, 217, 217))
    x = 91
    for dates in dateList:
        x += 170
        if dates == currentDate:
            drawLabel(getCurrentDay(dates.weekday())[:3] + " " + str(dates.day), x, 117, fill=rgb(25, 25, 25), size=27, font='DM Sans')
        else:
            drawLabel(getCurrentDay(dates.weekday())[:3] + " " + str(dates.day), x, 117, fill=rgb(92, 92, 93), size=27, font='DM Sans 36pt')
    button = Image.open('Images/button.png') # Icon is element from https://www.canva.com/
    drawImage(CMUImage(button), 1224, 13, height=52, width=128)
    drawLabel('New Task', 1298, 39, size=19, align='center', font='DM Sans 36pt')
    drawLabel('+', 1243, 41, size=28, font='DM Sans 36pt')
    drawTimes(app)

def getDatesList(date):
    datesList = [date]
    index = 1
    while True:
        tempDate = date + timedelta(days=index)
        if tempDate.weekday() != 6:
            datesList.append(tempDate)
            index += 1
        else:
            break
    index = 1
    while True:
        tempDate = date - timedelta(days=index)
        if tempDate.weekday() != 5 and len(datesList) != 7:
            datesList.insert(0, tempDate)
            index += 1
        else:
            break
    return datesList

def drawTimes(app):
    for i in range(0+app.index, app.index+7):
        drawLabel(app.times[i], 130, 234 + (i-app.index)*78, size=12, fill=rgb(92, 92, 93), font='DM Sans 36pt')

def getShownTimes(app):
    timeFormat = '%I %p'
    app.shownTimes = []
    for i in range(-1+app.index, app.index+8):
        currentTime = datetime.strptime(app.times[i], timeFormat)
        app.shownTimes.append(currentTime)

def getFormattedTimes(currDay):
    timeFormat = '%I:%M%p'
    formattedTimes = []
    timesList = ['7:00am', '7:15am', '7:30am', '7:45am', 
                 '8:00am', '8:15am', '8:30am', '8:45am', 
                 '9:00am', '9:15am', '9:30am', '9:45am',
                 '10:00am', '10:15am', '10:30am', '10:45am',
                 '11:00am', '11:15am', '11:30am', '11:45am',
                 '12:00pm', '12:15pm', '12:30pm', '12:45pm',
                 '1:00pm', '1:15pm', '1:30pm', '1:45pm',
                 '2:00pm', '2:15pm', '2:30pm', '2:45pm',
                 '3:00pm', '3:15pm', '3:30pm', '3:45pm',
                 '4:00pm', '4:15pm', '4:30pm', '4:45pm',
                 '5:00pm', '5:15pm', '5:30pm', '5:45pm',
                 '6:00pm', '6:15pm', '6:30pm', '6:45pm',
                 '7:00pm', '7:15pm', '7:30pm', '7:45pm',
                 '8:00pm', '8:15pm', '8:30pm', '8:45pm',
                 '9:00pm', '9:15pm', '9:30pm', '9:45pm',
                 '10:00pm']
    for times in timesList:
        currentTime = datetime.strptime(times, timeFormat)
        ### Code from https://www.geeksforgeeks.org/replace-function-of-datetime-date-class-in-python/ ###
        currentTime = currentTime.replace(day=currDay.day, month=currDay.month, year=currDay.year)
        ##################################################################################################
        formattedTimes.append(currentTime)
    return formattedTimes

def drawTaskPopUp(taskName):
    popUpMenu = Image.open('Images/popupmenu.png') # Image is shape from https://docs.google.com/presentation/u/1/
    drawImage(CMUImage(popUpMenu), 789, 13, width=422, height=385)
    drawLine(793, 78, 1207, 78, fill=rgb(217, 217, 217))
    drawLine(793, 333, 1207, 333, fill=rgb(217, 217, 217))
    drawLabel(taskName, 810, 46, align='left', size=35, font='DM Sans')
    drawLabel('Cancel', 1050, 364, fill=rgb(167, 173, 173), size=17, font='DM Sans')
    button = Image.open('Images/button.png') # Icon is element from https://www.canva.com/
    drawImage(CMUImage(button), 1095, 344, height=40, width=98)
    drawLabel('Schedule', 1144, 364, size=17, font='DM Sans')
    drawLabel('Single event', 840, 105, align='left', size=20, font='DM Sans', fill=rgb(167, 173, 173))

def drawCheckBox(boxChecked):
    if boxChecked:
        drawRect(810, 95, 20, 20, fill=gradient(rgb(140, 82, 255), rgb(255, 145, 77), start='left'))
        check = Image.open('Images/check.png') # Icon from https://www.flaticon.com/free-icon/check_3388530?term=check+mark&page=1&position=5&origin=search&related_id=3388530
        drawImage(CMUImage(check), 820, 105, height=18, width=18, align='center')
    else:
        drawRect(810, 95, 20, 20, fill=None, border=rgb(217, 217, 217))

def drawSingleEventMenu(startTime, endTime, startTimeFill, rect2Fill):
    drawRect(810, 135, 130, 40, fill=startTimeFill)
    drawLabel(startTime, 875, 155, size=30, font='DM Sans')
    drawLabel('to', 960, 155, size=30, fill=rgb(167, 173, 173), font='DM Sans')
    drawRect(980, 135, 130, 40, fill=rect2Fill)
    drawLabel(endTime, 1045, 155, size=30, font='DM Sans')
    drawLabel('on', 1134, 159, size=30, fill=rgb(167, 173, 173), font='DM Sans')
    drawDateButtons(app.singleEventDayButtonList)

def checkDayButtonPresses(mouseX, mouseY, buttonList):
    if isinstance(buttonList[0].value, str):
        for buttons in buttonList:
            buttons.checkForMultiPress(mouseX, mouseY)
            if buttons.selected:
                app.selectedHabitDays.add(buttons.value)
            else:
                if buttons.value in app.selectedHabitDays:
                    app.selectedHabitDays.remove(buttons.value)
    else:
        noneCount = 0
        for buttons in buttonList:
            buttons.checkForPress(mouseX, mouseY)
            if buttons.selected:
                app.selectedDate = buttons.value
            else:
                noneCount += 1
        if noneCount == 8:
            app.selectedDate = None

def checkTextFieldLegality(app):
    if '|' in app.startTime.value:
        timeFormat = '%I:%M%p|'
    else:
        timeFormat = '%I:%M%p'
    ##### Code from https://stackoverflow.com/questions/33076617/how-to-validate-time-format #####
    try:
        currentTime = datetime.strptime(app.startTime.value, timeFormat)
        app.startTime.legal = True
    except ValueError:
        app.startTime.legal = False
    ##############################################################################################
    if app.startTime.legal == False:
        app.startTime.fill = rgb(255, 204, 203)
    elif app.startTime.legal and app.startTime.inTextField:
        app.startTime.fill = rgb(238, 241, 247)
    if '|' in app.endTime.value:
        timeFormat = '%I:%M%p|'
    else:
        timeFormat = '%I:%M%p'
    ##### Code from https://stackoverflow.com/questions/33076617/how-to-validate-time-format #####
    try:
        currentTime = datetime.strptime(app.endTime.value, timeFormat)
        app.endTime.legal = True
    except ValueError:
        app.endTime.legal = False
    ##############################################################################################
    if app.endTime.legal == False:
        app.endTime.fill = rgb(255, 204, 203)
    elif app.endTime.legal and app.endTime.inTextField:
        app.endTime.fill = rgb(238, 241, 247)
    if '|' in app.habitStartTime.value:
        timeFormat = '%I:%M%p|'
    else:
        timeFormat = '%I:%M%p'
    ##### Code from https://stackoverflow.com/questions/33076617/how-to-validate-time-format #####
    try:
        currentTime = datetime.strptime(app.habitStartTime.value, timeFormat)
        app.habitStartTime.legal = True
    except ValueError:
        app.habitStartTime.legal = False
    ##############################################################################################
    if app.habitStartTime.legal == False:
        app.habitStartTime.fill = rgb(255, 204, 203)
    elif app.habitStartTime.legal and app.habitStartTime.inTextField:
        app.habitStartTime.fill = rgb(238, 241, 247)
    if '|' in app.habitEndTime.value:
        timeFormat = '%I:%M%p|'
    else:
        timeFormat = '%I:%M%p'
    ##### Code from https://stackoverflow.com/questions/33076617/how-to-validate-time-format #####
    try:
        currentTime = datetime.strptime(app.habitEndTime.value, timeFormat)
        app.habitEndTime.legal = True
    except ValueError:
        app.habitEndTime.legal = False
    ##############################################################################################
    if app.habitEndTime.legal == False:
        app.habitEndTime.fill = rgb(255, 204, 203)
    elif app.habitEndTime.legal and app.habitEndTime.inTextField:
        app.habitEndTime.fill = rgb(238, 241, 247)
    if '|' in app.deadline.value:
        timeFormat = '%I:%M%p|'
    else:
        timeFormat = '%I:%M%p'
    ##### Code from https://stackoverflow.com/questions/33076617/how-to-validate-time-format #####
    try:
        currentTime = datetime.strptime(app.deadline.value, timeFormat)
        app.deadline.legal = True
    except ValueError:
        app.deadline.legal = False
    ##############################################################################################
    if app.deadline.legal == False:
        app.deadline.fill = rgb(255, 204, 203)
    elif app.deadline.legal and app.deadline.inTextField:
        app.deadline.fill = rgb(238, 241, 247)

def isLegalTime(startTime, endTime):
    startTime = startTime.replace('|', '')
    endTime = endTime.replace('|', '')
    ### strptime from https://www.programiz.com/python-programming/datetime/strptime ###
    startTime = datetime.strptime(startTime, '%I:%M%p')
    endTime = datetime.strptime(endTime,'%I:%M%p')
    ####################################################################################
    if app.selectedDate == app.currentDate:
        if startTime.time() >= app.currentTime.time() and endTime.time() > app.currentTime.time():
            return True
        return False
    else:
        return startTime.time() < endTime.time()

def checkInTextField(app):
    for textFields in app.textFields:
        if textFields.inTextField:
            if textFields.timer == 8 and (textFields.value == '' or textFields.value[-1] != '|'):
                textFields.value += '|'
            textFields.timer += 1
            if textFields.timer == 16:
                textFields.timer = 0
                textFields.value = textFields.value.replace('|', '')
        else:
            if 8 <= textFields.timer <= 15 and '|' in textFields.value:
                textFields.value = textFields.value[:-1]
                textFields.timer = 0
    
def createDateButtons(startX, startY, currentDate, offset):
    dateButtonsList = []
    if currentDate != None:
        x = startX
        y = startY
        for i in range(0, 8):
            nextDate = currentDate + timedelta(days=i+offset)
            dateButtonsList.append(DateButton(x, y, 90, 50, nextDate))
            x += 95
            if x == 1190:
                x = startX
                y += 55
    else:
        dayList = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        x = startX
        y = startY
        for i in range(7):
            dateButtonsList.append(DateButton(x, y, 90, 50, dayList[i]))
            x += 95
            if x == 1190:
                x = startX
                y += 55
    return dateButtonsList

def drawMultipleEventsMenu(deadline, hours, minutes, deadlineFill, plusOpacity, minusOpacity):
    drawLabel('Duration', 810, 142, fill=rgb(167, 173, 173), size=25, align='left', font='DM Sans')
    drawRect(1000, 142, 163, 30, fill=None, border=rgb(217, 217, 217), align='center')
    plus = Image.open('Images/add.png') # Icon from https://www.flaticon.com/free-icon/subtraction_4230191?term=minus&page=1&position=36&origin=search&related_id=4230191
    drawCircle(1063, 142, 12, align='center', fill=rgb(238, 241, 247), opacity = plusOpacity)
    drawImage(CMUImage(plus), 1063, 142, height=20, width=20, align='center')
    minus = Image.open('Images/subtraction.png') # Icon from https://www.flaticon.com/free-icon/add_992651?term=add&page=1&position=2&origin=search&related_id=992651
    drawCircle(938, 142, 12, align='center', fill=rgb(238, 241, 247), opacity=minusOpacity)
    drawImage(CMUImage(minus), 938, 142, height=24, width=24, align='center')
    if hours == 0:
        drawLabel(f'{minutes} min', 1000, 142, align='center', size=17, font='DM Sans 36pt')
    elif minutes == 0:
        drawLabel(f'{hours} hrs', 1000, 142, align='center', size=17, font='DM Sans 36pt')
    else:
        drawLabel(f'{hours} hrs {minutes} min', 1000, 142, align='center', size=17, font='DM Sans 36pt')
    drawDateButtons(app.splitEventDayButtonList)
    drawLabel('Deadline', 810, 185, fill=rgb(167, 173, 173), size=25, align='left', font='DM Sans')
    drawRect(973, 185, 110, 35, align='center', fill=deadlineFill)
    drawLabel(deadline, 973, 185, align='center', size=25, font='DM Sans')
    drawLabel('on', 1035, 188, align='left', fill=rgb(167, 173, 173), size=25, font='DM Sans')

def getCurrentDay(number):
    if number == 0:
        return 'Monday'
    elif number == 1:
        return 'Tuesday'
    elif number == 2:
        return 'Wednesday'
    elif number == 3:
        return 'Thursday'
    elif number == 4:
        return 'Friday'
    elif number == 5:
        return 'Saturday'
    else:
        return 'Sunday'
    
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
    
def generateWeeklyEvents(app):
    app.weeklyEvents = dict()
    for dates in app.weeklyDateList:
        app.weeklyEvents[dates] = []
        for habits in app.habitsSet:
            if getCurrentDay(dates.weekday()) in habits.days:
                app.weeklyEvents[dates].append(habits)
        for singleEventTasks in app.singleEventTasks:
            if dates == singleEventTasks.date:
                app.weeklyEvents[dates].append(singleEventTasks)
        for splitEventTasks in app.splitTaskWorkSessions:
            for (startTime, endTime) in app.splitTaskWorkSessions[splitEventTasks]:
                if dates == startTime.date():
                    app.weeklyEvents[dates].append((startTime, endTime))

def getDailyEvents(app, currDay):
    dailyEvents = []
    for habits in app.habitsSet:
        if getCurrentDay(currDay.weekday()) in habits.days:
            dailyEvents.append(habits)
    for singleEventTasks in app.singleEventTasks:
        if currDay == singleEventTasks.date:
            dailyEvents.append(singleEventTasks)
    for splitEventTasks in app.splitTaskWorkSessions:
        for (startTime, endTime) in app.splitTaskWorkSessions[splitEventTasks]:
            if currDay == startTime.date():
                dailyEvents.append((startTime, endTime))
    return dailyEvents

def drawCalendarEvents(app):
    xCoord = 176
    for dates in app.weeklyEvents:
        for event in app.weeklyEvents[dates]:
            startY = 0
            endY = 0
            yCoord = 156
            if isinstance(event, tuple):
                splitTask = findSplitTask(app, event)
                (startTime, endTime) = event
                for i in range(len(app.shownTimes)-1):
                    if app.shownTimes[i].time() < startTime.time() < app.shownTimes[i+1].time() and startY == 0:
                        startY = yCoord + (startTime.minute/60)*78
                    elif app.shownTimes[i].time() == startTime.time() and startY == 0:
                        startY = yCoord
                    elif app.shownTimes[i+1].time() == startTime.time() and startY == 0:
                        startY = yCoord+78
                    if app.shownTimes[i].time() < endTime.time() < app.shownTimes[i+1].time() and endY == 0:
                        endY = yCoord + (endTime.minute/60)*78
                    elif app.shownTimes[i].time() == endTime.time() and endY == 0:
                        endY = yCoord
                    elif app.shownTimes[i+1].time() == endTime.time() and endY == 0:
                        endY = yCoord+78
                    if startY != 0 and endY != 0:
                        break
                    yCoord += 78
                if splitTask != None:
                    if '|' in splitTask.fill:
                        colors = splitTask.fill.split('|')
                    else:
                        colors = splitTask.fill.split(',')
                    r = int(colors[0])
                    g = int(colors[1])
                    b = int(colors[2])
                    if startY != 0 and endY == 0 and startY != 780:
                        if 780-startY < 30:
                            if 780-startY < 15:
                                drawRect(xCoord, startY, 170, 15, fill=rgb(r, g, b))
                            else:
                                drawRect(xCoord, startY, 170, 780-startY, fill=rgb(r, g, b))
                            drawLabel(splitTask.name, xCoord+5, startY+7.5, align='left', fill='white', font='DM Sans')
                            if startTime.time().hour > 11:
                                value = 'pm'
                            else:
                                value = 'am'
                            if startTime.time().minute == 0:
                                minute = '00'
                            elif startTime.time().minute < 10:
                                minute = '0' + str(startTime.time().minute)
                            else:
                                minute = str(startTime.time().minute)
                            if startTime.time().hour == 12:
                                hour = '12'
                            else:
                                hour = str((startTime.time().hour)%12)
                            drawLabel(hour + ':' + minute + value, xCoord+167, startY+7.5, align='right', fill='white', font='DM Sans 36pt')
                        else:
                            drawRect(xCoord, startY, 170, 780-startY, fill=rgb(r, g, b))
                            if startTime.time().hour > 11:
                                startValue = 'pm'
                            else:
                                startValue = 'am'
                            if startTime.time().minute == 0:
                                startMinute = '00'
                            elif startTime.time().minute < 10:
                                startMinute = '0' + str(startTime.time().minute)
                            else:
                                startMinute = str(startTime.time().minute)
                            if endTime.time().hour > 11:
                                endValue = 'pm'
                            else:
                                endValue = 'am'
                            if endTime.time().minute == 0:
                                endMinute = '00'
                            elif endTime.time().minute < 10:
                                endMinute = '0' + str(endTime.time().minute)
                            else:
                                endMinute = str(endTime.time().minute)
                            if startTime.time().hour == 12:
                                startHour = '12'
                            else:
                                startHour = str((startTime.time().hour)%12)
                            if endTime.time().hour == 12:
                                endHour = '12'
                            else:
                                endHour = str((endTime.time().hour)%12)
                            labelValue = startHour + ':' + startMinute + startValue + ' to ' + endHour + ':' + endMinute + endValue
                            if startY+12 > 156:
                                drawLabel(splitTask.name, xCoord+5, startY+12, align='left', fill='white', font='DM Sans', size=20)
                                drawLabel(labelValue, xCoord+5, startY+30, align='left', fill='white', font='DM Sans 36pt')
                    elif startY == 0 and endY != 0 and endY != 156:
                        if endY-156 < 30:
                            if endY-156 < 15:
                                drawRect(xCoord, 156, 170, 15, fill=rgb(r, g, b))
                            else:
                                drawRect(xCoord, 156, 170, endY-156, fill=rgb(r, g, b))
                            if startTime.time().hour > 11:
                                value = 'pm'
                            else:
                                value = 'am'
                            if startTime.time().minute == 0:
                                minute = '00'
                            elif startTime.time().minute < 10:
                                minute = '0' + str(startTime.time().minute)
                            else:
                                minute = str(startTime.time().minute)
                            if startTime.time().hour == 12:
                                hour = '12'
                            else:
                                hour = str((startTime.time().hour)%12)
                            if startY+7.5 > 156:
                                drawLabel(splitTask.name, xCoord+5, startY+7.5, align='left', fill='white', font='DM Sans')
                                drawLabel(hour + ':' + minute + value, xCoord+167, startY+7.5, align='right', fill='white', font='DM Sans 36pt')
                        else:
                            drawRect(xCoord, 156, 170, endY-156, fill=rgb(r, g, b))
                            if startTime.time().hour > 11:
                                startValue = 'pm'
                            else:
                                startValue = 'am'
                            if startTime.time().minute == 0:
                                startMinute = '00'
                            else:
                                startMinute = str(startTime.time().minute)
                            if endTime.time().hour > 11:
                                endValue = 'pm'
                            else:
                                endValue = 'am'
                            if endTime.time().minute == 0:
                                endMinute = '00'
                            elif endTime.time().minute < 10:
                                endMinute = '0' + str(endTime.time().minute)
                            else:
                                endMinute = str(endTime.time().minute)
                            if startTime.time().hour == 12:
                                startHour = '12'
                            else:
                                startHour = str((startTime.time().hour)%12)
                            if endTime.time().hour == 12:
                                endHour = '12'
                            else:
                                endHour = str((endTime.time().hour)%12)
                            labelValue = startHour + ':' + startMinute + startValue + ' to ' + endHour + ':' + endMinute + endValue
                            if startY+12 > 156:
                                drawLabel(splitTask.name, xCoord+5, startY+12, align='left', fill='white', font='DM Sans', size=20)
                                drawLabel(labelValue, xCoord+5, startY+30, align='left', fill='white', font='DM Sans 36pt')
                    elif startY != 0 and endY != 0:
                        if endY-startY < 30:
                            if endY-startY < 15:
                                drawRect(xCoord, startY, 170, 15, fill=rgb(r, g, b))
                            else:
                                drawRect(xCoord, startY, 170, endY-startY, fill=rgb(r, g, b))
                            if startTime.time().hour > 11:
                                value = 'pm'
                            else:
                                value = 'am'
                            if startTime.time().minute == 0:
                                minute = '00'
                            elif startTime.time().minute < 10:
                                minute = '0' + str(startTime.time().minute)
                            else:
                                minute = str(startTime.time().minute)
                            if startTime.time().hour == 12:
                                hour = '12'
                            else:
                                hour = str((startTime.time().hour)%12)
                            if startY+7.5 > 156:
                                drawLabel(splitTask.name, xCoord+5, startY+7.5, align='left', fill='white', font='DM Sans')
                                drawLabel(hour + ':' + minute + value, xCoord+167, startY+7.5, align='right', fill='white', font='DM Sans 36pt')
                        else:
                            drawRect(xCoord, startY, 170, endY-startY, fill=rgb(r, g, b))
                            if startTime.time().hour > 11:
                                startValue = 'pm'
                            else:
                                startValue = 'am'
                            if startTime.time().minute == 0:
                                startMinute = '00'
                            else:
                                startMinute = str(startTime.time().minute)
                            if endTime.time().hour > 11:
                                endValue = 'pm'
                            else:
                                endValue = 'am'
                            if endTime.time().minute == 0:
                                endMinute = '00'
                            elif endTime.time().minute < 10:
                                endMinute = '0' + str(endTime.time().minute)
                            else:
                                endMinute = str(endTime.time().minute)
                            if startTime.time().hour == 12:
                                startHour = '12'
                            else:
                                startHour = str((startTime.time().hour)%12)
                            if endTime.time().hour == 12:
                                endHour = '12'
                            else:
                                endHour = str((endTime.time().hour)%12)
                            labelValue = startHour + ':' + startMinute + startValue + ' to ' + endHour + ':' + endMinute + endValue
                            if startY+12 > 156:
                                drawLabel(splitTask.name, xCoord+5, startY+12, align='left', fill='white', font='DM Sans', size=20)
                                drawLabel(labelValue, xCoord+5, startY+30, align='left', fill='white', font='DM Sans 36pt')
            elif isinstance(event, Habit) or isinstance(event, SingleEvent):
                for i in range(len(app.shownTimes)-1):
                    if app.shownTimes[i].time() < event.startTime.time() < app.shownTimes[i+1].time() and startY == 0:
                        startY = yCoord + (event.startTime.minute/60)*78
                    elif app.shownTimes[i].time() == event.startTime.time() and startY == 0:
                        startY = yCoord
                    elif app.shownTimes[i+1].time() == event.startTime.time() and startY == 0:
                        startY = yCoord+78
                    if app.shownTimes[i].time() < event.endTime.time() < app.shownTimes[i+1].time() and endY == 0:
                        endY = yCoord + (event.endTime.minute/60)*78
                    elif app.shownTimes[i].time() == event.endTime.time() and endY == 0:
                        endY = yCoord
                    elif app.shownTimes[i+1].time() == event.endTime.time() and endY == 0:
                        endY = yCoord+78
                    if startY != 0 and endY != 0:
                        break
                    yCoord += 78
                if '|' in event.fill:
                    colors = event.fill.split('|')
                else:
                    colors = event.fill.split(',')
                r = int(colors[0])
                g = int(colors[1])
                b = int(colors[2])
                if startY != 0 and endY == 0 and startY != 780:
                    if 780-startY < 30:
                        if 780-startY < 15:
                            drawRect(xCoord, startY, 170, 15, fill=rgb(r, g, b))
                        else:
                            drawRect(xCoord, startY, 170, 780-startY, fill=rgb(r, g, b))
                        drawLabel(event.name, xCoord+5, startY+7.5, align='left', fill='white', font='DM Sans')
                        if event.startTime.time().hour > 11:
                            value = 'pm'
                        else:
                            value = 'am'
                        if event.startTime.time().minute == 0:
                            minute = '00'
                        elif event.startTime.time().minute < 10:
                            minute = '0' + str(event.startTime.time().minute)
                        else:
                            minute = str(event.startTime.time().minute)
                        if event.startTime.time().hour == 12:
                            hour = '12'
                        else:
                            hour = str((event.startTime.time().hour)%12)
                        if startY+7.5 > 156:
                            drawLabel(event.name, xCoord+5, startY+7.5, align='left', fill='white', font='DM Sans')
                            drawLabel(hour + ':' + minute + value, xCoord+167, startY+7.5, align='right', fill='white', font='DM Sans 36pt')
                    else:
                        drawRect(xCoord, startY, 170, 780-startY, fill=rgb(r, g, b))
                        if event.startTime.time().hour > 11:
                            startValue = 'pm'
                        else:
                            startValue = 'am'
                        if event.startTime.time().minute == 0:
                            startMinute = '00'
                        elif event.startTime.time().minute < 10:
                            startMinute = '0' + str(event.startTime.time().minute)
                        else:
                            startMinute = str(event.startTime.time().minute)
                        if event.endTime.time().hour > 11:
                            endValue = 'pm'
                        else:
                            endValue = 'am'
                        if event.endTime.time().minute == 0:
                            endMinute = '00'
                        elif event.endTime.time().minute < 10:
                            endMinute = '0' + str(event.endTime.time().minute)
                        else:
                            endMinute = str(event.endTime.time().minute)
                        if event.startTime.time().hour == 12:
                            startHour = '12'
                        else:
                            startHour = str((event.startTime.time().hour)%12)
                        if event.endTime.time().hour == 12:
                            endHour = '12'
                        else:
                            endHour = str((event.endTime.time().hour)%12)
                        labelValue = startHour + ':' + startMinute + startValue + ' to ' + endHour + ':' + endMinute + endValue
                        if startY+12 > 165:
                            drawLabel(event.name, xCoord+5, startY+12, align='left', fill='white', font='DM Sans', size=20)
                            drawLabel(labelValue, xCoord+5, startY+30, align='left', fill='white', font='DM Sans 36pt')
                elif startY == 0 and endY != 0 and endY != 156:
                    if endY-156 < 30:
                        if endY-156 < 15:
                            drawRect(xCoord, 156, 170, 15, fill=rgb(r, g, b))
                        else:
                            drawRect(xCoord, 156, 170, endY-156, fill=rgb(r, g, b))
                        if event.startTime.time().hour > 11:
                            value = 'pm'
                        else:
                            value = 'am'
                        if event.startTime.time().minute == 0:
                            minute = '00'
                        elif event.startTime.time().minute < 10:
                            minute = '0' + str(event.startTime.time().minute)
                        else:
                            minute = str(event.startTime.time().minute)
                        if event.startTime.time().hour == 12:
                            hour = '12'
                        else:
                            hour = str((event.startTime.time().hour)%12)
                        if startY+7.5 > 156:
                            drawLabel(event.name, xCoord+5, startY+7.5, align='left', fill='white', font='DM Sans')
                            drawLabel(hour + ':' + minute + value, xCoord+167, startY+7.5, align='right', fill='white', font='DM Sans 36pt')
                    else:
                        drawRect(xCoord, 156, 170, endY-156, fill=rgb(r, g, b))
                        if event.startTime.time().hour > 11:
                            startValue = 'pm'
                        else:
                            startValue = 'am'
                        if event.startTime.time().minute == 0:
                            startMinute = '00'
                        elif event.startTime.time().minute < 10:
                            startMinute = '0' + str(event.startTime.time().minute)
                        else:
                            startMinute = str(event.startTime.time().minute)
                        if event.endTime.time().hour > 11:
                            endValue = 'pm'
                        else:
                            endValue = 'am'
                        if event.endTime.time().minute == 0:
                            endMinute = '00'
                        elif event.endTime.time().minute < 10:
                            endMinute = '0' + str(event.endTime.time().minute)
                        else:
                            endMinute = str(event.endTime.time().minute)
                        if event.startTime.time().hour == 12:
                            startHour = '12'
                        else:
                            startHour = str((event.startTime.time().hour)%12)
                        if event.endTime.time().hour == 12:
                            endHour = '12'
                        else:
                            endHour = str((event.endTime.time().hour)%12)
                        labelValue = startHour + ':' + startMinute + startValue + ' to ' + endHour + ':' + endMinute + endValue
                        if startY+12 > 156:
                            drawLabel(event.name, xCoord+5, startY+12, align='left', fill='white', font='DM Sans', size=20)
                            drawLabel(labelValue, xCoord+5, startY+30, align='left', fill='white', font='DM Sans 36pt')
                elif startY != 0 and endY != 0:
                    if endY-startY < 30:
                        if endY-startY < 15:
                            drawRect(xCoord, startY, 170, 15, fill=rgb(r, g, b))
                        else:
                            drawRect(xCoord, startY, 170, endY-startY, fill=rgb(r, g, b))
                        if event.startTime.time().hour > 11:
                            value = 'pm'
                        else:
                            value = 'am'
                        if event.startTime.time().minute == 0:
                            minute = '00'
                        elif event.startTime.time().minute < 10:
                            minute = '0' + str(event.startTime.time().minute)
                        else:
                            minute = str(event.startTime.time().minute)
                        if event.startTime.time().hour == 12:
                            startHour = '12'
                        else:
                            startHour = str((event.startTime.time().hour)%12)
                        if startY+7.5 > 156:
                            drawLabel(event.name, xCoord+5, startY+7.5, align='left', fill='white', font='DM Sans')
                            drawLabel(startHour + ':' + minute + value, xCoord+167, startY+7.5, align='right', fill='white', font='DM Sans 36pt')
                    else:
                        drawRect(xCoord, startY, 170, endY-startY, fill=rgb(r, g, b))
                        if event.startTime.time().hour > 11:
                            startValue = 'pm'
                        else:
                            startValue = 'am'
                        if event.startTime.time().minute == 0:
                            startMinute = '00'
                        elif event.startTime.time().minute < 10:
                            startMinute = '0' + str(event.startTime.time().minute)
                        else:
                            startMinute = str(event.startTime.time().minute)
                        if event.endTime.time().hour > 11:
                            endValue = 'pm'
                        else:
                            endValue = 'am'
                        if event.endTime.time().minute == 0:
                            endMinute = '00'
                        elif event.endTime.time().minute < 10:
                            endMinute = '0' + str(event.endTime.time().minute)
                        else:
                            endMinute = str(event.endTime.time().minute)
                        if event.startTime.time().hour == 12:
                            startHour = '12'
                        else:
                            startHour = str((event.startTime.time().hour)%12)
                        if event.endTime.time().hour == 12:
                            endHour = '12'
                        else:
                            endHour = str((event.endTime.time().hour)%12)
                        labelValue = startHour + ':' + startMinute + startValue + ' to ' + endHour + ':' + endMinute + endValue
                        if startY+12 > 156:
                            drawLabel(event.name, xCoord+5, startY+12, align='left', fill='white', font='DM Sans', size=20)
                            drawLabel(labelValue, xCoord+5, startY+30, align='left', fill='white', font='DM Sans 36pt')
        xCoord += 170

def findSplitTask(app, event):
    for keys in app.splitTaskWorkSessions:
        if event in app.splitTaskWorkSessions[keys]:
            return keys

def generateWorkSessions(app):
    iterationTasks = copy.copy(app.splitTasks)
    for events in iterationTasks:
        availableDays = findAvailableDays(app, [], events.date - timedelta(days=1), getDurationEachDay(events.durationHours*60 + events.durationMinutes, events.daysTillDue))
        if availableDays != None:
            app.splitTaskWorkSessions[events] = availableDays

def getDurationEachDay(duration, days):
    durationsList = []
    for i in range(days):
        durationsList.append(duration//days)
    if sum(durationsList) != duration:
        durationsList[-1] += duration-sum(durationsList)
    return durationsList

def findAvailableDays(app, currSolution, currDay, durationEachDay):
    if durationEachDay == []:
        return currSolution
    else:
        for startTime in getFormattedTimes(currDay):
            if canAdd(app, startTime, durationEachDay[-1], currDay):
                temp = durationEachDay.pop()
                currDay -= timedelta(days=1)
                currSolution.append((startTime, startTime+timedelta(hours=temp//60, minutes=temp%60)))
                solution = findAvailableDays(app, currSolution, currDay, durationEachDay)
                if solution != None:
                    return solution
                durationEachDay.append(temp)
                currDay += timedelta(days=1)
                currSolution.pop()
        return None

def canAdd(app, startTime, duration, currDay):
    dailyEvents = getDailyEvents(app, currDay)
    for event in dailyEvents:
        if isinstance(event, Habit) or isinstance(event, SingleEvent):
            if event.startTime.time() <= (startTime+timedelta(hours=duration//60, minutes=duration%60)).time() <= event.endTime.time():
                return False
            elif event.startTime.time() <= startTime.time() <= event.endTime.time():
                return False
            elif event.startTime.time() <= (startTime - timedelta(minutes=10)).time() <= event.endTime.time():
                return False
            elif startTime.time() <= event.startTime.time() <= (startTime+timedelta(hours=duration//60, minutes=duration%60)).time():
                return False
            elif startTime.time() <= event.endTime.time() <= (startTime+timedelta(hours=duration//60, minutes=duration%60)).time():
                return False
            elif (startTime+timedelta(hours=duration//60, minutes=duration%60)).date() > currDay:
                return False
        elif isinstance(event, tuple):
            (splitStartTime, splitEndTime) = event
            if startTime.time() == splitStartTime.time() and (startTime+timedelta(hours=duration//60, minutes=duration%60)).time() == splitEndTime.time():
                return True
            elif splitStartTime.time() <= (startTime+timedelta(hours=duration//60, minutes=duration%60)).time() <= splitEndTime.time():
                return False
            elif splitStartTime.time() <= startTime.time() <= splitEndTime.time():
                return False
            elif splitStartTime.time() <= (startTime - timedelta(minutes=10)).time() <= splitEndTime.time():
                return False
            elif startTime.time() <= splitStartTime.time() <= (startTime+timedelta(hours=duration//60, minutes=duration%60)).time():
                return False
            elif startTime.time() <= splitEndTime.time() <= (startTime+timedelta(hours=duration//60, minutes=duration%60)).time():
                return False
            elif (startTime+timedelta(hours=duration//60, minutes=duration%60)).date() > currDay:
                return False
    return True       
    
class TaskNameTextField:

    def __init__(self, x, y, width, height, value, inTextField):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.value = value
        self.inTextField = inTextField
        self.timer = 0

    def addToField(self, key):
        self.value = self.value[:-1] + key + '|'

    def removeFromField(self):
        self.value = self.value[:-2] + '|'

    def checkForPress(self, mouseX, mouseY):
        if self.x <= mouseX <= self.x+self.width and self.y <= mouseY <= self.y+self.height:
            self.timer = 8
            self.inTextField = True
        else:
            self.timer = 0
            self.value = self.value.replace('|', '')
            self.inTextField = False

class TimeTextField:

    def __init__(self, x, y, width, height, value, fill, inTextField):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.value = value
        self.fill = fill
        self.inTextField = inTextField
        self.timer = 0
        self.legal = True

    def addToField(self, key):
        self.value = self.value[:-1] + key + '|'

    def removeFromField(self):
        self.value = self.value[:-2] + '|'

    def checkForPress(self, mouseX, mouseY):
        if self.x <= mouseX <= self.x+self.width and self.y <= mouseY <= self.y+self.height:
            self.timer = 8
            self.inTextField = True
        else:
            self.timer = 0
            self.value = self.value.replace('|', '')
            self.inTextField = False

    def checkHoveringOver(self, mouseX, mouseY):
        if self.x <= mouseX <= self.x+self.width and self.y <= mouseY <= self.y+self.height and self.legal:
            self.fill = rgb(238, 241, 247)
        elif self.legal:
            self.fill = 'white'

class Button:

    def __init__(self, x, y, width, height, value):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.value = value
        self.opacity = 0
        self.onButton = False

    def checkForPress(self, mouseX, mouseY):
        if self.x <= mouseX <= self.x+self.width and self.y <= mouseY <= self.y+self.height:
            self.value = True

    def checkForMenuButtonPress(self, mouseX, mouseY):
        if self.x <= mouseX <= self.x+self.width and self.y <= mouseY <= self.y+self.height and self.value == False:
            for buttons in app.taskBarButtons:
                if buttons.value == True:
                    buttons.value = False
            self.value = True

    def checkForCheckboxPress(self, mouseX, mouseY):
        if self.x <= mouseX <= self.x+self.width and self.y <= mouseY <= self.y+self.height:
            self.value = not self.value
            app.selectedDate = None

    def checkOnButton(self, mouseX, mouseY):
        if self.x <= mouseX <= self.x+self.width and self.y <= mouseY <= self.y+self.height:
            self.onButton = True
        else:
            self.onButton = False

class DateButton:

    def __init__(self, x, y, width, height, value):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.value = value
        self.selected = False

    def checkForPress(self, mouseX, mouseY):
        if self.x <= mouseX <= self.x+self.width and self.y <= mouseY <= self.y+self.height:
            self.selected = not self.selected
        else:
            if self in app.singleEventDayButtonList:
                for buttons in app.singleEventDayButtonList:
                    if buttons.x <= mouseX <= buttons.x+buttons.width and buttons.y <= mouseY <= buttons.y+buttons.height:
                        self.selected = False
            else:
                for buttons in app.splitEventDayButtonList:
                    if buttons.x <= mouseX <= buttons.x+buttons.width and buttons.y <= mouseY <= buttons.y+buttons.height:
                        self.selected = False
    
    def checkForMultiPress(self, mouseX, mouseY):
        if self.x <= mouseX <= self.x+self.width and self.y <= mouseY <= self.y+self.height:
            self.selected = not self.selected

class SingleEvent:

    def __init__(self, startTime, endTime, date, name, fill):
        self.startTime = startTime
        self.endTime = endTime
        self.date = date
        self.name = name
        self.fill = fill

class SplitEvent:

    def __init__(self, deadline, durationMinutes, durationHours, date, name, fill):
        self.deadline = deadline
        self.durationMinutes = durationMinutes
        self.durationHours = durationHours
        self.date = date
        self.name = name
        self.fill = fill
        ### Code taken from https://stackoverflow.com/questions/8419564/difference-between-two-dates-in-python ###
        self.daysTillDue = abs(self.date-app.currentDate).days - 1
        ##########################################################################################################
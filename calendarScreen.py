from datetime import date, timedelta, datetime
from cmu_graphics import*
from PIL import Image
from habits import*

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
    generateWorkSessions(app)

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

def getFormattedTimes(app, currDay):
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

def drawSingleEventMenu(startTime, endTime, currentDate, buttonNum, rect1Fill, rect2Fill):
    drawRect(810, 135, 130, 40, fill=rect1Fill)
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
    ##### Code from https://stackoverflow.com/questions/33076617/how-to-validate-time-format #####
    try:
        currentTime = datetime.strptime(app.startTime, timeFormat)
    except ValueError:
        app.rect1Fill = rgb(255, 204, 203)
    ##############################################################################################
    if '|' in app.endTime:
        timeFormat = '%I:%M%p|'
    else:
        timeFormat = '%I:%M%p'
    ##### Code from https://stackoverflow.com/questions/33076617/how-to-validate-time-format #####
    try:
        currentTime = datetime.strptime(app.endTime, timeFormat)
    except ValueError:
        app.rect2Fill = rgb(255, 204, 203)
    ##############################################################################################
    if '|' in app.habitStartTime:
        timeFormat = '%I:%M%p|'
    else:
        timeFormat = '%I:%M%p'
    ##### Code from https://stackoverflow.com/questions/33076617/how-to-validate-time-format #####
    try:
        currentTime = datetime.strptime(app.habitStartTime, timeFormat)
    except ValueError:
        app.rect3Fill = rgb(255, 204, 203)
    ##############################################################################################
    if '|' in app.habitEndTime:
        timeFormat = '%I:%M%p|'
    else:
        timeFormat = '%I:%M%p'
    ##### Code from https://stackoverflow.com/questions/33076617/how-to-validate-time-format #####
    try:
        currentTime = datetime.strptime(app.habitEndTime, timeFormat)
    except ValueError:
        app.rect4Fill = rgb(255, 204, 203)
    ##############################################################################################

def checkDeadlineLegality(app):
    if '|' in app.deadline:
        timeFormat = '%I:%M%p|'
    else:
        timeFormat = '%I:%M%p'
    ##### Code from https://stackoverflow.com/questions/33076617/how-to-validate-time-format #####
    try:
        currentTime = datetime.strptime(app.deadline, timeFormat)
    except ValueError:
        app.deadlineFill = rgb(255, 204, 203)
    ##############################################################################################

def isLegalTime(app):
    startTime = app.startTime.replace('|', '')
    endTime = app.endTime.replace('|', '')
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
    
def isLegalDeadline(app):
    if app.selectedDate == app.currentDate:
        time = app.deadline.replace('|', '')
        ### strptime from https://www.programiz.com/python-programming/datetime/strptime ###
        deadlineTime = datetime.strptime(time, '%I:%M%p')
        ####################################################################################
        if (deadlineTime-timedelta(hours=app.durationHours, minutes=app.durationMinutes)).time() <= app.currentTime.time():
            app.deadlineFill = rgb(255, 204, 203)
            return False
    return True

def checkInTextField(app):
    if app.taskNameTextField.inTextField:
        if app.taskNameTextField.timer == 8 and (app.taskNameTextField.value == '' or app.taskNameTextField.value[-1] != '|'):
            app.taskNameTextField.value += '|'
        app.taskNameTextField.timer += 1
        if app.taskNameTextField.timer == 16:
            app.taskNameTextField.timer = 0
            app.taskNameTextField.value = app.taskNameTextField.value.replace('|', '')
    else:
        if 8 <= app.taskNameTextField.timer <= 15 and '|' in app.taskNameTextField.value:
            app.taskNameTextField.value = app.taskNameTextField.value[:-1]
            app.taskNameTextField.timer = 0
    if app.habitsNameTextField.inTextField:
        if app.habitsNameTextField.timer == 8 and (app.habitsNameTextField.value == '' or app.habitsNameTextField.value[-1] != '|'):
            app.habitsNameTextField.value += '|'
        app.habitsNameTextField.timer += 1
        if app.habitsNameTextField.timer == 16:
            app.habitsNameTextField.timer = 0
            app.habitsNameTextField.value = app.habitsNameTextField.value.replace('|', '')
    else:
        if 8 <= app.habitsNameTextField.timer <= 15 and '|' in app.habitsNameTextField.value:
            app.habitsNameTextField.value = app.habitsNameTextField.value[:-1]
            app.habitsNameTextField.timer = 0
    if app.rect3TextField:
        app.rect3Fill = rgb(238, 241, 247)
        if app.cursorTimer == 8 and (app.habitStartTime == '' or app.habitStartTime[-1] != '|'):
            app.habitStartTime += "|"
        app.cursorTimer += 1
        if app.cursorTimer == 16:
            app.cursorTimer = 0
            app.habitStartTime = app.habitStartTime.replace('|', '')
    else:
        if app.habitStartTime != '' and app.habitStartTime[-1] == '|':
            app.habitStartTime = app.habitStartTime[:-1]
            app.cursorTimer = 0
    if app.rect4TextField:
        app.rect4Fill = rgb(238, 241, 247)
        if app.cursorTimer == 8 and (app.habitEndTime == '' or app.habitEndTime[-1] != '|'):
            app.habitEndTime += "|"
        app.cursorTimer += 1
        if app.cursorTimer == 16:
            app.cursorTimer = 0
            app.habitEndTime = app.habitEndTime.replace('|', '')
    else:
        if app.habitEndTime != '' and app.habitEndTime[-1] == '|':
            app.habitEndTime = app.habitEndTime[:-1]
            app.cursorTimer = 0
    if app.singleEventButton.value:
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
    else:
        if app.deadlineTextField:
            app.deadlineFill = rgb(238, 241, 247)
            if app.cursorTimer == 8 and (app.deadline == '' or app.deadline[-1] != '|'):
                app.deadline += '|'
            app.cursorTimer += 1
            if app.cursorTimer == 16:
                app.cursorTimer = 0
                app.deadline = app.deadline.replace('|', '')
        else:
            if app.deadline != '' and app.deadline[-1] == '|':
                app.cursorTimer = 0
                app.deadline = app.deadline[:-1]

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

def drawMultipleEventsMenu(deadline, hours, minutes, currentDate, buttonNum, deadlineFill, plusOpacity, minusOpacity):
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

def checkDeadlinePress(app, mouseX, mouseY):
    if 918 <= mouseX <= 1028 and 168 <= mouseY <= 202:
        app.deadlineTextField = True
    else:
        app.deadlineTextField = False

def checkDurationPress(app, mouseX, mouseY):
    if 918 <= mouseX <= 1068 and 127 <= mouseY <= 157:
        app.durationTextField = True
    else:
        app.durationTextField = False

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
            if app.splitTaskWorkSessions[splitEventTasks] != None:
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
                    drawRect(xCoord, startY, 170, 780-startY, fill=rgb(r, g, b))
                elif startY == 0 and endY != 0 and endY != 156:
                    drawRect(xCoord, 156, 170, endY-156, fill=rgb(r, g, b))
                elif startY != 0 and endY != 0:
                    drawRect(xCoord, startY, 170, endY-startY, fill=rgb(r, g, b))
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
                    drawRect(xCoord, startY, 170, 780-startY, fill=rgb(r, g, b))
                elif startY == 0 and endY != 0 and endY != 156:
                    drawRect(xCoord, 156, 170, endY-156, fill=rgb(r, g, b))
                elif startY != 0 and endY != 0:
                    drawRect(xCoord, startY, 170, endY-startY, fill=rgb(r, g, b))
        xCoord += 170

def findSplitTask(app, event):
    for keys in app.splitTaskWorkSessions:
        if event in app.splitTaskWorkSessions[keys]:
            return keys

def generateWorkSessions(app):
    for events in app.splitTasks:
        app.splitTaskWorkSessions[events] = findAvailableDays(app, [], events.date - timedelta(days=1), getDurationEachDay(events.durationHours*60 + events.durationMinutes, events.daysTillDue))

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
        for startTime in getFormattedTimes(app, currDay):
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
            elif (startTime - timedelta(minutes=10)).time() <= event.endTime.time():
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
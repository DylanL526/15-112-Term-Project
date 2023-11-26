from datetime import date, timedelta, datetime
from cmu_graphics import*
from calendarScreen import*
from tasks import*
from habits import*
from PIL import Image

def onAppStart(app):
    app.background = rgb(246, 248, 252)
    app.currentDate = date.today()
    app.currentTime = datetime.now()
    app.taskName = 'Task name'
    app.singleEventTasks = []
    app.splitTasks = []
    app.taskNameTextField = False
    app.rect1TextField = False
    app.rect2TextField = False
    app.cursorTimer = 8
    app.clickedDayButton = 9
    app.clickedDayButtons = []
    app.dayButtonList = []
    app.selectedDate = None
    app.startTime = '12:00pm'
    app.endTime = '12:00am'
    app.deadline = '12:00pm'
    app.duration = '30 min'
    app.rect1Fill = rgb(255, 255, 255)
    app.rect2Fill = rgb(255, 255, 255)
    app.calendar = True
    app.taskPopUp = False
    app.singleEventChecked = False
    app.tasks = False
    app.habits = False
    app.timeDelta = 0
    app.calendarButtonOpacity = 0
    app.tasksButtonOpacity = 0
    app.habitsButtonOpacity = 0
    app.onCalendarButton = False
    app.onTasksButton = False
    app.onHabitsButton = False

def redrawAll(app):
    drawTaskBar(app)
    if app.calendar == True:
        date = app.currentDate + timedelta(days=app.timeDelta)
        drawCalendar(app.currentDate, getDatesList(date))
        if app.taskPopUp:
            drawTaskPopUp(app.taskName)
            drawCheckBox(app.singleEventChecked)
            if app.singleEventChecked:
                drawSingleEventMenu(app.startTime, app.endTime, app.currentDate, app.clickedDayButton, app.rect1Fill, app.rect2Fill)
            else:
                drawMultipleEventsMenu(app.deadline, app.duration, app.currentDate, app.clickedDayButtons, rgb(238, 241, 247))

def drawTaskBar(app):
    drawRect(0, 0, 78, 78, fill=rgb(25, 28, 28))
    logo = Image.open('Images/hourglasslogo.png')
    drawRect(0, 78, 78, 702, fill=rgb(25, 28, 28))
    drawImage(CMUImage(logo), 39, 39, align='center', width=35, height=35)
    calendar = Image.open('Images/calendar.png')
    drawRect(0, 78, 78, 78, fill=rgb(36, 42, 47), opacity = app.calendarButtonOpacity)
    drawImage(CMUImage(calendar), 39, 117, align='center', width=23, height=23)
    tasks = Image.open('Images/tasks.png')
    drawRect(0, 156, 78, 78, fill=rgb(36, 42, 47), opacity = app.tasksButtonOpacity)
    drawImage(CMUImage(tasks), 39, 195, align='center', width=23, height=23)
    habits = Image.open('Images/habits.png')
    drawRect(0, 234, 78, 78, fill=rgb(36, 42, 47), opacity = app.habitsButtonOpacity)
    drawImage(CMUImage(habits), 39, 273, align='center', width=23, height=23)

def onMouseMove(app, mouseX, mouseY):
    checkOnButton(app, mouseX, mouseY)

def checkOnButton(app, mouseX, mouseY):
    if 0 <= mouseX <= 78:
        if 78 < mouseY < 156:
            app.onCalendarButton = True
        else:
            app.onCalendarButton = False
        if 156 < mouseY < 234:
            app.onTasksButton = True
        else:
            app.onTasksButton = False
        if 234 < mouseY < 312:
            app.onHabitsButton = True
        else:
            app.onHabitsButton = False
    else:
        app.onCalendarButton = False
        app.onTasksButton = False
        app.onHabitsButton = False
    if app.taskPopUp and app.singleEventChecked:
        if 810 <= mouseX <= 940:
            if 135 <= mouseY <= 175:
                app.rect1Fill = rgb(238, 241, 247)
            else:
                app.rect1Fill = rgb(255, 255, 255)
        else:
            app.rect1Fill = rgb(255, 255, 255)
        if 980 <= mouseX <= 1115:
            if 135 <= mouseY <= 175:
                app.rect2Fill = rgb(238, 241, 247)
            else:
                app.rect2Fill = rgb(255, 255, 255)
        else:
            app.rect2Fill = rgb(255, 255, 255)

def onStep(app):
    modifyButtonOpacity(app)
    checkInTextField(app)
    checkTextFieldLegality(app)
    if app.clickedDayButton != 9:
        app.selectedDate = app.dayButtonList[app.clickedDayButton]
    else:
        app.selectedDate = None

def modifyButtonOpacity(app):
    if app.onCalendarButton and app.calendarButtonOpacity < 100:
        app.calendarButtonOpacity += 25
    elif app.onTasksButton and app.tasksButtonOpacity < 100:
        app.tasksButtonOpacity += 25
    elif app.onHabitsButton and app.habitsButtonOpacity < 100:
        app.habitsButtonOpacity += 25
    if app.calendarButtonOpacity != 0 and app.onCalendarButton == False:
        app.calendarButtonOpacity -= 25
    if app.tasksButtonOpacity != 0 and app.onTasksButton == False:
        app.tasksButtonOpacity -= 25
    if app.habitsButtonOpacity != 0 and app.onHabitsButton == False:
        app.habitsButtonOpacity -= 25

def onMousePress(app, mouseX, mouseY):
    checkButtonPress(app, mouseX, mouseY)
    if app.taskPopUp and app.singleEventChecked:
        checkDayButtonPresses(app, mouseX, mouseY)
        checkStartEndTimePresses(app, mouseX, mouseY)

def checkButtonPress(app, mouseX, mouseY):
    if 0 <= mouseX <= 78:
        if 78 < mouseY < 156:
            app.calendar = True
            app.tasks = False
            app.habits = False
        elif 156 < mouseY < 234:
            app.tasks = True
            app.calendar = False
            app.habits = False
        elif 234 < mouseY < 312:
            app.tasks = True
            app.habits = False
            app.calendar = False
    elif 1224 < mouseX < 1352 and app.calendar == True:
        if 13 <= mouseY <= 65:
            app.taskPopUp = True
    if app.taskPopUp:
        if 1095 < mouseX < 1193:
            if 344 < mouseY < 384:
                if app.selectedDate != None and app.rect1Fill != rgb(255, 204, 203) and app.rect2Fill != rgb(255, 204, 203) and 'Task nam' not in app.taskName and isLegalTime(app):
                    app.taskPopUp = False
                elif isLegalTime(app) == False:
                    app.rect1Fill = rgb(255, 204, 203)
                    app.rect2Fill = rgb(255, 204, 203)
        if 1022 <= mouseX <= 1078:
            if 354 <= mouseY <= 374:
                app.taskPopUp = False
                app.taskName = 'Task name'
                app.taskNameTextField = False
                app.cursorTimer = 8
                app.clickedDayButton = 9
                app.startTime = '12:00pm'
                app.endTime = '12:00am'
        if 810 <= mouseX <= 830:
            if 95 <= mouseY <= 115:
                app.singleEventChecked = not app.singleEventChecked
        if 810 <= mouseX <= 1190:
            if 32 <= mouseY <= 60:
                app.cursorTimer = 8
                app.taskNameTextField = True
            else:
                app.taskNameTextField = False
                app.taskName = app.taskName.replace('|', '')
        else:
            app.taskNameTextField = False
            app.taskName = app.taskName.replace('|', '')

def onKeyPress(app, key):
    if key == 'right':
        app.timeDelta += 7
    elif key == 'left':
        app.timeDelta -= 7
    elif app.taskNameTextField:
        app.cursorTimer = 0
        app.taskName = app.taskName.replace('|', '')
        app.taskName += '|'
        if app.taskName == 'Task nam|' or app.taskName == 'Task name|':
            app.taskName = '|'
        if key == 'space' and len(app.taskName) < 21:
            app.taskName = app.taskName[:-1] + ' ' + '|'
        elif key == 'backspace':
            app.taskName = app.taskName[:-2] + '|'
        elif len(app.taskName) < 18:
            app.taskName = app.taskName[:-1] + key + '|'
    elif app.rect1TextField:
        app.cursorTimer = 0
        app.startTime = app.startTime.replace('|', '')
        app.startTime += '|'
        if key == 'backspace':
            app.startTime = app.startTime[:-2] + '|'
        elif len(app.startTime) < 8:
            if key.isdigit() or key == ':' or key == 'p' or key == 'a' or key == 'm':
                app.startTime = app.startTime[:-1] + key + '|'
    elif app.rect2TextField:
        app.cursorTimer = 0
        app.endTime = app.endTime.replace('|', '')
        app.endTime += '|'
        if key == 'backspace':
            app.endTime = app.endTime[:-2] + '|'
        elif len(app.endTime) < 8:
            if key.isdigit() or key == ':' or key == 'p' or key == 'a' or key == 'm':
                app.endTime = app.endTime[:-1] + key + '|'

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

runApp(width = 1366, height = 780)
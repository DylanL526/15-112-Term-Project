from datetime import date, timedelta, datetime
from cmu_graphics import*
from calendarScreen import*
from tasks import*
from habits import*
from stats import*
from PIL import Image
import csv
import random

def onAppStart(app):
    app.background = rgb(246, 248, 252)
    app.currentDate = date.today()
    app.currentTime = datetime.now()
    app.weeklyDateList = getDatesList(app.currentDate)
    app.weeklyEvents = dict()
    app.times = ['1 AM', '2 AM', '3 AM', '4 AM', '5 AM', '6 AM', '7 AM', '8 AM', '9 AM', '10 AM',
             '11 AM', '12 PM', '1 PM', '2 PM', '3 PM', '4 PM', '5 PM', '6 PM', '7 PM', '8 PM',
             '9 PM', '10 PM', '11 PM', '12 AM']
    app.shownTimes = []
    app.index = 8
    app.taskBarButtons = [Button(0, 78, 78, 78, True), Button(0, 156, 78, 78, False), Button(0, 234, 78, 78, False), Button(0, 312, 78, 78, False)]
    app.singleEventTasks = importSingleEventData()
    app.splitTasks = importSplitEventData()
    app.splitTaskWorkSessions = dict()
    app.habitsSet = importHabitData()
    app.taskNameTextField = TaskNameTextField(810, 32, 380, 32, "Task name", False)
    app.habitsNameTextField = TaskNameTextField(810, 32, 380, 32, "Habit name", False)
    app.selectedHabitDays = set()
    app.habitsPopUp = Button(1224, 13, 128, 52, False)
    app.rect1TextField = False
    app.rect2TextField = False
    app.rect3TextField = False
    app.rect4TextField = False
    app.deadlineTextField = False
    app.deadlineFill = rgb(255, 255, 255)
    app.minusButton = Button(926, 130, 24, 24, False)
    app.plusButton = Button(1053, 132, 20, 20, False)
    app.durationTextField = False
    app.cursorTimer = 8
    app.clickedDayButton = 9
    app.singleEventDayButtonList = createDateButtons(810, 195, app.currentDate, 0)
    app.splitEventDayButtonList = createDateButtons(810, 211, app.currentDate, 2)
    app.habitsDayButtonList = createDateButtons(810, 211, None, 0)
    app.cancelButton = Button(1020, 355, 60, 20, False)
    app.scheduleButton = Button(1095, 344, 98, 40, False)
    app.selectedDate = None
    app.startTime = '12:00pm'
    app.endTime = '12:00am'
    app.habitStartTime = '12:00pm'
    app.habitEndTime = '12:00am'
    app.deadline = '12:00pm'
    app.durationMinutes = 15
    app.durationHours = 0
    app.rect1Fill = rgb(255, 255, 255)
    app.rect2Fill = rgb(255, 255, 255)
    app.rect3Fill = rgb(255, 255, 255)
    app.rect4Fill = rgb(255, 255, 255)
    app.colorPalette = ["251| 194| 194|", "203| 120| 118", "180| 207| 164", "98| 134| 108", "244| 211| 94",
                        "246| 123| 69", "100| 85| 123", "187| 166| 221", "160| 197| 227", "50| 118| 155"] # Colors sourced from https://i.pinimg.com/736x/af/34/ec/af34ec62e403206b0c9fce24051f9160.jpg
    app.taskPopUp = Button(1224, 13, 128, 52, False)
    app.singleEventButton = Button(810, 95, 20, 20, False)
    app.timeDelta = 0
    generateWorkSessions(app)
    generateWeeklyEvents(app)
    getShownTimes(app)

### Code from https://www.freecodecamp.org/news/how-to-create-a-csv-file-in-python/ ###

def importHabitData():
    habits = set()
    with open("habitData.csv", 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            habits.add(Habit(row[0], row[1], datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S'), datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S')))
    return habits

def importSingleEventData():
    singleEvents = set()
    with open("singleEventData.csv", 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            color = row[4].replace('|', ',')
            singleEvents.add(SingleEvent(datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S'), datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S'), datetime.strptime(row[2], '%Y-%m-%d').date(), row[3], color))
    return singleEvents

def importSplitEventData():
    splitEvents = set()
    with open("splitEventData.csv", 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            color = row[5].replace('|', ',')
            splitEvents.add(SplitEvent(row[0], int(row[1]), int(row[2]), datetime.strptime(row[3], '%Y-%m-%d').date(), row[4], color))
    return splitEvents

def writeHabitData(name, days, startTime, endTime):
    with open('habitData.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, days, startTime, endTime])

def writeSingleEventData(startTime, endTime, date, name, fill):
    with open('singleEventData.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([startTime, endTime, date, name, fill])

def writeSplitEventData(deadline, durationMinutes, durationHours, date, name, fill):
    with open('splitEventData.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([deadline, durationMinutes, durationHours, date, name, fill])

#######################################################################################

def redrawAll(app):
    drawTaskBar(app)
    if app.taskBarButtons[0].value:
        date = app.currentDate + timedelta(days=app.timeDelta)
        drawCalendar(app, app.currentDate, getDatesList(date))
        if app.taskPopUp.value:
            drawTaskPopUp(app.taskNameTextField.value)
            drawCheckBox(app.singleEventButton.value)
            if app.singleEventButton.value:
                drawSingleEventMenu(app.startTime, app.endTime, app.currentDate, app.clickedDayButton, app.rect1Fill, app.rect2Fill)
            else:
                drawMultipleEventsMenu(app.deadline, app.durationHours, app.durationMinutes, app.currentDate, app.clickedDayButton, app.deadlineFill, app.plusButton.opacity, app.minusButton.opacity)
    elif app.taskBarButtons[1].value:
        drawTasks(app)
    elif app.taskBarButtons[2].value:
        drawHabits(app)
        if app.habitsPopUp.value:
            drawHabitsPopUp(app.habitsNameTextField.value, app.habitStartTime, app.habitEndTime, app.selectedHabitDays, app.rect3Fill, app.rect4Fill)
    elif app.taskBarButtons[3].value:
        drawStats(app)

def drawTaskBar(app):
    drawRect(0, 0, 78, 780, fill=rgb(25, 28, 28))
    for buttons in app.taskBarButtons:
        drawRect(buttons.x, buttons.y, buttons.width, buttons.height, fill=rgb(36, 42, 47), opacity=buttons.opacity)
    logo = Image.open('Images/hourglasslogo.png') # Icon taken from https://www.facebook.com/subtleclassics/
    drawImage(CMUImage(logo), 39, 39, align='center', width=35, height=35)
    calendar = Image.open('Images/calendar.png') # Icon taken from https://www.flaticon.com/free-icon/calendar_3239948?term=calendar&page=1&position=13&origin=search&related_id=3239948
    drawImage(CMUImage(calendar), 39, 117, align='center', width=23, height=23)
    tasks = Image.open('Images/tasks.png') # Icon taken from https://www.flaticon.com/free-icon/clipboard_839860?term=clipboard&page=1&position=2&origin=search&related_id=839860
    drawImage(CMUImage(tasks), 39, 195, align='center', width=23, height=23)
    habits = Image.open('Images/habits.png') # Icon taken from https://www.flaticon.com/free-icon/refresh_10899351?term=habits&page=1&position=29&origin=search&related_id=10899351
    drawImage(CMUImage(habits), 39, 273, align='center', width=23, height=23)
    stats = Image.open('Images/graph.png') # Icon taken from https://www.flaticon.com/free-icon/graph_2567943?term=stats&page=1&position=3&origin=tag&related_id=2567943
    drawImage(CMUImage(stats), 39, 351, align='center', width=23, height=23)

def onMouseMove(app, mouseX, mouseY):
    checkOnButton(app, mouseX, mouseY)

def checkOnButton(app, mouseX, mouseY):
    for buttons in app.taskBarButtons:
        buttons.checkOnButton(mouseX, mouseY)
    if app.taskPopUp.value and app.singleEventButton.value:
        if 810 <= mouseX <= 940 and 135 <= mouseY <= 175 and app.rect1Fill != rgb(255, 204, 203):
                app.rect1Fill = rgb(238, 241, 247)
        elif app.rect1Fill != rgb(255, 204, 203):
            app.rect1Fill = rgb(255, 255, 255)
        if 980 <= mouseX <= 1115 and 135 <= mouseY <= 175 and app.rect2Fill != rgb(255, 204, 203):
                app.rect2Fill = rgb(238, 241, 247)
        elif app.rect2Fill != rgb(255, 204, 203):
            app.rect2Fill = rgb(255, 255, 255)
    elif app.taskPopUp.value:
        if 918 <= mouseX <= 1028 and 168 <= mouseY <= 202:
            app.deadlineFill = rgb(238, 241, 247)
        else:
            app.deadlineFill = rgb(255, 255, 255)
        app.minusButton.checkOnButton(mouseX, mouseY)
        if app.minusButton.onButton:
            app.minusButton.opacity = 100
        else:
            app.minusButton.opacity = 0
        app.plusButton.checkOnButton(mouseX, mouseY)
        if app.plusButton.onButton:
            app.plusButton.opacity = 100
        else:
            app.plusButton.opacity = 0
    elif app.habitsPopUp.value:
        if 806 <= mouseX <= 936 and 121 <= mouseY <= 161:
            app.rect3Fill = rgb(238, 241, 247)
        else:
            app.rect3Fill = rgb(255, 255, 255)
        if 975 <= mouseX <= 1105 and 121 <= mouseY <= 161:
            app.rect4Fill = rgb(238, 241, 247)
        else:
            app.rect4Fill = rgb(255, 255, 255)

def onStep(app):
    modifyButtonOpacity(app)
    checkInTextField(app)
    checkTextFieldLegality(app)
    checkDeadlineLegality(app)

def modifyButtonOpacity(app):
    for buttons in app.taskBarButtons:
        if buttons.onButton and buttons.opacity < 100:
            buttons.opacity += 25
        elif buttons.onButton == False and buttons.opacity > 0:
            buttons.opacity -= 25

def onMousePress(app, mouseX, mouseY):
    checkButtonPress(app, mouseX, mouseY)
    if app.taskPopUp.value and app.singleEventButton.value:
        checkDayButtonPresses(mouseX, mouseY, app.singleEventDayButtonList)
        checkStartEndTimePresses(app, mouseX, mouseY)
    elif app.taskPopUp.value:
        checkDeadlinePress(app, mouseX, mouseY)
        checkDurationPress(app, mouseX, mouseY)
        checkPlusMinusButtons(app, mouseX, mouseY)
        checkDayButtonPresses(mouseX, mouseY, app.splitEventDayButtonList)
    elif app.habitsPopUp.value:
        checkHabitStartEndTimePresses(app, mouseX, mouseY)
        checkDayButtonPresses(mouseX, mouseY, app.habitsDayButtonList)

def checkPlusMinusButtons(app, mouseX, mouseY):
    app.minusButton.checkForPress(mouseX, mouseY)
    if app.minusButton.value:
        app.minusButton.value = False
        if app.durationMinutes == 0:
            app.durationHours -= 1
            app.durationMinutes = 45
        elif app.durationHours == 0 and app.durationMinutes == 15:
            return
        else:
            app.durationMinutes -= 15
    app.plusButton.checkForPress(mouseX, mouseY)
    if app.plusButton.value:
        app.plusButton.value = False
        if app.durationMinutes + 15 != 60:
            app.durationMinutes += 15
        else:
            app.durationHours += 1
            app.durationMinutes = 0

def checkButtonPress(app, mouseX, mouseY):
    for buttons in app.taskBarButtons:
        buttons.checkForMenuButtonPress(mouseX, mouseY)
    if app.taskBarButtons[0].value == True:
        app.taskPopUp.checkForPress(mouseX, mouseY)
    elif app.taskBarButtons[2].value == True:
        app.habitsPopUp.checkForPress(mouseX, mouseY)
    if app.taskPopUp.value and app.singleEventButton.value:
        app.taskNameTextField.checkForPress(mouseX, mouseY)
        app.scheduleButton.checkForPress(mouseX, mouseY)
        if app.scheduleButton.value:
                if app.selectedDate != None and app.rect1Fill != rgb(255, 204, 203) and app.rect2Fill != rgb(255, 204, 203) and 'Task name' not in app.taskNameTextField.value and isLegalTime(app):
                    app.startTime = app.startTime.replace('|', '')
                    app.endTime = app.endTime.replace('|', '')
                    fill = app.colorPalette[random.randrange(10)]
                    app.singleEventTasks.add(SingleEvent(datetime.strptime(app.startTime, '%I:%M%p'), datetime.strptime(app.endTime, '%I:%M%p'), app.selectedDate, app.taskNameTextField.value, fill))
                    writeSingleEventData(datetime.strptime(app.startTime, '%I:%M%p'), datetime.strptime(app.endTime, '%I:%M%p'), app.selectedDate, app.taskNameTextField.value, fill)
                    app.selectedDate = None
                    app.rect1Fill = rgb(255, 255, 255)
                    app.rect2Fill = rgb(255, 255, 255)
                    app.taskNameTextField.value = 'Task name'
                    app.taskNameTextField.inTextField = False
                    app.cursorTimer = 8
                    app.clickedDayButton = 9
                    app.startTime = '12:00pm'
                    app.endTime = '12:00am'
                    app.taskPopUp.value = False
                    generateWorkSessions(app)
                    generateWeeklyEvents(app)
                elif app.rect1Fill != rgb(255, 204, 203) and app.rect2Fill != rgb(255, 204, 203) and isLegalTime(app) == False:
                    app.rect1Fill = rgb(255, 204, 203)
                    app.rect2Fill = rgb(255, 204, 203)
        if 1022 <= mouseX <= 1078:
            if 354 <= mouseY <= 374:
                app.taskPopUp.value = False
                app.taskNameTextField.value = 'Task name'
                app.taskNameTextField.inTextField = False
                app.cursorTimer = 8
                app.clickedDayButton = 9
                app.startTime = '12:00pm'
                app.endTime = '12:00am'
        app.singleEventButton.checkForCheckboxPress(mouseX, mouseY)
    elif app.taskPopUp.value:
        app.cancelButton.checkForPress(mouseX, mouseY)
        app.scheduleButton.checkForPress(mouseX, mouseY)
        app.taskNameTextField.checkForPress(mouseX, mouseY)
        if app.scheduleButton.value:
                if app.selectedDate != None and app.deadlineFill != rgb(255, 204, 203) and 'Task name' not in app.taskNameTextField.value and isLegalDeadline(app):
                    fill = app.colorPalette[random.randrange(10)]
                    app.scheduleButton.value = False
                    app.splitTasks.add(SplitEvent(app.deadline, app.durationMinutes, app.durationHours, app.selectedDate, app.taskNameTextField.value, fill))
                    writeSplitEventData(app.deadline, app.durationMinutes, app.durationHours, app.selectedDate, app.taskNameTextField.value, fill)
                    app.durationMinutes = 15
                    app.durationHours = 0
                    app.deadline = app.deadline.replace('|', '')
                    app.selectedDate = None
                    app.deadlineFill = rgb(255, 255, 255)
                    app.taskNameTextField.value = 'Task name'
                    app.cursorTimer = 8
                    app.clickedDayButton = 9
                    app.taskNameTextField.inTextField = False
                    app.taskPopUp.value = False
                    generateWorkSessions(app)
                    generateWeeklyEvents(app)
        if app.cancelButton.value:
                app.deadline = '12:00pm'
                app.cancelButton.value = False
                app.taskNameTextField.inTextField = False
                app.taskNameTextField.value = "Task name"
                app.cursorTimer = 8
                app.clickedDayButton = 9
                app.durationMinutes = 15
                app.durationHours = 0
                app.taskPopUp.value = False
        app.singleEventButton.checkForCheckboxPress(mouseX, mouseY)
        if 918 <= mouseX <= 1028 and 168 <= mouseY <= 202:
            app.cursorTimer = 8
            app.deadlineTextField = True
        else:
            app.deadlineTextField = False
            app.deadline = app.deadline.replace('|', '')
    if app.habitsPopUp.value:
        app.cancelButton.checkForPress(mouseX, mouseY)
        app.scheduleButton.checkForPress(mouseX, mouseY)
        app.habitsNameTextField.checkForPress(mouseX, mouseY)
        if app.cancelButton.value:
            app.habitsPopUp.value = False
            app.cancelButton.value = False
        if app.scheduleButton.value:
                if app.selectedHabitDays != set() and app.rect3Fill != rgb(255, 204, 203) and app.rect4Fill != rgb(255, 204, 203) and 'Habit name' not in app.habitsNameTextField.value and isLegalHabitTime(app):
                    app.habitStartTime = app.habitStartTime.replace('|', '')
                    app.habitEndTime = app.habitEndTime.replace('|', '')
                    app.habitsSet.add(Habit(app.habitsNameTextField.value, app.selectedHabitDays, datetime.strptime(app.habitStartTime, '%I:%M%p'), datetime.strptime(app.habitEndTime, '%I:%M%p')))
                    writeHabitData(app.habitsNameTextField.value, app.selectedHabitDays, datetime.strptime(app.habitStartTime, '%I:%M%p'), datetime.strptime(app.habitEndTime, '%I:%M%p'))
                    app.habitsNameTextField.value = 'Habit name'
                    app.selectedHabitDays = set()
                    app.rect3Fill = rgb(255, 255, 255)
                    app.rect4Fill = rgb(255, 255, 255)
                    app.habitsPopUp.value = False
                    app.scheduleButton.value = False
                    generateWorkSessions(app)
                    generateWeeklyEvents(app)
                elif app.rect3Fill != rgb(255, 204, 203) and app.rect4Fill != rgb(255, 204, 203) and isLegalHabitTime(app) == False:
                    app.rect3Fill = rgb(255, 204, 203)
                    app.rect4Fill = rgb(255, 204, 203)

def onKeyPress(app, key):
    if app.taskPopUp.value == False:
        if key == 'right':
            app.timeDelta += 7
            app.weeklyDateList = getDatesList(app.currentDate + timedelta(days=app.timeDelta))
            generateWeeklyEvents(app)
            generateWorkSessions(app)
        elif key == 'left':
            app.timeDelta -= 7
            app.weeklyDateList = getDatesList(app.currentDate + timedelta(days=app.timeDelta))
            generateWeeklyEvents(app)
            generateWorkSessions(app)
        elif key == 'up' and app.index > 0:
            app.index -= 1
            getShownTimes(app)
        elif key == 'down' and app.index < 16:
            app.index += 1
            getShownTimes(app)
    elif app.taskNameTextField.inTextField:
        app.taskNameTextField.timer = 0
        app.taskNameTextField.value = app.taskNameTextField.value.replace('|', '') + '|'
        if 'Task name' in app.taskNameTextField.value:
            app.taskNameTextField.value = '|'
        if key == 'space' and len(app.taskNameTextField.value) < 21:
            app.taskNameTextField.addToField(' ')
        elif key == 'backspace':
            app.taskNameTextField.removeFromField()
        elif len(app.taskNameTextField.value) < 18:
            app.taskNameTextField.addToField(key)
    if app.habitsNameTextField.inTextField:
        app.habitsNameTextField.timer = 0
        app.habitsNameTextField.value = app.habitsNameTextField.value.replace('|', '') + '|'
        if 'Habit name' in app.habitsNameTextField.value:
            app.habitsNameTextField.value = '|'
        if key == 'space' and len(app.habitsNameTextField.value) < 21:
            app.habitsNameTextField.addToField(' ')
        elif key == 'backspace':
            app.habitsNameTextField.removeFromField()
        elif len(app.habitsNameTextField.value) < 18:
            app.habitsNameTextField.addToField(key)
    if app.rect1TextField:
        app.cursorTimer = 0
        app.startTime = app.startTime.replace('|', '')
        app.startTime += '|'
        if key == 'backspace':
            app.startTime = app.startTime[:-2] + '|'
        elif len(app.startTime) < 8:
            if key.isdigit() or key == ':' or key == 'p' or key == 'a' or key == 'm':
                app.startTime = app.startTime[:-1] + key + '|'
    if app.rect2TextField:
        app.cursorTimer = 0
        app.endTime = app.endTime.replace('|', '')
        app.endTime += '|'
        if key == 'backspace':
            app.endTime = app.endTime[:-2] + '|'
        elif len(app.endTime) < 8:
            if key.isdigit() or key == ':' or key == 'p' or key == 'a' or key == 'm':
                app.endTime = app.endTime[:-1] + key + '|'
    if app.rect3TextField:
        app.cursorTimer = 0
        app.habitStartTime = app.habitStartTime.replace('|', '')
        app.habitStartTime += '|'
        if key == 'backspace':
            app.habitStartTime = app.habitStartTime[:-2] + '|'
        elif len(app.habitStartTime) < 8:
            if key.isdigit() or key == ':' or key == 'p' or key == 'a' or key == 'm':
                app.habitStartTime = app.habitStartTime[:-1] + key + '|'
    if app.rect4TextField:
        app.cursorTimer = 0
        app.habitEndTime = app.habitEndTime.replace('|', '')
        app.habitEndTime += '|'
        if key == 'backspace':
            app.habitEndTime = app.habitEndTime[:-2] + '|'
        elif len(app.habitEndTime) < 8:
            if key.isdigit() or key == ':' or key == 'p' or key == 'a' or key == 'm':
                app.habitEndTime = app.habitEndTime[:-1] + key + '|'
    if app.deadlineTextField:
        app.cursorTimer = 0
        app.deadline = app.deadline.replace('|', '')
        app.deadline += '|'
        if key == 'backspace':
            app.deadline = app.deadline[:-2] + '|'
        elif len(app.deadline) < 8:
            if key.isdigit() or key == ':' or key == 'p' or key == 'a' or key == 'm':
                app.deadline = app.deadline[:-1] + key + '|'

runApp(width = 1366, height = 780)
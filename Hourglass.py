from datetime import date, timedelta, datetime
from cmu_graphics import*
from calendarScreen import*
from tasks import*
from habits import*
from stats import*
from PIL import Image
import csv
import random
import copy

def onAppStart(app):
    app.background = rgb(246, 248, 252)

    ### General Calendar Variables ###
    app.currentDate = date.today()
    app.currentTime = datetime.now()
    app.weeklyDateList = getDatesList(app.currentDate)
    app.weeklyEvents = dict()
    app.times = ['1 AM', '2 AM', '3 AM', '4 AM', '5 AM', '6 AM', '7 AM', '8 AM', '9 AM', '10 AM',
             '11 AM', '12 PM', '1 PM', '2 PM', '3 PM', '4 PM', '5 PM', '6 PM', '7 PM', '8 PM',
             '9 PM', '10 PM', '11 PM', '12 AM']
    app.shownTimes = []
    app.index = 8
    app.timeDelta = 0
    app.taskBarButtons = [Button(0, 78, 78, 78, True), Button(0, 156, 78, 78, False), Button(0, 234, 78, 78, False), Button(0, 312, 78, 78, False)]
    app.colorPalette = ["251| 194| 194|", "203| 120| 118", "180| 207| 164", "98| 134| 108", "244| 211| 94",
                        "246| 123| 69", "100| 85| 123", "187| 166| 221", "160| 197| 227", "50| 118| 155"] # Colors sourced from https://i.pinimg.com/736x/af/34/ec/af34ec62e403206b0c9fce24051f9160.jpg
    app.colorPaletteCopy = copy.copy(app.colorPalette)

    ### General Pop-Up Variables ###
    app.cancelButton = Button(1020, 355, 60, 20, False)
    app.scheduleButton = Button(1095, 344, 98, 40, False)
    app.selectedDate = None
    app.textFields = []

    ### Single/Split Event Pop-Up Variables ###
    app.taskPopUp = Button(1224, 13, 128, 52, False)
    app.singleEventButton = Button(810, 95, 20, 20, False)
    app.taskNameTextField = TaskNameTextField(810, 32, 380, 32, "Task name", False)
    app.minusButton = Button(926, 130, 24, 24, False)
    app.plusButton = Button(1053, 132, 20, 20, False)
    app.singleEventDayButtonList = createDateButtons(810, 195, app.currentDate, 0)
    app.splitEventDayButtonList = createDateButtons(810, 211, app.currentDate, 2)
    app.startTime = TimeTextField(810, 135, 130, 40, '12:00pm', 'white', False)
    app.endTime = TimeTextField(980, 135, 130, 40, '12:00am', 'white', False)
    app.deadline = TimeTextField(918, 168, 110, 34, '12:00pm', 'white', False)
    app.durationMinutes = 15
    app.durationHours = 0
    app.textFields.append(app.endTime)
    app.textFields.append(app.startTime)
    app.textFields.append(app.deadline)
    app.textFields.append(app.taskNameTextField)
    app.notEnoughTime = False

    ### Habit Pop-Up Variables ###
    app.habitsPopUp = Button(1224, 13, 128, 52, False)
    app.habitsNameTextField = TaskNameTextField(810, 32, 380, 32, "Habit name", False)
    app.selectedHabitDays = set()
    app.habitsDayButtonList = createDateButtons(810, 211, None, 0)
    app.habitStartTime = TimeTextField(806, 121, 130, 40, '12:00pm', 'white', False)
    app.habitEndTime = TimeTextField(975, 121, 130, 40, '12:00am', 'white', False)
    app.textFields.append(app.habitStartTime)
    app.textFields.append(app.habitEndTime)
    app.textFields.append(app.habitsNameTextField)

    ### Single Event Variables ###
    app.singleEventTasks = importSingleEventData()
    app.tasksIndex = 0
    app.taskWidgetCoords = dict()

    ### Split Event Variables ###
    app.splitTasks = importSplitEventData()
    app.splitTaskWorkSessions = dict()

    ### Habit Variables ###
    app.habitsSet = importHabitData()
    app.habitsIndex = 0
    app.habitWidgetCoords = dict()

    ### Functions to be called ###
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
                drawSingleEventMenu(app.startTime.value, app.endTime.value, app.startTime.fill, app.endTime.fill)
            else:
                drawMultipleEventsMenu(app.deadline.value, app.durationHours, app.durationMinutes, app.deadline.fill, app.plusButton.opacity, app.minusButton.opacity)
            if app.notEnoughTime:
                drawLabel('Not enough time', 810, 364, align='left', font='DM Sans', size=17, fill='red')
    elif app.taskBarButtons[1].value:
        drawTasks(app)
    elif app.taskBarButtons[2].value:
        drawHabits(app)
        if app.habitsPopUp.value:
            drawHabitsPopUp(app.habitsNameTextField.value, app.habitStartTime.value, app.habitEndTime.value, app.habitStartTime.fill, app.habitEndTime.fill)
    elif app.taskBarButtons[3].value:
        drawStats(app)

def onStep(app):
    modifyButtonOpacity(app)
    checkInTextField(app)
    checkTextFieldLegality(app)

def onMouseMove(app, mouseX, mouseY):
    checkOnButton(app, mouseX, mouseY)

def onMousePress(app, mouseX, mouseY):
    app.notEnoughTime = False
    checkButtonPress(app, mouseX, mouseY)
    if app.taskPopUp.value and app.singleEventButton.value:
        checkDayButtonPresses(mouseX, mouseY, app.singleEventDayButtonList)
        app.startTime.checkForPress(mouseX, mouseY)
        app.endTime.checkForPress(mouseX, mouseY)
    elif app.taskPopUp.value:
        app.deadline.checkForPress(mouseX, mouseY)
        checkPlusMinusButtons(app, mouseX, mouseY)
        checkDayButtonPresses(mouseX, mouseY, app.splitEventDayButtonList)
    elif app.habitsPopUp.value:
        app.habitStartTime.checkForPress(mouseX, mouseY)
        app.habitEndTime.checkForPress(mouseX, mouseY)
        checkDayButtonPresses(mouseX, mouseY, app.habitsDayButtonList)

def onKeyPress(app, key):
    if key == '~':
        loadSampleData()
        app.singleEventTasks = importSingleEventData()
        app.splitTasks = importSplitEventData()
        app.habitsSet = importHabitData()
        generateWorkSessions(app)
        generateWeeklyEvents(app)
    if app.taskPopUp.value == False:
        if key == 'right' and app.taskBarButtons[0].value:
            app.timeDelta += 7
            app.weeklyDateList = getDatesList(app.currentDate + timedelta(days=app.timeDelta))
            generateWorkSessions(app)
            generateWeeklyEvents(app)
        elif key == 'left' and app.taskBarButtons[0].value:
            app.timeDelta -= 7
            app.weeklyDateList = getDatesList(app.currentDate + timedelta(days=app.timeDelta))
            generateWorkSessions(app)
            generateWeeklyEvents(app)
        elif key == 'up' and app.index > 0 and app.taskBarButtons[0].value:
            app.index -= 1
            getShownTimes(app)
        elif key == 'down' and app.index < 16 and app.taskBarButtons[0].value:
            app.index += 1
            getShownTimes(app)
        elif key == 'down' and app.habitsIndex < len(app.habitsSet)-7 and app.taskBarButtons[2].value:
            app.habitWidgetCoords = dict()
            app.habitsIndex += 1
        elif key == 'up' and app.habitsIndex > 0 and app.taskBarButtons[2].value:
            app.habitWidgetCoords = dict()
            app.habitsIndex -= 1
        elif key == 'up' and app.tasksIndex > 0 and app.taskBarButtons[1].value:
            app.taskWidgetCoords = dict()
            app.tasksIndex -= 1
        elif key == 'down' and app.tasksIndex < (len(app.splitTasks)+len(app.singleEventTasks))-7 and app.taskBarButtons[1].value:
            app.taskWidgetCoords = dict()
            app.tasksIndex += 1
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
    if app.startTime.inTextField:
        app.startTime.timer = 0
        app.startTime.value = app.startTime.value.replace('|', '') + '|'
        if key == 'backspace':
            app.startTime.removeFromField()
        elif len(app.startTime.value) < 8:
            if key.isdigit() or key == ':' or key == 'p' or key == 'a' or key == 'm':
                app.startTime.addToField(key)
    if app.endTime.inTextField:
        app.endTime.timer = 0
        app.endTime.value = app.endTime.value.replace('|', '') + '|'
        if key == 'backspace':
            app.endTime.removeFromField()
        elif len(app.endTime.value) < 8:
            if key.isdigit() or key == ':' or key == 'p' or key == 'a' or key == 'm':
                app.endTime.addToField(key)
    if app.habitStartTime.inTextField:
        app.habitStartTime.timer = 0
        app.habitStartTime.value = app.habitStartTime.value.replace('|', '') + '|'
        if key == 'backspace':
            app.habitStartTime.removeFromField()
        elif len(app.habitStartTime.value) < 8:
            if key.isdigit() or key == ':' or key == 'p' or key == 'a' or key == 'm':
                app.habitStartTime.addToField(key)
    if app.habitEndTime.inTextField:
        app.habitEndTime.timer = 0
        app.habitEndTime.value = app.habitEndTime.value.replace('|', '') + '|'
        if key == 'backspace':
            app.habitEndTime.removeFromField()
        elif len(app.habitEndTime.value) < 8:
            if key.isdigit() or key == ':' or key == 'p' or key == 'a' or key == 'm':
                app.habitEndTime.addToField(key)
    if app.deadline.inTextField:
        app.deadline.timer = 0
        app.deadline.value = app.deadline.value.replace('|', '') + '|'
        if key == 'backspace':
            app.deadline.removeFromField()
        elif len(app.deadline.value) < 8:
            if key.isdigit() or key == ':' or key == 'p' or key == 'a' or key == 'm':
                app.deadline.addToField(key)

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

def checkOnButton(app, mouseX, mouseY):
    for buttons in app.taskBarButtons:
        buttons.checkOnButton(mouseX, mouseY)
    if app.taskPopUp.value and app.singleEventButton.value:
        app.startTime.checkHoveringOver(mouseX, mouseY)
        app.endTime.checkHoveringOver(mouseX, mouseY)
    elif app.taskPopUp.value:
        app.deadline.checkHoveringOver(mouseX, mouseY)
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
        app.habitStartTime.checkHoveringOver(mouseX, mouseY)
        app.habitEndTime.checkHoveringOver(mouseX, mouseY)

def modifyButtonOpacity(app):
    for buttons in app.taskBarButtons:
        if buttons.onButton and buttons.opacity < 100:
            buttons.opacity += 25
        elif buttons.onButton == False and buttons.opacity > 0:
            buttons.opacity -= 25

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

def getRandomColor(app):
    if app.colorPaletteCopy != []:
        fill = app.colorPaletteCopy[random.randrange(len(app.colorPaletteCopy))]
        app.colorPaletteCopy.remove(fill)
    else:
        app.colorPaletteCopy = copy.copy(app.colorPalette)
        fill = app.colorPaletteCopy[random.randrange(len(app.colorPaletteCopy))]
        app.colorPaletteCopy.remove(fill)
    return fill

def checkButtonPress(app, mouseX, mouseY):
    for buttons in app.taskBarButtons:
        buttons.checkForMenuButtonPress(mouseX, mouseY)
    if app.taskBarButtons[0].value:
        generateWeeklyEvents(app)
        app.taskPopUp.checkForPress(mouseX, mouseY)
    elif app.taskBarButtons[1].value:
        checkForTaskTrashPress(app, mouseX, mouseY)
    elif app.taskBarButtons[2].value:
        app.habitsPopUp.checkForPress(mouseX, mouseY)
        checkForHabitTrashPress(app, mouseX, mouseY)
    if app.taskPopUp.value and app.singleEventButton.value:
        app.taskNameTextField.checkForPress(mouseX, mouseY)
        app.cancelButton.checkForPress(mouseX, mouseY)
        app.singleEventButton.checkForCheckboxPress(mouseX, mouseY)
        app.startTime.checkForPress(mouseX, mouseY)
        if app.cancelButton.value:
            app.taskPopUp.value = False
            app.cancelButton.value = False
            app.taskNameTextField.value = 'Task name'
            app.taskNameTextField.inTextField = False
            app.startTime.value = '12:00pm'
            app.endTime.value = '12:00am'
        elif app.startTime.fill != rgb(255, 204, 203) and app.endTime.fill != rgb(255, 204, 203) and isLegalTime(app.startTime.value, app.endTime.value) == False:
            app.scheduleButton.checkForPress(mouseX, mouseY)
            if app.scheduleButton.value:
                app.scheduleButton.value = False
                app.startTime.fill = rgb(255, 204, 203)
                app.endTime.fill = rgb(255, 204, 203)
        elif app.selectedDate != None and app.startTime.fill != rgb(255, 204, 203) and app.endTime.fill != rgb(255, 204, 203) and 'Task name' not in app.taskNameTextField.value and isLegalTime(app.startTime.value, app.endTime.value):
            app.scheduleButton.checkForPress(mouseX, mouseY)
            if app.scheduleButton.value:
                app.scheduleButton.value = False
                app.cancelButton.value = False
                app.startTime.value = app.startTime.value.replace('|', '')
                app.endTime.value = app.endTime.value.replace('|', '')
                fill = getRandomColor(app)
                app.singleEventTasks.add(SingleEvent(datetime.strptime(app.startTime.value, '%I:%M%p'), datetime.strptime(app.endTime.value, '%I:%M%p'), app.selectedDate, app.taskNameTextField.value, fill))
                writeSingleEventData(datetime.strptime(app.startTime.value, '%I:%M%p'), datetime.strptime(app.endTime.value, '%I:%M%p'), app.selectedDate, app.taskNameTextField.value, fill)
                app.selectedDate = None
                app.startTime.fill = 'white'
                app.endTime.fill = 'white'
                app.taskNameTextField.value = 'Task name'
                app.taskNameTextField.inTextField = False
                app.cursorTimer = 8
                app.clickedDayButton = 9
                app.startTime.value = '12:00pm'
                app.endTime.value = '12:00am'
                app.taskPopUp.value = False
                generateWorkSessions(app)
                generateWeeklyEvents(app)
    elif app.taskPopUp.value:
        app.notEnoughTime = False
        app.taskNameTextField.checkForPress(mouseX, mouseY)
        app.cancelButton.checkForPress(mouseX, mouseY)
        app.singleEventButton.checkForCheckboxPress(mouseX, mouseY)
        app.deadline.checkForPress(mouseX, mouseY)
        if app.cancelButton.value:
            app.deadline.value = '12:00pm'
            app.cancelButton.value = False
            app.taskNameTextField.inTextField = False
            app.taskNameTextField.value = "Task name"
            app.durationMinutes = 15
            app.durationHours = 0
            app.taskPopUp.value = False
        elif app.selectedDate != None and app.deadline.fill != rgb(255, 204, 203) and 'Task name' not in app.taskNameTextField.value:
            app.scheduleButton.checkForPress(mouseX, mouseY)
            if app.scheduleButton.value:
                app.scheduleButton.value = False
                if findAvailableDays(app, [], app.selectedDate - timedelta(days=1), getDurationEachDay(app.durationHours*60 + app.durationMinutes, abs(app.selectedDate-app.currentDate).days - 1)) != None:
                    fill = getRandomColor(app)
                    app.splitTasks.add(SplitEvent(app.deadline.value, app.durationMinutes, app.durationHours, app.selectedDate, app.taskNameTextField.value, fill))
                    writeSplitEventData(app.deadline.value, app.durationMinutes, app.durationHours, app.selectedDate, app.taskNameTextField.value, fill)
                    app.durationMinutes = 15
                    app.durationHours = 0
                    app.deadline.value = app.deadline.value.replace('|', '')
                    app.selectedDate = None
                    app.deadline.fill = 'white'
                    app.taskNameTextField.value = 'Task name'
                    app.taskNameTextField.inTextField = False
                    app.taskPopUp.value = False
                    generateWorkSessions(app)
                    generateWeeklyEvents(app)
                else:
                    app.notEnoughTime = True
    if app.habitsPopUp.value:
        app.cancelButton.checkForPress(mouseX, mouseY)
        app.habitsNameTextField.checkForPress(mouseX, mouseY)
        app.habitStartTime.checkForPress(mouseX, mouseY)
        app.habitEndTime.checkForPress(mouseX, mouseY)
        if app.cancelButton.value:
            app.habitsPopUp.value = False
            app.cancelButton.value = False
        elif app.habitStartTime.fill != rgb(255, 204, 203) and app.habitEndTime.fill != rgb(255, 204, 203) and isLegalTime(app.habitStartTime.value, app.habitEndTime.value) == False:
            app.scheduleButton.checkForPress(mouseX, mouseY)
            if app.scheduleButton.value:
                app.scheduleButton.value = False
                app.habitStartTime.fill = rgb(255, 204, 203)
                app.habitEndTime.fill = rgb(255, 204, 203)
        elif app.selectedHabitDays != set() and app.habitStartTime.fill != rgb(255, 204, 203) and app.habitEndTime.fill != rgb(255, 204, 203) and 'Habit name' not in app.habitsNameTextField.value and isLegalTime(app.habitStartTime.value, app.habitEndTime.value):
            app.scheduleButton.checkForPress(mouseX, mouseY)
            if app.scheduleButton.value:
                app.habitStartTime.value = app.habitStartTime.value.replace('|', '')
                app.habitEndTime.value = app.habitEndTime.value.replace('|', '')
                app.habitsSet.add(Habit(app.habitsNameTextField.value, app.selectedHabitDays, datetime.strptime(app.habitStartTime.value, '%I:%M%p'), datetime.strptime(app.habitEndTime.value, '%I:%M%p')))
                writeHabitData(app.habitsNameTextField.value, app.selectedHabitDays, datetime.strptime(app.habitStartTime.value, '%I:%M%p'), datetime.strptime(app.habitEndTime.value, '%I:%M%p'))
                app.habitsNameTextField.value = 'Habit name'
                app.selectedHabitDays = set()
                app.habitStartTime.fill = 'white'
                app.habitEndTime.fill = 'white'
                app.habitsPopUp.value = False
                app.scheduleButton.value = False
                generateWorkSessions(app)
                generateWeeklyEvents(app)

runApp(width = 1366, height = 780)
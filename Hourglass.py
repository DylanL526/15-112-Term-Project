from datetime import date, timedelta
from cmu_graphics import*
from calendarScreen import*
from tasks import*
from habits import*
import PIL.Image

def onAppStart(app):
    app.background = rgb(246, 248, 252)
    app.currentDate = date.today()
    app.calendar = True
    app.tasks = False
    app.habits = False
    app.calendarButtonOpacity = 0
    app.tasksButtonOpacity = 0
    app.habitsButtonOpacity = 0
    app.onCalendarButton = False
    app.onTasksButton = False
    app.onHabitsButton = False

def redrawAll(app):
    drawTaskBar(app)
    if app.calendar == True:
        drawCalendar()

def drawTaskBar(app):
    drawRect(0, 0, 108, 1080, fill=rgb(25, 28, 28))
    logo = PIL.Image.open('Images/hourglasslogo.png')
    logo = logo.resize((54,54))
    drawImage(CMUImage(logo), 54, 54, align='center')
    calendar = PIL.Image.open('Images/calendar.png')
    calendar = calendar.resize((32, 32))
    drawRect(0, 108, 108, 108, fill=rgb(36, 42, 47), opacity = app.calendarButtonOpacity)
    drawImage(CMUImage(calendar), 54, 162, align='center')
    tasks = PIL.Image.open('Images/tasks.png')
    tasks = tasks.resize((35, 35))
    drawRect(0, 216, 108, 108, fill=rgb(36, 42, 47), opacity = app.tasksButtonOpacity)
    drawImage(CMUImage(tasks), 54, 270, align='center')
    habits = PIL.Image.open('Images/habits.png')
    habits = habits.resize((32, 32))
    drawRect(0, 324, 108, 108, fill=rgb(36, 42, 47), opacity = app.habitsButtonOpacity)
    drawImage(CMUImage(habits), 54, 378, align='center')

def onMouseMove(app, mouseX, mouseY):
    checkOnButton(app, mouseX, mouseY)

def checkOnButton(app, mouseX, mouseY):
    if 0 <= mouseX <= 108:
        if 108 < mouseY < 216:
            app.onCalendarButton = True
        else:
            app.onCalendarButton = False
        if 216 < mouseY < 324:
            app.onTasksButton = True
        else:
            app.onTasksButton = False
        if 324 < mouseY < 432:
            app.onHabitsButton = True
        else:
            app.onHabitsButton = False
    else:
        app.onCalendarButton = False
        app.onTasksButton = False
        app.onHabitsButton = False

def onStep(app):
    modifyButtonOpacity(app)

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

def checkButtonPress(app, mouseX, mouseY):
    if 0 <= mouseX <= 108:
        if 108 < mouseY < 216:
            app.calendar = True
        else:
            app.calendar = False
        if 216 < mouseY < 324:
            app.tasks = True
        else:
            app.tasks = False
        if 324 < mouseY < 432:
            app.habits = True
        else:
            app.habits = False

def getCurrentDay(app):
    number = app.currentDate.weekday()
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

def onKeyPress(app, key):
    if key == 'right':
        app.currentDate += timedelta(days=1)
    elif key == 'left':
        app.currentDate -= timedelta(days=1)

runApp(width = 1920, height = 1080)
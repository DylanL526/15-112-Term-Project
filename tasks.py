from cmu_graphics import*
from calendarScreen import*

def drawTasks(app):
    drawLabel('Tasks', 98, 39, size=35, align='left', font='DM Sans 36pt')
    drawLine(78, 78, 1366, 78, fill=rgb(217, 217, 217))
    drawTasksWidgets(app)

def drawTasksWidgets(app):
    sortedTaskList = getSortedTaskList(app)
    yValue = 98
    for tasks in sortedTaskList[0+app.tasksIndex:app.tasksIndex+7]:
        drawRect(98, yValue, 1248, 78, fill='white', border=rgb(167, 173, 173), borderWidth=1)
        if isinstance(tasks, SingleEvent):
            drawLabel(tasks.name, 112, yValue+24, font='DM Sans', align='left', size=30)
            dateValue = getCurrentDay(tasks.date.weekday()) + ', ' + getCurrentMonth(tasks.date.month) + ' ' + str(tasks.date.day) + ', ' + str(tasks.date.year)
            drawLabel(dateValue, 112, yValue+57, font='DM Sans 36pt', align='left', size=20, fill=rgb(167, 173, 173))
            drawLabel(str(tasks.startTime.strftime("%-I:%M")) + (str(tasks.startTime.strftime("%p"))).lower() + ' to ' + str(tasks.endTime.strftime("%-I:%M")) + (str(tasks.endTime.strftime("%p"))).lower(), 1335, yValue+57, align='right', size=20, fill=rgb(167, 173, 173), font='DM Sans 36pt')
        elif isinstance(tasks, SplitEvent):
            drawLabel(tasks.name, 112, yValue+24, font='DM Sans', align='left', size=30)
            labelValue = 'Due ' + getCurrentDay(tasks.date.weekday()) + ', ' + getCurrentMonth(tasks.date.month) + ' ' + str(tasks.date.day) + ' at ' + tasks.deadline
            drawLabel(labelValue, 112, yValue+57, font='DM Sans 36pt', align='left', size=20, fill=rgb(167, 173, 173))
            if tasks.durationHours == 0:
                drawLabel(str(tasks.durationMinutes) + ' minutes', 1335, yValue+57, align='right', size=20, fill=rgb(167, 173, 173), font='DM Sans 36pt')
            elif tasks.durationHours != 0 and tasks.durationMinutes == 0:
                drawLabel(str(tasks.durationHours) + ' hours', 1335, yValue+57, align='right', size=20, fill=rgb(167, 173, 173), font='DM Sans 36pt')
            else:
                drawLabel(str(tasks.durationHours) + ' hours, ' + str(tasks.durationMinutes) + ' minutes', 1335, yValue+57, align='right', size=20, fill=rgb(167, 173, 173), font='DM Sans 36pt')
        yValue += 98

def getSortedTaskList(app):
    taskDictionary = dict()
    dateList = []
    sortedTaskList = []
    for singleEventTasks in app.singleEventTasks:
        taskDictionary[singleEventTasks.date] = singleEventTasks
        dateList.append(singleEventTasks.date)
    for splitEventTasks in app.splitTasks:
        taskDictionary[splitEventTasks.date] = splitEventTasks
        dateList.append(splitEventTasks.date)
    dateList = sorted(dateList)
    for dates in dateList:
        sortedTaskList.append(taskDictionary[dates])
    return sortedTaskList
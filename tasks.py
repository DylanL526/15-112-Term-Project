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
            trash = Image.open('Images/bin.png') # Icon from https://www.flaticon.com/free-icon/bin_484662?term=trash+can&page=1&position=1&origin=tag&related_id=484662
            drawImage(CMUImage(trash), 1315, yValue+12, height=20, width=20)
            app.taskWidgetCoords[tasks] = (1315, yValue+12)
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
            trash = Image.open('Images/bin.png') # Icon from https://www.flaticon.com/free-icon/bin_484662?term=trash+can&page=1&position=1&origin=tag&related_id=484662
            drawImage(CMUImage(trash), 1315, yValue+12, height=20, width=20)
            app.taskWidgetCoords[tasks] = (1315, yValue+12)
        yValue += 98

def checkForTaskTrashPress(app, mouseX, mouseY):
    for tasks in app.taskWidgetCoords:
        (xCoord, yCoord) = app.taskWidgetCoords[tasks]
        if xCoord <= mouseX <= xCoord+20 and yCoord <= mouseY <= yCoord+20:
            if isinstance(tasks, SingleEvent):
                app.singleEventTasks.remove(tasks)
                app.taskWidgetCoords = dict()
                removeSingleEventData(tasks)
                break
            elif isinstance(tasks, SplitEvent):
                app.splitTasks.remove(tasks)
                app.splitTaskWorkSessions.pop(tasks)
                app.taskWidgetCoords = dict()
                removeSplitEventData(tasks)
                break

### Code from https://stackoverflow.com/questions/56987312/how-to-delete-only-one-row-from-a-csv-file-with-python ###

def removeSingleEventData(task):
    lines = []
    with open('singleEventData.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            lines.append(row)
            if row[3] == task.name:
                lines.remove(row)
    with open('singleEventData.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)

def removeSplitEventData(task):
    lines = []
    with open('splitEventData.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            lines.append(row)
            if row[4] == task.name:
                lines.remove(row)
    with open('splitEventData.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)

def loadSampleData():
    singleEventData = [["startTime", "endTime", "date", "name", "fill"],
                        ["1900-01-01 08:30:00","1900-01-01 09:30:00","2023-12-08","Study Group","251| 194| 194|"],
                        ["1900-01-01 12:00:00","1900-01-01 13:00:00","2023-12-09","Table Tennis","244| 211| 94"],
                        ["1900-01-01 10:00:00","1900-01-01 11:30:00","2023-12-09","Extratation","98| 134| 108"],
                        ["1900-01-01 09:00:00","1900-01-01 09:30:00","2023-12-09","Get Groceries","160| 197| 227"]]
    habitData = [["name", "days", "startTime", "endTime"],
                ["112 Lecture","{'Thursday', 'Tuesday'}","1900-01-01 09:30:00","1900-01-01 10:50:00"],
                ["70-100","{'Thursday', 'Tuesday'}","1900-01-01 11:00:00","1900-01-01 12:20:00"],
                ["112 Recitation","{'Wednesday', 'Friday'}","1900-01-01 10:00:00","1900-01-01 10:50:00"],
                ["108 Lecture","{'Wednesday', 'Friday', 'Monday'}","1900-01-01 13:00:00","1900-01-01 13:50:00"],
                ["120 Lecture","{'Wednesday', 'Friday', 'Monday'}","1900-01-01 15:00:00","1900-01-01 15:50:00"],
                ["FIC","{'Wednesday', 'Monday'}","1900-01-01 16:00:00","1900-01-01 16:50:00"],
                ["108 Recitation","{'Thursday', 'Tuesday'}","1900-01-01 14:00:00","1900-01-01 14:50:00"],
                ["GPI","{'Friday'}","1900-01-01 16:00:00","1900-01-01 16:50:00"],
                ["108 Recitation","{'Thursday', 'Tuesday'}","1900-01-01 08:00:00","1900-01-01 08:50:00"],
                ["Breakfast","{'Tuesday', 'Saturday', 'Monday', 'Sunday', 'Wednesday', 'Friday', 'Thursday'}","1900-01-01 07:00:00","1900-01-01 07:50:00"],
                ["Lunch","{'Monday', 'Wednesday', 'Friday'}","1900-01-01 11:30:00","1900-01-01 12:00:00"],
                ["Lunch","{'Sunday'}","1900-01-01 12:00:00","1900-01-01 13:00:00"],
                ["Lunch","{'Saturday'}","1900-01-01 13:15:00","1900-01-01 14:15:00"],
                ["Dinner","{'Sunday', 'Monday', 'Friday', 'Thursday', 'Saturday', 'Wednesday', 'Tuesday'}","1900-01-01 17:00:00","1900-01-01 18:00:00"]]
    splitEventData = [["deadline", "durationMinutes", "durationHours", "date", "name", "fill"]]
    with open('singleEventData.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(singleEventData)
    with open('habitData.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(habitData)
    with open('splitEventData.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(splitEventData)

#####################################################################################################################

def getSortedTaskList(app):
    taskList = []
    dateList = []
    sortedTaskList = []
    for singleEventTasks in app.singleEventTasks:
        taskList.append((singleEventTasks, singleEventTasks.date))
        dateList.append(singleEventTasks.date)
    for splitEventTasks in app.splitTasks:
        taskList.append((splitEventTasks, splitEventTasks.date))
        dateList.append(splitEventTasks.date)
    dateList = sorted(dateList)
    for date in dateList:
        for (task, taskDate) in taskList:
            if taskDate == date:
                sortedTaskList.append(task)
                taskList.remove((task, taskDate))
                break
    return sortedTaskList
from cmu_graphics import*
from calendarScreen import*

def drawStats(app):
    drawLabel('Statistics', 98, 39, size=35, align='left', font='DM Sans 36pt')
    drawLine(78, 78, 1366, 78, fill=rgb(217, 217, 217))
    drawLine(345, 150, 345, 702, fill=rgb(217, 217, 217))
    drawLine(306, 663, 1138, 663, fill=rgb(217, 217, 217))
    drawLabel('Time Spent on Events', 270, 406.5, size=25, rotateAngle=-90, font='DM Sans 36pt')
    drawLabel('Dates (Current Week)', 741.5, 715, size=25, font='DM Sans 36pt')
    timesList = sumTimes(app)
    coordList = []
    xValue = 444.125
    for i in range(7):
        drawLabel(str(app.weeklyDateList[i].month) + '/' + str(app.weeklyDateList[i].day), xValue, 677, fill=rgb(92, 92, 93), font='DM Sans', size=12)
        (hours, minutes) = timesList[i]
        if (hours != 0 and minutes == 0) or (hours == 0 and minutes != 0) or (hours != 0 and minutes != 0):
            hoursCoord = 612.3 - 50.7*(hours-1)
            minutesCoord = minutes/60 * 50.7
            yCoord = hoursCoord - minutesCoord
            drawCircle(xValue, yCoord, 5)
            coordList.append((xValue, yCoord))
        xValue += 99.125
    yValue = 612.3
    for i in range(1, 11):
        drawLabel(str(i) + ' hr', 333, yValue, fill=rgb(92, 92, 93), font='DM Sans', size=12, align='right')
        yValue -= 50.7
    for i in range(len(coordList)-1):
        (x1, y1) = coordList[i]
        (x2, y2) = coordList[i+1]
        drawLine(x1, y1, x2, y2)

def sumTimes(app):
    timesList = []
    for dates in app.weeklyDateList:
        timesList.append(getTotalTime(app, dates))
    return timesList

def getTotalTime(app, day):
    minuteCount = 0
    for habits in app.habitsSet:
        if getCurrentDay(day.weekday()) in habits.days:
            minuteCount += (habits.endTime - habits.startTime).seconds/60
    for singleEventTasks in app.singleEventTasks:
        if day == singleEventTasks.date:
            minuteCount += (singleEventTasks.endTime - singleEventTasks.startTime).seconds/60
    for keys in app.splitTaskWorkSessions:
        for (startTime, endTime) in app.splitTaskWorkSessions[keys]:
            if day == startTime.date():
                minuteCount += (endTime.minute - startTime.minute) + (endTime.hour - startTime.hour)*60
    return (minuteCount//60, minuteCount%60)
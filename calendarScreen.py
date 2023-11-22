from cmu_graphics import*

def drawCalendar(currentDate, currentDay):
    drawLabel('Calendar', 170, 39, size=35)
    drawRect(78, 156, 98, 624, fill=rgb(238, 241, 247))
    drawRect(78, 78, 1366, 78, fill=rgb(238, 241, 247))
    drawLine(78, 78, 1366, 78, fill=rgb(217, 217, 217))
    drawLine(78, 156, 1366, 156, fill=rgb(217, 217, 217))
    for y in range(234, 769, 78):
        drawLine(158, y, 1366, y, fill=rgb(217, 217, 217))
    for x in range(176, 1200, 170):
        drawLine(x, 78, x, 780, fill=rgb(217, 217, 217))
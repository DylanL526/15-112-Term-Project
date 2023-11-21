from cmu_graphics import*

def drawCalendar():
    drawLabel('Calendar', 258, 54, size=55)
    drawRect(108, 108, 1812, 108, fill=rgb(238, 241, 247))
    drawLine(108, 108, 1920, 108, fill=rgb(217, 217, 217))
    drawLine(108, 216, 1920, 216, fill=rgb(217, 217, 217))
    for i in range(247, 1920, 239):
        drawLine(i, 108, i, 1080, fill=rgb(217, 217, 217))
    for i in range(324, 1080, 108):
        drawLine(222, i, 1920, i, fill=rgb(217, 217, 217))
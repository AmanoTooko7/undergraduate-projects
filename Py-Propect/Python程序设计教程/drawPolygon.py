def drawPolygon(myTurtle, sideLength, numSides):#(对象, 绘制的边长度, 要绘制几边形)
    turnAngle = 360/numSides
    for i in range(numSides):
        myTurtle.forward(sideLength)
        myTurtle.right(turnAngle)
    

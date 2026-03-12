def drawSpiral(myTurtle, maxSide):#(对象,所画的的最大边长)
    for sideLength in range(0, maxSide, 2):#sideLengh为每次画的边长，为变量
        myTurtle.forward(sideLength)
        myTurtle.right(90)

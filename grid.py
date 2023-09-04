from tkinter import *
class DrawGrid():
    def __init__(self, hori = 22, verti = 22, sizeSquare = 10, xExtra = 0, yExtra = 0):
        self.hori = hori
        self.vert = verti
        self.sizeSquare = sizeSquare
        self.xExtra = xExtra
        self.yExtra = yExtra
        sizeBoardX = 1220
        sizeBoardY = 650
        self.allShapes = []
        self.window = Tk()
        self.canvas = Canvas(self.window, width = sizeBoardX, height = sizeBoardY)
        self.canvas.pack()
        self.window.bind("<Button-1>", self.ClickL)
        self.window.bind("<Button-3>", self.ClickR)
        self.window.bind("<Button-2>", self.ClickM)
        self.window.bind("<Button-4>", self.ClickB)
        self.window.bind("<Button-5>", self.ClickF)
        self.window.bind("<MouseWheel>", self.Events)
        self.colorByButton = {"left": "purple",
                         "middle": "yellow",
                         "right": "blue",
                         "back": "orange",
                         "forward": "pink",
                         "wheelUp": "brown",
                         "wheelDown": "grey"}


    def Layer(self, z):
        return 0
    

    def Offset(self, z):
        return 0
    

    def MakeSquareGrid(self, nrX, nrY):
        for x in range(nrX):
            for y in range(nrY):
                s = Shape(self, (x,y), "black", "white")
                self.allShapes.append(s)


    def MakePyramidGrid(self, sideLength, nrCopies = 3):
        M = sideLength - 1
        for copy in range(nrCopies):
            for z in range(M,-1,-1):
    #        for z in range(M,4,-1):
                for y in range(z+1):
                    for x in range(y+1):
                        # s = MakeSquare(board, x,y,z,variations[copy],copy = copy)
                        s = ShapePyramid(self, (x,y,z,copy), "black", "white")
                        self.allShapes.append(s)


    def _CreateSquare(self, xMin, yMin, xMax, yMax, width, outline, filling):
        self.canvas.create_rectangle(xMin, yMin,
                                    xMax, yMax,
                                    width = width, outline = outline, fill = filling)


    def Click(self, event, button):
        coordinates = (event.x, event.y)
        colorTaken = self.colorByButton[button]
        shapeCoordinates = self.FindShapeCoordinates(coordinates)
        self.UpdateColor(shapeCoordinates, colorTaken)


    def ClickL(self, event):
        self.Click(event, "left")
    
    
    def ClickR(self, event):
        self.Click(event, "right")


    def ClickM(self, event):
        self.Click(event, "middle")


    def ClickB(self, event):
        self.Click(event, "back")


    def ClickF(self, event):
        self.Click(event, "forward")


    def Events(self, event):
        print(event)
        print(event.delta)
        if event.delta > 0:
            self.Click(event, "wheelUp")
        elif event.delta < 0:
            self.Click(event, "wheelDown")
        else:
            raise Exception("Mousewheel moved without moving. Neat!")


    def FindShapeCoordinates(self, coordinates):
        for shape in self.allShapes:
            if shape.Contains(coordinates):
                return shape.coordinates


    def UpdateColor(self, coordinates, color):
        for shape in self.allShapes:
            if shape.coordinates == coordinates:
                shape.ChangeColor(color)

    #Maybe not
    def UpdateColorSet(self, coordinatesSet, color):
        for shape in self.allShapes:
            if shape.coordinates in coordinatesSet:
                shape.ChangeColor(color)


    def InputValidationDrawSquare(self, coordinates, copy):
        pass


    def Interactive(self):
        self.window.mainloop()


class Shape():
    xExtra = 0
    yExtra = 30
    deltaX = 22
    deltaY = 22

    def __init__(self, drObject, coordinates, color, filling, size = 10):
        self.drObject = drObject
        self.coordinates = coordinates
        self.size = size
        self.width = 1
        self.color = color
        self.filling = filling
        self.Mid(*coordinates)
        self.FindInterfaceCoordinates()
        self.DrawRectangle()
    

    def FindInterfaceCoordinates(self):
        self.xMin = self.midX - self.size + self.xExtra 
        self.xMax = self.midX + self.size + self.xExtra 
        self.yMin = - self.midY - self.size + self.yExtra
        self.yMax = - self.midY + self.size + self.yExtra


    def DrawRectangle(self):
        drObject = self.drObject
        drObject._CreateSquare(self.xMin, self.yMin,
                                    self.xMax, self.yMax,
                                    width = self.width, outline = self.color, filling = self.filling)


    def ChangeColor(self, color):
        self.filling = color
        self.DrawRectangle()


    #TODO: Kan beter ingedeeld worden
    def Mid(self, x = 0, y = 0, z = 0, copy = 0):
        
        layer = self.Layer(z)
        offset = self.Offset(copy)
        self.midX = self.deltaX*x + offset + 2.5 * self.deltaX
        self.midY = - self.deltaY*y - layer


    def Layer(self, z):
        return 0
    

    def Offset(self, copy):
        return 0


    def ValidateSize(self):
        assert self.size < self.deltaX
        assert self.size < self.deltaY

    
    def Contains(self, coordinates):
        x, y = coordinates
        return self.xMin <= x <= self.xMax and self.yMin <= y <= self.yMax


class ShapePyramid(Shape):
    deltaY = 15
    spaceForLastSquare = 25
    xExtra = Shape.xExtra + 20

    def Mid(self, x = 0, y = 0, z = 0, copy = 0):
        
        layer = self.Layer(z)
        offset = self.Offset(copy)
        self.midX = self.deltaX*x - self.deltaX/2*y + offset + 2.5 * self.deltaX
        self.midY = self.deltaY*y - layer


    def Offset(self, copy):
        return (6 * self.deltaX + 3) * copy     #TODO: 6 or depends or sideLength


    def Layer(self, z):
        return z * self.spaceForLastSquare + self.deltaY * (1+z) * z / 2
    

    def __eq__(self, other):
        return self.coordinates == other.coordinates
    #TODO: Wat als je een combinatie hebt van verschillende soorten grids?
    # Bijvoorbeeld vierkant en pyramide in 1 window.
    # Meegegeven coordinaten kunnen dubbel gebruikt worden tussen verschillende subclasses van Shape.


def SquareGrid():
    field = DrawGrid()
    field.MakeSquareGrid(10, 12)
    field.Interactive()


def PyramidGrid():
    field = DrawGrid()
    field.MakePyramidGrid(6)
    field.Interactive()


if __name__ == "__main__":
    # SquareGrid()
    PyramidGrid()
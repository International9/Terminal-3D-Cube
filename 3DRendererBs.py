import os, time, math

class Point:
    def __init__(self, x : float, y : float):
        self.x = x
        self.y = y
        
    def __eq__(self, value) -> bool:
        return self.x == value.x and self.y == value.y
        
    def __add__(self, value) -> bool:
        return Point(self.x + value.x, self.y + value.y)

class Point3D:
    def __init__(self, x : float, y : float, z : float):
        self.x = x
        self.y = y
        self.z = z
        
    def __eq__(self, value) -> bool:
        return self.x == value.x and self.y == value.y and self.z == value.z
        
    def __add__(self, value) -> bool:
        return Point(self.x + value.x, self.y + value.y, self.z + value.z)            
        
    @staticmethod
    def Rotate(p, angle, axis):
        cos_theta = math.cos(angle)
        sin_theta = math.sin(angle)

        if (axis == "x"):
            y = p.y * cos_theta - p.z * sin_theta
            z = p.y * sin_theta + p.z * cos_theta
            return Point3D(p.x, y, z)
        
        if (axis == "y"):
            x = p.x * cos_theta + p.z * sin_theta
            z = -p.x * sin_theta + p.z * cos_theta
            return Point3D(x, p.y, z)
        
        x = p.x * cos_theta - p.y * sin_theta
        y = p.x * sin_theta + p.y * cos_theta
        return Point3D(x, y, p.z)




SCREEN_HEIGHT = 22
SCREEN_WIDTH  = 22
NEAR_CLIPPING_PLANE = 0.01
FAR_CLIPPING_PLANE  = 80.0
FOCAL_LENGTH = 7
UPDATE_INTERVAL = .1666666667 # 1 / 60

PixelsOnScreen = [[" "]*SCREEN_HEIGHT]*SCREEN_WIDTH
origin = Point(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

cubePoints = [
    Point3D(-15, -15, 15), Point3D(15, -15, 45), 
    Point3D(-15, 15, 15),  Point3D(15, 15, 45),
    Point3D(15, 15, 15),   Point3D(-15, 15, 45),  
    Point3D(15, -15, 15),  Point3D(-15, -15, 45)
]

edgeTable = [
    [0, 2], [2, 4],
    [4, 6], [6, 0],
    [1, 3], [3, 5],
    [5, 7], [7, 1],
    [0, 7], [2, 5],
    [3, 4], [1, 6]
]    

def CalculateOriginPoint(pnts) -> Point3D:
    sum_x = sum(p.x for p in pnts)
    sum_y = sum(p.y for p in pnts)
    sum_z = sum(p.z for p in pnts)
    n = len(pnts)

    return Point3D(sum_x / n, sum_y / n, sum_z / n)

cubeOrigin = CalculateOriginPoint(cubePoints)

points = []
linePoints = []

def ThrdilizePoints(p : Point3D):
    if p.z == 0: return Point(p.x, p.y)
    
    xproj = (FOCAL_LENGTH * p.x) // (p.z + FOCAL_LENGTH)
    yproj = (FOCAL_LENGTH * p.y) // (p.z + FOCAL_LENGTH)
    
    return Point(xproj, yproj)
    
def UpdateScrPnts():
    points.clear()
    
    for p in cubePoints:
        if p.z >= FAR_CLIPPING_PLANE or p.z <= NEAR_CLIPPING_PLANE:
            continue
        
        np = ThrdilizePoints(p)
        points.append(np)
    
def RenderScreen():
    for I in range(SCREEN_HEIGHT):
        for j in range(SCREEN_WIDTH):
            
            curPnt = Point(j, I)
            
            # Cube {Priority: First}
            noCube = DrawPointsFromList(j, I, curPnt, points, "X")
            if (noCube): continue
            
            # Lines {Priority: Second}
            noLines = DrawPointsFromList(j, I, curPnt, linePoints, "o")
            if (noLines): continue            
            
            if curPnt == origin:
                PixelsOnScreen[j][I] = "+"
            elif curPnt.y == origin.y:
                PixelsOnScreen[j][I] = "—"        
            elif curPnt.x == origin.x:
                PixelsOnScreen[j][I] = "|"
            else:
                PixelsOnScreen[j][I] = " "    
                
            PixelsOnScreen[j][I] = " "
            print(PixelsOnScreen[j][I], end=" ")
        print()    
        
def DrawPointsFromList(j, I, curPnt, listP, char):
    for p in listP:
        if curPnt == Point(p.x + origin.x, -p.y + origin.y):
            PixelsOnScreen[j][I] = str(char[0])
            print(PixelsOnScreen[j][I], end=" ")
            
            return True
            
    return False
    
def DrawCubeLines():
    for edge in edgeTable:
        try:
            DrawLine(points[edge[0]], points[edge[1]])
        except: continue
    
def DrawLine(p1, p2):
    if p1 == p2: return
        
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    abx = abs(dx)
    aby = abs(dy)
    steps = max(aby, abx)
    Xinc = dx / steps
    Yinc = dy / steps
    
    X = p1.x + Xinc
    Y = p1.y + Yinc
    
    for i in range(int(steps) - 1):
        linePoints.append(Point(int(X), int(Y)))
        
        X += Xinc
        Y += Yinc

def DisposeLines():
    linePoints.clear()
        

def RotateCube(spd):
    for i in range(len(cubePoints)):
        curPnt = cubePoints[i]
        ang = math.radians(spd) * UPDATE_INTERVAL

        translated = Point3D(curPnt.x - cubeOrigin.x, curPnt.y - cubeOrigin.y, curPnt.z - cubeOrigin.z)
        rot = Point3D.Rotate(translated, ang, "y")

        cubePoints[i] = Point3D(rot.x + cubeOrigin.x, rot.y + cubeOrigin.y, rot.z + cubeOrigin.z)


Quit = False
speed = 0

def Start():
    global speed
    speed = float(input("Choose Move Speed: "))
            
def Update():
    global UPDATE_INTERVAL, cubePoints, speed
    
    RotateCube(speed)

    UpdateScrPnts()
    DrawCubeLines()
    RenderScreen()
    
    time.sleep(UPDATE_INTERVAL)
    os.system('cls' if os.name == 'nt' else 'clear')
    
    DisposeLines()
    
Start()
while not Quit:
    Update()

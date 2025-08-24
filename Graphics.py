from PIL import Image
import urllib.request
import cv2
import numpy as np
import math
from pynput.keyboard import Key, Listener
from Matrix import Matrix
from Object import Object
from Vector3 import Vector3
from Vector2 import Vector2
from Triangle import Triangle


windowName = "Graphics"
window = cv2.namedWindow(windowName, 0)
windowWidth = 800        
windowHeight = 800
centerX = int(windowWidth / 2)
centerY = int(windowHeight / 2)
pixelsPerUnit = 10

cameraPosition = Vector3()
cameraPosition.x = 0 * pixelsPerUnit
cameraPosition.y = 0 * pixelsPerUnit
cameraPosition.z = 0 * pixelsPerUnit
cameraRotation = Vector3()
cameraRotation.x = 20
cameraRotation.y = 0
cameraRotation.z = 20
cameraLookDirection = Vector3()
cameraLookDirection.y = 1
# camera default look direction is Vector3(0,1,0)
# z-axis is up, x-axis is right, y-axis is into the screen


def rotateAndScaleLocalCoord(coord: Vector3, rotation: Vector3, scale: Vector3):
    localRotationMatrix = Matrix.getRotationMatrix(rotation)
    scaleMatrix = Matrix.getScaleMatrix(scale)   
    scaledCoord = scaleMatrix.multiplyVector(coord)
    locallyRotatedCoord = localRotationMatrix.multiplyVector(scaledCoord)    

    return locallyRotatedCoord
###

def rotateCoordinate(coord: Vector3, rotations: Vector3):
    rotationMatrix = Matrix.getRotationMatrix(rotations)
    return rotationMatrix.multiplyVector(coord)
###

def getScreenCoord(coordinate: Vector3) -> Vector3:
    screenCoord = Vector3()

    screenCoord.x = centerX + cameraPosition.x + (coordinate.x * pixelsPerUnit)
    screenCoord.y = centerX + cameraPosition.z + (coordinate.z * pixelsPerUnit)
    screenCoord.z = centerY - cameraPosition.y - (coordinate.y * pixelsPerUnit) 

    return screenCoord
###

def getScreenShapeTriangles(localShape: Object) -> list:
    screenShapeTriangles = []
    xPosition = localShape.m_position.x
    yPosition = localShape.m_position.y
    zPosition = localShape.m_position.z    

    updatedCameraLookDir = Matrix.getRotationMatrix(cameraRotation).multiplyVector(cameraLookDirection)   

    for i in range(int(len(localShape.m_localCoords) / 3)):  
        screenTriangle = Triangle()
        screenCoords = [] # Vector3 list
        worldCoords = [] # Vector3 list

        for j in range(3):
            worldRotationMatrix = Matrix.getRotationMatrix(cameraRotation)
            coordVector = Vector3()
            coordVector.x = localShape.m_localCoords[(3 * i) + j][0]
            coordVector.y = localShape.m_localCoords[(3 * i) + j][1]
            coordVector.z = localShape.m_localCoords[(3 * i) + j][2]

            locallyRotatedScaledCoord = rotateAndScaleLocalCoord(coordVector, localShape.m_rotation, localShape.m_scale)        
            locallyPositionedCoord = Vector3()
            locallyPositionedCoord.x = locallyRotatedScaledCoord.x + xPosition
            locallyPositionedCoord.y = locallyRotatedScaledCoord.y + yPosition
            locallyPositionedCoord.z = locallyRotatedScaledCoord.z + zPosition    
            worldRotatedScaledPositionedCoord = worldRotationMatrix.multiplyVector(locallyPositionedCoord)
            
            worldCoords.append(worldRotatedScaledPositionedCoord)
            screenCoords.append(getScreenCoord(worldRotatedScaledPositionedCoord))
        #
                
        screenTriangle.A = screenCoords[0]
        screenTriangle.B = screenCoords[1]
        screenTriangle.C = screenCoords[2]
        
        AB = Vector3()
        BC = Vector3()
        AB = worldCoords[1].subtract(worldCoords[0])
        BC = worldCoords[2].subtract(worldCoords[1])
        screenTriangle.normal = AB.cross(BC).normalized()

        if (screenTriangle.normal.dot(cameraLookDirection) > 0):
            screenShapeTriangles.append(screenTriangle)                
        #
    #

    return screenShapeTriangles
###

def getPointsBetween(pointA: list, pointB: list) -> list:

    firstToSecondInPixels = [ int(pointB[0] - pointA[0]),  int(pointB[1] - (pointA[1])) ]
    largerMovementX = False
    largerMovementAmount = int(0)
    ratio = 1

    xDirection = 1
    yDirection = 1
    if (firstToSecondInPixels[0] < 0):
        xDirection = -1
    #
    if (firstToSecondInPixels[1] < 0):
        yDirection = -1
    #

    if abs(firstToSecondInPixels[0]) > abs(firstToSecondInPixels[1]):
        largerMovementAmount = abs(firstToSecondInPixels[0])
        if firstToSecondInPixels[0] != 0:
            if (firstToSecondInPixels[1] != 0):
                ratio = abs(firstToSecondInPixels[1] / firstToSecondInPixels[0])
            else:
                ratio = 0
            #
        else:
            ratio = 0
        #
        largerMovementX = True
    else:
        largerMovementAmount = abs(firstToSecondInPixels[1])
        if firstToSecondInPixels[1] != 0:
            if (firstToSecondInPixels[0] != 0):
                ratio = abs(firstToSecondInPixels[0] / firstToSecondInPixels[1])
            else:
                ratio = 0
            #
        else:
            ratio = 0
        #
    #

    smallerMovementTracker = ratio # makes sure we don't lose pixels because you can't divide real pixels
    largerMovementTracker = 1
    inBetweenPixels = []
    
    for i in range(largerMovementAmount):        
        startingXPos = pointA[0]
        startingYPos = pointA[1]        
        if (largerMovementX):
            inBetweenPixels.append([ startingXPos + (largerMovementTracker * xDirection), (startingYPos + (smallerMovementTracker * yDirection))])
        else:
            inBetweenPixels.append([ startingXPos + (smallerMovementTracker * xDirection), (startingYPos + (largerMovementTracker * yDirection))])
        #

        smallerMovementTracker += ratio
        largerMovementTracker += 1
    #

    return inBetweenPixels
###

def getAllEdgePointsTriangles(polygon: Object) -> list:
    triangleEdges = []

    for i in range(int(len(polygon) / 3)):  
        triangleEdges += getPointsBetween(polygon[3 * i], polygon[(3 * i) + 1])
        triangleEdges += getPointsBetween(polygon[(3 * i) + 1], polygon[(3 * i) + 2])
        triangleEdges += getPointsBetween(polygon[(3 * i) + 2], polygon[3 * i])
    #

    return triangleEdges
###

def getAllEdgePoints(segment: Object) -> list:
    allPointsAlongEdges = []

    for i in range(len(segment)):           
        allPointsAlongEdges += getPointsBetween(segment[i], segment[(i + 1) % (len(segment))])
    #

    return allPointsAlongEdges
###

def drawPolygon(polygon: Object, image):
    trianglesOnScreen = getScreenShapeTriangles(polygon)

    A = Vector2()
    B = Vector2()
    C = Vector2()

    for i in range(int(len(trianglesOnScreen))):  
        A.x = trianglesOnScreen[i].A.x
        A.y = trianglesOnScreen[i].A.y
        B.x = trianglesOnScreen[i].B.x
        B.y = trianglesOnScreen[i].B.y
        C.x = trianglesOnScreen[i].C.x
        C.y = trianglesOnScreen[i].C.y
         
        drawFacePoints(A, B, C, image)            
    #
###

def drawSegments(segments: Object, image):
    shapePointsOnScreen = getScreenShapeCoords(segments)
    allPoints = shapePointsOnScreen + getAllEdgePoints(shapePointsOnScreen)
    
    for coordinate in allPoints:
        xCoord = coordinate[0]
        yCoord = coordinate[1] 

        if (xCoord >= 0 and yCoord >= 0 and xCoord < windowWidth and yCoord < windowHeight):            
            image[xCoord, yCoord] = segments.m_color
        #
    #
###

def getMax(A: int, B: int) -> int:
    if (A > B):
        return A
    else:
        return B
###

def getMin(A: int, B: int) -> int:
    if (A < B):
        return A
    else:
        return B
###

def triangleArea(sideA: float, sideB: float, sideC: float) -> float:    
    semiperimeter = (sideA + sideB + sideC) / 2
    return math.sqrt(int(semiperimeter * (semiperimeter - sideA) * (semiperimeter - sideB) * (semiperimeter - sideC)))
###

def pointInTriangle(P: Vector2, A: Vector2, B: Vector2, C: Vector2) -> bool: 
    AB = B.subtract(A).magnitude()
    AC = C.subtract(A).magnitude()
    BC = C.subtract(B).magnitude()
    AP = P.subtract(A).magnitude()
    BP = P.subtract(B).magnitude()
    CP = P.subtract(C).magnitude()

    totalArea = triangleArea(AB, AC, BC)
    area1 = triangleArea(AB, BP, AP)
    area2 = triangleArea(BC, BP, CP)
    area3 = triangleArea(AC, AP, CP)

    return (int(area1 + area2 + area3) >= int(totalArea) - 2 and int(area1 + area2 + area3) <= int(totalArea) + 2)
###

def drawFacePoints(A: Vector2, B: Vector2, C: Vector2, image) -> list:
    facePoints = []

    minX = getMin(getMin(A.x, B.x), C.x)
    maxX = getMax(getMax(A.x, B.x), C.x)
    minY = getMin(getMin(A.y, B.y), C.y)
    maxY = getMax(getMax(A.y, B.y), C.y)

    for w in range(int(maxX - minX)):
        for h in range(int(maxY - minY)):
            point = Vector2()
            point.x = minX + w
            point.y = minY + h

            if (pointInTriangle(point, A, B, C)):
                if (point.x >= 0 and point.y >= 0 and point.x < windowWidth and point.y < windowHeight):            
                    image[point.x, point.y] = image2Pixels[point.x % 96,point.y % 96]
                #
            #
        #   
    #

    return facePoints
###

# Create shapes
box1 = Object()
box1.setBox()
box1.m_position = [ 10, 0, 0 ]
box2 = Object()
box2.setBox()
box2.m_position = [ 0, -10, 0 ]
box3 = Object()
box3.setBox()
box3.m_position = [ 0, 10, 0 ]
box4 = Object()
box4.setBox()
box4.m_position = [ -10, 0, 0 ]

polygon1 = Object()
polygon1.setDiamond()
polygon1.m_scale = [ 2, 2, 5 ]
polygon2 = Object()
polygon2.setDiamond()
polygon2.m_scale = [ 0.5, 0.5, 1.25 ]
polygon2.m_position = [ 5, 0, 0 ]
polygon2.m_rotation = [ 90, 0, 0 ]

imageBox = Object()
imageBox.setBox()
imageBox.m_scale.x = 10
imageBox.m_scale.y = 10
imageBox.m_scale.z = 10
imageBox.removeDuplicateEdges()
imageBox.m_color = (50,50,5)

xAxis = Object()
xAxis.m_rotation = cameraRotation
xAxis.m_localCoords = [ [ -10, 0, 0 ], [ 10, 0, 0 ] ]
xAxis.m_color = (50, 100, 100)
xAxis.m_b_isAxis = True

yAxis = Object()
yAxis.m_rotation = cameraRotation
yAxis.m_localCoords = [ [ 0, -20, 0 ], [ 0, 20, 0 ] ]
yAxis.m_color = (200, 200, 10)
yAxis.m_b_isAxis = True

zAxis = Object()
zAxis.m_rotation = cameraRotation
zAxis.m_localCoords = [ [ 0, 0, -100 ], [0, 0, 100 ] ]
zAxis.m_color = (100, 50, 100)
zAxis.m_b_isAxis = True

b_loopExited = False

image2 = Image.open("BrickWall.png")
image2Pixels = image2.load()

while b_loopExited == False:
    image  = Image.new( mode = "RGB", size = (windowWidth, windowHeight), color = (0, 0, 0, 100) )
    pixels = image.load()

    imageBox.m_textureData = image2Pixels
    drawPolygon(imageBox, pixels)

    # draw shapes    
    # drawPolygon(box1, pixels)   
    # drawPolygon(box2, pixels)   
    # drawPolygon(box3, pixels)   
    # drawPolygon(box4, pixels)    
    # drawPolygon(polygon1, pixels)
    # drawPolygon(polygon2, pixels)

    # draw axis
    # drawSegments(zAxis, pixels)
    # drawSegments(xAxis, pixels)
    # drawSegments(yAxis, pixels)

    # move objects
    # cameraRotation.x += 1
    cameraRotation.z += 10

    # box1.addRotation([1,1,0])
    # box2.addRotation([0,1,0])
    # box3.addRotation([0,0,1])
    # box4.addRotation([1,0,0])
    # box3.m_rotation.x += 1
    # box4.m_rotation.x += 1
    # polygon1.addRotation([0,0,1])
    # polygon1.m_position.z = 10 * math.sin(polygon1.m_rotation.z * 0.05)
    # polygon2.addRotation([0,-30,0])
    # polygon2.m_position.x = 10 * math.sin(polygon2.m_rotation.y * 0.001)
    # polygon2.m_position.y = 10 * math.cos(polygon2.m_rotation.y * 0.001)

    open_cv_image = np.array(image)
    # Convert RGB to BGR
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    cv2.imshow(windowName, open_cv_image)    

    # cv2.waitKey(50)    

    key = cv2.waitKey(50)    
    # if key == ord('w'):
    #     cameraRotation.x += 1
    # # 
    # if key == ord('s'):
    #     cameraRotation.x -= 1
    # #
    # if key == ord('a'):
    #     cameraRotation.z += 1
    # #
    # if key == ord('d'):
    #     cameraRotation.z -= 1
    # #
    if key == ord('q'):
        b_loopExited = True
    #
##
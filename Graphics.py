from PIL import Image #
import urllib.request
import cv2
import numpy as np
import math
from pynput.keyboard import Key, Listener


windowName = "Graphics"
window = cv2.namedWindow(windowName, 0)
windowWidth = 400        
windowHeight = 400
centerX = int(windowWidth / 2)
centerY = int(windowHeight / 2)
pixelsPerUnit = 10
cameraPosition = [ 0 * pixelsPerUnit, 0 * pixelsPerUnit, 0 * pixelsPerUnit ]
cameraRotation = [ -60,0,20 ]

def LmultiplySize2Matrix(matrix, coordinate):
    xCoord = ((matrix[0] * coordinate[0]) + (matrix[1] * coordinate[1]))
    yCoord = ((matrix[2] * coordinate[0]) + (matrix[3] * coordinate[1]))

    return [ xCoord, yCoord ]
###

def LmultiplySize3Matrix(matrix, coordinate):
    xCoord = ((matrix[0] * coordinate[0]) + (matrix[1] * coordinate[1]) + (matrix[2] * coordinate[2]))
    yCoord = ((matrix[3] * coordinate[0]) + (matrix[4] * coordinate[1]) + (matrix[5] * coordinate[2]))
    zCoord = ((matrix[6] * coordinate[0]) + (matrix[7] * coordinate[1]) + (matrix[8] * coordinate[2]))

    return [ xCoord, yCoord, zCoord ]
###

def MultiplyMatrices3x3(A, B):    
    newMatrix = [
        (A[0] * B[0]) + (A[1] * B[3]) + (A[2] * B[6]),    (A[0] * B[1]) + (A[1] * B[4]) + (A[2] * B[7]),    (A[0] * B[2]) + (A[1] * B[5]) + (A[2] * B[8]),
        (A[3] * B[0]) + (A[4] * B[3]) + (A[5] * B[6]),    (A[3] * B[1]) + (A[4] * B[4]) + (A[5] * B[7]),    (A[3] * B[2]) + (A[4] * B[5]) + (A[5] * B[8]),
        (A[6] * B[0]) + (A[7] * B[3]) + (A[8] * B[6]),    (A[6] * B[1]) + (A[7] * B[4]) + (A[8] * B[7]),    (A[6] * B[2]) + (A[7] * B[5]) + (A[8] * B[8])
    ]

    return newMatrix
###

def getScaleMatrix(scales):
    scaleMatrix = [
        scales[0], 0,         0,
        0,         scales[1], 0,
        0,         0,         scales[2]
    ]

    return scaleMatrix
###

def getRotationMatrix(rotations):
    xRot = math.radians(rotations[0])
    yRot = math.radians(rotations[1])
    zRot = math.radians(rotations[2])

    xRotationMatrix = [
        1, 0,               0             ,
        0, math.cos(xRot), -math.sin(xRot),
        0, math.sin(xRot),  math.cos(xRot)     
    ]

    yRotationMatrix = [
        math.cos(yRot), 0, -math.sin(yRot),
        0,              1,  0             ,
        math.sin(yRot), 0,  math.cos(yRot)      
    ]

    zRotationMatrix = [
        math.cos(zRot), -math.sin(zRot), 0,
        math.sin(zRot),  math.cos(zRot), 0,
        0,               0,              1     
    ]

    xyMatrix = MultiplyMatrices3x3(xRotationMatrix, yRotationMatrix)
    xyzRotationMatrix = MultiplyMatrices3x3(xyMatrix, zRotationMatrix)

    return xyzRotationMatrix
###    

def rotateAndScaleLocalCoord(coord, rotations, scales):
    localRotationMatrix = getRotationMatrix(rotations)
    scaleMatrix = getScaleMatrix(scales)   
    scaledCoord = LmultiplySize3Matrix(scaleMatrix, coord)
    locallyRotatedCoord = LmultiplySize3Matrix(localRotationMatrix, scaledCoord)    

    return locallyRotatedCoord
###

def rotateCoordinate(coord, rotations):
    rotationMatrix = getRotationMatrix(rotations)
    return LmultiplySize3Matrix(rotationMatrix, coord)
###

def getScreenCoord(coordinate):
    return [ 
        centerX + cameraPosition[0] + (coordinate[0] * pixelsPerUnit), 
        centerY - cameraPosition[1] - (coordinate[1] * pixelsPerUnit), 
        centerX + cameraPosition[2] + (coordinate[2] * pixelsPerUnit) 
    ]
###

def getScreenShapeCoords(localShape):
    screenShapeCoords = []
    xPosition = localShape["position"][0]
    yPosition = localShape["position"][1]
    zPosition = localShape["position"][2]
    rotations = localShape["rotation"]
    scales = localShape["scale"]

    for coord in localShape["localCoords"]:
        worldRotationMatrix = getRotationMatrix(cameraRotation)
        locallyRotatedScaledCoord = rotateAndScaleLocalCoord(coord, rotations, scales)        

        if (localShape["_isAxis"]):
            worldRotatedScaledPositionedCoord = LmultiplySize3Matrix(worldRotationMatrix, coord)
        else:
            locallyPositionedCoord = [ locallyRotatedScaledCoord[0] + xPosition, locallyRotatedScaledCoord[1] + yPosition, locallyRotatedScaledCoord[2] + zPosition]            
            worldRotatedScaledPositionedCoord = LmultiplySize3Matrix(worldRotationMatrix, locallyPositionedCoord)
        #
        
        screenShapeCoords.append(getScreenCoord(worldRotatedScaledPositionedCoord))        

    return screenShapeCoords
###

def getPointsBetween(pointA, pointB):

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

def getAllEdgePointsTriangles(polygon):
    triangleEdges = []

    for i in range(int(len(polygon) / 3)):  
        triangleEdges += getPointsBetween(polygon[3 * i], polygon[(3 * i) + 1])
        triangleEdges += getPointsBetween(polygon[(3 * i) + 1], polygon[(3 * i) + 2])
        triangleEdges += getPointsBetween(polygon[(3 * i) + 2], polygon[3 * i])
    #

    return triangleEdges
###

def getAllEdgePoints(segment):
    allPointsAlongEdges = []

    for i in range(len(segment)):           
        allPointsAlongEdges += getPointsBetween(segment[i], segment[(i + 1) % (len(segment))])
    #

    return allPointsAlongEdges
###

def drawPolygon(polygon, image, color):
    shapePointsOnScreen = getScreenShapeCoords(polygon)
    allPoints = shapePointsOnScreen + getAllEdgePointsTriangles(shapePointsOnScreen)

    for coordinate in allPoints:
        xCoord = coordinate[0]
        yCoord = coordinate[1] 

        if (xCoord >= 0 and yCoord >= 0 and xCoord < windowWidth and yCoord < windowHeight):            
            image[xCoord, yCoord] = color
        #
    #
###

def drawSegments(segments, image, color):
    shapePointsOnScreen = getScreenShapeCoords(segments)
    allPoints = shapePointsOnScreen + getAllEdgePoints(shapePointsOnScreen)

    for coordinate in allPoints:
        xCoord = coordinate[0]
        yCoord = coordinate[1] 

        if (xCoord >= 0 and yCoord >= 0 and xCoord < windowWidth and yCoord < windowHeight):            
            image[xCoord, yCoord] = color
        #
    #
###


# Create shapes
shapeColor = (0,255,0)
box1 = {
    "position": [ 10, 0, 0 ],
    "rotation": [ 0, 0, 0 ],
    "scale": [ 1, 1, 1 ],
    "localCoords": [ 
        [  1, 1, 1 ], [ -1, 1, 1 ], [ -1, -1, 1 ], 
        [ -1, -1, 1 ], [ 1, -1, 1 ], [ 1, 1, 1 ], 

        [ -1, -1, 1 ], [ 1, -1, 1 ], [ 1, -1, -1 ], 
        [ 1, -1, -1 ], [ -1, -1, -1 ], [ -1, -1, 1 ],

        [ 1, -1, -1 ], [ 1, 1, -1 ], [ -1, 1, -1 ],
        [ -1, 1, -1 ], [ -1, -1, -1 ], [ 1, -1, -1 ],

        [ 1, 1, 1 ], [ 1, 1, -1 ], [ -1, -1, -1 ],
        [ 1, -1, -1 ], [ 1, -1, 1 ], [ 1, 1, 1 ],

        [ -1, 1, 1 ], [ -1, -1, 1 ], [ -1, -1, -1 ],
        [ -1, -1, -1 ], [ -1, 1, -1 ], [ -1, 1, 1 ],

        [ 1, 1, 1 ], [ -1, 1, 1 ], [ -1, 1, -1 ],
        [ -1, 1, -1 ], [ 1, 1, -1 ], [ 1, 1, 1 ],
    ],
    "_isAxis": False
}

box2 = dict(box1)
box2["position"] = [ 0, -10, 0 ]
box3 = dict(box1)
box3["position"] = [ 0, 10, 0 ]
box4 = dict(box1)
box4["position"] = [ -10, 0, 0 ]

polygon1 = {
    "position": [ 0, 0, 0 ],
    "rotation": [ 0, 0, 0 ],
    "scale": [ 2, 2, 5 ],
    "localCoords": [ 
        # [  1, 1, 0 ], [ -1, 1, 0 ], [ 1, -1, 0 ], 
        # [ 1, -1, 0 ], [ -1, -1, 0 ], [ -1, 1, 0 ], 
        [ -1, -1, 0 ], [ 1, -1, 0 ], [ 0, 0, 1 ], 
        [ 1, -1, -0 ], [ 1, 1, 0 ], [ 0, 0, 1 ],
        [ 1, 1, 0 ], [ -1, 1, 0 ], [ 0, 0, 1 ],
        [ -1, 1, 0 ], [ -1, -1, 0 ], [ 0, 0, 1 ],
        [ -1, -1, 0 ], [ 1, -1, 0 ], [ 0, 0, -1 ], 
        [ 1, -1, -0 ], [ 1, 1, 0 ], [ 0, 0, -1 ],
        [ 1, 1, 0 ], [ -1, 1, 0 ], [ 0, 0, -1 ],
        [ -1, 1, 0 ], [ -1, -1, 0 ], [ 0, 0, -1 ]
    ],
    "_isAxis": False
}
polygon2 = dict(polygon1)
polygon2["scale"] = [ 0.5, 0.5, 1.25 ]
polygon2["position"] = [ 5, 0, 0 ]
polygon2["rotation"] = [ 90, 0, 0 ]

xColor = (50, 100, 100)
yColor = (200, 200, 10)
zColor = (100, 50, 100)
xAxis = {
    "position": [ 0, 0, 0 ],
    "rotation": cameraRotation,
    "scale": [ 1, 1, 1 ],
    "localCoords": [ [ -10, 0, 0 ], [ 10, 0, 0 ] ],
    "_isAxis": True    
}
yAxis = {
    "position": [ 0, 0, 0 ],
    "rotation": cameraRotation,
    "scale": [ 1, 1, 1 ],
    "localCoords": [ [ 0, -20, 0 ], [ 0, 20, 0 ] ],
    "_isAxis": True    
}
zAxis = {
    "position": [ 0, 0, 0 ],
    "rotation": cameraRotation,
    "scale": [ 1, 1, 1 ],
    "localCoords": [ [ 0, 0, -100 ], [0, 0, 100 ] ],
    "_isAxis": True    
}


b_loopExited = False

while b_loopExited == False:
    image  = Image.new( mode = "RGB", size = (windowWidth, windowHeight), color = (0, 0, 0, 100) )
    pixels = image.load()

    # draw shapes
    drawPolygon(box1, pixels, shapeColor)   
    drawPolygon(box2, pixels, shapeColor)   
    drawPolygon(box3, pixels, shapeColor)   
    drawPolygon(box4, pixels, shapeColor)    
    drawPolygon(polygon1, pixels, shapeColor)
    drawPolygon(polygon2, pixels, shapeColor)

    # draw axis
    drawSegments(zAxis, pixels, zColor)
    drawSegments(xAxis, pixels, xColor)
    drawSegments(yAxis, pixels, yColor)

    # move objects
    cameraRotation[2] += 1

    box1["rotation"][0] += 1
    box2["rotation"][1] += 1
    box3["rotation"][0] += 1
    box4["rotation"][2] += 1
    polygon1["rotation"][2] += 1
    polygon1["position"][2] = 10 * math.sin(polygon1["rotation"][2] * 0.05)
    polygon2["rotation"][1] -= 30
    polygon2["position"][0] = 10 * math.sin(polygon2["rotation"][1] * 0.001)
    polygon2["position"][1] = 10 * math.cos(polygon2["rotation"][1] * 0.001)

    open_cv_image = np.array(image)
    # Convert RGB to BGR
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    cv2.imshow(windowName, open_cv_image)    

    key = cv2.waitKey(50)    
    if key == ord('q'):
        b_loopExited = True
    #
##
import math
from Vector3 import Vector3


class Matrix():
    def __init__(self, matrix):
        self.m_matrix = matrix
    
    m_matrix = []

    def setMatrix(self, matrix):
        self.m_matrix = matrix
    ###

    def multiplyVector(self, vector: Vector3) -> Vector3:
        matrix = self.m_matrix
        newVector = Vector3()
        newVector.x = ((matrix[0] * vector.x) + (matrix[1] * vector.y) + (matrix[2] *  vector.z))
        newVector.y = ((matrix[3] * vector.x) + (matrix[4] * vector.y) + (matrix[5] *  vector.z))
        newVector.z = ((matrix[6] * vector.x) + (matrix[7] * vector.y) + (matrix[8] *  vector.z))

        return newVector
    ###

    def multiplyMatrix(self, BMatrix):   
        A = self.m_matrix
        B = BMatrix.m_matrix

        newMatrix = [
            (A[0] * B[0]) + (A[1] * B[3]) + (A[2] * B[6]),    (A[0] * B[1]) + (A[1] * B[4]) + (A[2] * B[7]),    (A[0] * B[2]) + (A[1] * B[5]) + (A[2] * B[8]),
            (A[3] * B[0]) + (A[4] * B[3]) + (A[5] * B[6]),    (A[3] * B[1]) + (A[4] * B[4]) + (A[5] * B[7]),    (A[3] * B[2]) + (A[4] * B[5]) + (A[5] * B[8]),
            (A[6] * B[0]) + (A[7] * B[3]) + (A[8] * B[6]),    (A[6] * B[1]) + (A[7] * B[4]) + (A[8] * B[7]),    (A[6] * B[2]) + (A[7] * B[5]) + (A[8] * B[8])
        ]

        multipliedMatrix = Matrix(newMatrix)

        return multipliedMatrix
    ###

    def getScaleMatrix(scale: Vector3):
        scaleMatrixPositions = [
            scale.x, 0,         0,
            0,         scale.y, 0,
            0,         0,         scale.z
        ]

        scaleMatrix = Matrix(scaleMatrixPositions)        
        
        return scaleMatrix
    ###

    def getRotationMatrix(rotations: Vector3):
        xRot = math.radians(rotations.x)
        yRot = math.radians(rotations.y)
        zRot = math.radians(rotations.z)

        xRotationMatrix = [
            1, 0,               0             ,
            0, math.cos(xRot), -math.sin(xRot),
            0, math.sin(xRot),  math.cos(xRot)     
        ]
        xMatrix = Matrix(xRotationMatrix)

        yRotationMatrix = [
            math.cos(yRot), 0, -math.sin(yRot),
            0,              1,  0             ,
            math.sin(yRot), 0,  math.cos(yRot)      
        ]
        yMatrix = Matrix(yRotationMatrix)

        zRotationMatrix = [
            math.cos(zRot), -math.sin(zRot), 0,
            math.sin(zRot),  math.cos(zRot), 0,
            0,               0,              1     
        ]
        zMatrix = Matrix(zRotationMatrix)

        xyMatrix = xMatrix.multiplyMatrix(yMatrix)
        xyzRotationMatrix = xyMatrix.multiplyMatrix(zMatrix)

        return xyzRotationMatrix
    ###    
###
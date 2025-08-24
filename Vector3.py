import math


class Vector3():
    def __init__(self):
            self.x = 0
            self.y = 0
            self.z = 0
        #
    ###

    def cross(self, other):
        crossProduct = Vector3()
        crossProduct.x = (self.y * other.z) - (self.z * other.y)
        crossProduct.y = - ((self.x * other.z) - (self.z * other.x))
        crossProduct.z = (self.x * other.y) - (self.y * other.x)
        
        return crossProduct     
    ###

    def dot(self, other):
        return (self.x * other.x) + (self.y * other.y) + (self.z * other.z)
    ###

    def magnitudeSquared(self):
        return (self.x * self.x) + (self.y * self.y) + (self.z * self.z)
    ###

    def magnitude(self):
        return math.sqrt(self.magnitudeSquared())
    ###

    # def amountProjectedOnto(self, projectOnto):
    #     if (projectOnto.magnitudeSquared() == 0):
    #         return 0
    #     else:
    #         return (((self.x * projectOnto.x) + (self.y * projectOnto.y)) / projectOnto.magnitude())
    #     #
    # ###

    # def projectedOnto(self, projectOnto):
    #     if ((self.x == 0 and self.y == 0) or (projectOnto.x == 0 and projectOnto.y == 0)):
    #         return Vector3()
    #     else:
    #         projectedVector = Vector3()
    #         AdotB = self.dot(projectOnto)
    #         BdotB = projectOnto.dot(projectOnto)
    #         dotRatio = AdotB / BdotB    

    #         projectedVector.x = projectOnto.x * dotRatio
    #         projectedVector.y = projectOnto.y * dotRatio
            

    #         return projectedVector
    #     #
    # ###

    def subtract(self, vector):
        result = Vector3()

        result.x = self.x - vector.x
        result.y = self.y - vector.y
        result.z = self.z - vector.z

        return result
    ###

    def add(self, vector):
        result = Vector3()

        result.x = self.x + vector.x
        result.y = self.y + vector.y
        result.z = self.z + vector.z

        return result
    ###

    def multiply(self, scalar):
        result = Vector3()

        result.x = self.x * scalar
        result.y = self.y * scalar
        result.z = self.z * scalar

        return result
    ###

    def divide(self, scalar):
        result = Vector3()

        result.x = self.x / scalar
        result.y = self.y / scalar
        result.z = self.z / scalar

        return result
    ###

    def normalized(self):
        normalized = Vector3()
        magnitude = self.magnitude()

        normalized.x = self.x / magnitude
        normalized.y = self.y / magnitude
        normalized.z = self.z / magnitude

        return normalized
    ###
###    
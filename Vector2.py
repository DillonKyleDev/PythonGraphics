import math


class Vector2():
    def __init__(self):
            self.x = 0.0
            self.y = 0.0
        #
    ###

    def dot(self, vector):
        return ((self.x * vector.x) + (self.y * vector.y))
    ###

    def magnitudeSquared(self):
        return self.dot(self)
    ###

    def magnitude(self):
        return math.sqrt(self.magnitudeSquared())
    ###

    def amountProjectedOnto(self, projectOnto):
        # if (projectOnto.magnitudeSquared() == 0):
        #     return 0
        # else:
        #     normalizedProj = self.normalized()
        #     return (((self.x * projectOnto.x) + (self.y * projectOnto.y)) / projectOnto.magnitude()) / projectOnto.magnitude()

        projectionMagnitude = self.projectedOnto(projectOnto).magnitude()

        amountProjected = projectionMagnitude / projectOnto.magnitude()

        return amountProjected
        #
    ###

    def projectedOnto(self, projectOnto):
        if ((self.x == 0 and self.y == 0) or (projectOnto.x == 0 and projectOnto.y == 0)):
            return Vector2()
        else:
            projectedVector = Vector2()
            AdotB = self.dot(projectOnto)
            BdotB = projectOnto.dot(projectOnto)
            dotRatio = AdotB / BdotB

            projectedVector.x = projectOnto.x * dotRatio
            projectedVector.y = projectOnto.y * dotRatio            

            return projectedVector
        #
    ###

    def subtract(self, vector):
        result = Vector2()

        result.x = self.x - vector.x
        result.y = self.y - vector.y        

        return result
    ###

    def add(self, vector):
        result = Vector2()

        result.x = self.x + vector.x
        result.y = self.y + vector.y        

        return result
    ###

    def multiply(self, scalar):
        result = Vector2()

        result.x = self.x * scalar
        result.y = self.y * scalar        

        return result
    ###

    def divide(self, scalar):
        result = Vector2()

        result.x = self.x / scalar
        result.y = self.y / scalar        

        return result
    ###

    def normalized(self):
        normalized = Vector2()
        magnitude = self.magnitude()

        normalized.x = self.x / magnitude
        normalized.y = self.y / magnitude

        return normalized
    ###
###    
from Vector3 import Vector3


class Object():
    def __init__(self):
        self.m_position = Vector3()
        self.m_rotation = Vector3()
        self.m_scale = Vector3()
        self.m_localCoords = []
        self.m_color = (0,255,0)
        self.m_b_isAxis = False
        self.m_textureData = []
    ###

    def setBox(self):
        self.m_localCoords = [ 
            [  1, 1, 1 ], [ -1, 1, 1 ], [ -1, -1, 1 ],
            [ -1, -1, 1 ], [ 1, -1, 1 ], [ 1, 1, 1 ], 

            [ -1, -1, 1 ], [ 1, -1, -1 ], [ 1, -1, 1 ],
            [ 1, -1, -1 ], [ -1, -1, 1 ], [ -1, -1, -1 ],

            [ 1, -1, -1 ], [ -1, 1, -1 ], [ 1, 1, -1 ],
            [ -1, 1, -1 ], [ 1, -1, -1 ], [ -1, -1, -1 ],

            [ 1, 1, 1 ], [ 1, -1, -1 ], [ 1, 1, -1 ],
            [ 1, -1, -1 ], [ 1, 1, 1 ], [ 1, -1, 1 ],

            [ -1, 1, 1 ], [ -1, -1, -1 ], [ -1, -1, 1 ],
            [ -1, -1, -1 ], [ -1, 1, 1 ], [ -1, 1, -1 ],

            [ 1, 1, 1 ],  [ -1, 1, -1 ],[ -1, 1, 1 ],
            [ -1, 1, -1 ], [ 1, 1, 1 ], [ 1, 1, -1 ],
        ]
    ###

    def setDiamond(self):
        self.m_localCoords = [
            [ -1, -1, 0 ], [ 1, -1, 0 ], [ 0, 0, 1 ], 
            [ 1, -1, -0 ], [ 1, 1, 0 ], [ 0, 0, 1 ],
            [ 1, 1, 0 ], [ -1, 1, 0 ], [ 0, 0, 1 ],
            [ -1, 1, 0 ], [ -1, -1, 0 ], [ 0, 0, 1 ],
            [ -1, -1, 0 ], [ 1, -1, 0 ], [ 0, 0, -1 ], 
            [ 1, -1, -0 ], [ 1, 1, 0 ], [ 0, 0, -1 ],
            [ 1, 1, 0 ], [ -1, 1, 0 ], [ 0, 0, -1 ],
            [ -1, 1, 0 ], [ -1, -1, 0 ], [ 0, 0, -1 ]
        ]
    ###

    def removeDuplicateEdges(self):
        coordSets = {""}

        for i in range(len(self.m_localCoords) - 1):           
            coordString1 = "".join([str(j) for j in (self.m_localCoords[i] + self.m_localCoords[ i + 1 % len(self.m_localCoords)])]) 
            coordString2 = "".join([str(j) for j in (self.m_localCoords[ i + 1 % len(self.m_localCoords)] + self.m_localCoords[i])]) 
            # print("Pair: ")
            # print(coordString1)
            # print(coordString2)
            coordSets.add(coordString1)
            coordSets.add(coordString2)
        #

        # print("Coord sets length: ")
        # print(len(coordSets) / 2)
        # print("Local coords length: ")
        # print(len(self.m_localCoords))


    ###

    def addRotation(self, rotation: Vector3):
        self.m_rotation.x += rotations.x
        self.m_rotation.y += rotations.y
        self.m_rotation.z += rotations.z
    ###
###

class Shape:
    def __init__(self, shape_type):
        self.shape_type = shape_type
        self.vertices = []
        self.indices = []
    
    def get_vertices(self):
        return self.vertices
    
    def get_indices(self):
        return self.indices


class Rectangle(Shape):
    def __init__(self, width=1.0, height=1.0):
        super().__init__("rectangle")
        w = width / 2.0
        h = height / 2.0
        
        self.vertices = [
            -w, -h, 0.0, 
             w, -h, 0.0, 
             w,  h, 0.0, 
            -w,  h, 0.0, 
        ]
        
        self.indices = [0, 1, 2, 0, 2, 3]


class Circle(Shape):
    def __init__(self, radius=0.5, segments=32):
        super().__init__("circle")
        import math

        self.vertices = [0.0, 0.0, 0.0]

        for i in range(segments):
            angle = 2.0 * math.pi * i / segments
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            self.vertices.extend([x, y, 0.0])

        for i in range(segments):
            self.indices.extend([0, i + 1, ((i + 1) % segments) + 1])


class Triangle(Shape):
    def __init__(self, size=1.0):
        super().__init__("triangle")

        h = size / 2.0
        self.vertices = [
             0.0,  h, 0.0,
            -h, -h, 0.0,
             h, -h, 0.0,
        ]

        self.indices = [0, 1, 2]


class Polygon(Shape):
    def __init__(self, sides=6, radius=0.5):
        super().__init__("polygon")
        import math

        for i in range(sides):
            angle = 2.0 * math.pi * i / sides
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            self.vertices.extend([x, y, 0.0])

        for i in range(sides):
            self.indices.extend([0, i, (i + 1) % sides])


class Line(Shape):
    def __init__(self, x1=0.0, y1=0.0, x2=1.0, y2=0.0):
        super().__init__("line")

        self.vertices = [
            x1, y1, 0.0,
            x2, y2, 0.0,
        ]

        self.indices = [0, 1]

class Cube(Shape):
    def __init__(self, size=1.0):
        super().__init__("cube")
        s = size / 2.0
        self.vertices = [
            -s,-s, s,  s,-s, s,  s, s, s, -s, s, s,
            -s,-s,-s,  s,-s,-s,  s, s,-s, -s, s,-s
        ]
        self.indices = [
            0,1,2, 0,2,3, 4,5,6, 4,6,7,
            0,4,7, 0,7,3, 1,5,6, 1,6,2,
            3,2,6, 3,6,7, 0,1,5, 0,5,4
        ]

from .component import Component

class Transform(Component):
    def __init__(self, name="transform", x=0.0, y=0.0, z=0.0, scale=1.0):
        super().__init__(name)
        self.x = x
        self.y = y
        self.z = z
        self.scale = scale

    def to_mat4(self):
        if isinstance(self.scale, (tuple, list)):
            if len(self.scale) == 3:
                sx, sy, sz = self.scale
            elif len(self.scale) == 2:
                sx, sy = self.scale
                sz = 1.0
            else:
                sx = sy = sz = 1.0
        else:
            sx = sy = sz = self.scale

        return [
            sx, 0.0, 0.0, 0.0,
            0.0, sy, 0.0, 0.0,
            0.0, 0.0, sz, 0.0,
            self.x, self.y, self.z, 1.0,
        ]

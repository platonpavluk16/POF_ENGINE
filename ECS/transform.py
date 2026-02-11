import math
from .component import Component


class Transform(Component):
    def __init__(self, x=0.0, y=0.0, z=0.0, scale=1.0):
        self.x = x
        self.y = y
        self.z = z
        self.scale = scale
        self.rotation_x = 0.0
        self.rotation_y = 0.0
        self.rotation_z = 0.0

    def to_mat4(self):
        s = self.scale

        rx = getattr(self, 'rotation_x', 0.0)
        ry = getattr(self, 'rotation_y', 0.0)
        rz = getattr(self, 'rotation_z', 0.0)

        cx, sx = math.cos(rx), math.sin(rx)
        cy, sy = math.cos(ry), math.sin(ry)
        cz, sz = math.cos(rz), math.sin(rz)

        return [
            s * (cy * cz), s * (cy * sz), s * (-sy), 0.0,
            s * (sx * sy * cz - cx * sz), s * (sx * sy * sz + cx * cz), s * (sx * cy), 0.0,
            s * (cx * sy * cz + sx * sz), s * (cx * sy * sz - sx * cz), s * (cx * cy), 0.0,
            self.x, self.y, self.z, 1.0
        ]
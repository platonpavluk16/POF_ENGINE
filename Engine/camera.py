import math

class Camera:
    def __init__(self, width=1024, height=768, position=(0, 0), zoom=1.0):
        self.width = width
        self.height = height
        self.x = position[0] if isinstance(position, (tuple, list)) else position
        self.y = position[1] if isinstance(position, (tuple, list)) else 0
        self.zoom = zoom
        self.target_object = None
        self.follow_speed = 5.0
        self.target_zoom = zoom
        self.pos = [0.0, 0.0, 3.0]
        self.fov = 125.0
        self.near = 0.1
        self.far = 100.0

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def target(self, target_object):
        self.target_object = target_object

    def set_zoom(self, zoom_level):
        self.target_zoom = zoom_level

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def update(self, dt=0.016):
        if self.target_object:
            target_x = self.target_object.x if hasattr(self.target_object, 'x') else 0
            target_y = self.target_object.y if hasattr(self.target_object, 'y') else 0

            self.x += (target_x - self.x) * self.follow_speed * dt
            self.y += (target_y - self.y) * self.follow_speed * dt

        self.zoom += (self.target_zoom - self.zoom) * 5.0 * dt

    def get_view_matrix(self):
        # Матриця вигляду (View Matrix)
        # Вона переміщує весь світ у протилежному напрямку від камери
        x, y, z = self.pos
        return [
            1.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0,
            -x, -y, -z, 1.0
        ]
    def get_projection_matrix(self):
        aspect = self.width / self.height if self.height != 0 else 1.0
        f = 1.0 / math.tan(math.radians(self.fov) / 2.0)

        return [
            f / aspect, 0.0, 0.0, 0.0,
            0.0, f, 0.0, 0.0,
            0.0, 0.0, (self.far + self.near) / (self.near - self.far), -1.0,
            0.0, 0.0, (2.0 * self.far * self.near) / (self.near - self.far), 0.0
        ]
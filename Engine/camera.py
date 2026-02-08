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
        translate_matrix = [
            1.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0,
            -self.x, -self.y, 0.0, 1.0,
        ]
        return translate_matrix

    def get_projection_matrix(self):
        left = -self.width / (2.0 * self.zoom)
        right = self.width / (2.0 * self.zoom)
        bottom = -self.height / (2.0 * self.zoom)
        top = self.height / (2.0 * self.zoom)
        near = -1.0
        far = 1.0

        proj = [
            2.0 / (right - left), 0.0, 0.0, 0.0,
            0.0, 2.0 / (top - bottom), 0.0, 0.0,
            0.0, 0.0, -2.0 / (far - near), 0.0,
            -(right + left) / (right - left),
            -(top + bottom) / (top - bottom),
            -(far + near) / (far - near),
            1.0,
        ]
        return proj
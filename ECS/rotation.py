from .component import Component

class RotationComponent(Component):
    def __init__(self, speed_x=0.0, speed_y=0.0, speed_z=0.0, enabled=True):
        super().__init__("rotation")
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.speed_z = speed_z
        self.enabled = enabled
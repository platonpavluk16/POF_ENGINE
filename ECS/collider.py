from ECS.component import Component


class Collider(Component):
    def __init__(self, name="collider", width=1.0, height=1.0, is_solid=True, mass=1.0):
        super().__init__(name)
        self.width = width
        self.height = height
        self.is_solid = is_solid
        self.mass = mass
        self.colliding_with = []

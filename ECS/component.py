class Component:
    def __init__(self, name):
        self.name = name


class Collider(Component):
    def __init__(self, name="collider", width=1.0, height=1.0, is_solid=True, mass=1.0):
        super().__init__(name)
        self.width = width
        self.height = height
        self.is_solid = is_solid
        self.mass = mass
        self.colliding_with = []


class Script(Component):
    def __init__(self, name="script", script_path=""):
        super().__init__(name)
        self.script_path = script_path
        self.script_instance = None
    
    def on_start(self):
        if self.script_instance and hasattr(self.script_instance, 'on_start'):
            self.script_instance.on_start()
    
    def on_update(self):
        if self.script_instance and hasattr(self.script_instance, 'on_update'):
            self.script_instance.on_update()
    
    def on_collision(self, other):
        if self.script_instance and hasattr(self.script_instance, 'on_collision'):
            self.script_instance.on_collision(other)

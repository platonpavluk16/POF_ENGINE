from .component import Component

class Render(Component):
    def __init__(self, name, shape=None, vertex_data=None, indices=None, color=(1.0, 1.0, 1.0, 1.0), transform=None):
        super().__init__(name)
        self.shape = shape

        if shape is not None:
            self.vertex_data = shape.get_vertices()
            self.indices = shape.get_indices()
            self.draw_mode = getattr(shape, "draw_mode", "triangles")
        else:
            self.vertex_data = vertex_data or []
            self.indices = indices or []
            self.draw_mode = "triangles"

        self.color = color
        self.transform = transform
        self._gpu = None
        self.collider = None
        self.scripts = []
        self.sprite = None

    def set_shape(self, shape):
        self.shape = shape
        if shape is not None:
            self.vertex_data = shape.get_vertices()
            self.indices = shape.get_indices()
            self.draw_mode = getattr(shape, "draw_mode", "triangles")
        else:
            self.vertex_data = []
            self.indices = []
            self.draw_mode = "triangles"
        self._gpu = None

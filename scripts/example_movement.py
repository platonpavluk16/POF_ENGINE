import Engine.input as input


class ExampleMovement:
    def __init__(self):
        self.speed = 0.002
        self.render = None

    def on_update(self):
        if not self.render or not self.render.transform:
            return

        if input.in_down("LEFT"):
            self.render.transform.x -= self.speed
        if input.in_down("RIGHT"):
            self.render.transform.x += self.speed
        if input.in_down("UP"):
            self.render.transform.y += self.speed
        if input.in_down("DOWN"):
            self.render.transform.y -= self.speed

    def on_collision(self, other):
        pass

import os

from Engine.engine import Engine
from ECS.scene import Scene
from Engine.editor import Editor
import Engine.input as input

def main():
    engine = Engine(1024, 768, "ECS Game Engine")

    scene_path = os.path.join(os.path.dirname(__file__), "scene.json")
    scene = Scene.load(scene_path)
    scene.spawn(engine)

    editor = None
    try:
        editor = Editor(engine, scene, scene_path)
    except RuntimeError as exc:
        print(exc)

    engine.camera.set_zoom(100.5)

    while not engine.should_close():
        engine.begin()
        input.in_update()

        if editor:
            editor.begin_frame()

        engine.draw()

        if editor:
            editor.end_frame()
        engine.end()

    if editor:
        editor.shutdown()
    engine.terminate()

if __name__ == "__main__":
    main()

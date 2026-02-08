import copy
import importlib.util
import json
import os
import sys
import traceback
import uuid
import time
import hashlib

from ECS.component import Collider, Script
from ECS.render import Render
from ECS.shapes import Rectangle, Triangle, Circle, Line, Polygon
from ECS.sprite import Sprite as SpriteComponent
from ECS.transform import Transform

SHAPE_TYPES = ("rectangle", "circle", "triangle", "line", "polygon")


def default_transform_component():
    return {"x": 0.0, "y": 0.0, "z": 0.0, "scale": 1.0}


def default_shape_data(shape_type):
    if shape_type == "rectangle":
        return {"type": "rectangle", "width": 1.0, "height": 1.0}
    if shape_type == "circle":
        return {"type": "circle", "radius": 0.5, "segments": 32}
    if shape_type == "triangle":
        return {"type": "triangle", "size": 1.0}
    if shape_type == "line":
        return {"type": "line", "x1": -0.5, "y1": 0.0, "x2": 0.5, "y2": 0.0}
    if shape_type == "polygon":
        return {"type": "polygon", "sides": 6, "radius": 0.5}
    return {"type": "rectangle", "width": 1.0, "height": 1.0}


def default_render_component(shape_type="rectangle"):
    return {
        "shape": default_shape_data(shape_type),
        "color": [0.7, 0.7, 0.7, 1.0],
    }


def default_script_component():
    return {"scripts": []}


def default_sprite_component(image_path=""):
    return {"image_path": image_path}


_script_cache = {}

def load_script_instance(script_path):
    if not script_path or not os.path.exists(script_path):
        return None
    
    try:
        with open(script_path, 'rb') as f:
            script_hash = hashlib.md5(f.read()).hexdigest()
        
        cache_key = os.path.abspath(script_path)
        
        if cache_key in _script_cache:
            cached_hash, cached_instance = _script_cache[cache_key]
            if cached_hash == script_hash:
                return cached_instance
        
        module_name = f"user_script_{hashlib.md5(cache_key.encode()).hexdigest()}"
        
        if module_name in sys.modules:
            del sys.modules[module_name]
        
        spec = importlib.util.spec_from_file_location(module_name, script_path)
        if not spec or not spec.loader:
            return None
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        
        for name in dir(module):
            obj = getattr(module, name)
            if isinstance(obj, type) and obj.__module__ == module_name:
                try:
                    instance = obj()
                    _script_cache[cache_key] = (script_hash, instance)
                    return instance
                except Exception as e:
                    print(f"Error instantiating script {name}: {e}")
                    return None
    except Exception as e:
        print(f"Error loading script {script_path}: {e}")
        traceback.print_exc()
    
    return None


def collider_from_shape(shape_data):
    shape_type = (shape_data.get("type") or "rectangle").lower()
    if shape_type == "rectangle":
        width = float(shape_data.get("width", 1.0))
        height = float(shape_data.get("height", 1.0))
        return width, height
    if shape_type == "circle":
        radius = float(shape_data.get("radius", 0.5))
        size = radius * 2.0
        return size, size
    if shape_type == "triangle":
        size = float(shape_data.get("size", 1.0))
        return size, size
    if shape_type == "line":
        x1 = float(shape_data.get("x1", -0.5))
        y1 = float(shape_data.get("y1", 0.0))
        x2 = float(shape_data.get("x2", 0.5))
        y2 = float(shape_data.get("y2", 0.0))
        width = max(0.01, abs(x2 - x1))
        height = max(0.01, abs(y2 - y1))
        return width, height
    if shape_type == "polygon":
        radius = float(shape_data.get("radius", 0.5))
        size = radius * 2.0
        return size, size
    return 1.0, 1.0


def default_collider_component(shape_data, is_solid=False, mass=1.0):
    width, height = collider_from_shape(shape_data)
    return {"width": width, "height": height, "is_solid": is_solid, "mass": mass}


def shape_from_data(shape_data):
    shape_type = (shape_data.get("type") or "rectangle").lower()
    if shape_type == "rectangle":
        return Rectangle(
            width=float(shape_data.get("width", 1.0)),
            height=float(shape_data.get("height", 1.0)),
        )
    if shape_type == "circle":
        return Circle(
            radius=float(shape_data.get("radius", 0.5)),
            segments=int(shape_data.get("segments", 32)),
        )
    if shape_type == "triangle":
        return Triangle(size=float(shape_data.get("size", 1.0)))
    if shape_type == "line":
        return Line(
            x1=float(shape_data.get("x1", -0.5)),
            y1=float(shape_data.get("y1", 0.0)),
            x2=float(shape_data.get("x2", 0.5)),
            y2=float(shape_data.get("y2", 0.0)),
        )
    if shape_type == "polygon":
        return Polygon(
            sides=int(shape_data.get("sides", 6)),
            radius=float(shape_data.get("radius", 0.5)),
        )
    return Rectangle()


def _shape_fingerprint(shape_data):
    return json.dumps(shape_data, sort_keys=True)


class SceneObject:
    def __init__(self, object_id, name, components=None):
        self.id = object_id
        self.name = name
        self.components = components or {}
        self.render = None
        self._shape_fingerprint = None
        self.ensure_transform()

    def ensure_transform(self):
        if "transform" not in self.components:
            self.components["transform"] = default_transform_component()

    def to_dict(self):
        return {"id": self.id, "name": self.name, "components": self.components}

    def create_render(self):
        render_data = self.components.get("render")
        if not render_data:
            self.render = None
            return None

        transform_data = self.components.get("transform", {})
        transform = Transform(
            x=float(transform_data.get("x", 0.0)),
            y=float(transform_data.get("y", 0.0)),
            z=float(transform_data.get("z", 0.0)),
            scale=transform_data.get("scale", 1.0),
        )

        shape_data = render_data.get("shape", {})
        shape = shape_from_data(shape_data)
        color = render_data.get("color", [1.0, 1.0, 1.0, 1.0])

        render = Render(self.name, shape=shape, color=tuple(color), transform=transform)
        self._shape_fingerprint = _shape_fingerprint(shape_data)

        collider_data = self.components.get("collider")
        if collider_data:
            render.collider = Collider(
                width=float(collider_data.get("width", 1.0)),
                height=float(collider_data.get("height", 1.0)),
                is_solid=bool(collider_data.get("is_solid", False)),
                mass=float(collider_data.get("mass", 1.0)),
            )

        script_data = self.components.get("script")
        if script_data:
            scripts_list = script_data.get("scripts", [])
            render.scripts = []
            for script_path in scripts_list:
                if script_path and os.path.exists(script_path):
                    script = Script("script", script_path)
                    script.script_instance = load_script_instance(script_path)
                    if script.script_instance:
                        script.script_instance.render = render
                    render.scripts.append(script)
        else:
            render.scripts = []

        sprite_data = self.components.get("sprite")
        if sprite_data:
            image_path = sprite_data.get("image_path", "")
            if image_path and os.path.exists(image_path):
                sprite = SpriteComponent("sprite", image_path)
                if sprite.loaded:
                    render.sprite = sprite
                    render.draw_mode = "triangles"

        self.render = render
        return render

    def apply_components(self):
        if not self.render:
            return

        self.render.name = self.name

        transform_data = self.components.get("transform", {})
        if self.render.transform:
            self.render.transform.x = float(transform_data.get("x", 0.0))
            self.render.transform.y = float(transform_data.get("y", 0.0))
            self.render.transform.z = float(transform_data.get("z", 0.0))
            self.render.transform.scale = transform_data.get("scale", 1.0)

        render_data = self.components.get("render", {})
        color = render_data.get("color", [1.0, 1.0, 1.0, 1.0])
        self.render.color = tuple(color)

        shape_data = render_data.get("shape", {})
        fingerprint = _shape_fingerprint(shape_data)
        if fingerprint != self._shape_fingerprint:
            self._shape_fingerprint = fingerprint
            self.render.set_shape(shape_from_data(shape_data))

        collider_data = self.components.get("collider")
        if collider_data:
            if self.render.collider is None:
                self.render.collider = Collider()
            self.render.collider.width = float(collider_data.get("width", 1.0))
            self.render.collider.height = float(collider_data.get("height", 1.0))
            self.render.collider.is_solid = bool(collider_data.get("is_solid", False))
            self.render.collider.mass = float(collider_data.get("mass", 1.0))
        else:
            self.render.collider = None

        script_data = self.components.get("script")
        if script_data:
            scripts_list = script_data.get("scripts", [])
            self.render.scripts = []
            for script_path in scripts_list:
                if script_path and os.path.exists(script_path):
                    script = Script("script", script_path)
                    script.script_instance = load_script_instance(script_path)
                    if script.script_instance:
                        script.script_instance.render = self.render
                    self.render.scripts.append(script)
        else:
            self.render.scripts = []

        sprite_data = self.components.get("sprite")
        if sprite_data:
            image_path = sprite_data.get("image_path", "")
            if image_path and os.path.exists(image_path):
                if self.render.sprite is None or self.render.sprite.image_path != image_path:
                    sprite = SpriteComponent("sprite", image_path)
                    if sprite.loaded:
                        self.render.sprite = sprite
                        self.render.draw_mode = "triangles"
                        self.render._gpu = None
            else:
                self.render.sprite = None
        else:
            self.render.sprite = None


class Scene:
    def __init__(self, name="Scene", objects=None, path=None):
        self.name = name
        self.objects = objects or []
        self.path = path

    @classmethod
    def load(cls, path):
        if not os.path.exists(path):
            scene = default_scene()
            scene.path = path
            scene.save()
            return scene

        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)

        scene_data = data.get("scene", data)
        scene_name = scene_data.get("name", "Scene")
        objects_data = scene_data.get("objects", [])

        objects = []
        for entry in objects_data:
            object_id = entry.get("id") or entry.get("name") or "object"
            object_name = entry.get("name", object_id)
            components = entry.get("components", {})
            objects.append(SceneObject(object_id, object_name, components))

        return cls(name=scene_name, objects=objects, path=path)

    def to_dict(self):
        return {
            "scene": {
                "name": self.name,
                "objects": [obj.to_dict() for obj in self.objects],
            }
        }

    def save(self, path=None):
        if path:
            self.path = path
        if not self.path:
            return
        with open(self.path, "w", encoding="utf-8") as handle:
            json.dump(self.to_dict(), handle, indent=2)

    def spawn(self, engine):
        for obj in self.objects:
            render = obj.create_render()
            if render:
                engine.add_render(render)

    def find_by_id(self, object_id):
        for obj in self.objects:
            if obj.id == object_id:
                return obj
        return None


def default_scene():
    rect = SceneObject(
        "rect",
        "Rectangle",
        {
            "transform": {"x": -0.3, "y": -0.3, "z": 0.0, "scale": 1.0},
            "render": {
                "shape": {"type": "rectangle", "width": 0.8, "height": 0.5},
                "color": [0.92, 0.22, 0.22, 1.0],
            },
            "collider": {"width": 0.8, "height": 0.5, "is_solid": True, "mass": 100000.0},
        },
    )

    tri = SceneObject(
        "tri",
        "Triangle",
        {
            "transform": {"x": 0.5, "y": -0.2, "z": 0.0, "scale": 1.0},
            "render": {"shape": {"type": "triangle", "size": 0.6}, "color": [0.2, 0.8, 0.2, 1.0]},
            "collider": {"width": 0.6, "height": 0.6, "is_solid": True, "mass": 5000000.0},
        },
    )

    cir = SceneObject(
        "cir",
        "Circle",
        {
            "transform": {"x": 0.0, "y": 0.4, "z": 0.0, "scale": 1.0},
            "render": {"shape": {"type": "circle", "radius": 0.4, "segments": 32}, "color": [0.2, 0.4, 0.9, 1.0]},
            "collider": {"width": 0.4, "height": 0.4, "is_solid": False, "mass": 1.0},
        },
    )

    return Scene(name="Main", objects=[rect, tri, cir])

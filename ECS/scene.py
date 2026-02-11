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
from ECS.shapes import Rectangle, Triangle, Circle, Line, Polygon, Cube
from ECS.sprite import Sprite as SpriteComponent
from ECS.transform import Transform

# Константи для редактора
SHAPE_TYPES = ("rectangle", "circle", "triangle", "line", "polygon", "cube")

_script_cache = {}


# --- Функції дефолтних значень для Editor.py ---

def default_transform_component():
    return {
        "x": 0.0, "y": 0.0, "z": 0.0,
        "scale": 1.0,
        "rotation_x": 0.0, "rotation_y": 0.0, "rotation_z": 0.0
    }


def default_shape_data(shape_type):
    if shape_type == "cube": return {"type": "cube", "size": 1.0}
    if shape_type == "circle": return {"type": "circle", "radius": 0.5, "segments": 32}
    return {"type": shape_type, "width": 1.0, "height": 1.0}


def default_render_component(shape_type="rectangle"):
    return {
        "shape": default_shape_data(shape_type),
        "color": [0.7, 0.7, 0.7, 1.0],
    }


def default_collider_component(shape_data=None, is_solid=False, mass=1.0):
    return {"width": 1.0, "height": 1.0, "is_solid": is_solid, "mass": mass}


def default_script_component():
    return {"scripts": []}


def default_sprite_component(image_path=""):
    return {"image_path": image_path}


# --- Динамічне завантаження скриптів ---

def load_script_instance(script_path):
    if not script_path or not os.path.exists(script_path):
        return None
    try:
        # Щоб скрипти оновлювалися без перезапуску, використовуємо хеш файлу
        with open(script_path, 'rb') as f:
            script_content = f.read()
            script_hash = hashlib.md5(script_content).hexdigest()

        cache_key = os.path.abspath(script_path)

        # Створюємо унікальне ім'я модуля
        module_name = f"user_script_{hashlib.md5(cache_key.encode()).hexdigest()}"

        spec = importlib.util.spec_from_file_location(module_name, script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Шукаємо клас у модулі (зазвичай це перший знайдений клас)
        for name in dir(module):
            obj = getattr(module, name)
            if isinstance(obj, type) and obj.__module__ == module_name:
                return obj()  # Створюємо екземпляр класу
    except Exception as e:
        print(f"Помилка завантаження скрипта {script_path}: {e}")
        traceback.print_exc()
    return None


def shape_from_data(shape_data):
    st = (shape_data.get("type") or "rectangle").lower()
    if st == "cube": return Cube(size=float(shape_data.get("size", 1.0)))
    if st == "rectangle": return Rectangle(width=float(shape_data.get("width", 1.0)),
                                           height=float(shape_data.get("height", 1.0)))
    if st == "circle": return Circle(radius=float(shape_data.get("radius", 0.5)),
                                     segments=int(shape_data.get("segments", 32)))
    if st == "triangle": return Triangle(size=float(shape_data.get("size", 1.0)))
    return Rectangle()


# --- КЛАС ОБ'ЄКТА ---

class SceneObject:
    def __init__(self, object_id, name, components=None):
        self.id = object_id
        self.name = name
        self.components = components or {}
        self.render = None
        self.ensure_transform()

    def ensure_transform(self):
        if "transform" not in self.components:
            self.components["transform"] = default_transform_component()

    def to_dict(self):
        return {"id": self.id, "name": self.name, "components": self.components}

    def create_render(self):
        # 1. Створюємо трансформ
        t_data = self.components.get("transform", {})
        transform = Transform(
            x=float(t_data.get("x", 0.0)), y=float(t_data.get("y", 0.0)), z=float(t_data.get("z", 0.0)),
            scale=float(t_data.get("scale", 1.0))
        )
        transform.rotation_x = float(t_data.get("rotation_x", 0.0))
        transform.rotation_y = float(t_data.get("rotation_y", 0.0))
        transform.rotation_z = float(t_data.get("rotation_z", 0.0))

        # 2. Якщо є компонент render, створюємо графіку
        r_data = self.components.get("render")
        if r_data:
            shape = shape_from_data(r_data.get("shape", {}))
            color = tuple(r_data.get("color", [1, 1, 1, 1]))
            render = Render(self.name, shape=shape, color=color, transform=transform)
        else:
            # Створюємо порожній рендер (Invisible Object) суто для скриптів
            render = Render(self.name, shape=None, transform=transform)

        render.owner = self
        render.scripts = []  # Ініціалізуємо список скриптів

        # 3. Додаємо колайдер
        c_data = self.components.get("collider")
        if c_data:
            render.collider = Collider(
                width=float(c_data.get("width", 1.0)), height=float(c_data.get("height", 1.0)),
                is_solid=bool(c_data.get("is_solid", False)), mass=float(c_data.get("mass", 1.0))
            )

        # 4. ДОДАЄМО СКРИПТИ (Ось те, що ти питав)
        s_data = self.components.get("script")
        if s_data:
            for path in s_data.get("scripts", []):
                if os.path.exists(path):
                    script_comp = Script("script", path)
                    script_comp.script_instance = load_script_instance(path)
                    if script_comp.script_instance:
                        # Даємо скрипту доступ до рендеру та самого об'єкта
                        script_comp.script_instance.render = render
                        script_comp.script_instance.owner = self
                        render.scripts.append(script_comp)

        self.render = render
        return render

    def apply_components(self):
        if not self.render: return
        t_data = self.components.get("transform", {})
        self.render.transform.x = float(t_data.get("x", 0.0))
        self.render.transform.y = float(t_data.get("y", 0.0))
        self.render.transform.z = float(t_data.get("z", 0.0))
        self.render.transform.scale = float(t_data.get("scale", 1.0))

        # Оновлення кольору
        r_data = self.components.get("render", {})
        if "color" in r_data:
            self.render.color = tuple(float(c) for c in r_data["color"])


# --- КЛАС СЦЕНИ ---

class Scene:
    def __init__(self, name="Scene", objects=None, path=None):
        self.name = name
        self.objects = objects or []
        self.path = path

    @classmethod
    def load(cls, path):
        if not os.path.exists(path): return cls(path=path)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        sc_data = data.get("scene", data)
        objs = []
        for o in sc_data.get("objects", []):
            objs.append(SceneObject(o.get("id", str(uuid.uuid4())[:8]), o.get("name", "Obj"), o.get("components", {})))
        return cls(name=sc_data.get("name", "Scene"), objects=objs, path=path)

    def spawn(self, engine):
        for obj in self.objects:
            render = obj.create_render()
            if render:
                engine.add_render(render)

    def find_by_id(self, object_id):
        for obj in self.objects:
            if str(obj.id) == str(object_id):
                return obj
        return None

    def save(self, path=None):
        p = path or self.path
        if not p: return
        data = {"scene": {"name": self.name, "objects": [obj.to_dict() for obj in self.objects]}}
        with open(p, "w", encoding="utf-8") as f: json.dump(data, f, indent=2)
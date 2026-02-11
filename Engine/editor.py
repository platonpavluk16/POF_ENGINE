import imgui
from imgui.integrations.glfw import GlfwRenderer
import os
import glfw
from ECS.scene import (
    SHAPE_TYPES,
    SceneObject,
    default_collider_component,
    default_render_component,
    default_script_component,
    default_sprite_component,
    default_shape_data,
    default_transform_component,
)


class Editor:
    def __init__(self, engine, scene, scene_path):
        self.engine = engine
        self.scene = scene
        self.scene_path = scene_path
        self.selected_id = None
        self.is_playing = False
        self.scene_name_buffer = scene.name
        imgui.create_context()
        self._apply_style()
        self.impl = GlfwRenderer(self.engine.window)
        glfw.set_framebuffer_size_callback(self.engine.window, self.engine._on_resize)

    def shutdown(self):
        self.impl.shutdown()

    def begin_frame(self):
        self.impl.process_inputs()
        imgui.new_frame()
        self._draw_ui()

    def end_frame(self):
        imgui.render()
        self.impl.render(imgui.get_draw_data())

    def _apply_style(self):
        style = imgui.get_style()
        style.window_rounding = 0.0
        colors = style.colors
        colors[imgui.COLOR_WINDOW_BACKGROUND] = (0.14, 0.14, 0.15, 1.0)
        colors[imgui.COLOR_TITLE_BACKGROUND] = (0.12, 0.12, 0.13, 1.0)
        colors[imgui.COLOR_BUTTON] = (0.20, 0.20, 0.22, 1.0)
        colors[imgui.COLOR_TEXT] = (0.86, 0.86, 0.86, 1.0)

    def _draw_ui(self):
        io = imgui.get_io()
        w, h = io.display_size
        self._draw_scenes_panel(260, 80)
        self._draw_hierarchy(260, h - 80)
        self._draw_inspector(w - 320, 320, h)

    def _draw_scenes_panel(self, width, height):
        imgui.set_next_window_position(0, 0)
        imgui.set_next_window_size(width, height)
        imgui.begin("Scenes", flags=imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_COLLAPSE)
        if imgui.button("Save Scene"): self._save_scene()
        imgui.end()

    def _draw_hierarchy(self, width, height):
        imgui.set_next_window_position(0, 80)
        imgui.set_next_window_size(width, height)
        imgui.begin("Hierarchy", flags=imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_RESIZE)
        if not self.is_playing:
            if imgui.button("Run"): self._set_playing(True)
            imgui.same_line()
            if imgui.button("Add 2D"): imgui.open_popup("a2d")
            imgui.same_line()
            if imgui.button("Add 3D"): imgui.open_popup("a3d")

            if imgui.begin_popup("a2d"):
                for t in SHAPE_TYPES:
                    if imgui.menu_item(t.title())[0]: self._add_object(t)
                imgui.end_popup()
            if imgui.begin_popup("a3d"):
                if imgui.menu_item("Cube")[0]: self._add_3d_object("cube")
                imgui.end_popup()
        else:
            if imgui.button("Stop"): self._set_playing(False)

        imgui.separator()
        for obj in self.scene.objects:
            if imgui.selectable(f"{obj.name}##{obj.id}", obj.id == self.selected_id)[0]:
                self.selected_id = obj.id
        imgui.end()

    def _draw_inspector(self, x_pos, width, height):
        imgui.set_next_window_position(x_pos, 0)
        imgui.set_next_window_size(width, height)
        imgui.begin("Inspector", flags=imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_RESIZE)
        obj = self.scene.find_by_id(self.selected_id) if self.selected_id else None
        if not obj:
            imgui.text("Select an object")
            imgui.end()
            return

        # Додавання компонентів
        if imgui.button("Add Component"): imgui.open_popup("add_c")
        if imgui.begin_popup("add_c"):
            # Додав "script" та "collider" у список
            for c in ["transform", "render", "rotation", "collider", "script"]:
                if c not in obj.components and imgui.menu_item(c.title())[0]:
                    self._add_comp(obj, c)
            imgui.end_popup()

        imgui.separator()

        # Відображення компонентів
        self._draw_transform(obj)
        self._draw_rotation_comp(obj)
        self._draw_render(obj)
        self._draw_collider_comp(obj)  # Відображення колайдера
        self._draw_script_comp(obj)  # ВІДОБРАЖЕННЯ СКРИПТІВ

        imgui.spacing()
        if imgui.button("Delete Object"): self._delete_object(obj)
        imgui.end()

    def _add_comp(self, obj, name):
        if name == "rotation":
            obj.components[name] = {"speed_x": 0.0, "speed_y": 1.0, "speed_z": 0.0, "enabled": True}
        elif name == "transform":
            obj.components[name] = default_transform_component()
        elif name == "render":
            obj.components[name] = default_render_component("rectangle")
        elif name == "collider":
            obj.components[name] = default_collider_component()
        elif name == "script":
            obj.components[name] = default_script_component()

        obj.apply_components()
        self._save_scene()

    def _draw_script_comp(self, obj):
        """Метод для малювання компонента Script"""
        s_data = obj.components.get("script")
        if not s_data: return

        expanded, _ = imgui.collapsing_header("Script Component", imgui.TREE_NODE_DEFAULT_OPEN)
        if expanded:
            changed = False
            scripts = s_data.get("scripts", [])

            for i, path in enumerate(scripts):
                changed_this, new_path = imgui.input_text(f"File Path ##{obj.id}_{i}", path, 256)
                if changed_this:
                    scripts[i] = new_path
                    changed = True

                imgui.same_line()
                if imgui.button(f"X##del_{obj.id}_{i}"):
                    scripts.pop(i)
                    changed = True
                    break

            if imgui.button("Add Script Path"):
                scripts.append("scripts/camera.py")
                changed = True

            if changed:
                s_data["scripts"] = scripts
                self._save_scene()

    def _draw_collider_comp(self, obj):
        """Метод для малювання компонента Collider"""
        col = obj.components.get("collider")
        if not col or not imgui.collapsing_header("Collider Component")[0]: return

        changed = False
        c, v = imgui.drag_float("Width", col.get("width", 1.0), 0.05)
        if c: col["width"] = v; changed = True

        c, v = imgui.drag_float("Height", col.get("height", 1.0), 0.05)
        if c: col["height"] = v; changed = True

        c, v = imgui.checkbox("Is Solid", col.get("is_solid", False))
        if c: col["is_solid"] = v; changed = True

        if changed: self._save_scene()

    def _draw_rotation_comp(self, obj):
        rot = obj.components.get("rotation")
        if not rot or not imgui.collapsing_header("Rotation Component", imgui.TREE_NODE_DEFAULT_OPEN)[0]: return

        changed = False
        c, v = imgui.checkbox("Enabled", rot.get("enabled", True))
        if c: rot["enabled"] = v; changed = True

        for axis in ["speed_x", "speed_y", "speed_z"]:
            c, v = imgui.drag_float(f"{axis.replace('_', ' ').title()}", rot.get(axis, 0.0), 0.05)
            if c: rot[axis] = v; changed = True

        if changed: self._save_scene()

    def _draw_transform(self, obj):
        t = obj.components.get("transform")
        if not t or not imgui.collapsing_header("Transform", imgui.TREE_NODE_DEFAULT_OPEN)[0]: return
        changed = False
        for a in ["x", "y", "z"]:
            c, v = imgui.drag_float(f"Pos {a.upper()}", float(t.get(a, 0.0)), 0.05)
            if c: t[a] = v; changed = True

        c, v = imgui.drag_float("Scale", float(t.get("scale", 1.0)), 0.05)
        if c: t["scale"] = v; changed = True

        if changed: obj.apply_components(); self._save_scene()

    def _draw_render(self, obj):
        r = obj.components.get("render")
        if not r or not imgui.collapsing_header("Render")[0]: return
        c, nc = imgui.color_edit4("Color", *r.get("color", [1, 1, 1, 1]))
        if c: r["color"] = list(nc); self._save_scene()

    def _add_3d_object(self, shape_type):
        obj_id = f"3d_{shape_type}_{len(self.scene.objects)}"
        components = {
            "transform": {"x": 0.0, "y": 0.0, "z": -5.0, "scale": 1.0, "rotation_x": 0, "rotation_y": 0,
                          "rotation_z": 0},
            "render": {"shape": {"type": shape_type}, "color": [1, 1, 1, 1]},
            "rotation": {"speed_x": 0.0, "speed_y": 1.0, "speed_z": 0.0, "enabled": True}
        }
        obj = SceneObject(obj_id, "New 3D Object", components)
        r = obj.create_render()
        if r: self.engine.add_render(r)
        self.scene.objects.append(obj)
        self.selected_id = obj.id
        self._save_scene()

    def _add_object(self, shape_type):
        obj_id = f"{shape_type}_{len(self.scene.objects)}"
        components = {"transform": default_transform_component(), "render": default_render_component(shape_type)}
        obj = SceneObject(obj_id, shape_type.title(), components)
        r = obj.create_render()
        if r: self.engine.add_render(r)
        self.scene.objects.append(obj)
        self.selected_id = obj.id
        self._save_scene()

    def _delete_object(self, obj):
        if obj.render: self.engine.remove_render(obj.render)
        self.scene.objects = [o for o in self.scene.objects if o.id != obj.id]
        self.selected_id = None
        self._save_scene()

    def _save_scene(self):
        if not self.is_playing: self.scene.save(self.scene_path)

    def _set_playing(self, playing):
        self.is_playing = playing
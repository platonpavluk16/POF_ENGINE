try:
    import imgui
    from imgui.integrations.glfw import GlfwRenderer
except ImportError:
    imgui = None
    GlfwRenderer = None

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
        if imgui is None or GlfwRenderer is None:
            raise RuntimeError("Missing dependency 'imgui'. Install it with: pip install imgui")
        self.engine = engine
        self.scene = scene
        self.scene_path = scene_path
        self.selected_id = None
        self.is_playing = False
        self.scene_name_buffer = scene.name

        imgui.create_context()
        self._apply_unity_style()
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

    def _apply_unity_style(self):
        style = imgui.get_style()
        style.window_rounding = 0.0
        style.frame_rounding = 2.0
        style.scrollbar_rounding = 2.0
        style.window_padding = (8.0, 8.0)
        style.item_spacing = (8.0, 6.0)
        colors = style.colors
        colors[imgui.COLOR_WINDOW_BACKGROUND] = (0.14, 0.14, 0.15, 1.0)
        colors[imgui.COLOR_TITLE_BACKGROUND] = (0.12, 0.12, 0.13, 1.0)
        colors[imgui.COLOR_TITLE_BACKGROUND_ACTIVE] = (0.16, 0.16, 0.18, 1.0)
        colors[imgui.COLOR_FRAME_BACKGROUND] = (0.20, 0.20, 0.22, 1.0)
        colors[imgui.COLOR_FRAME_BACKGROUND_HOVERED] = (0.26, 0.26, 0.28, 1.0)
        colors[imgui.COLOR_FRAME_BACKGROUND_ACTIVE] = (0.30, 0.30, 0.33, 1.0)
        colors[imgui.COLOR_BUTTON] = (0.20, 0.20, 0.22, 1.0)
        colors[imgui.COLOR_BUTTON_HOVERED] = (0.30, 0.30, 0.33, 1.0)
        colors[imgui.COLOR_BUTTON_ACTIVE] = (0.36, 0.36, 0.40, 1.0)
        colors[imgui.COLOR_HEADER] = (0.22, 0.22, 0.24, 1.0)
        colors[imgui.COLOR_HEADER_HOVERED] = (0.30, 0.30, 0.33, 1.0)
        colors[imgui.COLOR_HEADER_ACTIVE] = (0.36, 0.36, 0.40, 1.0)
        colors[imgui.COLOR_TEXT] = (0.86, 0.86, 0.86, 1.0)

    def _draw_ui(self):
        io = imgui.get_io()
        width, height = io.display_size
        left_width = 260
        right_width = 320
        scenes_height = 80

        self._draw_scenes_panel(left_width, scenes_height)
        self._draw_hierarchy(left_width, height - scenes_height)
        self._draw_inspector(width - right_width, right_width, height)

    def _draw_scenes_panel(self, width, height):
        flags = (
            imgui.WINDOW_NO_MOVE
            | imgui.WINDOW_NO_RESIZE
            | imgui.WINDOW_NO_COLLAPSE
            | imgui.WINDOW_NO_SAVED_SETTINGS
        )
        imgui.set_next_window_position(0, 0)
        imgui.set_next_window_size(width, height)
        imgui.begin("Scenes", flags=flags)

        if imgui.button("New Scene"):
            self._create_new_scene()

        imgui.same_line(120)
        if imgui.button("Save Scene"):
            self._save_scene()

        imgui.separator()
        
        changed, self.scene_name_buffer = imgui.input_text("Scene Name##scene_name", self.scene_name_buffer, 256)
        if changed:
            self.scene.name = self.scene_name_buffer
            self._save_scene()

        imgui.end()

    def _draw_hierarchy(self, width, height):
        flags = (
            imgui.WINDOW_NO_MOVE
            | imgui.WINDOW_NO_RESIZE
            | imgui.WINDOW_NO_COLLAPSE
            | imgui.WINDOW_NO_SAVED_SETTINGS
        )
        imgui.set_next_window_position(0, 80)
        imgui.set_next_window_size(width, height)
        imgui.begin("Hierarchy", flags=flags)

        if self.is_playing:
            if imgui.button("Stop"):
                self._set_playing(False)
            imgui.same_line()
            imgui.text("Play Mode - editing locked")
        else:
            if imgui.button("Run"):
                self._set_playing(True)
            imgui.same_line()
            if imgui.button("Add Shape"):
                imgui.open_popup("add_shape_popup")

            if imgui.begin_popup("add_shape_popup"):
                for shape_type in SHAPE_TYPES:
                    clicked, _ = imgui.menu_item(shape_type.title())
                    if clicked:
                        self._add_object(shape_type)
                imgui.end_popup()

        imgui.separator()

        for obj in self.scene.objects:
            is_selected = obj.id == self.selected_id
            clicked, _ = imgui.selectable(f"{obj.name}##{obj.id}", is_selected)
            if clicked:
                self.selected_id = obj.id

        imgui.end()

    def _draw_inspector(self, x_pos, width, height):
        flags = (
            imgui.WINDOW_NO_MOVE
            | imgui.WINDOW_NO_RESIZE
            | imgui.WINDOW_NO_COLLAPSE
            | imgui.WINDOW_NO_SAVED_SETTINGS
        )
        imgui.set_next_window_position(x_pos, 0)
        imgui.set_next_window_size(width, height)
        imgui.begin("Inspector", flags=flags)

        obj = self.scene.find_by_id(self.selected_id) if self.selected_id else None
        if not obj:
            imgui.text("Select an object")
            imgui.end()
            return

        changed, new_name = imgui.input_text("Name##obj_name", obj.name, 256)
        if changed:
            obj.name = new_name
            self._save_scene()

        if self.is_playing:
            imgui.text(f"ID: {obj.id}")
            imgui.text(f"Name: {obj.name}")
            imgui.separator()
            imgui.text("Play Mode: editing disabled.")
            imgui.end()
            return

        imgui.text(f"ID: {obj.id}")
        changed, new_name = imgui.input_text("Name", obj.name, 64)
        if changed and new_name.strip():
            obj.name = new_name.strip()
            if obj.render:
                obj.render.name = obj.name
            self._save_scene()

        imgui.separator()

        if imgui.button("Add Component"):
            imgui.open_popup("add_component_popup")

        if imgui.begin_popup("add_component_popup"):
            if "render" not in obj.components:
                clicked, _ = imgui.menu_item("Render")
                if clicked:
                    obj.components["render"] = default_render_component("rectangle")
                    if obj.render is None:
                        render = obj.create_render()
                        if render:
                            self.engine.add_render(render)
                    else:
                        obj.apply_components()
                    self._save_scene()

            if "collider" not in obj.components:
                clicked, _ = imgui.menu_item("Collider")
                if clicked:
                    shape_data = obj.components.get("render", {}).get("shape", {})
                    obj.components["collider"] = default_collider_component(shape_data)
                    obj.apply_components()
                    self._save_scene()

            if "transform" not in obj.components:
                clicked, _ = imgui.menu_item("Transform")
                if clicked:
                    obj.components["transform"] = default_transform_component()
                    obj.apply_components()
                    self._save_scene()

            if "script" not in obj.components:
                clicked, _ = imgui.menu_item("Script")
                if clicked:
                    obj.components["script"] = default_script_component()
                    obj.apply_components()
                    self._save_scene()

            if "sprite" not in obj.components:
                clicked, _ = imgui.menu_item("Sprite")
                if clicked:
                    obj.components["sprite"] = default_sprite_component()
                    if obj.render is None:
                        render = obj.create_render()
                        if render:
                            self.engine.add_render(render)
                    else:
                        obj.apply_components()
                    self._save_scene()

            imgui.end_popup()

        self._draw_transform(obj)
        self._draw_render(obj)
        self._draw_collider(obj)
        self._draw_script(obj)
        self._draw_sprite(obj)

        imgui.separator()
        if imgui.button("Delete Object"):
            self._delete_object(obj)

        imgui.end()

    def _draw_transform(self, obj):
        transform = obj.components.get("transform")
        if not transform:
            return

        if not imgui.collapsing_header("Transform", flags=imgui.TREE_NODE_DEFAULT_OPEN)[0]:
            return

        changed_any = False
        changed, value = imgui.drag_float("X", float(transform.get("x", 0.0)), 0.01)
        if changed:
            transform["x"] = value
            changed_any = True

        changed, value = imgui.drag_float("Y", float(transform.get("y", 0.0)), 0.01)
        if changed:
            transform["y"] = value
            changed_any = True

        changed, value = imgui.drag_float("Z", float(transform.get("z", 0.0)), 0.01)
        if changed:
            transform["z"] = value
            changed_any = True

        changed, value = imgui.drag_float("Scale", float(transform.get("scale", 1.0)), 0.01)
        if changed:
            transform["scale"] = value
            changed_any = True

        if changed_any:
            obj.apply_components()
            self._save_scene()

    def _draw_render(self, obj):
        render_data = obj.components.get("render")
        if not render_data:
            return

        if not imgui.collapsing_header("Render", flags=imgui.TREE_NODE_DEFAULT_OPEN)[0]:
            return

        shape_data = render_data.get("shape", {})
        shape_type = (shape_data.get("type") or "rectangle").lower()
        if shape_type not in SHAPE_TYPES:
            shape_type = "rectangle"

        current_index = SHAPE_TYPES.index(shape_type)
        labels = [s.title() for s in SHAPE_TYPES]
        changed, new_index = imgui.combo("Shape", current_index, labels)
        if changed:
            new_type = SHAPE_TYPES[new_index]
            render_data["shape"] = default_shape_data(new_type)
            obj.apply_components()
            self._save_scene()
            shape_data = render_data["shape"]
            shape_type = new_type

        changed_any = False
        if shape_type == "rectangle":
            changed, value = imgui.drag_float("Width", float(shape_data.get("width", 1.0)), 0.01)
            if changed:
                shape_data["width"] = value
                changed_any = True
            changed, value = imgui.drag_float("Height", float(shape_data.get("height", 1.0)), 0.01)
            if changed:
                shape_data["height"] = value
                changed_any = True
        elif shape_type == "circle":
            changed, value = imgui.drag_float("Radius", float(shape_data.get("radius", 0.5)), 0.01)
            if changed:
                shape_data["radius"] = value
                changed_any = True
            changed, value = imgui.drag_int("Segments", int(shape_data.get("segments", 32)), 1)
            if changed:
                shape_data["segments"] = max(3, value)
                changed_any = True
        elif shape_type == "triangle":
            changed, value = imgui.drag_float("Size", float(shape_data.get("size", 1.0)), 0.01)
            if changed:
                shape_data["size"] = value
                changed_any = True
        elif shape_type == "line":
            changed, value = imgui.drag_float("X1", float(shape_data.get("x1", -0.5)), 0.01)
            if changed:
                shape_data["x1"] = value
                changed_any = True
            changed, value = imgui.drag_float("Y1", float(shape_data.get("y1", 0.0)), 0.01)
            if changed:
                shape_data["y1"] = value
                changed_any = True
            changed, value = imgui.drag_float("X2", float(shape_data.get("x2", 0.5)), 0.01)
            if changed:
                shape_data["x2"] = value
                changed_any = True
            changed, value = imgui.drag_float("Y2", float(shape_data.get("y2", 0.0)), 0.01)
            if changed:
                shape_data["y2"] = value
                changed_any = True
        elif shape_type == "polygon":
            changed, value = imgui.drag_int("Sides", int(shape_data.get("sides", 6)), 1)
            if changed:
                shape_data["sides"] = max(3, value)
                changed_any = True
            changed, value = imgui.drag_float("Radius", float(shape_data.get("radius", 0.5)), 0.01)
            if changed:
                shape_data["radius"] = value
                changed_any = True

        color = list(render_data.get("color", [1.0, 1.0, 1.0, 1.0]))
        if len(color) < 4:
            color = color + [1.0] * (4 - len(color))
        changed, new_color = imgui.color_edit4("Color", *color)
        if changed:
            render_data["color"] = list(new_color)
            changed_any = True

        if changed_any:
            obj.apply_components()
            self._save_scene()

    def _draw_collider(self, obj):
        collider = obj.components.get("collider")
        if not collider:
            return

        if not imgui.collapsing_header("Collider", flags=imgui.TREE_NODE_DEFAULT_OPEN)[0]:
            return

        changed_any = False
        changed, value = imgui.drag_float("Width", float(collider.get("width", 1.0)), 0.01)
        if changed:
            collider["width"] = value
            changed_any = True

        changed, value = imgui.drag_float("Height", float(collider.get("height", 1.0)), 0.01)
        if changed:
            collider["height"] = value
            changed_any = True

        changed, value = imgui.checkbox("Is Solid", bool(collider.get("is_solid", False)))
        if changed:
            collider["is_solid"] = value
            changed_any = True

        changed, value = imgui.drag_float("Mass", float(collider.get("mass", 1.0)), 0.1)
        if changed:
            collider["mass"] = value
            changed_any = True

        if imgui.button("Remove Collider"):
            obj.components.pop("collider", None)
            obj.apply_components()
            self._save_scene()
            return

        if changed_any:
            obj.apply_components()
            self._save_scene()

    def _draw_script(self, obj):
        script_data = obj.components.get("script")
        if not script_data:
            return

        if not imgui.collapsing_header("Scripts", flags=imgui.TREE_NODE_DEFAULT_OPEN)[0]:
            return

        scripts_list = script_data.get("scripts", [])
        
        if imgui.button("Add Script"):
            import tkinter as tk
            from tkinter import filedialog
            root = tk.Tk()
            root.withdraw()
            file_path = filedialog.askopenfilename(
                title="Select Python Script",
                filetypes=[("Python Files", "*.py"), ("All Files", "*.*")]
            )
            if file_path and file_path not in scripts_list:
                scripts_list.append(file_path)
                from ECS.scene import load_script_instance
                from ECS.component import Script
                script = Script("script", file_path)
                script.script_instance = load_script_instance(file_path)
                if obj.render:
                    if script.script_instance:
                        script.script_instance.render = obj.render
                    obj.render.scripts.append(script)
                self._save_scene()

        imgui.separator()

        scripts_to_remove = []
        for i, script_path in enumerate(scripts_list):
            script_name = ""
            if script_path and os.path.exists(script_path):
                script_name = os.path.splitext(os.path.basename(script_path))[0]
            else:
                script_name = "(Invalid path)"

            imgui.text(f"{i + 1}. {script_name}")
            imgui.same_line(300)
            
            if imgui.button(f"Remove##script_{i}"):
                scripts_to_remove.append(i)

        for i in reversed(scripts_to_remove):
            scripts_list.pop(i)
            if obj.render and i < len(obj.render.scripts):
                obj.render.scripts.pop(i)
            self._save_scene()

        if not scripts_list:
            imgui.text("(No scripts)")

    def _draw_sprite(self, obj):
        sprite_data = obj.components.get("sprite")
        if not sprite_data:
            return

        if not imgui.collapsing_header("Sprite", flags=imgui.TREE_NODE_DEFAULT_OPEN)[0]:
            return

        image_path = sprite_data.get("image_path", "")
        
        if imgui.button("Browse Image"):
            import tkinter as tk
            from tkinter import filedialog
            root = tk.Tk()
            root.withdraw()
            file_path = filedialog.askopenfilename(
                title="Select Image File",
                filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp"), ("All Files", "*.*")]
            )
            if file_path:
                sprite_data["image_path"] = file_path
                obj.apply_components()
                self._save_scene()

        imgui.separator()
        
        if image_path:
            img_name = os.path.basename(image_path)
            imgui.text(f"Image: {img_name}")
            
            if obj.render and obj.render.sprite:
                sprite = obj.render.sprite
                imgui.text(f"Size: {sprite.width}x{sprite.height}")
        else:
            imgui.text("(No image selected)")

        if imgui.button("Remove Sprite"):
            del obj.components["sprite"]
            obj.apply_components()
            self._save_scene()

    def _create_new_scene(self):
        from ECS.scene import Scene
        
        renderables_to_remove = list(self.engine.renderables)
        for render in renderables_to_remove:
            self.engine.remove_render(render)
        
        scene_name = "New_Scene"
        idx = 1
        scene_path = os.path.join(os.path.dirname(self.scene_path), f"{scene_name}_{idx}.json")
        
        while os.path.exists(scene_path):
            idx += 1
            scene_path = os.path.join(os.path.dirname(self.scene_path), f"{scene_name}_{idx}.json")
        
        new_scene = Scene(name=f"{scene_name}_{idx}", path=scene_path)
        new_scene.spawn(self.engine)
        
        self.scene = new_scene
        self.scene.save()
        self.scene_path = scene_path
        self.selected_id = None

    def _add_object(self, shape_type):
        if self.is_playing:
            return
        base_name = shape_type.title()
        existing_names = {obj.name for obj in self.scene.objects}
        name = base_name
        index = 2
        while name in existing_names:
            name = f"{base_name} {index}"
            index += 1

        base_id = name.lower().replace(" ", "_")
        existing_ids = {obj.id for obj in self.scene.objects}
        object_id = base_id
        index = 2
        while object_id in existing_ids:
            object_id = f"{base_id}_{index}"
            index += 1

        components = {
            "transform": default_transform_component(),
            "render": default_render_component(shape_type),
        }
        obj = SceneObject(object_id, name, components)
        render = obj.create_render()
        if render:
            self.engine.add_render(render)

        self.scene.objects.append(obj)
        self.selected_id = obj.id
        self._save_scene()

    def _delete_object(self, obj):
        if self.is_playing:
            return
        if obj.render:
            self.engine.remove_render(obj.render)
        self.scene.objects = [item for item in self.scene.objects if item.id != obj.id]
        if self.selected_id == obj.id:
            self.selected_id = None
        self._save_scene()

    def _save_scene(self):
        if self.is_playing:
            return
        self.scene.save(self.scene_path)

    def _set_playing(self, playing):
        if self.is_playing == playing:
            return
        self.is_playing = playing
        if not self.is_playing:
            for obj in self.scene.objects:
                obj.apply_components()

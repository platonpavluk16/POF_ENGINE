import os
from OpenGL.GL import *
import ctypes
from .component import Component

try:
    from PIL import Image
except ImportError:
    Image = None


class Sprite(Component):
    def __init__(self, name="sprite", image_path=""):
        super().__init__(name)
        self.image_path = image_path
        self.width = 1.0
        self.height = 1.0
        self.texture_id = None
        self.vertex_data = []
        self.indices = []
        self.loaded = False
        
        if image_path and os.path.exists(image_path):
            self.load(image_path)
    
    def load(self, image_path):
        if not Image:
            print("PIL not installed. Install with: pip install Pillow")
            return False
        
        if not os.path.exists(image_path):
            print(f"Image not found: {image_path}")
            return False
        
        try:
            img = Image.open(image_path)
            img = img.convert("RGBA")
            
            self.width = img.width / 100.0
            self.height = img.height / 100.0
            
            img_data = img.tobytes()
            
            self.texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
            
            glBindTexture(GL_TEXTURE_2D, 0)
            
            self.image_path = image_path
            self.loaded = True
            
            return True
        except Exception as e:
            print(f"Error loading sprite {image_path}: {e}")
            return False
    
    def get_quad_vertices(self, width, height):
        w = width / 2.0
        h = height / 2.0
        
        return [
            -w, -h, 0.0,
             w, -h, 0.0,
             w,  h, 0.0,
            -w,  h, 0.0,
        ]
    
    def get_quad_uv(self):
        return [
            0.0, 1.0,
            1.0, 1.0,
            1.0, 0.0,
            0.0, 0.0,
        ]
    
    def get_quad_indices(self):
        return [
            0, 1, 2,
            0, 2, 3,
        ]

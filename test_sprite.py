import sys
sys.path.insert(0, '.')

from ECS.sprite import Sprite
import os

test_image = "488_107.jpg"
if os.path.exists(test_image):
    sprite = Sprite("test", test_image)
    print(f"Sprite loaded: {sprite.loaded}")
    print(f"Width: {sprite.width}, Height: {sprite.height}")
    print(f"Texture ID: {sprite.texture_id}")
    print(f"Vertices: {sprite.get_quad_vertices(sprite.width, sprite.height)}")
    print(f"UV: {sprite.get_quad_uv()}")
    print(f"Indices: {sprite.get_quad_indices()}")
else:
    print(f"Test image {test_image} not found")
    print(f"Current dir: {os.getcwd()}")
    print(f"Files: {os.listdir('.')}")

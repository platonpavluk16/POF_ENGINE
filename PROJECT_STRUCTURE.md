# POF Engine - Project Structure

## 📋 Overview
POF Engine is a lightweight 2D game engine built on an **Entity Component System (ECS)** architecture, featuring OpenGL rendering, input handling, and a built-in editor.

---

## 🗂️ Directory Structure

```
game_engine_python/
├── Engine/                    # Core engine systems
│   ├── engine.py             # Main engine class with rendering loop
│   ├── camera.py             # Camera system and viewport management
│   ├── editor.py             # Built-in editor UI
│   └── input.py              # Keyboard input handling
│
├── ECS/                       # Entity Component System
│   ├── component.py          # Base Component class and built-in components
│   │   ├── Component         # Base class
│   │   ├── Collider          # Physics collider data
│   │   └── Script            # Script execution component
│   │
│   ├── transform.py          # Transform component (position, rotation, scale)
│   ├── render.py             # Rendering system for 3D objects
│   ├── sprite.py             # Sprite rendering component
│   ├── shapes.py             # Shape definitions (Rectangle, Circle, Triangle, etc.)
│   ├── color.py              # Color utility functions
│   ├── collider.py           # Physics/collision system
│   └── scene.py              # Scene management and serialization
│
├── scripts/                   # Custom game scripts
│   └── example_movement.py   # Example script for entity behavior
│
├── main.py                    # Application entry point
├── scene.json                 # Scene configuration (editable)
├── logo.png                   # Engine logo
├── README.md                  # User documentation
├── LICENSE                    # MIT License
└── requirements.txt           # Python dependencies

```

---

## 🎮 Core Components

### Engine Module
- **engine.py**: Main game loop, OpenGL context management, rendering pipeline
- **camera.py**: Viewport/camera transformation, zoom controls
- **editor.py**: In-editor tools for development
- **input.py**: Input processing and event handling

### ECS Module
- **Component**: Base class for all entity behaviors
  - **Transform**: Position (x, y, z), scale, rotation data
  - **Collider**: Physics properties (width, height, mass, solidity)
  - **Script**: Attach Python scripts to entities
  - **Render**: Visual representation with shapes/colors
  - **Sprite**: Texture/image rendering

- **Scene**: Loads/saves game objects from JSON, manages entity instances

---

## 🔧 Supported Shapes
- **Rectangle**: Basic 2D box
- **Circle**: Round shapes with customizable segments
- **Triangle**: Equilateral triangles
- **Line**: Simple line segments
- **Polygon**: N-sided regular polygons

---

## 📝 Scene Format (JSON)

```json
{
  "scene": {
    "name": "SceneName",
    "objects": [
      {
        "id": "unique_id",
        "name": "EntityName",
        "components": {
          "transform": { "x": 0, "y": 0, "z": 0, "scale": 1.0 },
          "render": {
            "shape": { "type": "circle", "radius": 1.0, "segments": 32 },
            "color": [0.0, 0.23, 0.7, 1.0]
          },
          "collider": { "width": 0.4, "height": 0.4, "is_solid": true, "mass": 1.0 },
          "script": { "scripts": ["path/to/script.py"] }
        }
      }
    ]
  }
}
```

---

## 🚀 Getting Started

### Installation
```bash
# Clone repository
git clone https://github.com/platonpavluk16/POF_ENGINE.git
cd POF_ENGINE

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run engine
python main.py
```

### Creating Scripts
Scripts inherit from `EntityScript` and have lifecycle methods:
```python
class MyScript(EntityScript):
    def on_start(self):
        """Called when entity is spawned"""
        pass
    
    def on_update(self):
        """Called every frame"""
        pass
    
    def on_collision(self, other):
        """Called when collision occurs"""
        pass
```

---

## 🔌 Extension Points

### Custom Components
Extend `Component` class to create new entity behaviors:
```python
from ECS.component import Component

class HealthComponent(Component):
    def __init__(self, hp=100):
        super().__init__("health")
        self.hp = hp
```

### Custom Shapes
Extend shape classes in `shapes.py` for custom geometry rendering.

### Input Handling
Use `Engine.input` module to detect key presses and mouse input.

---

## 📦 Dependencies
- **glfw**: Window management and context
- **PyOpenGL**: OpenGL rendering
- **numpy**: Mathematical operations

---

## 🎯 Future Features
- [ ] Sound system
- [ ] Particle effects
- [ ] Animation system
- [ ] Advanced physics
- [ ] Asset manager
- [ ] Performance profiler

---

## 📄 License
MIT License - See LICENSE file for details

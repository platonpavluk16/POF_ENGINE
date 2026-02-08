# POF Engine - Architecture Documentation

## 🏗️ System Architecture

### Entity-Component-System (ECS) Pattern

The engine uses the ECS pattern for flexible entity management:

```
┌─────────────────────────────────────┐
│         Scene (GameObject Manager)  │
├─────────────────────────────────────┤
│                                     │
│  ┌──────────────────────────────┐  │
│  │    Entity (Game Object)      │  │
│  │  ┌────────────────────────┐  │  │
│  │  │ Transform Component    │  │  │
│  │  │ (position, rotation)   │  │  │
│  │  ├────────────────────────┤  │  │
│  │  │ Render Component       │  │  │
│  │  │ (shape, color)         │  │  │
│  │  ├────────────────────────┤  │  │
│  │  │ Collider Component     │  │  │
│  │  │ (physics data)         │  │  │
│  │  ├────────────────────────┤  │  │
│  │  │ Script Component       │  │  │
│  │  │ (custom behavior)      │  │  │
│  │  └────────────────────────┘  │  │
│  └──────────────────────────────┘  │
│                                     │
└─────────────────────────────────────┘
```

**Benefits:**
- Decoupled component logic
- Flexible composition of behaviors
- Easy to add/remove features
- Data-oriented design

---

## 🔄 Engine Loop

```python
while engine.is_running():
    engine.begin()
    {
        # Update input state
        input.in_update()
        
        # Editor frame logic
        if editor:
            editor.begin_frame()
        
        # Render all entities
        engine.draw()
        
        # Editor UI
        if editor:
            editor.end_frame()
    }
    engine.end()
```

---

## 📐 Coordinate System

**Conventions:**
- **X-axis**: Left (-) to Right (+)
- **Y-axis**: Bottom (-) to Top (+)
- **Z-axis**: Back (-) to Front (+)
- **Origin (0, 0)**: Center of viewport

Example entity positions:
```
         (0, 2)
           ▲
           │
(-2, 0) ◄──┼──► (2, 0)
           │
           ▼
         (0, -2)
```

---

## 🎨 Rendering Pipeline

### OpenGL Setup
1. Create GLFW window and OpenGL context
2. Compile vertex and fragment shaders
3. Create VAO/VBO for rendering

### Render Loop
1. Clear framebuffer
2. For each entity with Render component:
   - Set model matrix (Transform)
   - Set shader uniforms (color, shape type)
   - Draw mesh
3. Swap buffers

### Shader System
- **Vertex Shader**: Handles model/view/projection transformations
- **Fragment Shader**: Implements shape SDF (Signed Distance Functions) for:
  - Circle rendering
  - Rectangle rendering
  - Triangle rendering
  - Polygon rendering

---

## 💾 Scene Persistence

### JSON Structure
```json
{
  "scene": {
    "name": "Game Scene",
    "objects": [
      {
        "id": "entity_uuid",
        "name": "Entity Name",
        "components": { /* component data */ }
      }
    ]
  }
}
```

### Scene Loading Flow
```
Load JSON → Parse entities → Create GameObjects → 
Add Components → Load Scripts → Spawn Entities
```

### Script Loading
- Dynamic import from file paths
- Scripts attached to entities via Script component
- Auto-initialization with `on_start()` callback

---

## ⌨️ Input System

### Input Processing
```python
# Check key state
if input.is_key_pressed(input.KEY_W):
    # Handle W key
    pass

# Available keys: Arrow keys, WASD, Space, Ctrl, etc.
```

### Input Update Cycle
- `input.in_update()` called every frame
- Updates key states
- Processes keyboard events

---

## 🔗 Component Dependencies

### Transform Component
**Dependencies:** None (base)
**Used by:** All visual/physical entities

### Render Component
**Dependencies:** Transform (reads position/scale)
**Provides:** Visual representation

### Collider Component
**Dependencies:** Transform (reads dimensions)
**Provides:** Physics/collision data

### Script Component
**Dependencies:** Transform (may read/write)
**Provides:** Custom update logic

---

## 📊 Class Hierarchy

```
Component (abstract)
├── Transform
├── Render
├── Collider
├── Script
└── [Custom Components]

Entity
└── [owns multiple Components]

Scene
└── [owns multiple Entities]

Engine
├── Scene
├── Camera
├── Input
└── [Renderer]
```

---

## 🔌 Extension Architecture

### Adding Custom Components

```python
# 1. Extend Component class
class MyComponent(Component):
    def __init__(self, param1, param2):
        super().__init__("my_component")
        self.param1 = param1
        self.param2 = param2

# 2. Add to component.py
# 3. Update scene.py default_* functions
# 4. Update Scene.load() parser
```

### Adding Custom Shapes

```python
# 1. Extend Shape class in shapes.py
class CustomShape(Shape):
    def __init__(self, **kwargs):
        self.property = kwargs.get('property')

# 2. Update fragment shader with SDF
# 3. Register in SHAPE_TYPES
```

---

## ⚙️ Performance Considerations

### Current Optimizations
- ✅ Batch rendering (single draw call per frame)
- ✅ GPU-side shape rendering (no CPU geometry)
- ✅ Efficient matrix math (numpy)

### Potential Improvements
- Spatial partitioning (quadtree) for collision
- Object pooling for frequently created entities
- Frustum culling for off-screen objects
- Multithreading for script execution

---

## 🐛 Debug Tools

### Editor Features
- Entity list view
- Component inspector
- Property editing
- Real-time preview

### Logging
- Script execution errors printed to console
- Collision detection logging available

---

## 📚 Module Responsibilities

| Module | Responsibility |
|--------|-----------------|
| `main.py` | Entry point, application setup |
| `Engine/engine.py` | Rendering loop, GL context |
| `Engine/camera.py` | Viewport transformation |
| `Engine/input.py` | Keyboard events |
| `Engine/editor.py` | Development tools UI |
| `ECS/scene.py` | Entity management, JSON I/O |
| `ECS/component.py` | Component classes |
| `ECS/transform.py` | Position/rotation data |
| `ECS/render.py` | Rendering system |
| `ECS/shapes.py` | Shape definitions |
| `scripts/` | Game-specific logic |

---

## 🔮 Design Patterns Used

1. **Entity Component System** - Flexible composition
2. **Observer Pattern** - Input events
3. **Singleton Pattern** - Engine instance
4. **Factory Pattern** - Entity/component creation
5. **Strategy Pattern** - Different shape rendering
6. **Decorator Pattern** - Components decorating entities

---

*Last Updated: 2026*

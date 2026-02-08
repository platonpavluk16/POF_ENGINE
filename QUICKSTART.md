# Quick Start Development Guide

## 🎮 Your First Project Setup (5 minutes)

### Step 1: Environment Setup
```bash
# Navigate to project
cd d:\project\game_engine_python

# Activate virtual environment
venv\Scripts\activate

# Install dependencies (if not done)
pip install -r requirements.txt
```

### Step 2: Run the Engine
```bash
python main.py
```
You should see a window with a **blue circle** in the center.

---

## 🎨 Creating Your First Entity

### Edit `scene.json`

```json
{
  "scene": {
    "name": "My First Scene",
    "objects": [
      {
        "id": "player",
        "name": "Player",
        "components": {
          "transform": {
            "x": 0.0,
            "y": 0.0,
            "z": 0.0,
            "scale": 1.0
          },
          "render": {
            "shape": {
              "type": "rectangle",
              "width": 0.5,
              "height": 0.5
            },
            "color": [1.0, 0.0, 0.0, 1.0]
          }
        }
      },
      {
        "id": "enemy",
        "name": "Enemy",
        "components": {
          "transform": {
            "x": 2.0,
            "y": 1.0,
            "z": 0.0,
            "scale": 1.5
          },
          "render": {
            "shape": {
              "type": "circle",
              "radius": 0.5,
              "segments": 32
            },
            "color": [0.0, 1.0, 0.0, 1.0]
          }
        }
      }
    ]
  }
}
```

Run `python main.py` → You'll see a **red rectangle** and **green circle**!

---

## 📜 Creating Custom Scripts

### Step 1: Create Script File
Create `scripts/movement.py`:
```python
class MovementScript:
    def __init__(self, entity):
        self.entity = entity
        self.speed = 2.0
    
    def on_start(self):
        print(f"Movement script started for {self.entity.name}")
    
    def on_update(self):
        # Access transform
        transform = self.entity.transform
        
        # Simple movement example
        import Engine.input as input
        
        if input.is_key_pressed(input.KEY_W):
            transform.y += self.speed * 0.016  # 60 FPS delta
        if input.is_key_pressed(input.KEY_S):
            transform.y -= self.speed * 0.016
        if input.is_key_pressed(input.KEY_A):
            transform.x -= self.speed * 0.016
        if input.is_key_pressed(input.KEY_D):
            transform.x += self.speed * 0.016
```

### Step 2: Attach to Entity in `scene.json`
```json
{
  "id": "player",
  "name": "Player",
  "components": {
    "transform": { "x": 0.0, "y": 0.0, "z": 0.0, "scale": 1.0 },
    "render": {
      "shape": { "type": "rectangle", "width": 0.5, "height": 0.5 },
      "color": [1.0, 0.0, 0.0, 1.0]
    },
    "script": {
      "scripts": ["d:/project/game_engine_python/scripts/movement.py"]
    }
  }
}
```

### Step 3: Run
```bash
python main.py
# Use W/A/S/D to move the red rectangle!
```

---

## 🔧 Common Tasks

### Add Collision Detection

```json
{
  "id": "player",
  "components": {
    "collider": {
      "width": 0.5,
      "height": 0.5,
      "is_solid": true,
      "mass": 1.0
    }
  }
}
```

### Change Shape Type
```json
{
  "render": {
    "shape": {
      "type": "triangle",  // or "circle", "polygon", "line"
      "size": 1.0
    }
  }
}
```

### Adjust Color (RGBA)
```json
{
  "render": {
    "color": [r, g, b, a]  // 0.0 to 1.0
    // Examples:
    // Red: [1.0, 0.0, 0.0, 1.0]
    // Green: [0.0, 1.0, 0.0, 1.0]
    // Blue: [0.0, 0.0, 1.0, 1.0]
    // White: [1.0, 1.0, 1.0, 1.0]
    // Semi-transparent: [1.0, 1.0, 1.0, 0.5]
  }
}
```

---

## 📐 Coordinate System Quick Reference

```
         Screen Center (0, 0)
         Top-Left: (-X, +Y)      Top-Right: (+X, +Y)
         
         (-2, 2) ─────┬───── (2, 2)
                      │
         (-2, 0) ─────●───── (2, 0)  ← This is (0,0)
                      │
         (-2,-2) ─────┴────  (2,-2)
         
         Bottom-Left: (-X, -Y)   Bottom-Right: (+X, -Y)
```

---

## ⌨️ Input Keys Available

```python
input.KEY_W, input.KEY_A, input.KEY_S, input.KEY_D
input.KEY_UP, input.KEY_DOWN, input.KEY_LEFT, input.KEY_RIGHT
input.KEY_SPACE
input.KEY_LEFT_CONTROL, input.KEY_RIGHT_CONTROL
input.KEY_LEFT_SHIFT, input.KEY_RIGHT_SHIFT
input.KEY_1 through input.KEY_9
input.KEY_ESCAPE
```

Usage:
```python
if input.is_key_pressed(input.KEY_W):
    # Handle W key
    pass
```

---

## 🎯 Project Commands

### Run Engine
```bash
python main.py
```

### Run with Console Output
```bash
python -u main.py
```

### Check Dependencies
```bash
pip list
```

### Upgrade Packages
```bash
pip install -r requirements.txt --upgrade
```

---

## 📂 File Organization Best Practices

```
scripts/
├── player/
│   └── movement.py
├── enemies/
│   ├── patrol.py
│   └── attack.py
└── systems/
    ├── spawner.py
    └── health.py
```

---

## 🐛 Debugging Tips

### Print Entity Properties
```python
class DebugScript:
    def on_update(self):
        print(f"Position: ({self.entity.transform.x}, {self.entity.transform.y})")
        print(f"Children: {len(self.entity.children)}")
```

### Check Active Keys
```python
def on_update(self):
    if input.is_key_pressed(input.KEY_W):
        print("W pressed!")
```

### View Scene Tree
The editor (when running) shows all entities and components in the scene.

---

## 📚 Next Level

After mastering basics:
1. Read [ARCHITECTURE.md](ARCHITECTURE.md) for deep dive
2. Explore [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for system design
3. Create custom components (extend `Component` class)
4. Create custom shapes (extend shape classes)

---

## 🆘 Common Issues

| Issue | Solution |
|-------|----------|
| Entity not appearing | Check transform position, render component, and camera zoom |
| Script not running | Verify script path in JSON, check console errors |
| Input not working | Ensure window is focused, check key names |
| Slow performance | Reduce number of entities, optimize scripts |

---

## 💡 Tips & Tricks

1. **Test in Editor**: Press play in the built-in editor to see changes in real-time
2. **Use Console Logging**: Print transform values to debug positioning
3. **Keep Scripts Simple**: One responsibility per script
4. **Reuse Components**: Multiple entities can use the same script file
5. **Comment Your JSON**: Use `// comments` in scene.json for organization

---

Happy coding! 🚀

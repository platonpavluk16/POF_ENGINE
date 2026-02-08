# Project Management System - Developer Guide

## Overview

The POF Engine now includes a complete project management system that allows developers to:
- Create and manage multiple game projects
- Organize project assets and scripts
- Configure project settings (resolution, FPS, colors)
- Import/Export projects
- Create script templates automatically

---

## Quick Start

### Starting the Engine

```bash
python main.py
```

This will show the Project Selector interface:
```
============================================================
  POF ENGINE - Project Selector
============================================================

1. Create New Project
2. Load Existing Project
3. Run Last Project
4. Exit

------------------------------------------------------------
Choose an option: 
```

### Creating Your First Project

1. Choose option **1 (Create New Project)**
2. Enter project name (e.g., "MyGame")
3. Enter description (optional)
4. Enter viewport dimensions (default: 1024x768)

The system will create:
```
projects/
└── MyGame/
    ├── project.json          # Project configuration
    ├── scene.json            # Default scene with welcome object
    ├── assets/               # For images, sounds, etc.
    └── scripts/              # For game scripts
```

---

## Project Structure

### project.json
Contains project metadata and settings:

```json
{
  "name": "MyGame",
  "description": "My first game",
  "created": "2026-02-08T12:00:00.000000",
  "modified": "2026-02-08T12:00:00.000000",
  "version": "0.1.0",
  "engine_version": "0.1.0",
  "settings": {
    "width": 1024,
    "height": 768,
    "target_fps": 60,
    "clear_color": [0.1, 0.1, 0.1, 1.0]
  }
}
```

### Directory Structure

| Directory | Purpose |
|-----------|---------|
| `assets/` | Images, sounds, fonts, and other game assets |
| `scripts/` | Python scripts for game logic |
| `project.json` | Project configuration and metadata |
| `scene.json` | Game scene definition |

---

## Using ProjectManager Directly

### In Python Code

```python
from Engine.project_manager import ProjectManager

# Initialize manager
manager = ProjectManager()

# Create a new project
project = manager.create_project(
    name="MyAwesomeGame",
    description="An awesome game",
    width=1280,
    height=720
)

# Load existing project
manager.load_project("MyAwesomeGame")

# List all projects
projects = manager.list_projects()
print(f"Available projects: {projects}")

# Get current project path
current_path = manager.get_current_project_path()

# Get scene path
scene_path = manager.get_project_scene_path()
```

---

## Project Settings

### Modifying Settings

In the Project Selector menu, choose **5 (Project Settings)** to modify:

1. **Resolution**: Change viewport width and height
2. **Target FPS**: Set target frame rate
3. **Clear Color**: Set background color (RGBA)

### Programmatically

```python
manager.save_project_settings({
    "width": 1920,
    "height": 1080,
    "target_fps": 144,
    "clear_color": [0.0, 0.0, 0.2, 1.0]  # Dark blue
})
```

---

## Creating Script Templates

### Using the UI

In Project Selector, choose **5 (Project Settings)** then select script creation.

### Using ProjectManager

```python
# Create a script template
script_path = manager.create_script_template("player_movement")

# The script will be at:
# projects/MyGame/scripts/player_movement.py
```

The template includes structure for:
- `on_start()` - Called when entity spawns
- `on_update()` - Called every frame
- `on_collision()` - Called on collision

### Example Player Movement Script

```python
# projects/MyGame/scripts/player_movement.py

class PlayerMovement:
    def __init__(self, entity):
        self.entity = entity
        self.speed = 3.0
    
    def on_start(self):
        print(f"Player script started for {self.entity.name}")
    
    def on_update(self):
        import Engine.input as input
        
        if input.is_key_pressed(input.KEY_W):
            self.entity.transform.y += self.speed * 0.016
        if input.is_key_pressed(input.KEY_S):
            self.entity.transform.y -= self.speed * 0.016
        if input.is_key_pressed(input.KEY_A):
            self.entity.transform.x -= self.speed * 0.016
        if input.is_key_pressed(input.KEY_D):
            self.entity.transform.x += self.speed * 0.016
    
    def on_collision(self, other):
        print(f"Collided with {other.name}")
```

---

## Project Information

### Viewing Project Details

```python
info = manager.get_project_info("MyGame")

print(f"Name: {info['name']}")
print(f"Description: {info['description']}")
print(f"Created: {info['created']}")
print(f"Version: {info['version']}")
print(f"Resolution: {info['settings']['width']}x{info['settings']['height']}")
print(f"Scripts: {info['script_count']}")
print(f"Assets: {info['asset_count']}")
```

---

## Exporting and Importing Projects

### Export Project as ZIP

```python
export_path = manager.export_project("MyGame", "MyGame_backup.zip")
print(f"Exported to: {export_path}")
```

### Import Project from ZIP

```python
manager.import_project("MyGame_backup.zip", "MyGame_Restored")
print("Project imported successfully")
```

---

## Project Organization Best Practices

### Script Organization

Organize scripts by category:

```
projects/MyGame/scripts/
├── player/
│   ├── movement.py
│   ├── combat.py
│   └── inventory.py
├── enemies/
│   ├── ai.py
│   ├── patrol.py
│   └── attack.py
├── systems/
│   ├── health.py
│   ├── spawner.py
│   └── events.py
└── utils/
    ├── helpers.py
    └── constants.py
```

### Asset Organization

```
projects/MyGame/assets/
├── sprites/
│   ├── player/
│   ├── enemies/
│   └── environment/
├── sounds/
│   ├── effects/
│   └── music/
├── fonts/
└── data/
```

### Project Naming Conventions

- **Projects**: PascalCase (MyAwesomeGame, SpaceShooter)
- **Scripts**: snake_case (player_movement, enemy_ai)
- **Assets**: kebab-case (player-idle, explosion-effect)

---

## Multi-Project Workflow

### Switching Between Projects

```python
manager.load_project("Project1")
# ... work with Project1 ...

manager.load_project("Project2")
# ... work with Project2 ...
```

### Project Templates

Create a template project:

```python
# Create template
template = manager.create_project("GameTemplate", "Base template")

# Later, use it to create new projects
# Copy and rename the template folder
```

---

## Troubleshooting

### Project Not Found

```python
try:
    manager.load_project("NonExistent")
except FileNotFoundError:
    print("Project does not exist")
    projects = manager.list_projects()
    print(f"Available projects: {projects}")
```

### Scene File Missing

```python
if not os.path.exists(manager.get_project_scene_path()):
    print("Scene file missing - create default scene")
```

### Permission Errors

```python
try:
    manager.delete_project("MyProject")
except PermissionError:
    print("Cannot delete - insufficient permissions")
```

---

## Advanced Usage

### Custom Project Creation

```python
# Create project with custom settings
project = manager.create_project(
    name="CustomGame",
    description="Custom configuration",
    width=1920,
    height=1080
)

# Update settings immediately
manager.save_project_settings({
    "target_fps": 120,
    "clear_color": [0.2, 0.2, 0.3, 1.0]
})
```

### Batch Operations

```python
# List all projects and print info
for project_name in manager.list_projects():
    info = manager.get_project_info(project_name)
    print(f"{info['name']}: {info['script_count']} scripts")
```

### Project Backup

```python
import shutil
from datetime import datetime

# Create backup
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
manager.export_project(
    "MyGame",
    f"backups/MyGame_{timestamp}.zip"
)
```

---

## Complete Example Workflow

```python
from Engine.project_manager import ProjectManager

# Initialize
manager = ProjectManager()

# Create new game project
game = manager.create_project(
    name="AdventureQuest",
    description="Epic adventure game",
    width=1024,
    height=768
)

# Create player movement script
manager.create_script_template("player_movement")

# Configure project settings
manager.save_project_settings({
    "target_fps": 60,
    "clear_color": [0.05, 0.1, 0.2, 1.0]  # Dark blue background
})

# Get project information
info = manager.get_project_info("AdventureQuest")
print(f"Created: {info['name']}")
print(f"Resolution: {info['settings']['width']}x{info['settings']['height']}")
print(f"Location: {info['path']}")

# Ready to run!
# python main.py → Select "Load Existing Project" → AdventureQuest
```

---

## Project Management Commands

| Operation | Code |
|-----------|------|
| Create project | `manager.create_project(name, description, width, height)` |
| Load project | `manager.load_project(name)` |
| List projects | `manager.list_projects()` |
| Delete project | `manager.delete_project(name)` |
| Get project info | `manager.get_project_info(name)` |
| Save settings | `manager.save_project_settings(settings_dict)` |
| Create script | `manager.create_script_template(script_name)` |
| Export project | `manager.export_project(name, export_path)` |
| Import project | `manager.import_project(zip_path, project_name)` |
| Get current path | `manager.get_current_project_path()` |
| Get scene path | `manager.get_project_scene_path()` |

---

## Files Reference

- **Engine/project_manager.py** - Core project management logic
- **Engine/project_ui.py** - Interactive UI for project management
- **main.py** - Application entry point with project selection
- **projects/** - Default directory for all projects

---

*Project Management System - POF Engine v0.1.0*

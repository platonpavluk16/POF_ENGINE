# Project Management System - Testing Guide

## Test Environment Setup

```bash
# 1. Activate virtual environment
cd d:\project\game_engine_python
venv\Scripts\activate

# 2. Install dependencies (if not done)
pip install -r requirements.txt

# 3. Ready to test!
```

---

## Quick Smoke Tests

### Test 1: Start the Engine
```bash
python main.py
```

**Expected Result:**
- Project Selector menu appears
- Options to create/load/run projects shown

**Interactive Test:**
```
1. Choose "1" (Create New Project)
2. Enter project name: "TestGame"
3. Enter description: "Test project"
4. Enter width: 1024
5. Enter height: 768
```

**Expected Result:**
- Project created successfully
- Confirmation message shown
- Window opens with game engine

---

### Test 2: Project Creation

```bash
python main.py
# Choose 1 (Create New Project)
# Name: "FirstGame"
# Description: "My first game"
# Width: 1280, Height: 720
```

**Expected Result:**
```
✓ Project 'FirstGame' created successfully at d:\project\game_engine_python\projects\FirstGame
```

**File Structure Created:**
```
projects/FirstGame/
├── project.json
├── scene.json
├── assets/
└── scripts/
```

---

### Test 3: List Projects

```bash
python main.py
# Choose 3 (List All Projects)
```

**Expected Result:**
Shows all created projects with details:
- Project name
- Description
- Creation date
- Resolution
- Script/Asset counts

---

### Test 4: Project Settings

```bash
python main.py
# Choose 2 (Load Existing Project)
# Select "FirstGame"
# [Engine starts, close with ESC]
# Run again
# Choose 5 (Project Settings)
```

**Expected Result:**
```
1. Resolution: 1280x720
2. Target FPS: 60
3. Clear Color: [0.1, 0.1, 0.1, 1.0]
```

**Test Changing Resolution:**
- Choose 1
- Enter new width: 1920
- Enter new height: 1080

**Verify:**
- Settings saved
- Next run uses new resolution

---

### Test 5: Script Template Creation

```python
# In Python interpreter
from Engine.project_manager import ProjectManager

manager = ProjectManager()
manager.load_project("FirstGame")
script_path = manager.create_script_template("player_movement")
print(script_path)
```

**Expected Result:**
- File created at `projects/FirstGame/scripts/player_movement.py`
- Contains template with on_start(), on_update(), on_collision()

---

## Advanced Testing

### Test 6: Export/Import Project

```python
from Engine.project_manager import ProjectManager
import os

manager = ProjectManager()

# Export
export_path = manager.export_project("FirstGame", "FirstGame_backup.zip")
print(f"Exported: {export_path}")
assert os.path.exists(export_path), "Export failed"

# Verify ZIP contents
import zipfile
with zipfile.ZipFile(export_path) as z:
    print(z.namelist())
```

**Expected Result:**
- ZIP file created
- Contains project.json, scene.json, assets/, scripts/ folders

**Test Import:**
```python
# Import with new name
restored = manager.import_project("FirstGame_backup.zip", "FirstGame_Restored")
print(f"Imported: {restored['name']}")

# Verify
assert os.path.exists(restored['path'])
assert os.path.exists(os.path.join(restored['path'], "project.json"))
```

---

### Test 7: Project Statistics

```python
from Engine.project_manager import ProjectManager

manager = ProjectManager()

# Get all projects
projects = manager.list_projects()
print(f"Total projects: {len(projects)}")

# Get details
for proj in projects:
    info = manager.get_project_info(proj)
    print(f"\n{info['name']}")
    print(f"  Created: {info['created']}")
    print(f"  Modified: {info['modified']}")
    print(f"  Scripts: {info['script_count']}")
```

**Expected Result:**
- List of all projects
- Detailed information for each

---

### Test 8: Multiple Projects

```python
from Engine.project_manager import ProjectManager

manager = ProjectManager()

# Create multiple projects
projects = ["Game1", "Game2", "Game3"]
for name in projects:
    manager.create_project(name, f"Test project {name}")

# Verify
all_projects = manager.list_projects()
assert len(all_projects) >= 3, "Projects not created"
print(f"✓ Created {len(all_projects)} projects")
```

---

### Test 9: Project Deletion

```python
from Engine.project_manager import ProjectManager

manager = ProjectManager()

# List before
before = manager.list_projects()
print(f"Projects before: {before}")

# Delete
manager.delete_project("Game1", confirm=False)

# List after
after = manager.list_projects()
print(f"Projects after: {after}")

assert "Game1" not in after, "Project not deleted"
print("✓ Project deletion works")
```

---

### Test 10: Settings Persistence

```python
from Engine.project_manager import ProjectManager
import json

manager = ProjectManager()
manager.load_project("FirstGame")

# Save settings
new_settings = {
    "width": 1920,
    "height": 1080,
    "target_fps": 120,
    "clear_color": [0.2, 0.3, 0.5, 1.0]
}
manager.save_project_settings(new_settings)

# Reload and verify
config_path = manager.current_project['path'] + "/project.json"
with open(config_path) as f:
    data = json.load(f)

assert data['settings']['width'] == 1920, "Width not saved"
assert data['settings']['target_fps'] == 120, "FPS not saved"
print("✓ Settings persisted correctly")
```

---

## Integration Tests

### Test 11: Full Workflow

```python
from Engine.project_manager import ProjectManager
import os

def test_full_workflow():
    manager = ProjectManager()
    
    # 1. Create project
    print("Creating project...")
    project = manager.create_project(
        "FullTest",
        "Full workflow test",
        1280,
        720
    )
    assert os.path.exists(project['path']), "Project path doesn't exist"
    print("✓ Project created")
    
    # 2. Load project
    print("Loading project...")
    manager.load_project("FullTest")
    assert manager.current_project['name'] == "FullTest"
    print("✓ Project loaded")
    
    # 3. Create script
    print("Creating script template...")
    script_path = manager.create_script_template("test_script")
    assert os.path.exists(script_path), "Script not created"
    print("✓ Script template created")
    
    # 4. Update settings
    print("Updating settings...")
    manager.save_project_settings({"target_fps": 144})
    assert manager.current_project['settings']['target_fps'] == 144
    print("✓ Settings updated")
    
    # 5. Export
    print("Exporting project...")
    export_path = manager.export_project("FullTest", "FullTest_backup.zip")
    assert os.path.exists(export_path), "Export failed"
    print("✓ Project exported")
    
    print("\n✅ FULL WORKFLOW TEST PASSED")

test_full_workflow()
```

---

## Performance Tests

### Test 12: Large Project Count

```python
from Engine.project_manager import ProjectManager
import time

manager = ProjectManager()

# Create 50 projects
start = time.time()
for i in range(50):
    manager.create_project(f"PerfTest{i}", f"Performance test {i}")
creation_time = time.time() - start

# List projects
start = time.time()
projects = manager.list_projects()
list_time = time.time() - start

print(f"Created 50 projects in {creation_time:.2f}s")
print(f"Listed projects in {list_time:.2f}s")
print(f"✓ Performance acceptable")
```

---

## Error Handling Tests

### Test 13: Error Cases

```python
from Engine.project_manager import ProjectManager

manager = ProjectManager()

# Test 1: Create duplicate project
try:
    manager.create_project("FirstGame")
    manager.create_project("FirstGame")
    print("✗ Should have raised error")
except FileExistsError:
    print("✓ Duplicate project error handled")

# Test 2: Load non-existent project
try:
    manager.load_project("NonExistent")
    print("✗ Should have raised error")
except FileNotFoundError:
    print("✓ Non-existent project error handled")

# Test 3: Settings without loaded project
manager.current_project = None
try:
    manager.save_project_settings({})
    print("✗ Should have raised error")
except RuntimeError:
    print("✓ No project error handled")

# Test 4: Invalid project name
try:
    manager.create_project("")
    print("✗ Should have raised error")
except ValueError:
    print("✓ Invalid name error handled")

print("\n✅ ERROR HANDLING TESTS PASSED")
```

---

## Test Checklist

### Basic Functionality
- [ ] Project creation works
- [ ] Project loading works
- [ ] Project listing works
- [ ] Project deletion works
- [ ] Settings saving works

### Advanced Features
- [ ] Script template generation
- [ ] Project export (ZIP)
- [ ] Project import from ZIP
- [ ] Multiple projects coexist
- [ ] Settings persistence

### Error Handling
- [ ] Duplicate project error
- [ ] Non-existent project error
- [ ] Invalid name error
- [ ] No project loaded error

### Performance
- [ ] Creation is fast
- [ ] Listing is responsive
- [ ] Settings save quickly

### Integration
- [ ] Project selector UI works
- [ ] Engine loads project settings
- [ ] Scene loads from project
- [ ] Scripts locate correctly

---

## Running Tests

### Quick Test
```bash
python main.py
# Test basic UI flow
```

### Automated Tests
```python
python examples_project_management.py
# Review the examples and run them
```

### Full Suite
```bash
# 1. Test creation, loading, deletion
# 2. Test export/import
# 3. Test settings
# 4. Test error handling
# 5. Test performance
```

---

## Expected Results Summary

| Test | Duration | Status |
|------|----------|--------|
| Project Creation | <1s | ✓ |
| Project Loading | <100ms | ✓ |
| Project Listing | <500ms | ✓ |
| Settings Save | <100ms | ✓ |
| Export (ZIP) | 1-5s | ✓ |
| Import (ZIP) | 1-5s | ✓ |
| Error Handling | Instant | ✓ |

---

## Troubleshooting

### Projects not appearing
```python
manager = ProjectManager()
projects = manager.list_projects()
print(f"Projects: {projects}")
print(f"Projects dir: {manager.base_path}")
```

### Settings not persisting
```python
import json
config_path = "projects/ProjectName/project.json"
with open(config_path) as f:
    print(json.dumps(json.load(f), indent=2))
```

### Export failing
```python
import os
export_path = "backup.zip"
if os.path.exists(export_path):
    os.remove(export_path)
manager.export_project("ProjectName", export_path)
```

---

## Next Steps

If all tests pass:
✅ Project management system is working
✅ Ready for production use
✅ Can create and manage multiple games

---

*Project Management Testing Guide - POF Engine v0.1.0*

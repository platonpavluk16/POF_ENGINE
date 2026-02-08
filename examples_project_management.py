"""
Project Management Examples
Demonstrates how to use the ProjectManager API programmatically
"""

# Example 1: Create a new project
# ================================

from Engine.project_manager import ProjectManager

# Initialize the project manager
manager = ProjectManager()

# Create a new project
project = manager.create_project(
    name="MyFirstGame",
    description="My first POF Engine game",
    width=1024,
    height=768
)

print(f"Created project at: {project['path']}")
print(f"Scene file: {project['scene_path']}")
print(f"Scripts folder: {project['scripts_path']}")

# Example 2: List all available projects
# =======================================

all_projects = manager.list_projects()
print(f"Available projects: {all_projects}")

# Example 3: Load an existing project
# ===================================

manager.load_project("MyFirstGame")
current_project = manager.current_project

print(f"Loaded project: {current_project['name']}")
print(f"Description: {current_project['description']}")
print(f"Resolution: {current_project['settings']['width']}x{current_project['settings']['height']}")

# Example 4: Get detailed project information
# ============================================

info = manager.get_project_info("MyFirstGame")

print(f"\nProject Information:")
print(f"  Name: {info['name']}")
print(f"  Created: {info['created']}")
print(f"  Modified: {info['modified']}")
print(f"  Version: {info['version']}")
print(f"  Resolution: {info['settings']['width']}x{info['settings']['height']}")
print(f"  Target FPS: {info['settings']['target_fps']}")
print(f"  Scripts: {info['script_count']}")
print(f"  Assets: {info['asset_count']}")

# Example 5: Modify project settings
# ==================================

manager.save_project_settings({
    "width": 1920,
    "height": 1080,
    "target_fps": 120,
    "clear_color": [0.1, 0.2, 0.3, 1.0]  # Dark blue background
})

print("\n✓ Project settings updated")

# Example 6: Create a script template
# ===================================

script_path = manager.create_script_template("player_controller")
print(f"\nScript template created at: {script_path}")

# The template includes on_start(), on_update(), and on_collision() methods

# Example 7: Get paths for the current project
# =============================================

current_path = manager.get_current_project_path()
scene_path = manager.get_project_scene_path()
assets_path = manager.current_project["assets_path"]
scripts_path = manager.current_project["scripts_path"]

print(f"\nProject paths:")
print(f"  Project: {current_path}")
print(f"  Scene: {scene_path}")
print(f"  Assets: {assets_path}")
print(f"  Scripts: {scripts_path}")

# Example 8: Export project
# =========================

export_path = manager.export_project("MyFirstGame", "MyFirstGame_backup.zip")
print(f"\n✓ Project exported to: {export_path}")

# Example 9: Import project from backup
# =====================================

# restored_project = manager.import_project("MyFirstGame_backup.zip", "MyFirstGame_Restored")
# print(f"✓ Project imported: {restored_project['name']}")

# Example 10: Complete workflow - Create and configure a new project
# =================================================================

def setup_new_game_project(game_name):
    """Complete workflow to set up a new game project"""
    
    # Create project
    project = manager.create_project(
        name=game_name,
        description=f"{game_name} - POF Engine game",
        width=1280,
        height=720
    )
    
    print(f"✓ Created project: {game_name}")
    
    # Load the project
    manager.load_project(game_name)
    
    # Configure settings
    manager.save_project_settings({
        "target_fps": 60,
        "clear_color": [0.05, 0.05, 0.1, 1.0]  # Dark background
    })
    
    print(f"✓ Configured project settings")
    
    # Create common script templates
    manager.create_script_template("player_movement")
    manager.create_script_template("enemy_ai")
    manager.create_script_template("game_manager")
    
    print(f"✓ Created script templates")
    
    return manager.current_project

# Usage
# game_project = setup_new_game_project("AdventureQuest")
# print(f"\nProject ready at: {game_project['path']}")

# Example 11: Interactive project browser
# ========================================

def browse_projects():
    """Browse and display information about all projects"""
    
    projects = manager.list_projects()
    
    if not projects:
        print("No projects found")
        return
    
    print(f"\n{'='*60}")
    print("  Available Projects")
    print(f"{'='*60}\n")
    
    for i, project_name in enumerate(projects, 1):
        info = manager.get_project_info(project_name)
        
        print(f"{i}. {info['name']}")
        print(f"   Description: {info['description']}")
        print(f"   Resolution: {info['settings']['width']}x{info['settings']['height']}")
        print(f"   Scripts: {info['script_count']} | Assets: {info['asset_count']}")
        print(f"   Path: {info['path']}\n")

# browse_projects()

# Example 12: Batch project management
# ====================================

def list_project_scripts(project_name):
    """List all scripts in a project"""
    
    info = manager.get_project_info(project_name)
    scripts_path = info['path'] + "/scripts"
    
    import os
    
    if not os.path.exists(scripts_path):
        return []
    
    scripts = [f for f in os.listdir(scripts_path) if f.endswith(".py")]
    return scripts

# scripts = list_project_scripts("MyFirstGame")
# print(f"Scripts in MyFirstGame: {scripts}")

# Example 13: Project statistics
# ==============================

def project_statistics():
    """Display statistics about all projects"""
    
    projects = manager.list_projects()
    
    total_projects = len(projects)
    total_scripts = 0
    total_assets = 0
    
    for project_name in projects:
        info = manager.get_project_info(project_name)
        total_scripts += info['script_count']
        total_assets += info['asset_count']
    
    print(f"\nProject Statistics:")
    print(f"  Total Projects: {total_projects}")
    print(f"  Total Scripts: {total_scripts}")
    print(f"  Total Assets: {total_assets}")
    print(f"  Average Scripts: {total_scripts / total_projects if total_projects > 0 else 0:.1f}")
    print(f"  Average Assets: {total_assets / total_projects if total_projects > 0 else 0:.1f}")

# project_statistics()

# Example 14: Project cloning (backup and restore workflow)
# =========================================================

def backup_and_restore_project(source_name, backup_name):
    """Create a backup and restore it with a new name"""
    
    # Export project
    export_path = manager.export_project(source_name, f"{backup_name}.zip")
    print(f"✓ Backed up to: {export_path}")
    
    # Import with new name
    restored = manager.import_project(export_path, backup_name)
    print(f"✓ Restored as: {restored['name']}")
    
    return restored

# backup_and_restore_project("MyFirstGame", "MyFirstGame_v1")

"""
Quick Reference - Common Operations
====================================

Create project:
    manager.create_project("GameName", "Description", 1024, 768)

Load project:
    manager.load_project("GameName")

List all projects:
    manager.list_projects()

Get project info:
    manager.get_project_info("GameName")

Update settings:
    manager.save_project_settings({"width": 1920, "height": 1080})

Create script:
    manager.create_script_template("script_name")

Get current project path:
    manager.get_current_project_path()

Get scene path:
    manager.get_project_scene_path()

Export project:
    manager.export_project("GameName", "export.zip")

Import project:
    manager.import_project("export.zip", "NewGameName")

Delete project:
    manager.delete_project("GameName")
"""

"""
POF Engine - Main Application Entry Point
Handles project initialization and engine startup
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from Engine.engine import Engine
from ECS.scene import Scene
from Engine.editor import Editor
import Engine.input as input_engine
from Engine.project_manager import ProjectManager
from Engine.project_ui import ProjectCreator


def run_with_project_selection():
    """Run engine with project selection/creation workflow."""
    creator = ProjectCreator()
    manager = creator.manager
    
    print("\n" + "="*60)
    print("  POF ENGINE - Project Selector")
    print("="*60)
    
    while True:
        projects = manager.list_projects()
        
        print("\n1. Create New Project")
        print("2. Load Existing Project")
        if projects:
            print("3. Run Last Project")
        print("4. Exit")
        print("\n" + "-"*60)
        
        choice = input("Choose an option: ").strip()
        
        if choice == "1":
            creator.create_project_interactive()
            if manager.current_project:
                return manager
        elif choice == "2":
            creator.load_project_interactive()
            if manager.current_project:
                return manager
        elif choice == "3" and projects:
            manager.load_project(projects[0])
            return manager
        elif choice == "4":
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")


def main():
    """Main application entry point."""
    try:
        # Get project manager
        manager = run_with_project_selection()
        
        if not manager.current_project:
            print("✗ No project loaded")
            return
        
        project = manager.current_project
        scene_path = project["scene_path"]
        
        print("\n" + "="*60)
        print(f"  Running: {project['name']}")
        print("="*60 + "\n")
        
        # Get engine settings from project
        settings = project["settings"]
        width = settings.get("width", 1024)
        height = settings.get("height", 768)
        title = f"POF Engine - {project['name']}"
        fps = settings.get("target_fps", 60)
        
        # Initialize engine
        engine = Engine(width, height, title)
        
        # Load scene
        if not os.path.exists(scene_path):
            print(f"✗ Scene file not found: {scene_path}")
            return
        
        scene = Scene.load(scene_path)
        scene.spawn(engine)
        
        # Initialize editor
        editor = None
        try:
            editor = Editor(engine, scene, scene_path)
            print("✓ Editor initialized")
        except RuntimeError as exc:
            print(f"⚠ Editor not available: {exc}")
        
        # Set default camera zoom
        engine.camera.set_zoom(100.5)
        
        print(f"✓ Engine started - Press ESC to exit\n")
        
        # Main game loop
        frame_count = 0
        while not engine.should_close():
            engine.begin()
            input_engine.update()
            
            if editor:
                editor.begin_frame()
            
            engine.draw()
            
            if editor:
                editor.end_frame()
            
            engine.end()
            frame_count += 1
        
        # Cleanup
        if editor:
            editor.shutdown()
        engine.terminate()
        
        print(f"\n✓ Engine closed (ran {frame_count} frames)")
        
    except KeyboardInterrupt:
        print("\n\n✗ Application interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

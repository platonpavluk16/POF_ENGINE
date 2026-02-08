import os
import json
import shutil
from pathlib import Path
from datetime import datetime


class ProjectManager:
    """Manages game projects - creation, loading, saving, and organization."""
    
    PROJECTS_DIR = "projects"
    PROJECT_CONFIG_FILE = "project.json"
    SCENE_FILE = "scene.json"
    ASSETS_DIR = "assets"
    SCRIPTS_DIR = "scripts"
    
    def __init__(self, base_path=None):
        """Initialize ProjectManager.
        
        Args:
            base_path: Root directory for all projects. Defaults to ./projects
        """
        if base_path is None:
            base_path = os.path.join(os.path.dirname(__file__), "..", self.PROJECTS_DIR)
        
        self.base_path = os.path.abspath(base_path)
        self.current_project = None
        
        # Create projects directory if it doesn't exist
        os.makedirs(self.base_path, exist_ok=True)
    
    def create_project(self, name, description="", width=1024, height=768):
        """Create a new game project.
        
        Args:
            name: Project name
            description: Project description
            width: Default viewport width
            height: Default viewport height
            
        Returns:
            dict: Project data with paths and metadata
        """
        # Validate project name
        if not name or len(name.strip()) == 0:
            raise ValueError("Project name cannot be empty")
        
        project_path = os.path.join(self.base_path, name)
        
        # Check if project already exists
        if os.path.exists(project_path):
            raise FileExistsError(f"Project '{name}' already exists at {project_path}")
        
        # Create project structure
        os.makedirs(project_path, exist_ok=True)
        os.makedirs(os.path.join(project_path, self.ASSETS_DIR), exist_ok=True)
        os.makedirs(os.path.join(project_path, self.SCRIPTS_DIR), exist_ok=True)
        
        # Create project metadata
        project_data = {
            "name": name,
            "description": description,
            "created": datetime.now().isoformat(),
            "modified": datetime.now().isoformat(),
            "version": "0.1.0",
            "engine_version": "0.1.0",
            "settings": {
                "width": width,
                "height": height,
                "target_fps": 60,
                "clear_color": [0.1, 0.1, 0.1, 1.0]
            }
        }
        
        # Save project metadata
        config_path = os.path.join(project_path, self.PROJECT_CONFIG_FILE)
        with open(config_path, "w") as f:
            json.dump(project_data, f, indent=2)
        
        # Create default scene
        default_scene = {
            "scene": {
                "name": "Main",
                "objects": [
                    {
                        "id": "welcome",
                        "name": "Welcome",
                        "components": {
                            "transform": {
                                "x": 0.0,
                                "y": 0.5,
                                "z": 0.0,
                                "scale": 1.0
                            },
                            "render": {
                                "shape": {
                                    "type": "rectangle",
                                    "width": 2.0,
                                    "height": 0.5
                                },
                                "color": [0.2, 0.8, 0.2, 1.0]
                            }
                        }
                    }
                ]
            }
        }
        
        scene_path = os.path.join(project_path, self.SCENE_FILE)
        with open(scene_path, "w") as f:
            json.dump(default_scene, f, indent=2)
        
        print(f"✓ Project '{name}' created successfully at {project_path}")
        return self._load_project_data(project_path)
    
    def load_project(self, name):
        """Load an existing project.
        
        Args:
            name: Project name
            
        Returns:
            dict: Project data
        """
        project_path = os.path.join(self.base_path, name)
        
        if not os.path.exists(project_path):
            raise FileNotFoundError(f"Project '{name}' not found")
        
        project_data = self._load_project_data(project_path)
        self.current_project = project_data
        
        print(f"✓ Project '{name}' loaded successfully")
        return project_data
    
    def _load_project_data(self, project_path):
        """Load project data from filesystem.
        
        Args:
            project_path: Full path to project directory
            
        Returns:
            dict: Project data with all paths
        """
        config_path = os.path.join(project_path, self.PROJECT_CONFIG_FILE)
        
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Project config not found: {config_path}")
        
        with open(config_path, "r") as f:
            config = json.load(f)
        
        config["path"] = project_path
        config["scene_path"] = os.path.join(project_path, self.SCENE_FILE)
        config["assets_path"] = os.path.join(project_path, self.ASSETS_DIR)
        config["scripts_path"] = os.path.join(project_path, self.SCRIPTS_DIR)
        
        return config
    
    def list_projects(self):
        """List all available projects.
        
        Returns:
            list: List of project names
        """
        if not os.path.exists(self.base_path):
            return []
        
        projects = []
        for item in os.listdir(self.base_path):
            item_path = os.path.join(self.base_path, item)
            config_path = os.path.join(item_path, self.PROJECT_CONFIG_FILE)
            if os.path.isdir(item_path) and os.path.exists(config_path):
                projects.append(item)
        
        return sorted(projects)
    
    def delete_project(self, name, confirm=True):
        """Delete a project.
        
        Args:
            name: Project name
            confirm: If True, raises error unless name matches
            
        Returns:
            bool: True if deleted successfully
        """
        project_path = os.path.join(self.base_path, name)
        
        if not os.path.exists(project_path):
            raise FileNotFoundError(f"Project '{name}' not found")
        
        if confirm and name != self.current_project.get("name", ""):
            print(f"Warning: Deleting project '{name}'")
        
        shutil.rmtree(project_path)
        
        if self.current_project and self.current_project.get("name") == name:
            self.current_project = None
        
        print(f"✓ Project '{name}' deleted successfully")
        return True
    
    def get_project_info(self, name):
        """Get detailed information about a project.
        
        Args:
            name: Project name
            
        Returns:
            dict: Project information
        """
        project_data = self.load_project(name)
        
        info = {
            "name": project_data["name"],
            "description": project_data["description"],
            "created": project_data["created"],
            "modified": project_data["modified"],
            "version": project_data["version"],
            "settings": project_data["settings"],
            "path": project_data["path"],
            "scene_count": 1,  # Can extend for multiple scenes
            "script_count": len(self._get_scripts(project_data["scripts_path"])),
            "asset_count": len(self._get_assets(project_data["assets_path"]))
        }
        
        return info
    
    def _get_scripts(self, scripts_path):
        """Get all scripts in project.
        
        Args:
            scripts_path: Path to scripts directory
            
        Returns:
            list: Script file names
        """
        if not os.path.exists(scripts_path):
            return []
        
        scripts = []
        for file in os.listdir(scripts_path):
            if file.endswith(".py"):
                scripts.append(file)
        
        return scripts
    
    def _get_assets(self, assets_path):
        """Get all assets in project.
        
        Args:
            assets_path: Path to assets directory
            
        Returns:
            list: Asset file names
        """
        if not os.path.exists(assets_path):
            return []
        
        assets = []
        for file in os.listdir(assets_path):
            assets.append(file)
        
        return assets
    
    def save_project_settings(self, settings):
        """Update project settings.
        
        Args:
            settings: Dictionary of settings to update
            
        Returns:
            dict: Updated project data
        """
        if not self.current_project:
            raise RuntimeError("No project loaded")
        
        config_path = self.current_project["path"]
        config_file = os.path.join(config_path, self.PROJECT_CONFIG_FILE)
        
        # Load current config
        with open(config_file, "r") as f:
            config = json.load(f)
        
        # Update settings
        config["settings"].update(settings)
        config["modified"] = datetime.now().isoformat()
        
        # Save updated config
        with open(config_file, "w") as f:
            json.dump(config, f, indent=2)
        
        # Update current project
        self.current_project = self._load_project_data(config_path)
        
        print("✓ Project settings saved")
        return self.current_project
    
    def export_project(self, name, export_path):
        """Export project as ZIP archive.
        
        Args:
            name: Project name
            export_path: Path to export ZIP file
            
        Returns:
            str: Path to exported file
        """
        project_path = os.path.join(self.base_path, name)
        
        if not os.path.exists(project_path):
            raise FileNotFoundError(f"Project '{name}' not found")
        
        export_name = os.path.splitext(export_path)[0]
        archive_path = shutil.make_archive(export_name, "zip", project_path)
        
        print(f"✓ Project exported to {archive_path}")
        return archive_path
    
    def import_project(self, zip_path, project_name=None):
        """Import project from ZIP archive.
        
        Args:
            zip_path: Path to ZIP file
            project_name: Name for imported project. Defaults to archive name
            
        Returns:
            dict: Project data
        """
        if not os.path.exists(zip_path):
            raise FileNotFoundError(f"File not found: {zip_path}")
        
        if project_name is None:
            project_name = os.path.splitext(os.path.basename(zip_path))[0]
        
        project_path = os.path.join(self.base_path, project_name)
        
        # Extract zip
        shutil.unpack_archive(zip_path, project_path)
        
        print(f"✓ Project imported as '{project_name}'")
        return self._load_project_data(project_path)
    
    def create_script_template(self, script_name):
        """Create a new script template in current project.
        
        Args:
            script_name: Name of the script (without .py extension)
            
        Returns:
            str: Path to created script
        """
        if not self.current_project:
            raise RuntimeError("No project loaded")
        
        scripts_path = self.current_project["scripts_path"]
        script_path = os.path.join(scripts_path, f"{script_name}.py")
        
        template = f'''"""
{script_name} - Custom game script
"""


class {self._to_class_name(script_name)}:
    """Custom script for entity behavior."""
    
    def __init__(self, entity):
        """Initialize script.
        
        Args:
            entity: The entity this script is attached to
        """
        self.entity = entity
        self.speed = 1.0
    
    def on_start(self):
        """Called when entity is spawned."""
        print(f"{{self.__class__.__name__}} started for {{self.entity.name}}")
    
    def on_update(self):
        """Called every frame."""
        pass
    
    def on_collision(self, other):
        """Called when collision occurs.
        
        Args:
            other: The entity we collided with
        """
        pass
'''
        
        with open(script_path, "w") as f:
            f.write(template)
        
        print(f"✓ Script template created: {script_path}")
        return script_path
    
    @staticmethod
    def _to_class_name(name):
        """Convert snake_case to PascalCase.
        
        Args:
            name: Input name
            
        Returns:
            str: PascalCase name
        """
        return "".join(word.capitalize() for word in name.split("_"))
    
    def get_current_project_path(self):
        """Get path to current project.
        
        Returns:
            str: Full path to current project or None
        """
        return self.current_project["path"] if self.current_project else None
    
    def get_project_scene_path(self):
        """Get path to current project's scene file.
        
        Returns:
            str: Path to scene.json or None
        """
        return self.current_project["scene_path"] if self.current_project else None

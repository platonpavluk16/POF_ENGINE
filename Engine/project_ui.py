"""
Project Creation and Management UI
Provides interactive interface for creating and managing game projects
"""

import os
import json
from Engine.project_manager import ProjectManager


class ProjectCreator:
    """Interactive project creation and management interface."""
    
    def __init__(self):
        """Initialize ProjectCreator."""
        self.manager = ProjectManager()
    
    def show_menu(self):
        """Display main project menu."""
        while True:
            print("\n" + "="*50)
            print("  POF ENGINE - Project Manager")
            print("="*50)
            print("\n1. Create New Project")
            print("2. Load Existing Project")
            print("3. List All Projects")
            print("4. Delete Project")
            print("5. Project Settings")
            print("6. Exit")
            print("\n" + "-"*50)
            
            choice = input("Choose an option (1-6): ").strip()
            
            if choice == "1":
                self.create_project_interactive()
            elif choice == "2":
                self.load_project_interactive()
            elif choice == "3":
                self.list_projects_interactive()
            elif choice == "4":
                self.delete_project_interactive()
            elif choice == "5":
                self.project_settings_interactive()
            elif choice == "6":
                print("Exiting Project Manager...")
                break
            else:
                print("Invalid choice. Please try again.")
    
    def create_project_interactive(self):
        """Interactively create a new project."""
        print("\n" + "-"*50)
        print("CREATE NEW PROJECT")
        print("-"*50)
        
        # Get project name
        name = input("\nEnter project name: ").strip()
        if not name:
            print("✗ Project name cannot be empty")
            return
        
        # Get description
        description = input("Enter project description (optional): ").strip()
        
        # Get resolution
        width = self._get_positive_input("Enter viewport width (default 1024): ", 1024)
        height = self._get_positive_input("Enter viewport height (default 768): ", 768)
        
        try:
            project = self.manager.create_project(name, description, width, height)
            print(f"\n✓ Project created successfully!")
            print(f"  Location: {project['path']}")
            self.show_project_summary(project)
        except FileExistsError as e:
            print(f"\n✗ Error: {e}")
        except ValueError as e:
            print(f"\n✗ Error: {e}")
    
    def load_project_interactive(self):
        """Interactively load an existing project."""
        projects = self.manager.list_projects()
        
        if not projects:
            print("\n✗ No projects found")
            return
        
        print("\n" + "-"*50)
        print("AVAILABLE PROJECTS")
        print("-"*50)
        
        for i, project_name in enumerate(projects, 1):
            print(f"{i}. {project_name}")
        
        try:
            choice = int(input(f"\nSelect project (1-{len(projects)}): ")) - 1
            if 0 <= choice < len(projects):
                project = self.manager.load_project(projects[choice])
                self.show_project_summary(project)
            else:
                print("✗ Invalid selection")
        except ValueError:
            print("✗ Invalid input")
    
    def list_projects_interactive(self):
        """List all available projects with details."""
        projects = self.manager.list_projects()
        
        print("\n" + "-"*50)
        print("ALL PROJECTS")
        print("-"*50)
        
        if not projects:
            print("\n(No projects found)")
            return
        
        for project_name in projects:
            try:
                info = self.manager.get_project_info(project_name)
                print(f"\n📦 {info['name']}")
                print(f"   Description: {info['description'] or 'N/A'}")
                print(f"   Version: {info['version']}")
                print(f"   Created: {info['created'][:10]}")
                print(f"   Modified: {info['modified'][:10]}")
                print(f"   Resolution: {info['settings']['width']}x{info['settings']['height']}")
                print(f"   Scripts: {info['script_count']} | Assets: {info['asset_count']}")
            except Exception as e:
                print(f"\n✗ Error loading {project_name}: {e}")
    
    def delete_project_interactive(self):
        """Interactively delete a project."""
        projects = self.manager.list_projects()
        
        if not projects:
            print("\n✗ No projects found")
            return
        
        print("\n" + "-"*50)
        print("DELETE PROJECT")
        print("-"*50)
        
        for i, project_name in enumerate(projects, 1):
            print(f"{i}. {project_name}")
        
        try:
            choice = int(input(f"\nSelect project to delete (1-{len(projects)}): ")) - 1
            if 0 <= choice < len(projects):
                project_name = projects[choice]
                confirm = input(f"\nAre you sure? Type '{project_name}' to confirm: ").strip()
                
                if confirm == project_name:
                    self.manager.delete_project(project_name, confirm=False)
                    print(f"✓ Project deleted")
                else:
                    print("✗ Deletion cancelled")
            else:
                print("✗ Invalid selection")
        except ValueError:
            print("✗ Invalid input")
    
    def project_settings_interactive(self):
        """Modify project settings."""
        if not self.manager.current_project:
            print("\n✗ No project loaded. Please load a project first.")
            return
        
        project = self.manager.current_project
        print("\n" + "-"*50)
        print(f"PROJECT SETTINGS - {project['name']}")
        print("-"*50)
        
        settings = project["settings"]
        print(f"\n1. Resolution: {settings['width']}x{settings['height']}")
        print(f"2. Target FPS: {settings['target_fps']}")
        print(f"3. Clear Color: {settings['clear_color']}")
        print("4. Back to main menu")
        
        choice = input("\nChoice (1-4): ").strip()
        
        if choice == "1":
            width = self._get_positive_input("Enter width: ", settings['width'])
            height = self._get_positive_input("Enter height: ", settings['height'])
            self.manager.save_project_settings({"width": width, "height": height})
        elif choice == "2":
            fps = self._get_positive_input("Enter target FPS: ", settings['target_fps'])
            self.manager.save_project_settings({"target_fps": fps})
        elif choice == "3":
            print("Enter RGBA color values (0.0-1.0)")
            try:
                r = float(input("Red [0-1]: "))
                g = float(input("Green [0-1]: "))
                b = float(input("Blue [0-1]: "))
                a = float(input("Alpha [0-1]: "))
                
                color = [max(0, min(1, c)) for c in [r, g, b, a]]
                self.manager.save_project_settings({"clear_color": color})
            except ValueError:
                print("✗ Invalid color values")
    
    def show_project_summary(self, project):
        """Display project summary."""
        settings = project.get("settings", {})
        print(f"\n  Name: {project.get('name', 'N/A')}")
        print(f"  Description: {project.get('description', 'N/A')}")
        print(f"  Version: {project.get('version', 'N/A')}")
        print(f"  Resolution: {settings.get('width', 'N/A')}x{settings.get('height', 'N/A')}")
        print(f"  Target FPS: {settings.get('target_fps', 'N/A')}")
        print(f"  Location: {project.get('path', 'N/A')}")
    
    @staticmethod
    def _get_positive_input(prompt, default=None):
        """Get positive integer input from user.
        
        Args:
            prompt: Input prompt
            default: Default value if input is invalid
            
        Returns:
            int: User input or default
        """
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            else:
                print(f"Using default: {default}")
                return default
        except ValueError:
            print(f"Using default: {default}")
            return default


def init_project_workflow():
    """Run the project creation workflow."""
    print("\n" + "="*50)
    print("  Welcome to POF Engine Project Manager")
    print("="*50)
    
    creator = ProjectCreator()
    return creator.show_menu()

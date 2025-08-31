"""Initialize new CV projects with interactive wizard."""

from pathlib import Path
import yaml
from rich.console import Console

from ..templates import get_template_files
from ..wizard import run_init_wizard

console = Console()

def create_cv_project(project_path: Path, wizard_data: dict[str, any]) -> None:
    """Create a new CV project with template files and user data."""
    project_path.mkdir(parents=True, exist_ok=True)
    
    # Copy template files from the package
    template_files = get_template_files()
    
    for template_file, content in template_files.items():
        target_file = project_path / template_file
        target_file.parent.mkdir(parents=True, exist_ok=True)
        target_file.write_text(content, encoding="utf-8")
    
    # Create output directories
    (project_path / "out" / "pdf").mkdir(parents=True, exist_ok=True)
    (project_path / "out" / "png").mkdir(parents=True, exist_ok=True)
    
    # Customize with wizard data
    customize_project(project_path, wizard_data)
    
    # Show completion message
    wizard_data["wizard"].completion_message(project_path, wizard_data["variant"])


def customize_project(project_path: Path, wizard_data: dict[str, any]) -> None:
    """Customize the project with wizard-collected data."""
    
    # Update personal.yaml
    personal_file = project_path / "data" / "personal.yaml"
    if personal_file.exists():
        with open(personal_file, 'w', encoding='utf-8') as f:
            yaml.dump(wizard_data["personal"], f, default_flow_style=False, allow_unicode=True)
    
    # Update section files with sample data
    sections = wizard_data.get("sections", {})
    
    for section_name, section_data in sections.items():
        section_file = project_path / "data" / "sections" / f"{section_name}.yaml"
        if section_file.exists():
            # Load existing structure and update
            with open(section_file, 'r', encoding='utf-8') as f:
                existing = yaml.safe_load(f) or {}
            
            # Map section names to YAML keys
            data_key_map = {
                "experience": "positions",
                "education": "degrees", 
                "publications": "papers",
                "skills": "categories",
                "awards": "awards"
            }
            
            data_key = data_key_map.get(section_name, section_name)
            existing[data_key] = section_data
            
            with open(section_file, 'w', encoding='utf-8') as f:
                yaml.dump(existing, f, default_flow_style=False, allow_unicode=True)


def init_project_interactive(project_path: Path) -> None:
    """Initialize project with interactive wizard."""
    if project_path.exists() and any(project_path.iterdir()):
        console.print(f"[yellow]Warning: Directory {project_path} already exists and is not empty.[/yellow]")
        from rich.prompt import Confirm
        if not Confirm.ask("Continue anyway?"):
            console.print("Cancelled.")
            return
    
    # Run the wizard
    wizard_data = run_init_wizard(project_path)
    
    # Create the project
    create_cv_project(project_path, wizard_data)
"""YAML data validation for resumyst CV projects."""

from pathlib import Path
import yaml
from rich.console import Console
from rich.panel import Panel

console = Console()

class CVValidator:
    """Validates CV data files and provides helpful error messages."""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.data_path = project_path / "data"
        self.errors = []
        self.warnings = []
    
    def validate_project(self) -> bool:
        """Validate entire CV project. Returns True if valid."""
        self.errors = []
        self.warnings = []
        
        # Check project structure
        self._validate_structure()
        
        # Validate data files
        self._validate_personal_data()
        self._validate_config_data()
        self._validate_section_files()
        
        return len(self.errors) == 0
    
    def _validate_structure(self):
        """Check that required directories and files exist."""
        required_files = [
            "data/personal.yaml",
            "data/config.yaml",
            "lib/template.typ",
            "build/cv.typ"
        ]
        
        for file_path in required_files:
            full_path = self.project_path / file_path
            if not full_path.exists():
                self.errors.append(f"Missing required file: {file_path}")
    
    def _validate_personal_data(self):
        """Validate personal information."""
        personal_file = self.data_path / "personal.yaml"
        if not personal_file.exists():
            return
            
        try:
            with open(personal_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            if not data:
                self.errors.append("personal.yaml is empty")
                return
                
            # Check required fields
            if "name" not in data or not data["name"].get("full"):
                self.errors.append("Missing full name in personal.yaml")
            
            if "contact" not in data:
                self.errors.append("Missing contact information in personal.yaml")
            else:
                contact = data["contact"]
                if not contact.get("email"):
                    self.warnings.append("Missing email in contact information")
                elif "@" not in contact["email"]:
                    self.warnings.append("Email appears to be invalid")
                    
        except yaml.YAMLError as e:
            self.errors.append(f"YAML syntax error in personal.yaml: {e}")
        except Exception as e:
            self.errors.append(f"Error reading personal.yaml: {e}")
    
    def _validate_config_data(self):
        """Validate configuration file."""
        config_file = self.data_path / "config.yaml"
        if not config_file.exists():
            return
            
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                
            if not data:
                self.errors.append("config.yaml is empty")
                return
                
            # Check for essential configuration sections
            required_sections = ["layout", "typography", "colors", "formatting"]
            for section in required_sections:
                if section not in data:
                    self.warnings.append(f"Missing {section} configuration in config.yaml")
                    
        except yaml.YAMLError as e:
            self.errors.append(f"YAML syntax error in config.yaml: {e}")
        except Exception as e:
            self.errors.append(f"Error reading config.yaml: {e}")
    
    def _validate_section_files(self):
        """Validate section data files."""
        sections_path = self.data_path / "sections"
        if not sections_path.exists():
            self.errors.append("Missing data/sections directory")
            return
        
        # Check common section files
        section_files = {
            "experience.yaml": "positions",
            "education.yaml": "degrees", 
            "publication.yaml": "papers",
            "skills.yaml": "categories"
        }
        
        for filename, expected_key in section_files.items():
            file_path = sections_path / filename
            if file_path.exists():
                self._validate_section_file(file_path, expected_key)
    
    def _validate_section_file(self, file_path: Path, expected_key: str):
        """Validate individual section file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            if not data:
                self.warnings.append(f"{file_path.name} is empty")
                return
            
            if expected_key not in data:
                self.warnings.append(f"Missing '{expected_key}' key in {file_path.name}")
                return
            
            items = data[expected_key]
            if not isinstance(items, list):
                self.errors.append(f"'{expected_key}' in {file_path.name} should be a list")
                return
            
            # Validate specific section types
            if "experience" in file_path.name:
                self._validate_experience_items(items, file_path.name)
            elif "education" in file_path.name:
                self._validate_education_items(items, file_path.name)
            elif "publication" in file_path.name:
                self._validate_publication_items(items, file_path.name)
                
        except yaml.YAMLError as e:
            self.errors.append(f"YAML syntax error in {file_path.name}: {e}")
        except Exception as e:
            self.errors.append(f"Error reading {file_path.name}: {e}")
    
    def _validate_experience_items(self, items: list[dict], filename: str):
        """Validate experience entries."""
        required_fields = ["position", "company", "start_date"]
        
        for i, item in enumerate(items):
            for field in required_fields:
                if field not in item or not item[field]:
                    self.errors.append(f"Missing {field} in {filename} entry {i+1}")
            
            # Validate date format
            if "start_date" in item:
                self._validate_date(item["start_date"], f"{filename} entry {i+1} start_date")
            if "end_date" in item:
                self._validate_date(item["end_date"], f"{filename} entry {i+1} end_date")
    
    def _validate_education_items(self, items: list[dict], filename: str):
        """Validate education entries."""
        required_fields = ["degree", "institution", "start_date"]
        
        for i, item in enumerate(items):
            for field in required_fields:
                if field not in item or not item[field]:
                    self.errors.append(f"Missing {field} in {filename} entry {i+1}")
    
    def _validate_publication_items(self, items: list[dict], filename: str):
        """Validate publication entries."""
        required_fields = ["title", "authors", "year"]
        
        for i, item in enumerate(items):
            for field in required_fields:
                if field not in item or not item[field]:
                    self.errors.append(f"Missing {field} in {filename} entry {i+1}")
            
            # Validate authors is a list
            if "authors" in item and not isinstance(item["authors"], list):
                self.errors.append(f"Authors should be a list in {filename} entry {i+1}")
    
    def _validate_date(self, date_str: str, context: str):
        """Validate date format (YYYY-MM or YYYY-MM-DD or 'present')."""
        if date_str.lower() == "present":
            return
        
        if not isinstance(date_str, str):
            self.errors.append(f"Date should be a string in {context}")
            return
        
        parts = date_str.split("-")
        if len(parts) < 2 or len(parts) > 3:
            self.warnings.append(f"Date format should be YYYY-MM or YYYY-MM-DD in {context}")
            return
        
        try:
            year = int(parts[0])
            month = int(parts[1])
            if year < 1900 or year > 2030:
                self.warnings.append(f"Year seems unrealistic in {context}")
            if month < 1 or month > 12:
                self.warnings.append(f"Month should be 1-12 in {context}")
        except ValueError:
            self.warnings.append(f"Date contains non-numeric values in {context}")
    
    def print_results(self):
        """Print validation results with nice formatting."""
        if not self.errors and not self.warnings:
            console.print("[green]✅ All data validated successfully![/green]")
            return True
        
        if self.errors:
            error_text = "\n".join([f"❌ {error}" for error in self.errors])
            console.print(Panel(
                error_text,
                title="[red]Validation Errors[/red]",
                border_style="red"
            ))
        
        if self.warnings:
            warning_text = "\n".join([f"⚠️  {warning}" for warning in self.warnings])
            console.print(Panel(
                warning_text, 
                title="[yellow]Warnings[/yellow]",
                border_style="yellow"
            ))
        
        return len(self.errors) == 0


def validate_project(project_path: Path) -> bool:
    """Validate CV project and print results. Returns True if valid."""
    validator = CVValidator(project_path)
    is_valid = validator.validate_project()
    validator.print_results()
    return is_valid
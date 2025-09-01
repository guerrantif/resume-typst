"""Interactive CV data editor."""

from pathlib import Path
import yaml
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.panel import Panel

console = Console()

class CVEditor:
    """Interactive editor for CV sections."""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.data_path = project_path / "data"
    
    def show_menu(self):
        """Show main editing menu."""
        console.print("\n[bold blue]📝 CV Editor[/bold blue]")
        console.print("What would you like to edit?\n")
        
        options = {
            "1": "Personal Information",
            "2": "Work Experience", 
            "3": "Education",
            "4": "Skills",
            "5": "Publications",
            "6": "Awards",
            "7": "View Current Data",
            "0": "Exit"
        }
        
        table = Table(show_header=False, box=None)
        for key, value in options.items():
            style = "cyan" if key != "0" else "red"
            table.add_row(f"[{style}]{key}.[/{style}]", f"[bold]{value}[/bold]")
        
        console.print(table)
        
        choice = Prompt.ask(
            "\n[cyan]Choose section to edit[/cyan]",
            choices=list(options.keys()),
            default="0"
        )
        
        if choice == "0":
            return False
        elif choice == "1":
            self.edit_personal()
        elif choice == "2":
            self.edit_experience()
        elif choice == "3":
            self.edit_education()
        elif choice == "4":
            self.edit_skills()
        elif choice == "5":
            self.edit_publications()
        elif choice == "6":
            self.edit_awards()
        elif choice == "7":
            self.view_data()
        
        return True
    
    def edit_personal(self):
        """Edit personal information."""
        personal_file = self.data_path / "personal.yaml"
        
        console.print("\n[bold blue]👤 Personal Information[/bold blue]")
        
        # Load current data
        data = {}
        if personal_file.exists():
            with open(personal_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f) or {}
        
        # Edit fields
        current_name = data.get("name", {}).get("full", "")
        name = Prompt.ask("[cyan]Full name[/cyan]", default=current_name)
        
        current_email = data.get("contact", {}).get("email", "")
        email = Prompt.ask("[cyan]Email[/cyan]", default=current_email)
        
        current_phone = data.get("contact", {}).get("phone", "")
        phone = Prompt.ask("[cyan]Phone[/cyan]", default=current_phone)
        
        current_website = data.get("contact", {}).get("website", "")
        website = Prompt.ask("[cyan]Website[/cyan]", default=current_website)

        current_location = data.get("contact", {}).get("location", "")
        location = Prompt.ask("[cyan]Location[/cyan]", default=current_location)

        # Update data
        data["name"] = {"full": name}
        data["contact"] = {
            "email": email,
            "phone": phone,
            "website": website,
            "location": location
        }
        
        # Save
        with open(personal_file, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
        
        console.print("[green]✅ Personal information updated![/green]")
    
    def edit_experience(self):
        """Edit work experience."""
        # TODO: Implement experience editing
        console.print("\n[bold blue]💼 Work Experience[/bold blue]")
        console.print("[dim]Full experience editing coming soon![/dim]")
        console.print("[dim]For now, edit data/sections/experience.yaml directly.[/dim]")
    
    def edit_education(self):
        """Edit education."""
        # TODO: Implement education editing
        console.print("\n[bold blue]🎓 Education[/bold blue]")
        console.print("[dim]Full education editing coming soon![/dim]")
        console.print("[dim]For now, edit data/sections/education.yaml directly.[/dim]")
    
    def edit_skills(self):
        """Edit skills."""
        # TODO: Implement skills editing
        console.print("\n[bold blue]🛠️  Skills[/bold blue]")
        console.print("[dim]Full skills editing coming soon![/dim]")
        console.print("[dim]For now, edit data/sections/skills.yaml directly.[/dim]")
    
    def edit_publications(self):
        """Edit publications."""
        # TODO: Implement publications editing
        console.print("\n[bold blue]📚 Publications[/bold blue]")
        console.print("[dim]Full publications editing coming soon![/dim]")
        console.print("[dim]For now, edit data/sections/publication.yaml directly.[/dim]")
    
    def edit_awards(self):
        """Edit awards."""
        # TODO: Implement awards editing
        console.print("\n[bold blue]🏆 Awards[/bold blue]")
        console.print("[dim]Full awards editing coming soon![/dim]")
        console.print("[dim]For now, edit data/sections/awards.yaml directly.[/dim]")
    
    def view_data(self):
        """View current CV data summary."""
        console.print("\n[bold blue]📋 Current CV Data[/bold blue]")
        
        # Personal info
        personal_file = self.data_path / "personal.yaml"
        if personal_file.exists():
            with open(personal_file, 'r', encoding='utf-8') as f:
                personal = yaml.safe_load(f) or {}
            
            name = personal.get("name", {}).get("full", "Not set")
            email = personal.get("contact", {}).get("email", "Not set")
            
            console.print(f"[cyan]Name:[/cyan] {name}")
            console.print(f"[cyan]Email:[/cyan] {email}")
        else:
            console.print("[yellow]No personal information found[/yellow]")
        
        console.print()
        
        # Section counts
        sections = {
            "Experience": "experience.yaml",
            "Education": "education.yaml", 
            "Publications": "publication.yaml",
            "Skills": "skills.yaml",
            "Awards": "awards.yaml"
        }
        
        for section_name, filename in sections.items():
            file_path = self.data_path / "sections" / filename
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f) or {}
                
                # Count items
                if "positions" in data:
                    count = len(data["positions"])
                elif "degrees" in data:
                    count = len(data["degrees"])
                elif "papers" in data:
                    count = len(data["papers"])
                elif "categories" in data:
                    count = len(data["categories"])
                elif "awards" in data:
                    count = len(data["awards"])
                else:
                    count = "unknown"
                
                console.print(f"[cyan]{section_name}:[/cyan] {count} items")
            else:
                console.print(f"[cyan]{section_name}:[/cyan] [dim]No file[/dim]")


def run_interactive_editor(project_path: Path):
    """Run the interactive CV editor."""
    if not (project_path / "data").exists():
        console.print("[red]No CV project found in current directory[/red]")
        return
    
    editor = CVEditor(project_path)
    
    console.print(Panel(
        "[bold magenta]resumyst[/bold magenta] Interactive Editor\n"
        "Edit your CV data with guided prompts.",
        border_style="magenta"
    ))
    
    try:
        while editor.show_menu():
            if not Confirm.ask("\n[cyan]Continue editing?[/cyan]", default=True):
                break
        
        console.print("\n[green]✨ Happy with your edits![/green]")
        console.print("[dim]Run 'resumyst build' to generate your CV.[/dim]")
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Editor cancelled.[/yellow]")
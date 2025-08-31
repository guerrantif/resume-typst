"""Interactive wizards for resumyst setup and data entry."""

from pathlib import Path
import click
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.text import Text

console = Console()

class CVWizard:
    """Interactive wizard for CV setup and data entry."""
    
    def __init__(self):
        self.console = console
    
    def welcome(self) -> None:
        """Display welcome message."""
        welcome_text = Text()
        welcome_text.append("✨ Welcome to ", style="bright_white")
        welcome_text.append("resumyst", style="bold magenta")
        welcome_text.append(" ✨", style="bright_white")
        welcome_text.append("\n\nConjure the perfect CV with Typst magic!", style="dim")
        
        panel = Panel(
            welcome_text,
            border_style="magenta",
            padding=(1, 2)
        )
        self.console.print(panel)
        self.console.print()

    def collect_basic_info(self) -> dict[str, any]:
        """Collect basic personal information."""
        self.console.print("[bold blue]📝 Basic Information[/bold blue]")
        self.console.print("Let's start with your basic details:\n")
        
        # Name
        full_name = Prompt.ask(
            "[cyan]Full name[/cyan]",
            default="Your Name"
        )
        
        # Email
        email = Prompt.ask(
            "[cyan]Email address[/cyan]",
            default="your.email@example.com"
        )
        
        # Phone (optional)
        phone = Prompt.ask(
            "[cyan]Phone number[/cyan] [dim](optional, press Enter to skip)[/dim]", 
            default=""
        )
        
        # Website/portfolio (optional)
        website = Prompt.ask(
            "[cyan]Website or portfolio URL[/cyan] [dim](optional, press Enter to skip)[/dim]",
            default=""
        )
        
        # Location (optional)
        location = Prompt.ask(
            "[cyan]Location (city, country)[/cyan] [dim](optional, press Enter to skip)[/dim]",
            default=""
        )
        
        # LinkedIn (optional)
        linkedin = Prompt.ask(
            "[cyan]LinkedIn URL[/cyan] [dim](optional, press Enter to skip)[/dim]",
            default=""
        )
        
        # Build contact info, only including optional fields if provided
        contact = {
            "email": email  # Email is required
        }
        
        # Only add phone if user provided one
        if phone and phone.strip():
            contact["phone"] = phone.strip()
            
        # Only add website if user provided one
        if website and website.strip():
            contact["website"] = website.strip()
            
        # Only add location if user provided one
        if location and location.strip():
            contact["location"] = location.strip()
            
        # Only add LinkedIn if user provided one
        if linkedin and linkedin.strip():
            contact["linkedin"] = linkedin.strip()
        
        return {
            "name": {"full": full_name},
            "contact": contact
        }

    def choose_cv_type(self) -> str:
        """Let user choose CV type/template."""
        self.console.print("\n[bold blue]🎨 CV Style[/bold blue]")
        self.console.print("What type of CV are you creating?\n")
        
        choices = {
            "1": ("academic", "Academic CV - Full publications, research focus"),
            "2": ("industry", "Industry CV - Practical experience emphasis"),
            "3": ("short", "Short CV - Concise 1-2 page format")
        }
        
        for key, (variant, description) in choices.items():
            self.console.print(f"[cyan]{key}.[/cyan] [bold]{variant.title()}[/bold] - {description}")
        
        choice = Prompt.ask(
            "\n[cyan]Choose your CV style[/cyan]",
            choices=list(choices.keys()),
            default="2"
        )
        
        variant = choices[choice][0]
        self.console.print(f"✨ Great choice! Creating [bold magenta]{variant}[/bold magenta] CV")
        return variant

    def collect_sections_info(self) -> dict[str, any]:
        """Collect information about which sections to include."""
        self.console.print("\n[bold blue]📋 Sections[/bold blue]")
        self.console.print("Which sections would you like to include?\n")
        
        # Default sections that most people want
        sections = {}
        
        # Always include basic sections
        if Confirm.ask("[cyan]Include work experience?[/cyan]", default=True):
            sections["experience"] = self.get_sample_experience()
            
        if Confirm.ask("[cyan]Include education?[/cyan]", default=True):
            sections["education"] = self.get_sample_education()
            
        if Confirm.ask("[cyan]Include skills?[/cyan]", default=True):
            sections["skills"] = self.get_sample_skills()
            
        # Optional sections
        if Confirm.ask("[cyan]Include publications?[/cyan]", default=False):
            sections["publications"] = self.get_sample_publications()
            
        if Confirm.ask("[cyan]Include awards?[/cyan]", default=False):
            sections["awards"] = self.get_sample_awards()
        
        return sections

    def get_sample_experience(self) -> list:
        """Generate sample experience entry."""
        return [{
            "id": "sample_job",
            "position": "Software Engineer",
            "company": "Fictional Tech Corp",
            "start_date": "2022-01",
            "end_date": "present",
            "location": "Berlin, Germany",
            "details": [
                "Developed and maintained web applications using modern frameworks",
                "Collaborated with cross-functional teams to deliver high-quality software",
                "Improved system performance and reduced loading times by 40%"
            ]
        }]

    def get_sample_education(self) -> list:
        """Generate sample education entry."""
        return [{
            "id": "sample_degree",
            "degree": "Bachelor of Science",
            "field": "Computer Science", 
            "institution": "Example University",
            "location": "Munich, Germany",
            "start_date": "2018-09",
            "end_date": "2022-06",
            "details": [
                "Graduated with honors, GPA: 3.8/4.0",
                "Relevant coursework: Data Structures, Algorithms, Software Engineering"
            ]
        }]

    def get_sample_skills(self) -> list:
        """Generate sample skills."""
        return [{
            "group": "Programming Languages",
            "items": ["Python", "JavaScript", "TypeScript", "Java"]
        }, {
            "group": "Technologies",
            "items": ["React", "Node.js", "Docker", "Git"]
        }]

    def get_sample_publications(self) -> list:
        """Generate sample publication."""
        return [{
            "id": "sample_paper",
            "title": "Advanced Methods for Data Processing Applications",
            "authors": ["Alice Wonderland", "Bob Builder"],
            "year": 2023,
            "venue": "Conference on Marginally Useful Algorithms (CMUA)",
            "exclude_from": ["short"]
        }]

    def get_sample_awards(self) -> list:
        """Generate sample award."""
        return [{
            "title": "Excellence Award",
            "issuer": "Example University",
            "year": 2023,
            "description": "Awarded for outstanding performance and academic achievement"
        }]

    def completion_message(self, project_path: Path, variant: str) -> None:
        """Show completion message with next steps."""
        self.console.print("\n[bold green]🎉 Project created successfully![/bold green]")
        
        next_steps = f"""
[bold blue]Next steps:[/bold blue]

1. [cyan]cd {project_path}[/cyan]
2. [cyan]resumyst edit[/cyan] - Customize your data
3. [cyan]resumyst build {variant}[/cyan] - Generate your CV
4. [cyan]resumyst serve[/cyan] - Preview with live reload

[dim]Your CV data is in the 'data/' folder - edit the YAML files to customize.[/dim]
        """
        
        panel = Panel(
            next_steps.strip(),
            border_style="green",
            padding=(1, 2)
        )
        self.console.print(panel)

def run_init_wizard(project_path: Path) -> dict[str, any]:
    """Run the complete initialization wizard."""
    wizard = CVWizard()
    
    # Welcome
    wizard.welcome()
    
    # Collect info
    personal_info = wizard.collect_basic_info()
    cv_type = wizard.choose_cv_type()
    sections_info = wizard.collect_sections_info()
    
    return {
        "personal": personal_info,
        "variant": cv_type,
        "sections": sections_info,
        "wizard": wizard
    }
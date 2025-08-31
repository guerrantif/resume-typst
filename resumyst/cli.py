"""Main CLI interface for resumyst."""

import sys
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel

console = Console()


@click.group()
@click.version_option(prog_name="resumyst")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.pass_context
def cli(ctx, verbose: bool) -> None:
    """Conjure the perfect CV with Typst magic - transform YAML data into professional documents."""
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    if verbose:
        console.print("[dim]Verbose mode enabled[/dim]")


@cli.command()
@click.argument("name", required=False)
@click.option("--path", "-p", help="Path where to create the CV project", type=click.Path())
@click.option("--quick", "-q", is_flag=True, help="Skip wizard, create with defaults")
def init(name: str | None, path: str | None, quick: bool = False) -> None:
    """Initialize a new CV project with interactive wizard."""
    if name is None:
        name = click.prompt("What's your CV project name?", default="my-cv")
    
    project_path = Path(path) / name if path else Path(name)
    
    try:
        if quick:
            # Quick mode - just copy templates  
            from .commands.init import create_cv_project
            from .wizard import CVWizard
            wizard_data = {
                "personal": {"name": {"full": "Your Name"}, "contact": {"email": "your@email.com", "phone": "+1-555-0123", "website": "https://yoursite.com"}}, 
                "sections": {}, 
                "variant": "academic",
                "wizard": CVWizard()
            }
            create_cv_project(project_path, wizard_data)
            console.print(f"[green]✅ Created basic CV project at {project_path}[/green]")
            console.print(f"[dim]Run 'resumyst edit' to customize your CV data[/dim]")
        else:
            # Interactive wizard mode
            from .commands.init import init_project_interactive
            init_project_interactive(project_path)
        
        console.print(Panel(
            f"[green]✅ CV project created successfully![/green]\n\n"
            f"Next steps:\n"
            f"  cd {project_path}\n"
            f"  resumyst build academic\n\n"
            f"Edit your CV data in the [cyan]data/[/cyan] directory.",
            title="🎉 Success",
            expand=False
        ))
        
    except Exception as e:
        console.print(f"[red]Error creating project: {e}[/red]")
        sys.exit(1)


@cli.command()
@click.argument("variant", type=click.Choice(["academic", "industry", "short"]), required=False)
@click.option("--all", "build_all", is_flag=True, help="Build all variants")
@click.option("--format", "output_format", type=click.Choice(["pdf", "png"]), default="pdf", help="Output format")
@click.option("--watch", is_flag=True, help="Watch for changes and rebuild automatically")
@click.option("--no-validate", is_flag=True, help="Skip data validation before building")
@click.option("--no-auto-install", is_flag=True, help="Don't auto-install Typst if missing")
def build(variant: str | None, build_all: bool, output_format: str, watch: bool, no_validate: bool, no_auto_install: bool) -> None:
    """Build CV variants with validation."""
    if build_all:
        variants = ["academic", "industry", "short"]
    elif variant:
        variants = [variant]
    else:
        variant = click.prompt("Which variant?", type=click.Choice(["academic", "industry", "short"]))
        variants = [variant]
    
    try:
        from .commands.build import build_cv
        
        if watch and len(variants) == 1:
            console.print(f"[yellow]👀 Watching for changes... (variant: {variants[0]})[/yellow]")
            build_cv(variants[0], output_format, watch=True, skip_validation=no_validate, auto_install=not no_auto_install)
        else:
            for v in variants:
                console.print(f"[blue]🔨 Building {v} variant ({output_format})[/blue]")
                build_cv(v, output_format, skip_validation=no_validate, auto_install=not no_auto_install)
                
        console.print("[green]✅ Build complete![/green]")
        
    except Exception as e:
        console.print(f"[red]Error building CV: {e}[/red]")
        sys.exit(1)



@cli.command()
@click.argument("section", required=False)
def edit(section: str | None) -> None:
    """Interactive CV data editor."""
    try:
        from .editor import run_interactive_editor
        project_path = Path.cwd()
        
        if not (project_path / "data").exists():
            console.print("[red]No CV project found in current directory[/red]")
            console.print("[dim]Run 'resumyst init' to create a new project.[/dim]")
            sys.exit(1)
        
        run_interactive_editor(project_path)
        
    except Exception as e:
        console.print(f"[red]Editor error: {e}[/red]")
        sys.exit(1)


@cli.command()
@click.option("--variant", "-v", default="academic", type=click.Choice(["academic", "industry", "short"]), help="CV variant to preview")
@click.option("--port", "-p", default=8000, type=int, help="Server port")
@click.option("--no-browser", is_flag=True, help="Don't open browser automatically")
def serve(variant: str, port: int, no_browser: bool) -> None:
    """Start live preview server with auto-reload."""
    try:
        from .server import start_preview_server
        project_path = Path.cwd()
        
        if not (project_path / "data").exists():
            console.print("[red]No CV project found in current directory[/red]")
            console.print("[dim]Run 'resumyst init' to create a new project.[/dim]")
            sys.exit(1)
        
        start_preview_server(project_path, variant, port, not no_browser)
        
    except Exception as e:
        console.print(f"[red]Server error: {e}[/red]")
        sys.exit(1)


@cli.command()
def validate() -> None:
    """Validate CV data files."""
    try:
        from .validator import validate_project
        project_path = Path.cwd()
        
        if not (project_path / "data").exists():
            console.print("[red]No CV project found in current directory[/red]")
            sys.exit(1)
            
        console.print("🔍 Validating CV project...")
        is_valid = validate_project(project_path)
        
        if is_valid:
            console.print("\n[green]🎉 Your CV data is ready to build![/green]")
        else:
            console.print("\n[yellow]Fix the errors above and try again.[/yellow]")
            sys.exit(1)
            
    except Exception as e:
        console.print(f"[red]Validation error: {e}[/red]")
        sys.exit(1)


@cli.command()
@click.option("--format", "output_format", type=click.Choice(["pdf", "png"]), default="pdf")
def clean(output_format: str) -> None:
    """Clean build outputs."""
    try:
        from .commands.build import clean_outputs
        clean_outputs(output_format)
        console.print(f"[green]✅ Cleaned {output_format} outputs[/green]")
    except Exception as e:
        console.print(f"[red]Error cleaning: {e}[/red]")
        sys.exit(1)


def main() -> None:
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
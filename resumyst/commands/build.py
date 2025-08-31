"""Build CV variants using Typst with validation."""

import shutil
import subprocess
from pathlib import Path

from rich.console import Console
from ..validator import validate_project

console = Console()


def build_cv(variant: str, output_format: str = "pdf", watch: bool = False, skip_validation: bool = False) -> None:
    """Build a specific CV variant with optional validation."""
    # Check if we're in a CV project directory
    project_path = Path.cwd()
    if not (project_path / "build/cv.typ").exists():
        raise FileNotFoundError(
            "No CV project found. Run 'resumyst init' first or navigate to a CV project directory."
        )
    
    # Validate data before building (unless skipped)
    if not skip_validation:
        console.print("🔍 Validating CV data...")
        if not validate_project(project_path):
            console.print("[red]❌ Validation failed. Use --no-validate to build anyway.[/red]")
            return
        console.print()  # Add space after validation
    
    # Determine output path
    output_dir = Path("out") / output_format
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / f"cv-{variant}.{output_format}"
    
    # Build command
    cmd = [
        "typst",
        "watch" if watch else "compile",
        "build/cv.typ",
        str(output_file),
        "--root", ".",
        "--input", f"variant={variant}",
    ]
    
    try:
        if watch:
            # For watch mode, run interactively
            subprocess.run(cmd, check=True)
        else:
            # For one-time build, capture output
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            if result.returncode == 0:
                console.print(f"[green]✅ Built {variant} -> {output_file}[/green]")
            else:
                console.print(f"[red]❌ Build failed: {result.stderr}[/red]")
                
    except subprocess.CalledProcessError as e:
        if e.stderr:
            console.print(f"[red]Typst error: {e.stderr}[/red]")
        raise RuntimeError(f"Failed to build {variant} variant")
    except FileNotFoundError:
        raise RuntimeError(
            "Typst not found. Please install Typst: https://github.com/typst/typst#installation"
        )


def clean_outputs(output_format: str | None = None) -> None:
    """Clean build outputs."""
    if output_format:
        output_dir = Path("out") / output_format
        if output_dir.exists():
            shutil.rmtree(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
    else:
        # Clean all formats
        out_dir = Path("out")
        if out_dir.exists():
            shutil.rmtree(out_dir)
            out_dir.mkdir(parents=True, exist_ok=True)
            (out_dir / "pdf").mkdir(parents=True, exist_ok=True)
            (out_dir / "png").mkdir(parents=True, exist_ok=True)
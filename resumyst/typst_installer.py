"""Automatic Typst installation utility for resumyst."""

import platform
import subprocess
import shutil
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

console = Console()

def check_typst_installed() -> bool:
    """Check if Typst is already installed and available in PATH."""
    return shutil.which("typst") is not None

def get_typst_version() -> str | None:
    """Get the installed Typst version."""
    try:
        result = subprocess.run(
            ["typst", "--version"], 
            capture_output=True, 
            text=True, 
            check=True,
            timeout=10
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return None

def install_typst_with_cargo() -> bool:
    """Install Typst using Cargo (Rust package manager)."""
    try:
        console.print("Installing Typst via Cargo...")
        subprocess.run(
            ["cargo", "install", "typst-cli"], 
            check=True,
            capture_output=True,
            timeout=300
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return False

def install_typst_with_winget() -> bool:
    """Install Typst using Windows Package Manager (winget)."""
    try:
        console.print("Installing Typst via winget...")
        subprocess.run(
            ["winget", "install", "typst"], 
            check=True,
            capture_output=True,
            timeout=120
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return False

def install_typst_with_brew() -> bool:
    """Install Typst using Homebrew on macOS."""
    try:
        console.print("Installing Typst via Homebrew...")
        subprocess.run(
            ["brew", "install", "typst"], 
            check=True,
            capture_output=True,
            timeout=120
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return False

def install_typst_with_apt() -> bool:
    """Install Typst using apt package manager on Ubuntu/Debian."""
    console.print("APT installation requires sudo privileges.")
    console.print("For security, please install manually: sudo apt update && sudo apt install typst")
    return False

def install_typst_with_snap() -> bool:
    """Install Typst using Snap package manager on Linux.""" 
    console.print("Snap installation requires sudo privileges.")
    console.print("For security, please install manually: sudo snap install typst")
    return False

def auto_install_typst() -> bool:
    """Automatically install Typst based on the current platform."""
    system = platform.system().lower()
    
    console.print(Panel(
        "🚀 Typst not found. Attempting automatic installation...",
        title="Auto-Installation",
        style="yellow"
    ))
    
    # Try different installation methods based on platform
    installation_methods = []
    
    if system == "windows":
        installation_methods = [
            ("Windows Package Manager (winget)", install_typst_with_winget),
            ("Cargo (Rust)", install_typst_with_cargo),
        ]
    elif system == "darwin":  # macOS
        installation_methods = [
            ("Homebrew", install_typst_with_brew),
            ("Cargo (Rust)", install_typst_with_cargo),
        ]
    elif system == "linux":
        installation_methods = [
            ("Snap", install_typst_with_snap),
            ("APT (Ubuntu/Debian)", install_typst_with_apt),
            ("Cargo (Rust)", install_typst_with_cargo),
        ]
    else:
        # Fallback to Cargo for other systems
        installation_methods = [
            ("Cargo (Rust)", install_typst_with_cargo),
        ]
    
    # Try each installation method
    for method_name, install_func in installation_methods:
        console.print(f"⏳ Trying {method_name}...")
        
        if install_func():
            # Verify installation
            if check_typst_installed():
                version = get_typst_version()
                console.print(Panel(
                    f"✅ Typst successfully installed via {method_name}!\n"
                    f"Version: {version}",
                    title="Installation Success",
                    style="green"
                ))
                return True
            else:
                console.print(f"⚠️  {method_name} completed but Typst not found in PATH")
        else:
            console.print(f"❌ {method_name} failed")
    
    # If all methods failed
    console.print(Panel(
        "❌ Automatic installation failed. Please install Typst manually:\n\n"
        "• Visit: https://typst.app/docs/installation/\n"
        "• Or use your system's package manager\n"
        "• Then restart resumyst",
        title="Installation Failed",
        style="red"
    ))
    return False

def ensure_typst_available(auto_install: bool = True) -> bool:
    """Ensure Typst is available, optionally auto-installing if needed."""
    if check_typst_installed():
        version = get_typst_version()
        console.print(f"✅ Typst found: {version}")
        return True
    
    if not auto_install:
        console.print("❌ Typst not found. Please install it first.")
        return False
    
    return auto_install_typst()


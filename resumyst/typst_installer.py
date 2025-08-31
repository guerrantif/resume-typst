"""Simple and robust Typst installation utility for resumyst."""

import platform
import subprocess
import shutil
import urllib.request
import zipfile
import tarfile
from pathlib import Path
from rich.console import Console

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

def install_with_cargo() -> bool:
    """Install Typst using Cargo (most reliable method)."""
    if not shutil.which("cargo"):
        return False
    
    try:
        console.print("Installing Typst via Cargo...")
        subprocess.run(
            ["cargo", "install", "--locked", "typst-cli"], 
            check=True,
            capture_output=True,
            timeout=300
        )
        return True
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return False

def install_with_package_manager() -> bool:
    """Install using platform-specific package manager."""
    system = platform.system().lower()
    
    try:
        if system == "darwin" and shutil.which("brew"):
            console.print("Installing Typst via Homebrew...")
            subprocess.run(["brew", "install", "typst"], check=True, capture_output=True, timeout=120)
            return True
        elif system == "windows" and shutil.which("winget"):
            console.print("Installing Typst via winget...")
            subprocess.run(["winget", "install", "--id", "Typst.Typst"], check=True, capture_output=True, timeout=120)
            return True
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        pass
    
    return False

def download_typst_binary() -> bool:
    """Download and install Typst binary (fallback method)."""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    # Map platform to download URL patterns
    if system == "linux":
        if machine in ["x86_64", "amd64"]:
            suffix = "x86_64-unknown-linux-musl.tar.xz"
        elif machine in ["aarch64", "arm64"]:
            suffix = "aarch64-unknown-linux-musl.tar.xz"
        else:
            return False
    elif system == "darwin":
        suffix = "x86_64-apple-darwin.tar.xz"  # Universal binary works on both Intel and ARM
    elif system == "windows":
        suffix = "x86_64-pc-windows-msvc.zip"
    else:
        return False
    
    try:
        console.print("Downloading Typst binary...")
        
        # Get latest release info
        api_url = "https://api.github.com/repos/typst/typst/releases/latest"
        with urllib.request.urlopen(api_url, timeout=10) as response:
            import json
            release_data = json.loads(response.read().decode())
            tag_name = release_data["tag_name"]
        
        # Download binary
        filename = f"typst-{tag_name}-{suffix}"
        download_url = f"https://github.com/typst/typst/releases/download/{tag_name}/{filename}"
        
        # Create temporary directory
        import tempfile
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            archive_path = temp_path / filename
            
            # Download
            urllib.request.urlretrieve(download_url, archive_path)
            
            # Extract
            if suffix.endswith('.zip'):
                with zipfile.ZipFile(archive_path, 'r') as zip_file:
                    zip_file.extractall(temp_path)
            else:
                with tarfile.open(archive_path, 'r:*') as tar_file:
                    tar_file.extractall(temp_path)
            
            # Find binary
            binary_name = "typst.exe" if system == "windows" else "typst"
            binary_path = None
            for file_path in temp_path.rglob(binary_name):
                binary_path = file_path
                break
            
            if not binary_path or not binary_path.exists():
                return False
            
            # Install to user's local bin
            if system == "windows":
                # Windows: try to install to a directory in PATH
                install_dir = Path.home() / "AppData" / "Local" / "Programs" / "Typst"
                install_dir.mkdir(parents=True, exist_ok=True)
                dest_path = install_dir / "typst.exe"
            else:
                # Unix-like: install to ~/.local/bin
                install_dir = Path.home() / ".local" / "bin"
                install_dir.mkdir(parents=True, exist_ok=True)
                dest_path = install_dir / "typst"
            
            # Copy binary
            shutil.copy2(binary_path, dest_path)
            dest_path.chmod(0o755)  # Make executable on Unix
            
            console.print(f"Typst installed to {dest_path}")
            console.print(f"Add {install_dir} to your PATH if needed")
            
            return True
            
    except Exception:
        return False

def auto_install_typst() -> bool:
    """Automatically install Typst using the best available method."""
    console.print("[yellow]Typst not found. Attempting installation...[/yellow]")
    
    # Try methods in order of reliability
    methods = [
        ("package manager", install_with_package_manager),
        ("Cargo", install_with_cargo),
        ("binary download", download_typst_binary),
    ]
    
    for method_name, install_func in methods:
        console.print(f"Trying {method_name}...")
        
        if install_func():
            # Verify installation
            if check_typst_installed():
                version = get_typst_version()
                console.print(f"[green]Typst successfully installed via {method_name}![/green]")
                console.print(f"[green]Version: {version}[/green]")
                return True
            else:
                console.print(f"[yellow]{method_name} completed but Typst not found in PATH[/yellow]")
        else:
            console.print(f"[red]{method_name} failed[/red]")
    
    # All methods failed
    console.print("[red]Automatic installation failed.[/red]")
    console.print("Please install Typst manually:")
    console.print("• Visit: https://github.com/typst/typst#installation")
    console.print("• Or use: cargo install --locked typst-cli")
    return False

def ensure_typst_available(auto_install: bool = True) -> bool:
    """Ensure Typst is available, optionally auto-installing if needed."""
    if check_typst_installed():
        version = get_typst_version()
        console.print(f"[green]Typst found: {version}[/green]")
        return True
    
    if not auto_install:
        console.print("[red]Typst not found. Please install it first.[/red]")
        return False
    
    return auto_install_typst()
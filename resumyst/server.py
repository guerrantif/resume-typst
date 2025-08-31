"""Live preview server for resumyst CV projects."""

import os
import time
import threading
import webbrowser
from pathlib import Path
import subprocess
import socket
from http.server import HTTPServer, SimpleHTTPRequestHandler
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from rich.console import Console
from rich.panel import Panel

console = Console()

class CVFileWatcher(FileSystemEventHandler):
    """Watches for changes in CV data files and rebuilds."""
    
    def __init__(self, project_path: Path, variant: str = "academic"):
        self.project_path = project_path
        self.variant = variant
        self.last_rebuild = 0
        self.rebuild_cooldown = 2  # seconds
        
    def on_modified(self, event):
        """Handle file modification events."""
        if event.is_directory:
            return
            
        # Only react to relevant files
        file_path = Path(event.src_path)
        relevant_paths = [
            self.project_path / "data",
            self.project_path / "lib",
            self.project_path / "build"
        ]
        
        if not any(file_path.is_relative_to(path) for path in relevant_paths):
            return
            
        # Skip temporary files
        if file_path.name.startswith('.') or file_path.suffix in ['.tmp', '.swp']:
            return
            
        # Cooldown to prevent rapid rebuilds
        current_time = time.time()
        if current_time - self.last_rebuild < self.rebuild_cooldown:
            return
            
        self.last_rebuild = current_time
        self._rebuild_cv()
    
    def _rebuild_cv(self):
        """Rebuild the CV."""
        try:
            console.print("[dim]📝 Change detected, rebuilding...[/dim]")
            
            # Build CV
            result = subprocess.run([
                "typst", "compile", "build/cv.typ", 
                f"out/pdf/cv-{self.variant}.pdf",
                "--root", ".",
                "--input", f"variant={self.variant}"
            ], 
            capture_output=True, 
            text=True,
            cwd=self.project_path
            )
            
            if result.returncode == 0:
                console.print("[green]✅ CV updated![/green]")
            else:
                console.print(f"[red]❌ Build failed: {result.stderr}[/red]")
                
        except Exception as e:
            console.print(f"[red]❌ Rebuild error: {e}[/red]")


class PDFHTTPHandler(SimpleHTTPRequestHandler):
    """HTTP handler that serves PDF files with proper headers."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=kwargs.pop('directory', None), **kwargs)
    
    def end_headers(self):
        """Add headers for PDF viewing."""
        if self.path.endswith('.pdf'):
            self.send_header('Content-Type', 'application/pdf')
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
        super().end_headers()
    
    def log_message(self, format, *args):
        """Suppress HTTP server logs."""
        pass


class CVPreviewServer:
    """Live preview server for CV projects."""
    
    def __init__(self, project_path: Path, variant: str = "academic", port: int = 8000):
        self.project_path = project_path
        self.variant = variant
        self.port = port
        self.server: HTTPServer | None = None
        self.observer: Observer | None = None
        self.server_thread: threading.Thread | None = None
        
    def start(self, open_browser: bool = True):
        """Start the preview server and file watcher."""
        
        # Initial build
        self._initial_build()
        
        # Start file watcher
        self._start_file_watcher()
        
        # Start HTTP server
        self._start_http_server()
        
        # Open browser
        if open_browser:
            self._open_browser()
        
        # Show status
        self._show_status()
        
        try:
            # Keep the server running
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
    
    def _initial_build(self):
        """Perform initial CV build."""
        console.print("🔨 Building initial CV...")
        
        try:
            result = subprocess.run([
                "typst", "compile", "build/cv.typ",
                f"out/pdf/cv-{self.variant}.pdf", 
                "--root", ".",
                "--input", f"variant={self.variant}"
            ],
            capture_output=True,
            text=True,
            cwd=self.project_path
            )
            
            if result.returncode == 0:
                console.print("[green]✅ Initial build complete![/green]")
            else:
                console.print(f"[red]❌ Initial build failed: {result.stderr}[/red]")
                raise Exception("Initial build failed")
                
        except Exception as e:
            console.print(f"[red]❌ Build error: {e}[/red]")
            raise
    
    def _start_file_watcher(self):
        """Start watching for file changes."""
        self.observer = Observer()
        event_handler = CVFileWatcher(self.project_path, self.variant)
        
        # Watch data and lib directories
        self.observer.schedule(event_handler, str(self.project_path / "data"), recursive=True)
        self.observer.schedule(event_handler, str(self.project_path / "lib"), recursive=True)
        self.observer.schedule(event_handler, str(self.project_path / "build"), recursive=False)
        
        self.observer.start()
        console.print("[blue]👁️  Watching for changes...[/blue]")
    
    def _start_http_server(self):
        """Start HTTP server to serve PDF files."""
        os.chdir(self.project_path)
        
        handler = lambda *args, **kwargs: PDFHTTPHandler(*args, directory=str(self.project_path), **kwargs)
        self.server = HTTPServer(("localhost", self.port), handler)
        
        self.server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.server_thread.start()
        
        console.print(f"[blue]🌐 Server running on http://localhost:{self.port}[/blue]")
    
    def _open_browser(self):
        """Open browser to view the CV."""
        pdf_url = f"http://localhost:{self.port}/out/pdf/cv-{self.variant}.pdf"
        
        try:
            webbrowser.open(pdf_url)
            console.print(f"[green]🚀 Opened CV in browser![/green]")
        except Exception as e:
            console.print(f"[yellow]⚠️  Could not open browser automatically: {e}[/yellow]")
            console.print(f"[cyan]Manual URL: {pdf_url}[/cyan]")
    
    def _show_status(self):
        """Show server status information."""
        pdf_url = f"http://localhost:{self.port}/out/pdf/cv-{self.variant}.pdf"
        edit_files = [
            "data/personal.yaml",
            "data/sections/experience.yaml", 
            "data/sections/education.yaml",
            "data/sections/publication.yaml"
        ]
        
        status_text = f"""
[bold blue]🔴 Live Preview Server Running[/bold blue]

[cyan]CV Preview:[/cyan] {pdf_url}
[cyan]Variant:[/cyan] {self.variant}
[cyan]Project:[/cyan] {self.project_path.name}

[dim]💡 Tips:[/dim]
• Edit files in [cyan]data/[/cyan] folder - changes auto-rebuild
• Use [cyan]resumyst edit[/cyan] for guided editing
• Press [red]Ctrl+C[/red] to stop server

[dim]Key files to edit:[/dim]
{chr(10).join(f"• {file}" for file in edit_files)}
        """
        
        panel = Panel(
            status_text.strip(),
            border_style="blue",
            padding=(1, 2)
        )
        
        console.print(panel)
    
    def stop(self):
        """Stop the server and file watcher."""
        console.print("\n[yellow]🛑 Shutting down preview server...[/yellow]")
        
        if self.observer:
            self.observer.stop()
            self.observer.join()
            
        if self.server:
            self.server.shutdown()
            
        console.print("[green]✅ Server stopped cleanly![/green]")


def start_preview_server(project_path: Path, variant: str = "academic", port: int = 8000, open_browser: bool = True):
    """Start the live preview server."""
    
    # Validate project
    if not (project_path / "build/cv.typ").exists():
        console.print("[red]❌ No CV project found in current directory[/red]")
        console.print("[dim]Run 'resumyst init' to create a new project.[/dim]")
        return
    
    # Check if typst is available
    try:
        subprocess.run(["typst", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        console.print("[red]❌ Typst not found. Please install Typst first.[/red]")
        console.print("[dim]Visit: https://typst.app/docs/installation/[/dim]")
        return
    
    # Check if port is available
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex(("localhost", port)) == 0:
            console.print(f"[red]❌ Port {port} is already in use[/red]")
            return
    
    # Start server
    server = CVPreviewServer(project_path, variant, port)
    server.start(open_browser)
"""
POV-Ray Renderer

Batch renders .pov files to PNG images.
"""

import os
import subprocess
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Optional, Tuple
from pathlib import Path


class POVRayError(Exception):
    """Exception raised for POV-Ray rendering errors."""
    pass


class POVRayRenderer:
    """Batch renderer for POV-Ray scene files."""
    
    def __init__(
        self,
        output_dir: str = "output/frames",
        width: int = 800,
        height: int = 600,
        antialias: float = 0.1,
        quality: int = 9,
        max_workers: int = 4
    ):
        """
        Initialize POV-Ray renderer.
        
        Args:
            output_dir: Directory to write PNG files
            width: Image width in pixels
            height: Image height in pixels
            antialias: Anti-aliasing threshold (0.0-1.0)
            quality: POV-Ray quality setting (0-11)
            max_workers: Maximum parallel render processes
        """
        self.output_dir = os.path.abspath(output_dir)
        self.width = width
        self.height = height
        self.antialias = antialias
        self.quality = quality
        self.max_workers = max_workers
        
        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Find POV-Ray executable
        self.povray_path = self._find_povray()
    
    def _find_povray(self) -> str:
        """
        Find POV-Ray executable.
        
        Returns:
            Path to POV-Ray executable
            
        Raises:
            POVRayError: If POV-Ray is not found
        """
        # Try common names
        for name in ['povray', 'pvengine64', 'pvengine']:
            path = shutil.which(name)
            if path:
                return path
        
        # Check common installation paths
        common_paths = [
            '/usr/bin/povray',
            '/usr/local/bin/povray',
            '/opt/povray/bin/povray',
            'C:\\Program Files\\POV-Ray\\v3.7\\bin\\pvengine64.exe',
        ]
        
        for path in common_paths:
            if os.path.isfile(path):
                return path
        
        raise POVRayError(
            "POV-Ray not found. Please install POV-Ray and ensure it's in your PATH.\n"
            "Installation instructions:\n"
            "  - Linux: sudo apt install povray\n"
            "  - macOS: brew install povray\n"
            "  - Windows: Download from http://www.povray.org/download/"
        )
    
    def _build_command(self, input_file: str, output_file: str) -> List[str]:
        """
        Build POV-Ray command line.
        
        Args:
            input_file: Path to .pov file
            output_file: Path to output .png file
            
        Returns:
            Command as list of arguments
        """
        import platform
        
        if platform.system() == 'Windows':
            # Windows GUI version needs special handling
            cmd = [
                self.povray_path,
                '/NR',  # No restore - don't restore previous window state
                '/RENDER',  # Start rendering immediately  
                '/EXIT',    # Exit when done
                f'{input_file}',  # Input file (no +I prefix for Windows)
                f'+O{output_file}',
                f'+W{self.width}',
                f'+H{self.height}',
                '+FN',  # PNG output
                f'+A{self.antialias}',  # Anti-aliasing
                f'+Q{self.quality}',  # Quality
                '-D',  # No display preview
                '+UA',  # Transparent background
            ]
        else:
            cmd = [
                self.povray_path,
                f'+I{input_file}',
                f'+O{output_file}',
                f'+W{self.width}',
                f'+H{self.height}',
                '+FN',
                f'+A{self.antialias}',
                f'+Q{self.quality}',
                '-D',
                '+UA',
            ]
        
        return cmd
    
    def render_file(self, pov_file: str, output_file: Optional[str] = None) -> Tuple[bool, str]:
        """
        Render a single .pov file to PNG.
        
        Args:
            pov_file: Path to .pov file
            output_file: Path to output .png (auto-generated if None)
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        import platform
        import time
        
        if output_file is None:
            basename = os.path.splitext(os.path.basename(pov_file))[0]
            output_file = os.path.join(self.output_dir, f"{basename}.png")
        
        cmd = self._build_command(pov_file, output_file)
        
        try:
            if platform.system() == 'Windows':
                # Windows: Start POV-Ray, wait for output file to be fully written, then kill process
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                
                # Wait for output file to appear
                max_wait = 300  # 5 minutes max
                waited = 0
                while waited < max_wait:
                    time.sleep(0.2)
                    waited += 0.2
                    if os.path.exists(output_file):
                        break
                
                if not os.path.exists(output_file):
                    process.terminate()
                    return False, f"Output file not created after {max_wait}s"
                
                # Wait for file size to stabilize (file fully written)
                # Check that size doesn't change for 1 second
                last_size = -1
                stable_count = 0
                while stable_count < 5 and waited < max_wait:  # Need 5 consecutive stable checks (1 second)
                    time.sleep(0.2)
                    waited += 0.2
                    try:
                        current_size = os.path.getsize(output_file)
                        if current_size == last_size and current_size > 0:
                            stable_count += 1
                        else:
                            stable_count = 0
                            last_size = current_size
                    except:
                        stable_count = 0
                
                # Kill POV-Ray process
                try:
                    process.terminate()
                    process.wait(timeout=2)
                except:
                    try:
                        process.kill()
                    except:
                        pass
                
                if not os.path.exists(output_file):
                    return False, f"Output file not created after {max_wait}s: {output_file}"
                
                return True, output_file
            else:
                # Linux/Mac: Normal execution
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                
                if result.returncode != 0:
                    return False, f"POV-Ray error: {result.stderr}"
                
                if not os.path.exists(output_file):
                    return False, f"Output file not created: {output_file}"
                
                return True, output_file
            
        except subprocess.TimeoutExpired:
            return False, f"Render timeout for {pov_file}"
        except Exception as e:
            return False, f"Render error: {str(e)}"
    
    def render_batch(
        self,
        pov_files: List[str],
        progress_callback=None
    ) -> List[Tuple[str, bool, str]]:
        """
        Render multiple .pov files in parallel.
        
        Args:
            pov_files: List of .pov file paths
            progress_callback: Optional callback(completed, total, filename)
            
        Returns:
            List of (pov_file, success, message) tuples
        """
        results = []
        total = len(pov_files)
        completed = 0
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all render jobs
            future_to_file = {
                executor.submit(self.render_file, pov_file): pov_file
                for pov_file in pov_files
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_file):
                pov_file = future_to_file[future]
                try:
                    success, message = future.result()
                except Exception as e:
                    success, message = False, str(e)
                
                results.append((pov_file, success, message))
                completed += 1
                
                if progress_callback:
                    progress_callback(completed, total, os.path.basename(pov_file))
        
        # Sort results by filename to maintain order
        results.sort(key=lambda x: x[0])
        return results
    
    def get_output_files(self, pov_files: List[str]) -> List[str]:
        """
        Get list of output PNG files for given POV files.
        
        Args:
            pov_files: List of .pov file paths
            
        Returns:
            List of expected .png file paths
        """
        output_files = []
        for pov_file in pov_files:
            basename = os.path.splitext(os.path.basename(pov_file))[0]
            output_files.append(os.path.join(self.output_dir, f"{basename}.png"))
        return output_files


def check_povray_available() -> Tuple[bool, str]:
    """
    Check if POV-Ray is available.
    
    Returns:
        Tuple of (available: bool, message: str)
    """
    try:
        renderer = POVRayRenderer()
        return True, f"POV-Ray found at: {renderer.povray_path}"
    except POVRayError as e:
        return False, str(e)
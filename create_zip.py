
import zipfile
import os
from pathlib import Path
import datetime

def create_project_zip():
    # Get current directory (project root)
    project_root = Path('.')
    
    # Create zip filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"AiogramShopBot_{timestamp}.zip"
    
    # Files and directories to exclude
    exclude_patterns = {
        '.git', '__pycache__', '.pytest_cache', 'node_modules',
        '.env', 'database.db', '*.pyc', '*.pyo', '*.pyd',
        '.DS_Store', 'Thumbs.db', 'data/*'
    }
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(project_root):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if not any(pattern in d for pattern in exclude_patterns)]
            
            for file in files:
                file_path = Path(root) / file
                
                # Skip excluded files
                if any(pattern in str(file_path) for pattern in exclude_patterns):
                    continue
                
                # Add file to zip
                arcname = file_path.relative_to(project_root)
                zipf.write(file_path, arcname)
                print(f"Added: {arcname}")
    
    file_size = os.path.getsize(zip_filename) / (1024 * 1024)  # Size in MB
    print(f"\n✅ Zip file created successfully!")
    print(f"📁 Filename: {zip_filename}")
    print(f"📊 Size: {file_size:.2f} MB")
    print(f"📍 Location: {os.path.abspath(zip_filename)}")
    
    return zip_filename

if __name__ == "__main__":
    create_project_zip()

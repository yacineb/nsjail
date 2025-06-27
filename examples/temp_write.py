#!/usr/bin/env python3
"""
Demonstrate writing to the temporary directory in the sandbox.
This shows how the tmpfs mount works for isolated temporary storage.
"""

import os
import tempfile
import time
import json
from pathlib import Path

def main():
    print("=== Sandbox Temporary Directory Demo ===")
    
    # Get the temporary directory dynamically
    temp_dir = tempfile.gettempdir()
    print(f"Temporary directory: {temp_dir}")
    print(f"Current working directory: {os.getcwd()}")
    
    # Show temp directory contents before writing
    tmp_path = Path(temp_dir)
    print(f"\n{temp_dir} directory contents before writing:")
    if tmp_path.exists():
        for item in tmp_path.iterdir():
            print(f"  - {item.name}")
    else:
        print(f"  {temp_dir} directory does not exist")
    
    # Write some test files to temp directory
    print(f"\nWriting test files to {temp_dir}...")
    
    # File 1: Simple text file
    test_file1 = tmp_path / "sandbox_test.txt"
    with open(test_file1, 'w') as f:
        f.write("Hello from sandbox!\n")
        f.write(f"Timestamp: {time.time()}\n")
        f.write("This file is stored in tmpfs (shared memory)\n")
    print(f"Created: {test_file1}")
    
    # File 2: JSON data
    test_data = {
        "sandbox_id": "demo_sandbox",
        "timestamp": time.time(),
        "files_created": 3,
        "tmpfs_info": "This data is stored in memory",
        "temp_dir": temp_dir
    }
    
    test_file2 = tmp_path / "sandbox_data.json"
    with open(test_file2, 'w') as f:
        json.dump(test_data, f, indent=2)
    print(f"Created: {test_file2}")
    
    # File 3: Using Python's tempfile module (automatically uses temp dir)
    with tempfile.NamedTemporaryFile(mode='w', suffix='.log', delete=False) as f:
        f.write("This is a temporary log file\n")
        f.write(f"Created at: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Temp directory: {temp_dir}\n")
        temp_file_path = f.name
    
    print(f"Created: {temp_file_path}")
    
    # Show temp directory contents after writing
    print(f"\n{temp_dir} directory contents after writing:")
    for item in tmp_path.iterdir():
        if item.is_file():
            size = item.stat().st_size
            print(f"  - {item.name} ({size} bytes)")
        else:
            print(f"  - {item.name}/ (directory)")
    
    # Read and display one of the files
    print(f"\nReading back the JSON file:")
    with open(test_file2, 'r') as f:
        data = json.load(f)
        print(json.dumps(data, indent=2))
    
    print(f"\n=== Demo complete ===")
    print("Note: These files will be automatically cleaned up when the sandbox exits")
    print("because they're stored in tmpfs (shared memory).")
    print(f"Using temp directory: {temp_dir}")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
File I/O Example: Write a text file to /data and read it back
"""

import os
import sys

def write_file_to_data():
    """Write a text file to the /data directory"""
    # Define the file path
    file_path = "/data/example.txt"
    
    # Content to write to the file
    content = """Hello from the sandbox!
This is a test file created by the file I/O example.
The file is stored in the /data directory.
Current timestamp: 2024
"""
    
    try:
        # Ensure the /data directory exists
        os.makedirs("/data", exist_ok=True)
        
        # Write content to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"✅ Successfully wrote file to: {file_path}")
        print(f"📝 Content written: {len(content)} characters")
        return file_path
        
    except PermissionError:
        print("❌ Permission denied: Cannot write to /data directory")
        return None
    except Exception as e:
        print(f"❌ Error writing file: {e}")
        return None

def read_file_from_data(file_path):
    """Read the text file from the /data directory"""
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            return None
        
        # Read content from the file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        print(f"✅ Successfully read file from: {file_path}")
        print(f"📖 Content length: {len(content)} characters")
        print("\n📄 File contents:")
        print("-" * 40)
        print(content)
        print("-" * 40)
        
        return content
        
    except PermissionError:
        print("❌ Permission denied: Cannot read from /data directory")
        return None
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return None

def main():
    """Main function to demonstrate file I/O operations"""
    print("🚀 Starting File I/O Example")
    print("=" * 50)
    
    # Step 1: Write file to /data
    print("\n📝 Step 1: Writing file to /data directory")
    file_path = write_file_to_data()
    
    if file_path is None:
        print("❌ Failed to write file. Exiting.")
        sys.exit(1)
    
    # Step 2: Read file from /data
    print("\n📖 Step 2: Reading file from /data directory")
    content = read_file_from_data(file_path)
    
    if content is None:
        print("❌ Failed to read file.")
        sys.exit(1)
    
    # Step 3: Verify the operation
    print("\n✅ Step 3: Verification")
    print("🎉 File I/O operations completed successfully!")
    
    # Additional info
    file_size = os.path.getsize(file_path)
    print(f"📊 File size: {file_size} bytes")
    print(f"📍 File location: {file_path}")

if __name__ == "__main__":
    main() 
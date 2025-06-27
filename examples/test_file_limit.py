#!/usr/bin/env python3
"""
Test the file descriptor limit in the sandbox.
This program tries to open more files than the rlimit_nofile limit allows.
"""

import os
import tempfile
import resource
import sys
from pathlib import Path

def get_file_descriptor_limit():
    """Get the current file descriptor limit."""
    soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
    return soft, hard

def count_open_file_descriptors():
    """Count the number of open file descriptors for the current process."""
    try:
        # Count open file descriptors for current process
        fd_count = len(os.listdir('/proc/self/fd'))
        print(f"\nCurrent open file descriptors: {fd_count}")
    except Exception as e:  
        print(f"Could not count file descriptors: {e}")

def main():
    print("=== File Descriptor Limit Test ===")

    count_open_file_descriptors()
    
    # Get current limits
    soft_limit, hard_limit = get_file_descriptor_limit()
    print(f"Current soft limit: {soft_limit}")
    print(f"Current hard limit: {hard_limit}")
    
    # Get temp directory
    temp_dir = tempfile.gettempdir()
    print(f"Using temp directory: {temp_dir}")
    
    # Try to open files until we hit the limit
    files = []
    file_count = 0
    
    print(f"\nAttempting to open files...")
    print(f"Target: {soft_limit + 10} files (exceeding limit by 10)")
    
    try:
        for i in range(soft_limit + 10):
            # Create a temporary file
            temp_file = tempfile.NamedTemporaryFile(
                mode='w',
                suffix=f'_{i}.txt',
                delete=False,
                dir=temp_dir
            )
            
            # Write some data to the file
            temp_file.write(f"This is test file number {i}\n")
            temp_file.write(f"File descriptor: {temp_file.fileno()}\n")
            temp_file.flush()
            
            files.append(temp_file)
            file_count += 1
            
            if file_count % 10 == 0:
                print(f"Opened {file_count} files so far...")
                
    except OSError as e:
        print(f"\n❌ Error after opening {file_count} files:")
        print(f"Error: {e}")
        print(f"Error code: {e.errno}")
        
        if e.errno == 24:  # EMFILE - Too many open files
            print("This is the expected EMFILE error (Too many open files)")
        else:
            print(f"Unexpected error code: {e.errno}")
    
    # Show final status
    print(f"\n=== Final Status ===")
    print(f"Successfully opened: {file_count} files")
    print(f"Limit was: {soft_limit} files")
    
    if file_count >= soft_limit:
        print("✅ Successfully hit the file descriptor limit!")
    else:
        print("❌ Did not reach the file descriptor limit")
    
    # Clean up opened files
    print(f"\nCleaning up {len(files)} opened files...")
    for i, file in enumerate(files):
        try:
            file.close()
            # Remove the temporary file
            os.unlink(file.name)
        except Exception as e:
            print(f"Error closing file {i}: {e}")
    
    print("Cleanup complete!")

    count_open_file_descriptors()
    


if __name__ == "__main__":
    main() 
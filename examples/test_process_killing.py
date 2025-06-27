#!/usr/bin/env python3
"""
Test script to list all processes and attempt to kill them all.
This tests the effectiveness of seccomp filtering that removes kill-related syscalls.
"""

import os
import signal
import psutil
import time
from typing import List, Dict

def get_all_processes() -> List[Dict]:
    """Get information about all running processes."""
    processes = []
    try:
        for proc in psutil.process_iter(['pid', 'name', 'username', 'status']):
            try:
                proc_info = proc.info
                processes.append(proc_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
    except Exception as e:
        print(f"Error getting process list: {e}")
    
    return processes

def kill_process(pid: int, signal_type: int = signal.SIGTERM) -> bool:
    """Attempt to kill a specific process."""
    try:
        os.kill(pid, signal_type)
        return True
    except ProcessLookupError:
        print(f"Process {pid} not found")
        return False
    except PermissionError:
        print(f"Permission denied to kill process {pid}")
        return False
    except OSError as e:
        print(f"OS error killing process {pid}: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error killing process {pid}: {e}")
        return False

def kill_all_processes_except_self():
    """Attempt to kill all processes except the current one."""
    current_pid = os.getpid()
    processes = get_all_processes()
    
    print(f"Current process PID: {current_pid}")
    print(f"Found {len(processes)} processes")
    print("\n" + "="*80)
    print("PROCESS LIST:")
    print("="*80)
    
    # Display all processes
    for proc in processes:
        pid = proc['pid']
        name = proc.get('name', 'Unknown')
        username = proc.get('username', 'Unknown')
        status = proc.get('status', 'Unknown')
        print(f"PID: {pid:>6} | Name: {name:<20} | User: {username:<15} | Status: {status}")
    
    print("\n" + "="*80)
    print("ATTEMPTING TO KILL ALL PROCESSES (except self):")
    print("="*80)
    
    killed_count = 0
    failed_count = 0
    
    for proc in processes:
        pid = proc['pid']
        name = proc.get('name', 'Unknown')
        
        # Skip our own process
        if pid == current_pid:
            print(f"Skipping own process: PID {pid} ({name})")
            continue
        
        print(f"Attempting to kill PID {pid} ({name})...", end=" ")
        
        # Try SIGTERM first
        if kill_process(pid, signal.SIGTERM):
            print("SIGTERM sent successfully")
            killed_count += 1
        else:
            # Try SIGKILL as fallback
            print("SIGTERM failed, trying SIGKILL...", end=" ")
            if kill_process(pid, signal.SIGKILL):
                print("SIGKILL sent successfully")
                killed_count += 1
            else:
                print("Both SIGTERM and SIGKILL failed")
                failed_count += 1
    
    print("\n" + "="*80)
    print("SUMMARY:")
    print("="*80)
    print(f"Total processes found: {len(processes)}")
    print(f"Successfully killed: {killed_count}")
    print(f"Failed to kill: {failed_count}")
    print(f"Own process (skipped): 1")
    
    return killed_count, failed_count

def test_signal_sending():
    """Test different signal sending methods."""
    print("\n" + "="*80)
    print("TESTING SIGNAL SENDING METHODS:")
    print("="*80)
    
    # Test os.kill
    print("Testing os.kill...")
    try:
        os.kill(1, signal.SIGUSR1)  # Try to send signal to init process
        print("✓ os.kill() call succeeded")
    except Exception as e:
        print(f"✗ os.kill() failed: {e}")
    
    # Test psutil.Process.kill
    print("Testing psutil.Process.kill...")
    try:
        proc = psutil.Process(1)
        proc.kill()
        print("✓ psutil.Process.kill() call succeeded")
    except Exception as e:
        print(f"✗ psutil.Process.kill() failed: {e}")
    
    # Test signal sending to multiple processes
    print("Testing signal sending to multiple processes...")
    try:
        for proc in psutil.process_iter(['pid']):
            try:
                os.kill(proc.info['pid'], signal.SIGUSR1)
                print(f"✓ Sent SIGUSR1 to PID {proc.info['pid']}")
                break  # Just test with first process
            except Exception as e:
                print(f"✗ Failed to send SIGUSR1 to PID {proc.info['pid']}: {e}")
                break
    except Exception as e:
        print(f"✗ Error in signal sending test: {e}")

def main():
    """Main function to run the process killing test."""
    print("PROCESS KILLING TEST SCRIPT")
    print("This script tests the effectiveness of seccomp filtering")
    print("by attempting to list and kill all processes.")
    print()
    
    # Test signal sending methods first
    test_signal_sending()
    
    # Wait a moment
    time.sleep(1)
    
    # Attempt to kill all processes
    killed, failed = kill_all_processes_except_self()
    
    print("\n" + "="*80)
    print("TEST COMPLETE")
    print("="*80)
    
    if killed > 0:
        print("⚠️  WARNING: Some processes were successfully killed!")
        print("   This indicates the seccomp filtering may not be working properly.")
    else:
        print("✅ SUCCESS: No processes were killed.")
        print("   This indicates the seccomp filtering is working correctly.")
    
    if failed > 0:
        print(f"ℹ️  {failed} processes could not be killed (likely due to permissions)")

if __name__ == "__main__":
    main() 
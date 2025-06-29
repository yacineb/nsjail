#!/usr/bin/env python3
"""
Script attempting to reboot the system using various methods.
This is likely to be blocked by the sandbox's security measures.
"""

import os
import sys
import subprocess
import time
import signal

def print_status(message):
    """Print a status message with timestamp."""
    print(f"[{time.strftime('%H:%M:%S')}] {message}")

def try_reboot_method(method_name, command, description=""):
    """Try a specific reboot method and report the result."""
    print_status(f"Attempting reboot method: {method_name}")
    if description:
        print(f"  Description: {description}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
        print(f"  Exit code: {result.returncode}")
        if result.stdout:
            print(f"  stdout: {result.stdout.strip()}")
        if result.stderr:
            print(f"  stderr: {result.stderr.strip()}")
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("  Timeout: Command took too long to execute")
        return False
    except Exception as e:
        print(f"  Error: {e}")
        return False

def try_system_call_reboot():
    """Try to reboot using system calls."""
    print_status("Attempting reboot via system calls")
    
    try:
        # Try to import os and use system calls
        os.system("reboot")
        return True
    except Exception as e:
        print(f"  Error: {e}")
        return False

def try_signal_reboot():
    """Try to send reboot signal to init process."""
    print_status("Attempting reboot via signals")
    
    try:
        # Try to send SIGTERM to init (PID 1)
        os.kill(1, signal.SIGTERM)
        print("  Sent SIGTERM to init process")
        return True
    except PermissionError:
        print("  Permission denied: Cannot send signal to init")
        return False
    except Exception as e:
        print(f"  Error: {e}")
        return False

def try_write_to_proc():
    """Try to write to /proc/sysrq-trigger."""
    print_status("Attempting reboot via /proc/sysrq-trigger")
    
    try:
        with open("/proc/sysrq-trigger", "w") as f:
            f.write("b")  # 'b' triggers reboot
        print("  Wrote 'b' to /proc/sysrq-trigger")
        return True
    except PermissionError:
        print("  Permission denied: Cannot write to /proc/sysrq-trigger")
        return False
    except FileNotFoundError:
        print("  File not found: /proc/sysrq-trigger")
        return False
    except Exception as e:
        print(f"  Error: {e}")
        return False

def try_magic_sysrq():
    """Try magic sysrq reboot."""
    print_status("Attempting reboot via magic sysrq")
    
    try:
        # Enable sysrq
        with open("/proc/sys/kernel/sysrq", "w") as f:
            f.write("1")
        
        # Trigger reboot
        with open("/proc/sysrq-trigger", "w") as f:
            f.write("b")
        
        print("  Triggered magic sysrq reboot")
        return True
    except Exception as e:
        print(f"  Error: {e}")
        return False

def main():
    """Main function to attempt various reboot methods."""
    print("=" * 60)
    print("SYSTEM REBOOT ATTEMPT SCRIPT")
    print("=" * 60)
    print("This script attempts to reboot the system using various methods.")
    print("In a properly secured sandbox, these attempts should be blocked.")
    print()
    
    # List of reboot methods to try
    reboot_methods = [
        ("systemctl reboot", "systemctl reboot", "Systemd reboot command"),
        ("shutdown -r now", "shutdown -r now", "Traditional shutdown reboot"),
        ("init 6", "init 6", "SysV init reboot"),
        ("telinit 6", "telinit 6", "Telinit reboot"),
        ("halt -r", "halt -r", "Halt with reboot"),
        ("poweroff -r", "poweroff -r", "Poweroff with reboot"),
        ("sudo reboot", "sudo reboot", "Sudo reboot (if sudo available)"),
    ]
    
    success_count = 0
    total_methods = len(reboot_methods)
    
    # Try command-line reboot methods
    for method_name, command, description in reboot_methods:
        if try_reboot_method(method_name, command, description):
            success_count += 1
        print()
    
    # Try system call methods
    if try_system_call_reboot():
        success_count += 1
    print()
    
    # Try signal methods
    if try_signal_reboot():
        success_count += 1
    print()
    
    # Try proc filesystem methods
    if try_write_to_proc():
        success_count += 1
    print()
    
    # Try magic sysrq
    if try_magic_sysrq():
        success_count += 1
    print()
    
    # Summary
    print("=" * 60)
    print("REBOOT ATTEMPT SUMMARY")
    print("=" * 60)
    print(f"Total methods attempted: {total_methods + 4}")  # +4 for the additional methods
    print(f"Successful attempts: {success_count}")
    print(f"Blocked attempts: {total_methods + 4 - success_count}")
    
    if success_count == 0:
        print("\n✅ All reboot attempts were successfully blocked by the sandbox!")
        print("This indicates the sandbox is properly secured.")
    else:
        print(f"\n⚠️  {success_count} reboot method(s) succeeded!")
        print("This may indicate a security issue with the sandbox.")
    
    print("\nNote: If the system actually reboots, this script won't complete.")
    print("If you're seeing this message, the reboot attempts were blocked.")

if __name__ == "__main__":
    main() 
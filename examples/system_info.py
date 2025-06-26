#!/usr/bin/env python3
"""
System Information Example: Display home directory, user, and CPU count
"""

import os
import getpass
import multiprocessing
import platform

def get_home_directory():
    """Get and return the home directory information"""
    try:
        home_dir = os.path.expanduser("~")
        return {
            'path': home_dir,
            'exists': os.path.exists(home_dir),
            'readable': os.access(home_dir, os.R_OK),
            'writable': os.access(home_dir, os.W_OK)
        }
    except Exception as e:
        return {'error': str(e)}

def get_user_information():
    """Get and return user information"""
    try:
        return {
            'username': getpass.getuser(),
            'real_name': os.environ.get('USER', 'Unknown'),
            'uid': os.getuid() if hasattr(os, 'getuid') else 'N/A',
            'gid': os.getgid() if hasattr(os, 'getgid') else 'N/A'
        }
    except Exception as e:
        return {'error': str(e)}

def get_cpu_information():
    """Get and return CPU information"""
    try:
        return {
            'cpu_count': os.cpu_count(),
            'platform': platform.platform(),
            'processor': platform.processor()
        }
    except Exception as e:
        return {'error': str(e)}

def get_current_directory():
    """Get and return current working directory information"""
    try:
        current_dir = os.getcwd()
        return {
            'path': current_dir,
            'exists': os.path.exists(current_dir),
            'readable': os.access(current_dir, os.R_OK),
            'writable': os.access(current_dir, os.W_OK),
            'absolute': os.path.abspath(current_dir)
        }
    except Exception as e:
        return {'error': str(e)}

def get_ram_information():
    """Get and return RAM information"""
    try:
        # Try to use psutil for cross-platform RAM info
        try:
            import psutil
            memory = psutil.virtual_memory()
            return {
                'total': memory.total,
                'available': memory.available,
                'used': memory.used,
                'percent': memory.percent,
                'total_gb': round(memory.total / (1024**3), 2),
                'available_gb': round(memory.available / (1024**3), 2),
                'used_gb': round(memory.used / (1024**3), 2)
            }
        except ImportError:
            # Fallback for systems without psutil
            if platform.system() == "Linux":
                # Read from /proc/meminfo on Linux
                with open('/proc/meminfo', 'r') as f:
                    lines = f.readlines()
                    total = 0
                    available = 0
                    for line in lines:
                        if line.startswith('MemTotal:'):
                            total = int(line.split()[1]) * 1024  # Convert KB to bytes
                        elif line.startswith('MemAvailable:'):
                            available = int(line.split()[1]) * 1024  # Convert KB to bytes
                            break
                    used = total - available
                    percent = (used / total) * 100 if total > 0 else 0
                    return {
                        'total': total,
                        'available': available,
                        'used': used,
                        'percent': round(percent, 1),
                        'total_gb': round(total / (1024**3), 2),
                        'available_gb': round(available / (1024**3), 2),
                        'used_gb': round(used / (1024**3), 2)
                    }
            elif platform.system() == "Darwin":  # macOS
                # Use sysctl on macOS
                import subprocess
                result = subprocess.run(['sysctl', '-n', 'hw.memsize'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    total = int(result.stdout.strip())
                    # For macOS, we'll just show total RAM as available RAM is complex to get
                    return {
                        'total': total,
                        'available': total,  # Approximation
                        'used': 0,  # Not available without psutil
                        'percent': 0,
                        'total_gb': round(total / (1024**3), 2),
                        'available_gb': round(total / (1024**3), 2),
                        'used_gb': 0
                    }
            else:
                # Generic fallback
                return {'error': 'RAM information not available on this platform'}
    except Exception as e:
        return {'error': str(e)}

def print_home_info(home_info):
    """Print home directory information"""
    print("🏠 Home Directory Information:")
    print("-" * 40)
    
    if 'error' in home_info:
        print(f"❌ Error: {home_info['error']}")
        return
    
    print(f"📍 Path: {home_info['path']}")
    print(f"📁 Exists: {'✅ Yes' if home_info['exists'] else '❌ No'}")
    print(f"📖 Readable: {'✅ Yes' if home_info['readable'] else '❌ No'}")
    print(f"✏️  Writable: {'✅ Yes' if home_info['writable'] else '❌ No'}")

def print_user_info(user_info):
    """Print user information"""
    print("\n👤 User Information:")
    print("-" * 40)
    
    if 'error' in user_info:
        print(f"❌ Error: {user_info['error']}")
        return
    
    print(f"👤 Username: {user_info['username']}")
    print(f"📝 Real Name: {user_info['real_name']}")
    print(f"🆔 User ID: {user_info['uid']}")
    print(f"👥 Group ID: {user_info['gid']}")

def print_cpu_info(cpu_info):
    """Print CPU information"""
    print("\n🖥️  CPU Information:")
    print("-" * 40)
    
    if 'error' in cpu_info:
        print(f"❌ Error: {cpu_info['error']}")
        return
    
    print(f"🔢 CPU Count: {cpu_info['cpu_count']}")
    print(f"💻 Platform: {cpu_info['platform']}")
    print(f"🔧 Processor: {cpu_info['processor']}")

def print_ram_info(ram_info):
    """Print RAM information"""
    print("\n💾 RAM Information:")
    print("-" * 40)
    
    if 'error' in ram_info:
        print(f"❌ Error: {ram_info['error']}")
        return
    
    print(f"💾 Total RAM: {ram_info['total_gb']} GB ({ram_info['total']:,} bytes)")
    print(f"✅ Available RAM: {ram_info['available_gb']} GB ({ram_info['available']:,} bytes)")
    print(f"📊 Used RAM: {ram_info['used_gb']} GB ({ram_info['used']:,} bytes)")
    print(f"📈 Usage: {ram_info['percent']}%")

def print_current_dir_info(current_dir_info):
    """Print current working directory information"""
    print("\n📂 Current Working Directory:")
    print("-" * 40)
    
    if 'error' in current_dir_info:
        print(f"❌ Error: {current_dir_info['error']}")
        return
    
    print(f"📍 Path: {current_dir_info['path']}")
    print(f"🔗 Absolute Path: {current_dir_info['absolute']}")
    print(f"📁 Exists: {'✅ Yes' if current_dir_info['exists'] else '❌ No'}")
    print(f"📖 Readable: {'✅ Yes' if current_dir_info['readable'] else '❌ No'}")
    print(f"✏️  Writable: {'✅ Yes' if current_dir_info['writable'] else '❌ No'}")

def main():
    """Main function to display system information"""
    print("🚀 System Information Display")
    print("=" * 50)
    
    # Get home directory information
    home_info = get_home_directory()
    print_home_info(home_info)
    
    # Get user information
    user_info = get_user_information()
    print_user_info(user_info)
    
    # Get current working directory information
    current_dir_info = get_current_directory()
    print_current_dir_info(current_dir_info)
    
    # Get RAM information
    ram_info = get_ram_information()
    print_ram_info(ram_info)
    
    # Get CPU information
    cpu_info = get_cpu_information()
    print_cpu_info(cpu_info)
    
    # Summary
    print("\n✅ System information display completed!")
    print("=" * 50)

if __name__ == "__main__":
    main() 
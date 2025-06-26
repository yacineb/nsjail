#!/usr/bin/env python3
"""
IP Address Fetcher: Get current public IP address using ipify API
This program demonstrates how to make HTTP requests to external APIs.
"""

import urllib.request
import json
import socket
import time

def get_public_ip():
    """Get public IP address using ipify API"""
    try:
        print("🌐 Fetching public IP address from ipify API...")
        
        # Make request to ipify API
        url = "https://api.ipify.org?format=json"
        
        with urllib.request.urlopen(url, timeout=10) as response:
            data = response.read()
            ip_info = json.loads(data.decode('utf-8'))
            
        return ip_info.get('ip')
        
    except urllib.error.URLError as e:
        print(f"❌ Network error: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

def get_local_ip():
    """Get local IP address"""
    try:
        # Get local hostname
        hostname = socket.gethostname()
        
        # Get local IP address
        local_ip = socket.gethostbyname(hostname)
        
        return {
            'hostname': hostname,
            'local_ip': local_ip
        }
    except Exception as e:
        print(f"❌ Error getting local IP: {e}")
        return None

def display_ip_info():
    """Display comprehensive IP information"""
    print("🚀 IP Address Information")
    print("=" * 50)
    
    # Get local IP information
    print("\n🏠 Local Network Information:")
    print("-" * 40)
    
    local_info = get_local_ip()
    if local_info:
        print(f"🖥️  Hostname: {local_info['hostname']}")
        print(f"🏠 Local IP: {local_info['local_ip']}")
    else:
        print("❌ Could not retrieve local IP information")
    
    # Get public IP information
    print("\n🌍 Public IP Information:")
    print("-" * 40)
    
    start_time = time.time()
    public_ip = get_public_ip()
    end_time = time.time()
    
    if public_ip:
        print(f"🌐 Public IP: {public_ip}")
        print(f"⏱️  Response time: {end_time - start_time:.2f} seconds")
        
        # Additional information about the IP
        print(f"🔗 API URL: https://api.ipify.org?format=json")
        print(f"📡 Protocol: HTTPS")
        print(f"🌍 Service: ipify.org")
    else:
        print("❌ Could not retrieve public IP address")
        print("💡 Possible reasons:")
        print("   - No internet connection")
        print("   - Network firewall blocking the request")
        print("   - API service temporarily unavailable")
    
    # Summary
    print("\n📊 Summary:")
    print("-" * 40)
    if public_ip and local_info:
        print("✅ Both local and public IP addresses retrieved successfully")
        print(f"🏠 Local: {local_info['local_ip']}")
        print(f"🌐 Public: {public_ip}")
    elif public_ip:
        print("✅ Public IP retrieved, local IP failed")
        print(f"🌐 Public: {public_ip}")
    elif local_info:
        print("✅ Local IP retrieved, public IP failed")
        print(f"🏠 Local: {local_info['local_ip']}")
    else:
        print("❌ Failed to retrieve any IP information")

def test_network_connectivity():
    """Test basic network connectivity"""
    print("\n🔍 Network Connectivity Test:")
    print("-" * 40)
    
    # Test DNS resolution
    try:
        socket.gethostbyname("google.com")
        print("✅ DNS resolution working")
    except Exception as e:
        print(f"❌ DNS resolution failed: {e}")
        return False
    
    # Test HTTPS connectivity
    try:
        urllib.request.urlopen("https://httpbin.org/get", timeout=5)
        print("✅ HTTPS connectivity working")
    except Exception as e:
        print(f"❌ HTTPS connectivity failed: {e}")
        return False
    
    return True

def main():
    """Main function"""
    try:
        # Test network connectivity first
        if test_network_connectivity():
            display_ip_info()
        else:
            print("❌ Network connectivity issues detected")
            print("💡 Please check your internet connection")
    except KeyboardInterrupt:
        print("\n⏹️  Operation interrupted by user")
    except Exception as e:
        print(f"\n❌ Program failed with error: {e}")
    
    print("\n✅ IP address check completed!")

if __name__ == "__main__":
    main() 
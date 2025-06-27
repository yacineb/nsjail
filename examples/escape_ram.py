#!/usr/bin/env python3
"""
RAM Allocation Test: Attempt to allocate 2GB of RAM
This program tests the memory limitations set in the sandbox configuration.
"""

import time

def allocate_memory(size_mb):
    """Attempt to allocate specified amount of memory in MB"""
    try:
        # Convert MB to bytes
        size_bytes = size_mb * 1024 * 1024
        
        print(f"🔄 Attempting to allocate {size_mb} MB ({size_bytes:,} bytes) of RAM...")
        
        # Allocate memory by creating a large byte array
        memory_block = bytearray(size_bytes)
        
        print(f"✅ Successfully allocated {size_mb} MB of RAM!")
        print(f"📊 Memory block size: {len(memory_block):,} bytes")
        
        # Fill the memory with some data to ensure it's actually allocated
        print("🔄 Filling memory with data...")
        for i in range(0, len(memory_block), 1024):  # Fill in 1KB chunks
            memory_block[i:i+1024] = b'X' * min(1024, len(memory_block) - i)
        
        print("✅ Memory filled successfully!")
        return memory_block
        
    except MemoryError as e:
        print(f"❌ MemoryError: Failed to allocate {size_mb} MB of RAM")
        print(f"💡 Error details: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

def test_memory_allocation():
    """Test different memory allocation scenarios"""
    print("🚀 RAM Allocation Test")
    print("=" * 50)
    
    # Test 1: Try to allocate 2GB (2048 MB)
    print("\n📋 Test 1: Allocating 2GB of RAM")
    print("-" * 40)
    
    start_time = time.time()
    memory_block_1gb = allocate_memory(2048)
    end_time = time.time()
    
    if memory_block_1gb:
        print(f"⏱️  Allocation time: {end_time - start_time:.2f} seconds")
        print("🎉 2GB allocation successful! This exceeds the sandbox limit.")
        
        # Keep the memory allocated for a moment to demonstrate
        print("🔄 Holding memory for 3 seconds...")
        time.sleep(3)
        
        # Explicitly delete the memory block
        del memory_block_1gb
        print("🗑️  Memory block released")
    else:
        print("✅ Sandbox memory limit working correctly!")
    
    # Test 2: Try smaller allocations if 2GB fails
    if not memory_block_1gb:
        print("\n📋 Test 2: Testing smaller allocations")
        print("-" * 40)
        
        test_sizes = [100, 500, 800, 900, 1000]  # MB
        
        for size in test_sizes:
            print(f"\n🔄 Testing {size} MB allocation...")
            memory_block = allocate_memory(size)
            
            if memory_block:
                print(f"✅ {size} MB allocation successful")
                del memory_block
                print(f"🗑️  {size} MB memory released")
            else:
                print(f"❌ {size} MB allocation failed - likely hit sandbox limit")
                break
    
    print("\n📊 Test Summary:")
    print("-" * 40)
    if memory_block_1gb:
        print("⚠️  1GB allocation succeeded - sandbox memory limit may not be working")
    else:
        print("✅ Sandbox memory limit is working correctly")
    
    print("🎯 Expected behavior: Allocation should fail due to 1GB limit in sandbox.cfg")

def main():
    """Main function"""
    try:
        test_memory_allocation()
    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
    
    print("\n✅ RAM allocation test completed!")

if __name__ == "__main__":
    main()

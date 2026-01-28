#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify Windows compatibility fixes
"""

import os
import sys
import subprocess

def test_batch_files_exist():
    """Test that Windows batch files exist"""
    print("Testing batch file existence...")
    
    files = ['setup.bat', 'start.bat']
    for filename in files:
        if os.path.exists(filename):
            print(f"  ✅ {filename} exists")
        else:
            print(f"  ❌ {filename} missing")
            return False
    
    return True

def test_windows_doc_exists():
    """Test that Windows documentation exists"""
    print("\nTesting Windows documentation...")
    
    if os.path.exists('WINDOWS.md'):
        print("  ✅ WINDOWS.md exists")
        with open('WINDOWS.md', 'r', encoding='utf-8') as f:
            content = f.read()
            if 'setup.bat' in content and 'start.bat' in content:
                print("  ✅ WINDOWS.md references batch files")
                return True
            else:
                print("  ❌ WINDOWS.md doesn't reference batch files")
                return False
    else:
        print("  ❌ WINDOWS.md missing")
        return False

def test_config_example_exists():
    """Test that config.example.py exists"""
    print("\nTesting config example file...")
    
    if os.path.exists('config.example.py'):
        print("  ✅ config.example.py exists")
        return True
    else:
        print("  ❌ config.example.py missing")
        return False

def test_readme_mentions_windows():
    """Test that README files mention Windows support"""
    print("\nTesting README files for Windows mentions...")
    
    success = True
    for readme in ['README.md', 'README_TR.md']:
        if os.path.exists(readme):
            with open(readme, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'Windows' in content or 'WINDOWS.md' in content:
                    print(f"  ✅ {readme} mentions Windows support")
                else:
                    print(f"  ❌ {readme} doesn't mention Windows support")
                    success = False
        else:
            print(f"  ❌ {readme} missing")
            success = False
    
    return success

def test_bot_error_handling():
    """Test that bot.py has proper error handling"""
    print("\nTesting bot.py error handling...")
    
    if not os.path.exists('bot.py'):
        print("  ❌ bot.py missing")
        return False
    
    with open('bot.py', 'r', encoding='utf-8') as f:
        content = f.read()
        
        checks = [
            ('try:', 'Try block exists'),
            ('except ImportError', 'ImportError handling'),
            ('config.py file not found', 'Clear error message'),
            ('copy config.example.py config.py', 'Unix copy instruction'),
        ]
        
        success = True
        for check_str, desc in checks:
            if check_str in content:
                print(f"  ✅ {desc}")
            else:
                print(f"  ❌ {desc} missing")
                success = False
        
        return success

def main():
    print("="*60)
    print("Windows Compatibility Test Suite")
    print("="*60)
    print()
    
    tests = [
        test_batch_files_exist,
        test_windows_doc_exists,
        test_config_example_exists,
        test_readme_mentions_windows,
        test_bot_error_handling,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"  ❌ Test failed with error: {e}")
            results.append(False)
    
    print("\n" + "="*60)
    print("Test Results")
    print("="*60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if all(results):
        print("\n✅ All tests passed!")
        print("\nWindows users can now:")
        print("  1. Run setup.bat to configure the bot")
        print("  2. Edit config.py with their bot token")
        print("  3. Run start.bat to start the bot")
        print("\nSee WINDOWS.md for complete instructions.")
        return 0
    else:
        print("\n❌ Some tests failed!")
        return 1

if __name__ == '__main__':
    sys.exit(main())

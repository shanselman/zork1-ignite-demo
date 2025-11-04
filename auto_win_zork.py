#!/usr/bin/env python3
"""Automated Zork I completion script using Fic interpreter"""

import sys
import time
try:
    import pexpect
    import pexpect.popen_spawn as popen_spawn
except ImportError:
    print("ERROR: pexpect not installed. Run: pip install pexpect")
    sys.exit(1)

def run_zork_walkthrough(story_file, commands_file):
    """Run Zork with automated command sequence"""
    
    # Read commands from file
    with open(commands_file, 'r') as f:
        commands = [line.strip() for line in f if line.strip()]
    
    print("=" * 60)
    print("AUTOMATED ZORK I COMPLETION")
    print("=" * 60)
    print(f"Story file: {story_file}")
    print(f"Commands to execute: {len(commands)}")
    print("=" * 60)
    print()
    
    # Start Fic interpreter
    fic_path = r"D:\github\zork1\Fic\fic.py"
    
    try:
        # Spawn the process
        child = popen_spawn.PopenSpawn(f'python "{fic_path}" "{story_file}"', timeout=3, encoding='utf-8')
        
        print("Game started! Executing commands...\n")
        
        # Wait for initial prompt
        child.expect('>', timeout=5)
        
        # Execute each command
        for i, cmd in enumerate(commands):
            if i % 10 == 0:
                print(f"Progress: {i}/{len(commands)} commands executed...")
            
            child.sendline(cmd)
            try:
                child.expect('>', timeout=2)
            except:
                pass  # Some commands may not have a prompt
        
        # Get final output
        time.sleep(1)
        try:
            remaining = child.read()
            print("\n" + remaining)
        except:
            pass
        
        child.close()
        
        print()
        print("=" * 60)
        print("✓ Walkthrough completed!")
        print("=" * 60)
        
    except FileNotFoundError:
        print(f"ERROR: Could not find Fic interpreter at {fic_path}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    story_file = r'D:\github\zork1\zork1.z3'
    commands_file = r'D:\github\zork1\win_zork.txt'
    
    run_zork_walkthrough(story_file, commands_file)

import sys
import subprocess

# Simple wrapper to play Zork using Windows Frotz
story_file = r"D:\github\zork1\COMPILED\zork1.z3"
frotz_exe = r"D:\github\zork1\COMPILED\Frotz\Frotz.exe"

print("Starting Zork I: The Great Underground Empire")
print("=" * 50)
subprocess.run([frotz_exe, story_file])

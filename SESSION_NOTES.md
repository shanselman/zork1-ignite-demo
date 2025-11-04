# Zork1 Project - Session Notes

**Last Updated**: November 4, 2024  
**Repository**: https://github.com/shanselman/zork1-ignite-demo

## Project Overview

This is a working Zork I implementation with CLI playability. The repository contains:
1. Original Zork I source code (ZIL files)
2. Compiled Z-machine game files (.z3 format)
3. Working Z-machine interpreter (Fic)
4. Python automation scripts
5. Gameplay documentation

## What We Accomplished

### 1. Found and Installed a Z-Machine CLI Interpreter

**Selected Tool**: Fic - https://github.com/mjdarby/Fic

**Why Fic?**
- Pure Python Z-machine interpreter
- Supports Z-machine v3 (which Zork I uses)
- Terminal-based with curses interface
- Active and maintained

**Installation Steps**:
```bash
cd D:\github\zork1
git clone https://github.com/mjdarby/Fic.git
cd Fic
pip install readchar windows-curses
```

**Location**: `D:\github\zork1\Fic\`

### 2. Successfully Played Zork I

**How to Play**:
```bash
cd D:\github\zork1\Fic
python fic.py ..\zork1.z3
```

**Game File**: `D:\github\zork1\zork1.z3`
- Release 119 / Serial number 880429
- Z-machine version 3

**Achievement**:
- Score: 50/350 points
- Rank: Amateur Adventurer
- Moves: 76
- Key accomplishments:
  - Defeated the troll
  - Found treasure (bag of coins)
  - Navigated maze
  - Saved game as: `zork_progress.sav`

### 3. Created Automation Scripts

**Files Created**:

1. **`auto_win_zork.py`** - Automated playthrough script
   - Uses pexpect to interact with Fic
   - Executes commands from file
   - Location: `D:\github\zork1\auto_win_zork.py`

2. **`win_zork.txt`** - Command sequence file
   - Contains 337 commands for walkthrough
   - Can be used as reference
   - Location: `D:\github\zork1\win_zork.txt`

3. **`play_zork.py`** - Simple launcher for Windows Frotz
   - Alternative method using Frotz.exe
   - Location: `D:\github\zork1\play_zork.py`

4. **`zork_cli.py`** - Custom mock interpreter
   - Basic hardcoded interpreter (not fully functional)
   - Educational/demonstration purposes
   - Location: `D:\github\zork1\zork_cli.py`

### 4. Documentation Created

1. **`ZORK_ACHIEVEMENT.md`** - Gameplay record
   - Documents the successful playthrough
   - Lists achievements and inventory
   - Technical setup instructions

2. **`SESSION_NOTES.md`** (this file)
   - Session summary for future reference
   - Commands and procedures
   - Repository structure

## Repository Structure

```
D:\github\zork1\
├── Fic/                          # Z-machine interpreter (cloned)
│   └── fic.py                    # Main interpreter script
├── COMPILED/
│   ├── Frotz/                    # Windows Frotz interpreter
│   │   └── Frotz.exe
│   └── zork1-ignite.z3          # Compiled game file
├── *.zil                         # Original ZIL source files
├── zork1.z3                      # Main compiled game file
├── auto_win_zork.py             # Automated playthrough script
├── play_zork.py                 # Frotz launcher
├── zork_cli.py                  # Mock interpreter
├── win_zork.txt                 # Walkthrough commands
├── zork_progress.sav            # Saved game (50 points)
├── ZORK_ACHIEVEMENT.md          # Gameplay documentation
├── SESSION_NOTES.md             # This file
└── README.md                    # Original repo readme

Git Remotes:
- origin: https://github.com/historicalsource/zork1.git (original source)
- demo: https://github.com/shanselman/zork1-ignite-demo.git (our fork)
```

## Key Commands Reference

### Playing Zork Interactively

```bash
# Method 1: Using Fic (recommended)
cd D:\github\zork1\Fic
python fic.py ..\zork1.z3

# Method 2: Using Frotz (Windows GUI opens)
cd D:\github\zork1
python play_zork.py
```

### Basic Zork Commands

```
Movement: n, s, e, w, ne, nw, se, sw, u, d
Actions: look, take, drop, open, close, read, examine
Combat: kill [enemy] with [weapon]
Utility: inventory (i), score, save, restore, quit
```

### Git Commands Used

```bash
# View current remotes
git remote -v

# Create new GitHub repo and push
gh repo create zork1-ignite-demo --public --source=. --remote=demo --push

# Add all files and commit
git add -A
git commit -m "message"
git push demo master
```

## Important Technical Notes

### Fic Interpreter Limitations

1. **No stdin redirection**: Fic uses curses, so you can't pipe commands
   ```bash
   # This DOES NOT work:
   cat commands.txt | python fic.py zork1.z3
   ```

2. **Interactive only**: Must use async PowerShell sessions or pexpect for automation

3. **Windows compatibility**: Requires `windows-curses` package on Windows

### PowerShell Sessions for Automation

The successful approach was using PowerShell async sessions:

```powershell
# Start game in async mode
powershell -mode async -sessionId zorkgame
cd D:\github\zork1\Fic && python fic.py ..\zork1.z3

# Send commands
write_powershell -sessionId zorkgame -input "open mailbox{enter}take leaflet{enter}"

# Read output
read_powershell -sessionId zorkgame -delay 3
```

## Next Session Reminders

### To Continue Playing

1. The game is saved at `zork_progress.sav` with 50/350 points
2. To restore: run Fic, then use command `restore` and enter `zork_progress.sav`
3. Current location: Lost in the maze
4. Inventory: skeleton key, bag of coins, sword, lamp, leaflet

### To Complete the Game

Goal: Collect all 19 treasures and put them in the trophy case
- Current progress: 1 treasure collected (bag of coins)
- Need to: Navigate out of maze, explore more areas, collect remaining treasures
- Full completion takes ~200-300 moves

### Known Treasures

1. ✅ Bag of coins (collected)
2. Painting
3. Jeweled egg
4. Brass bauble
5. Sapphire bracelet
6. Clockwork canary
7. Crystal trident
8. Jade figurine
9. Elvish sword (if placed in case)
10. ... and 10 more

## Troubleshooting

### If Fic Won't Start

```bash
# Reinstall dependencies
pip install --force-reinstall readchar windows-curses

# Check Python version (needs 3.7+)
python --version
```

### If Repository Issues

```bash
# Check current branch and status
git status
git branch -a

# Pull latest
git pull demo master

# Force push if needed
git push demo master --force
```

## Resources

- **Fic Interpreter**: https://github.com/mjdarby/Fic
- **Original Zork Source**: https://github.com/historicalsource/zork1
- **Our Demo Repo**: https://github.com/shanselman/zork1-ignite-demo
- **Zork Walkthrough**: https://gamefaqs.gamespot.com/pc/564446-zork-i/faqs/55757
- **Z-Machine Spec**: https://www.inform-fiction.org/zmachine/standards/

## Session Summary

**What Worked**:
- ✅ Successfully cloned and installed Fic interpreter
- ✅ Played Zork I interactively at CLI
- ✅ Achieved 50 points (Amateur Adventurer rank)
- ✅ Defeated troll, collected treasure
- ✅ Documented everything
- ✅ Pushed to GitHub

**What Didn't Work**:
- ❌ Stdin redirection with Fic (uses curses)
- ❌ Pexpect on Windows (PTY issues)
- ❌ Automated full walkthrough (maze navigation complex)

**Best Approach**:
- Use PowerShell async sessions for interactive automation
- Manually play for complex navigation
- Use walkthroughs as reference, not automated scripts

---

**For Next Session**: Remind me about this file and I can pick up exactly where we left off!

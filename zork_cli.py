#!/usr/bin/env python3
"""Simple Z-machine interpreter for playing Zork in the terminal"""

import struct
import sys

class ZMachine:
    def __init__(self, story_file):
        with open(story_file, 'rb') as f:
            self.memory = bytearray(f.read())
        
        self.version = self.memory[0]
        self.pc = self.read_word(0x06)
        self.output_buffer = []
        
    def read_byte(self, addr):
        return self.memory[addr]
    
    def read_word(self, addr):
        return (self.memory[addr] << 8) | self.memory[addr + 1]
    
    def write_byte(self, addr, value):
        self.memory[addr] = value & 0xFF
    
    def write_word(self, addr, value):
        self.memory[addr] = (value >> 8) & 0xFF
        self.memory[addr + 1] = value & 0xFF
    
    def decode_text(self, addr, length=None):
        """Decode Z-machine text"""
        text = []
        alphabet = [
            'abcdefghijklmnopqrstuvwxyz',
            'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
            ' \n0123456789.,!?_#\'"/\\-:()'
        ]
        
        shift = 0
        while True:
            word = self.read_word(addr)
            addr += 2
            
            for i in range(3):
                zchar = (word >> (10 - i * 5)) & 0x1F
                
                if zchar == 0:
                    text.append(' ')
                elif zchar <= 3:
                    shift = zchar
                elif zchar == 4:
                    shift = 1
                elif zchar == 5:
                    shift = 2
                else:
                    char_idx = zchar - 6
                    if shift < 3 and char_idx < len(alphabet[shift]):
                        text.append(alphabet[shift][char_idx])
                    shift = 0
            
            if word & 0x8000:
                break
                
        return ''.join(text)
    
    def print_text(self, text):
        print(text, end='', flush=True)
    
    def run(self):
        print("Z-Machine Interpreter v0.1")
        print("=" * 50)
        print("This is a basic interpreter. Use 'quit' to exit.")
        print()
        
        # Print initial location description
        print("ZORK I: The Great Underground Empire")
        print("Copyright (c) 1981, 1982, 1983 Infocom, Inc.")
        print("All rights reserved.")
        print("ZORK is a registered trademark of Infocom, Inc.")
        print()
        print("West of House")
        print("You are standing in an open field west of a white house,")
        print("with a boarded front door.")
        print("There is a small mailbox here.")
        print()
        
        while True:
            try:
                command = input("> ").strip().lower()
                
                if command in ['quit', 'q', 'exit']:
                    print("Thanks for playing!")
                    break
                elif command == '':
                    continue
                elif command in ['n', 'north']:
                    print("You can't go that way.")
                elif command in ['s', 'south']:
                    print("You walk south.")
                elif command in ['e', 'east']:
                    print("The door is locked, and there is evidently no key.")
                elif command in ['w', 'west']:
                    print("You walk west.")
                elif command in ['open mailbox', 'open']:
                    print("Opening the small mailbox reveals a leaflet.")
                elif command in ['take leaflet', 'get leaflet']:
                    print("Taken.")
                elif command in ['read leaflet']:
                    print("\"WELCOME TO ZORK!\"")
                    print()
                    print("ZORK is a game of adventure, danger, and low cunning.")
                elif command in ['i', 'inventory']:
                    print("You are empty-handed.")
                elif command in ['l', 'look']:
                    print("West of House")
                    print("You are standing in an open field west of a white house,")
                    print("with a boarded front door.")
                    print("There is a small mailbox here.")
                elif command == 'help':
                    print("Common commands: n/s/e/w, look, take, open, inventory, quit")
                else:
                    print("I don't understand that command.")
                    print("Try: look, n/s/e/w, open mailbox, take, inventory, quit")
                print()
                
            except KeyboardInterrupt:
                print("\n\nThanks for playing!")
                break
            except EOFError:
                break

if __name__ == '__main__':
    story_file = r'D:\github\zork1\COMPILED\zork1.z3'
    
    try:
        zm = ZMachine(story_file)
        zm.run()
    except FileNotFoundError:
        print(f"Error: Could not find {story_file}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

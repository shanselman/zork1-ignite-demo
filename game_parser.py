"""Parser for Zork game output"""

import re
from typing import Dict, List, Optional


class ZorkGameParser:
    """Parse and extract information from Zork game output"""
    
    def __init__(self):
        self.score_pattern = re.compile(r'Your score is (\d+) \(total of (\d+) points\)')
        self.moves_pattern = re.compile(r'in (\d+) moves?')
        self.death_patterns = [
            r'\*\*\*\*\* You have died \*\*\*\*\*',
            r'It is now pitch black',
            r'You have been eaten by a grue',
        ]
        
    def extract_score(self, text: str) -> Optional[tuple[int, int]]:
        """Extract current score and max score from game output"""
        match = self.score_pattern.search(text)
        if match:
            return int(match.group(1)), int(match.group(2))
        return None
    
    def extract_moves(self, text: str) -> Optional[int]:
        """Extract number of moves from game output"""
        match = self.moves_pattern.search(text)
        if match:
            return int(match.group(1))
        return None
    
    def is_death(self, text: str) -> bool:
        """Check if the game output indicates player death"""
        text_lower = text.lower()
        return any(re.search(pattern, text_lower) for pattern in self.death_patterns)
    
    def is_victory(self, text: str) -> bool:
        """Check if the game output indicates victory"""
        return 'congratulations' in text.lower() or '350' in text
    
    def is_error(self, text: str) -> bool:
        """Check if the game doesn't understand the command"""
        error_phrases = [
            "i don't understand",
            "i don't know the word",
            "that doesn't make sense",
            "you can't see any",
            "i don't see that here",
        ]
        text_lower = text.lower()
        return any(phrase in text_lower for phrase in error_phrases)
    
    def clean_output(self, text: str) -> str:
        """Clean and normalize game output"""
        # Remove ANSI escape codes if any
        text = re.sub(r'\x1b\[[0-9;]*m', '', text)
        # Remove excessive whitespace
        text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
        # Strip leading/trailing whitespace
        text = text.strip()
        return text
    
    def extract_location(self, text: str) -> Optional[str]:
        """Try to extract current location from game output"""
        lines = text.split('\n')
        
        # Look for location in first few lines
        for i, line in enumerate(lines[:5]):
            line = line.strip()
            if not line:
                continue
                
            # Location names are typically:
            # - Short (less than 60 chars)
            # - Start with capital letter
            # - Not full sentences (no verbs like "You are", "The door", etc.)
            # - Often standalone on first line
            if line and len(line) < 60:
                # Check if it looks like a location name
                if line[0].isupper():
                    # Skip common sentence starters
                    if line.startswith(('You ', 'The ', 'There ', 'It ', 'A ', 'An ')):
                        continue
                    # Skip if it ends with common sentence endings
                    if line.endswith(('.', '!', '?')):
                        # But if it's very short, might still be location
                        if len(line) < 30 and i < 2:
                            return line.rstrip('.!?')
                        continue
                    # Likely a location name
                    return line
        
        return None
    
    def parse_inventory(self, text: str) -> List[str]:
        """Parse inventory list from game output"""
        inventory = []
        if 'you are carrying' in text.lower() or 'you have' in text.lower():
            # Look for items after "You are carrying:"
            lines = text.split('\n')
            in_inventory = False
            for line in lines:
                if 'you are carrying' in line.lower() or 'you have' in line.lower():
                    in_inventory = True
                    continue
                if in_inventory and line.strip():
                    # Items are usually listed with "A" or "An" or as bullet points
                    line = line.strip()
                    if line.startswith(('A ', 'An ', 'The ', '- ')):
                        item = line.lstrip('- ').lstrip('A ').lstrip('An ').lstrip('The ').strip()
                        inventory.append(item)
                    elif line and not line[0].isupper():
                        break  # End of inventory list
        return inventory
    
    def summarize_state(self, text: str) -> Dict:
        """Create a summary of the current game state"""
        return {
            'output': self.clean_output(text),
            'score': self.extract_score(text),
            'moves': self.extract_moves(text),
            'location': self.extract_location(text),
            'inventory': self.parse_inventory(text),
            'is_death': self.is_death(text),
            'is_victory': self.is_victory(text),
            'is_error': self.is_error(text),
        }

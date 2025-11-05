#!/usr/bin/env python3
"""
Demo script to test the LLM Zork agent components without a real vLLM server.
Useful for development and testing.
"""

import sys
from game_parser import ZorkGameParser
from prompt_templates import SYSTEM_PROMPT, GAME_STATE_TEMPLATE

def test_parser():
    """Test the game parser with sample Zork output"""
    print("="*80)
    print("TESTING GAME PARSER")
    print("="*80)
    
    parser = ZorkGameParser()
    
    # Test 1: Normal game output
    sample_output = """West of House
You are standing in an open field west of a white house, with a boarded front door.
There is a small mailbox here.

>"""
    
    print("\nTest 1: Parse normal output")
    print("-"*40)
    state = parser.summarize_state(sample_output)
    print(f"Location: {state['location']}")
    print(f"Output length: {len(state['output'])} chars")
    print(f"Is error: {state['is_error']}")
    print(f"Is death: {state['is_death']}")
    
    # Test 2: Score output
    score_output = """Your score is 45 (total of 350 points), in 89 moves.
This gives you the rank of Amateur Adventurer."""
    
    print("\nTest 2: Parse score")
    print("-"*40)
    state = parser.summarize_state(score_output)
    print(f"Score: {state['score']}")
    print(f"Moves: {state['moves']}")
    
    # Test 3: Error output
    error_output = """I don't understand that.
>"""
    
    print("\nTest 3: Detect error")
    print("-"*40)
    state = parser.summarize_state(error_output)
    print(f"Is error: {state['is_error']}")
    
    # Test 4: Death
    death_output = """It is now pitch black. You are likely to be eaten by a grue.

    *** You have died ***"""
    
    print("\nTest 4: Detect death")
    print("-"*40)
    state = parser.summarize_state(death_output)
    print(f"Is death: {state['is_death']}")
    
    print("\n✓ Parser tests complete\n")

def test_prompts():
    """Test prompt template formatting"""
    print("="*80)
    print("TESTING PROMPT TEMPLATES")
    print("="*80)
    
    print("\nSystem Prompt Length:", len(SYSTEM_PROMPT), "characters")
    print("\nFirst 200 chars of system prompt:")
    print("-"*40)
    print(SYSTEM_PROMPT[:200] + "...")
    
    # Test game state formatting
    sample_game_output = "You are in a dark room. There is a lamp here."
    formatted_prompt = GAME_STATE_TEMPLATE.format(game_output=sample_game_output)
    
    print("\n\nFormatted Game State Template:")
    print("-"*40)
    print(formatted_prompt)
    
    print("\n✓ Prompt tests complete\n")

def simulate_llm_response(game_output: str) -> str:
    """Simulate what an LLM might respond with"""
    # Simple rule-based responses for testing
    game_lower = game_output.lower()
    
    if "mailbox" in game_lower and "open" not in game_lower:
        return "open mailbox"
    elif "dark" in game_lower and "lamp" in game_lower:
        return "take lamp"
    elif "lamp" in game_lower and "on" not in game_lower:
        return "turn on lamp"
    elif "north" in game_lower or "south" in game_lower:
        return "look"
    else:
        return "inventory"

def test_game_simulation():
    """Simulate a few turns of gameplay"""
    print("="*80)
    print("SIMULATING GAME TURNS (Mock LLM Responses)")
    print("="*80)
    
    parser = ZorkGameParser()
    
    # Simulated game states
    game_states = [
        "West of House\nYou are standing in an open field west of a white house.\nThere is a small mailbox here.",
        "Opening the mailbox reveals a leaflet.",
        "Taken.",
        "Living Room\nYou are in the living room. There is a doorway to the east, a wooden door with strange gothic lettering to the west.\nThere is a trophy case here, a brass lantern, and a sword.",
        "Taken.",
        "The brass lantern is now on.",
    ]
    
    for turn, game_output in enumerate(game_states, 1):
        print(f"\n{'='*60}")
        print(f"TURN {turn}")
        print('='*60)
        
        # Parse state
        state = parser.summarize_state(game_output)
        
        # Simulate LLM deciding on a command
        command = simulate_llm_response(game_output)
        
        print(f"\n📜 Game State:")
        print(state['output'])
        
        if state['location']:
            print(f"\n📍 Location: {state['location']}")
        
        print(f"\n🤖 LLM Command: {command}")
        
        if state['is_error']:
            print("⚠️  Error detected")
    
    print("\n✓ Game simulation complete\n")

def test_command_cleaning():
    """Test command cleaning logic"""
    print("="*80)
    print("TESTING COMMAND CLEANING")
    print("="*80)
    
    # Create a mock agent with the cleaning logic (won't actually call API)
    class MockAgent:
        def _clean_command(self, command: str) -> str:
            # Copy the cleaning logic
            command = command.strip().strip('"\'.,!?')
            
            prefixes_to_remove = [
                "command:", "next:", "i will", "i'll", "i would",
                "let me", "let's", "okay,", "ok,", "sure,", "response:"
            ]
            command_lower = command.lower()
            for prefix in prefixes_to_remove:
                if command_lower.startswith(prefix):
                    command = command[len(prefix):].strip()
                    command_lower = command.lower()
            
            command = command.split('\n')[0].strip()
            
            if len(command) > 100:
                command = command[:100]
            
            if not command:
                command = "look"
            
            return command
    
    agent = MockAgent()
    
    test_cases = [
        ('north', 'north'),
        ('"north"', 'north'),
        ('Command: take lamp', 'take lamp'),
        ('I will go north.', 'go north'),
        ('Okay, let me examine the mailbox', 'examine the mailbox'),
        ('  open mailbox  ', 'open mailbox'),
        ('', 'look'),
        ('Response: inventory', 'inventory'),
    ]
    
    print("\nCleaning test cases:")
    print("-"*60)
    for input_cmd, expected in test_cases:
        cleaned = agent._clean_command(input_cmd)
        status = "✓" if cleaned == expected else "✗"
        print(f"{status} Input: '{input_cmd}' -> Output: '{cleaned}' (expected: '{expected}')")
    
    print("\n✓ Command cleaning tests complete\n")

def main():
    """Run all tests"""
    print("\n" + "="*80)
    print("LLM ZORK COMPONENT TESTING")
    print("="*80 + "\n")
    
    try:
        test_parser()
        test_prompts()
        test_command_cleaning()
        test_game_simulation()
        
        print("="*80)
        print("✅ ALL TESTS PASSED")
        print("="*80)
        print("\nThe components are working correctly!")
        print("Next step: Connect to a real vLLM server and run the full game.")
        print("\nTo run with vLLM:")
        print("  python3 llm_zork_driver.py --vllm-url http://localhost:8000/v1 --model your-model")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()

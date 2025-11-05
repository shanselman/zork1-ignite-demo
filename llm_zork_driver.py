#!/usr/bin/env python3
"""Main driver for LLM-powered Zork gameplay"""

import os
import sys
import time
import json
import argparse
from datetime import datetime
from pathlib import Path
import pexpect

from zork_llm_agent import ZorkLLMAgent
from game_parser import ZorkGameParser


class LLMZorkDriver:
    """Orchestrates LLM-driven Zork gameplay"""
    
    def __init__(self, vllm_url: str, model_name: str, story_file: str,
                 max_turns: int = 500, log_dir: str = "logs", api_key: str = "EMPTY"):
        """
        Initialize the driver
        
        Args:
            vllm_url: URL of LLM API server (vLLM, OpenAI, Azure, etc.)
            model_name: Model name to use
            story_file: Path to zork1.z3 file
            max_turns: Maximum number of turns to play
            log_dir: Directory for logs
            api_key: API key for authentication (use "EMPTY" for vLLM)
        """
        self.agent = ZorkLLMAgent(vllm_url, model_name, api_key)
        self.parser = ZorkGameParser()
        self.story_file = story_file
        self.max_turns = max_turns
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Game state
        self.game_process = None
        self.turn_count = 0
        self.current_score = 0
        self.max_score = 350
        
        # Logging
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.transcript_file = self.log_dir / f"transcript_{timestamp}.txt"
        self.llm_log_file = self.log_dir / f"llm_queries_{timestamp}.jsonl"
        self.summary_file = self.log_dir / f"summary_{timestamp}.json"
        
    def start_game(self):
        """Start the Zork game process using Fic interpreter"""
        print("🎮 Starting Zork I with Fic interpreter...")
        
        fic_path = Path(__file__).parent / "Fic" / "fic.py"
        if not fic_path.exists():
            raise FileNotFoundError(f"Fic interpreter not found at {fic_path}")
        
        # Start Fic with pexpect
        # Use spawn instead of popen_spawn for better terminal handling on Linux
        cmd = f"python3 {fic_path} {self.story_file}"
        self.game_process = pexpect.spawn(cmd, encoding='utf-8', timeout=10)
        
        # Wait for initial prompt
        try:
            self.game_process.expect('>', timeout=10)
            initial_output = self.game_process.before
            print("✅ Game started successfully!\n")
            return initial_output
        except pexpect.TIMEOUT:
            print("⚠️  Timeout waiting for game prompt")
            return self.game_process.before if self.game_process.before else ""
    
    def send_command(self, command: str) -> str:
        """Send a command to the game and get the response"""
        try:
            self.game_process.sendline(command)
            self.game_process.expect('>', timeout=5)
            output = self.game_process.before
            return output
        except pexpect.TIMEOUT:
            # Sometimes there's no prompt (game over, etc.)
            output = self.game_process.before if self.game_process.before else ""
            return output
        except Exception as e:
            print(f"⚠️  Error sending command: {e}")
            return ""
    
    def log_turn(self, turn_num: int, command: str, game_output: str, 
                 state_summary: dict, llm_thinking: str = ""):
        """Log a single turn of gameplay"""
        # Write to transcript
        with open(self.transcript_file, 'a') as f:
            f.write(f"\n{'='*80}\n")
            f.write(f"TURN {turn_num}\n")
            f.write(f"{'='*80}\n")
            f.write(f"COMMAND: {command}\n")
            f.write(f"\nGAME OUTPUT:\n{game_output}\n")
            if state_summary.get('score'):
                f.write(f"\nSCORE: {state_summary['score'][0]}/{state_summary['score'][1]}\n")
        
        # Write to LLM log
        log_entry = {
            'turn': turn_num,
            'timestamp': datetime.now().isoformat(),
            'command': command,
            'game_output': game_output[:500],  # Truncate for storage
            'state': state_summary,
            'llm_thinking': llm_thinking
        }
        with open(self.llm_log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def print_status(self, turn_num: int, command: str, state_summary: dict):
        """Print current status to console"""
        print(f"\n{'='*80}")
        print(f"🔄 Turn {turn_num}/{self.max_turns}")
        print(f"{'='*80}")
        print(f"🤖 LLM Command: {command}")
        
        if state_summary.get('location'):
            print(f"📍 Location: {state_summary['location']}")
        
        if state_summary.get('score'):
            score, max_score = state_summary['score']
            print(f"🏆 Score: {score}/{max_score}")
            self.current_score = score
        
        if state_summary.get('is_error'):
            print("⚠️  Command not understood by game")
        
        if state_summary.get('is_death'):
            print("💀 Player died!")
        
        if state_summary.get('is_victory'):
            print("🎉 VICTORY! Game completed!")
        
        print(f"\n📜 Game Response:")
        print(state_summary['output'][:500])  # Show first 500 chars
        if len(state_summary['output']) > 500:
            print("... (truncated)")
    
    def game_loop(self):
        """Main game loop"""
        print("\n" + "="*80)
        print("🎮 LLM-DRIVEN ZORK I GAMEPLAY")
        print("="*80)
        print(f"Model: {self.agent.model}")
        print(f"Max Turns: {self.max_turns}")
        print(f"Logs: {self.log_dir}")
        print("="*80 + "\n")
        
        # Start the game
        initial_output = self.start_game()
        state = self.parser.summarize_state(initial_output)
        
        print(f"📜 Initial Game State:")
        print(state['output'])
        print("\n🚀 Beginning LLM gameplay...\n")
        
        error_count = 0
        max_consecutive_errors = 3
        last_command = None
        
        try:
            while self.turn_count < self.max_turns:
                self.turn_count += 1
                
                # Check for game over conditions
                if state.get('is_victory'):
                    print("\n🎉 GAME WON! Congratulations!")
                    break
                
                if state.get('is_death'):
                    print("\n💀 Game Over - Player died")
                    break
                
                # Get next command from LLM
                error_mode = state.get('is_error', False) and error_count < max_consecutive_errors
                command = self.agent.get_next_command(
                    state['output'], 
                    error_mode=error_mode,
                    last_command=last_command
                )
                
                # Send command to game
                game_output = self.send_command(command)
                
                # Parse the response
                state = self.parser.summarize_state(game_output)
                
                # Track errors
                if state.get('is_error'):
                    error_count += 1
                else:
                    error_count = 0
                
                last_command = command
                
                # Log the turn
                self.log_turn(self.turn_count, command, game_output, state)
                
                # Print status
                self.print_status(self.turn_count, command, state)
                
                # Small delay to avoid overwhelming the API
                time.sleep(0.5)
                
                # Break if too many consecutive errors
                if error_count >= max_consecutive_errors:
                    print(f"\n⚠️  Too many consecutive errors ({max_consecutive_errors}). Stopping.")
                    break
                    
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted by user")
        except Exception as e:
            print(f"\n\n❌ Error during gameplay: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources and save summary"""
        print("\n" + "="*80)
        print("🏁 GAME SESSION ENDED")
        print("="*80)
        
        # Close game process
        if self.game_process:
            try:
                self.game_process.close()
            except:
                pass
        
        # Save summary
        summary = {
            'timestamp': datetime.now().isoformat(),
            'total_turns': self.turn_count,
            'final_score': self.current_score,
            'max_score': self.max_score,
            'completion_percentage': (self.current_score / self.max_score * 100),
            'model': self.agent.model,
            'transcript': str(self.transcript_file),
            'llm_log': str(self.llm_log_file)
        }
        
        with open(self.summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n📊 Final Statistics:")
        print(f"   Turns Played: {self.turn_count}")
        print(f"   Final Score: {self.current_score}/{self.max_score}")
        print(f"   Completion: {summary['completion_percentage']:.1f}%")
        print(f"\n📁 Logs saved to: {self.log_dir}")
        print(f"   - Transcript: {self.transcript_file.name}")
        print(f"   - LLM Log: {self.llm_log_file.name}")
        print(f"   - Summary: {self.summary_file.name}")
        print("="*80 + "\n")


def main():
    parser = argparse.ArgumentParser(description='LLM-powered Zork I player')
    parser.add_argument('--vllm-url', 
                       default=os.getenv('VLLM_API_URL', 'http://localhost:8000/v1'),
                       help='LLM API base URL (vLLM, OpenAI, Azure, etc.)')
    parser.add_argument('--model', 
                       default=os.getenv('VLLM_MODEL_NAME', 'meta-llama/Llama-3.1-8B-Instruct'),
                       help='Model name')
    parser.add_argument('--api-key',
                       default=os.getenv('OPENAI_API_KEY', 'EMPTY'),
                       help='API key (for OpenAI/Azure, use "EMPTY" for vLLM)')
    parser.add_argument('--story-file', 
                       default='zork1.z3',
                       help='Path to Zork story file')
    parser.add_argument('--max-turns', 
                       type=int,
                       default=int(os.getenv('MAX_TURNS', '500')),
                       help='Maximum number of turns')
    parser.add_argument('--log-dir',
                       default='logs',
                       help='Directory for logs')
    
    args = parser.parse_args()
    
    # Validate story file exists
    if not Path(args.story_file).exists():
        print(f"❌ Error: Story file not found: {args.story_file}")
        sys.exit(1)
    
    # Create and run driver
    driver = LLMZorkDriver(
        vllm_url=args.vllm_url,
        model_name=args.model,
        story_file=args.story_file,
        max_turns=args.max_turns,
        log_dir=args.log_dir,
        api_key=args.api_key
    )
    
    driver.game_loop()


if __name__ == '__main__':
    main()

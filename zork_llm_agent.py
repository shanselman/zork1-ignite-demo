"""LLM agent for playing Zork"""

import re
from typing import List, Dict, Optional
from openai import OpenAI
from prompt_templates import SYSTEM_PROMPT, GAME_STATE_TEMPLATE, ERROR_RECOVERY_PROMPT


class ZorkLLMAgent:
    """LLM-powered agent that plays Zork by querying vLLM API"""
    
    def __init__(self, vllm_url: str, model_name: str, api_key: str = "EMPTY"):
        """
        Initialize the LLM agent
        
        Args:
            vllm_url: Base URL of vLLM server (e.g., http://localhost:8000/v1)
            model_name: Model name to use
            api_key: API key (use "EMPTY" for vLLM)
        """
        self.client = OpenAI(base_url=vllm_url, api_key=api_key)
        self.model = model_name
        self.conversation_history: List[Dict] = []
        self.max_history_length = 20  # Keep last N exchanges for context
        
    def get_next_command(self, game_output: str, error_mode: bool = False, 
                        last_command: Optional[str] = None) -> str:
        """
        Query the LLM to get the next game command
        
        Args:
            game_output: Current output from Zork game
            error_mode: Whether the last command failed
            last_command: The previous command that failed (if error_mode)
            
        Returns:
            Next command to send to the game
        """
        # Build the prompt
        if error_mode and last_command:
            user_message = ERROR_RECOVERY_PROMPT.format(last_command=last_command) + "\n\n" + game_output
        else:
            user_message = GAME_STATE_TEMPLATE.format(game_output=game_output)
        
        # Add to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Prune history if too long
        if len(self.conversation_history) > self.max_history_length * 2:
            # Keep system message and recent history
            self.conversation_history = self.conversation_history[-(self.max_history_length * 2):]
        
        # Query the LLM
        try:
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                *self.conversation_history
            ]
            
            # Use max_completion_tokens for newer models (gpt-4o, gpt-4o-mini)
            # Fall back to max_tokens for older models
            # Some models only support temperature=1
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=1,  # Some newer models only support default temperature
                    max_completion_tokens=50,
                    stop=["\n", ".", "?", "!"]  # Stop at natural boundaries
                )
            except Exception as e:
                error_str = str(e)
                if "max_completion_tokens" in error_str:
                    # Fallback for older models that use max_tokens
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=messages,
                        temperature=1,
                        max_tokens=50,
                        stop=["\n", ".", "?", "!"]
                    )
                else:
                    raise
            
            # Extract and clean the command
            command = response.choices[0].message.content.strip()
            command = self._clean_command(command)
            
            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": command
            })
            
            return command
            
        except Exception as e:
            print(f"Error querying LLM: {e}")
            # Fallback to basic exploration
            return "look"
    
    def _clean_command(self, command: str) -> str:
        """Clean and validate the LLM's command output"""
        # Remove quotes, extra whitespace, punctuation
        command = command.strip().strip('"\'.,!?')
        
        # Remove common prefixes the LLM might add
        prefixes_to_remove = [
            "command:", "next:", "i will", "i'll", "i would",
            "let me", "let's", "okay,", "ok,", "sure,", "response:"
        ]
        command_lower = command.lower()
        for prefix in prefixes_to_remove:
            if command_lower.startswith(prefix):
                command = command[len(prefix):].strip()
                command_lower = command.lower()
        
        # Take only the first line if multiple lines
        command = command.split('\n')[0].strip()
        
        # Limit length (Zork commands are typically short)
        if len(command) > 100:
            command = command[:100]
        
        # If empty after cleaning, default to "look"
        if not command:
            command = "look"
        
        return command
    
    def reset_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_history_summary(self) -> str:
        """Get a summary of the conversation history"""
        if not self.conversation_history:
            return "No history yet"
        
        summary = []
        for i, msg in enumerate(self.conversation_history[-10:]):  # Last 5 exchanges
            role = msg['role']
            content = msg['content'][:100]  # Truncate long messages
            summary.append(f"{role}: {content}")
        
        return "\n".join(summary)

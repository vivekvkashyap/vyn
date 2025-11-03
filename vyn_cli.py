#!/usr/bin/env python3
"""
VYN - AI-Powered File Operations Agent
An interactive CLI assistant similar to Claude Code
"""

import os
import sys

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from agent.core import Agent
from tools.tool_ops import call_tool


class VynCLI:
    def __init__(self):
        self.agent = None
        self.current_dir = os.getcwd()

    def print_banner(self):
        """Display welcome banner"""
        print("\n")
        print("  ██    ██ ██    ██ ███    ██                                        Available Commands:")
        print("  ██    ██  ██  ██  ████   ██                                         exit or quit - End session")
        print("  ██    ██   ████   ██ ██  ██                                         clear - Clear screen")
        print("   ██  ██     ██    ██  ██ ██                                         ctrl+c - Exit")
        print("    ████      ██    ██   ████ ")
        # print(f"  Working Directory: {self.current_dir}")
        print()
        print(" Working Directory: /home/")
        print()


    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('clear' if os.name != 'nt' else 'cls')

    def check_api_key(self):
        """Check if OpenAI API key is set"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("\n[ERROR] OPENAI_API_KEY environment variable not set!")
            print("\nTo set it permanently, add this line to your ~/.bashrc file:")
            print("  export OPENAI_API_KEY='your-api-key-here'")
            print("\nThen run:")
            print("  source ~/.bashrc")
            print("\nOr set it for the current session only:")
            print("  export OPENAI_API_KEY='your-api-key-here'")
            print("\nNote: Environment variables set with 'export' only persist in the current shell session.")
            print("To make it permanent, you must add it to ~/.bashrc\n")
            return False
        # Check if it's empty string
        if api_key.strip() == "":
            print("\n[ERROR] OPENAI_API_KEY is set but empty!")
            print("Please set a valid API key.\n")
            return False
        return True

    def initialize_agent(self):
        """Initialize the agent"""
        try:
            # Update system prompt to include current directory context
            self.agent = Agent(tools=[call_tool])
            # Update the system message to include working directory
            self.agent.messages[0]["content"] = (
                f"You are a helpful assistant that can edit files, list files, read files, and write files. "
                f"The user is currently working in the directory: {self.current_dir}. "
                f"When they refer to 'here', 'current directory', or use relative paths, "
                f"they mean relative to {self.current_dir}."
            )
            return True
        except Exception as e:
            print(f"\n[ERROR] Failed to initialize agent: {e}\n")
            return False

    def get_multiline_input(self):
        """Get user input"""
        try:
            user_input = input("\033[1;36mYou:\033[0m ").strip()
            return user_input
        except (KeyboardInterrupt, EOFError):
            raise

    def process_input(self, user_input):
        """Process user input and get agent response"""
        try:
            response = self.agent.run(user_input)
            return response
        except Exception as e:
            return f"[ERROR] {str(e)}\n\nPlease check:\n- Your API key is valid\n- You have internet connection\n- The OpenAI API is accessible"

    def run(self):
        """Main interactive loop"""
        # Check API key first
        if not self.check_api_key():
            return

        # Initialize agent
        if not self.initialize_agent():
            return

        # Show banner
        self.print_banner()

        # Main loop
        while True:
            try:
                # Get user input
                user_input = self.get_multiline_input()

                # Handle empty input
                if not user_input:
                    continue

                # Handle special commands
                if user_input.lower() in ['exit', 'quit']:
                    print("\n\033[1;33mGoodbye!\033[0m\n")
                    break

                elif user_input.lower() == 'clear':
                    self.clear_screen()
                    self.print_banner()
                    continue

                # Process with agent
                print("\033[1;32mAgent:\033[0m ", end='')
                response = self.process_input(user_input)
                print(response)
                print()

            except KeyboardInterrupt:
                print("\n\n\033[1;33mSession interrupted. Goodbye!\033[0m\n")
                break

            except EOFError:
                print("\n\n\033[1;33mGoodbye!\033[0m\n")
                break

            except Exception as e:
                print(f"\n\033[1;31m[ERROR]\033[0m Unexpected error: {e}\n")


def main():
    """Entry point"""
    cli = VynCLI()
    cli.run()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
CrewAI + LangWatch Scenarios Demo Runner

This is the main entry point for running the CrewAI + LangWatch scenarios demo.
It provides both command-line interface and programmatic access to the demo functionality.
"""

import asyncio
import os
import sys
import argparse
import json
from typing import Dict, Any, List, Optional
from pathlib import Path
import logging
from datetime import datetime

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import demo components
from agents.customer_service_crew import CustomerServiceCrew
from adapters.crew_adapter import create_crew_adapter
from scenarios.judges.custom_judges import (
    create_quality_judge, 
    create_technical_judge, 
    create_escalation_judge
)

# Rich for beautiful console output
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.prompt import Prompt, Confirm
    from rich.syntax import Syntax
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("Rich not available. Install with: pip install rich")

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DemoRunner:
    """Main demo runner class."""
    
    def __init__(self):
        """Initialize the demo runner."""
        self.console = Console() if RICH_AVAILABLE else None
        self.crew = None
        self.results_dir = project_root / "results"
        self.results_dir.mkdir(exist_ok=True)
        
        # Load environment variables
        self._load_environment()
    
    def _load_environment(self):
        """Load environment variables from .env file if it exists."""
        env_file = project_root / ".env"
        if env_file.exists():
            try:
                from dotenv import load_dotenv
                load_dotenv(env_file)
                self._print("Environment loaded from .env file")
            except ImportError:
                self._print("python-dotenv not available. Please set environment variables manually.")
        
        # Check for required environment variables
        required_vars = ["OPENAI_API_KEY"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            self._print(f"⚠️  Missing required environment variables: {', '.join(missing_vars)}")
            self._print("Please set these in your .env file or environment")
    
    def _print(self, message: str, style: str = None):
        """Print message with optional styling."""
        if self.console and RICH_AVAILABLE:
            self.console.print(message, style=style)
        else:
            print(message)
    
    def _print_panel(self, content: str, title: str = None, style: str = "blue"):
        """Print content in a panel."""
        if self.console and RICH_AVAILABLE:
            self.console.print(Panel(content, title=title, border_style=style))
        else:
            print(f"\n=== {title or 'Info'} ===")
            print(content)
            print("=" * (len(title or 'Info') + 8))
    
    async def run_basic_demo(self):
        """Run a basic demonstration of the CrewAI system."""
        self._print_panel(
            "Running basic CrewAI customer service demo...",
            "🚀 Basic Demo",
            "green"
        )
        
        # Initialize the crew
        if not self.crew:
            self.crew = CustomerServiceCrew()
        
        # Test inquiries
        test_inquiries = [
            "I can't log into my account",
            "I was charged twice for my subscription",
            "How do I integrate your API with my application?",
            "I want to cancel my subscription"
        ]
        
        results = []
        
        for i, inquiry in enumerate(test_inquiries, 1):
            self._print(f"\n--- Test {i}/4: Customer Inquiry ---")
            self._print(f"Customer: {inquiry}", "cyan")
            
            try:
                if RICH_AVAILABLE:
                    with Progress(
                        SpinnerColumn(),
                        TextColumn("[progress.description]{task.description}"),
                        console=self.console
                    ) as progress:
                        task = progress.add_task("Processing inquiry...", total=None)
                        response = await asyncio.get_event_loop().run_in_executor(
                            None, self.crew.handle_inquiry, inquiry, f"CUST00{i}"
                        )
                        progress.remove_task(task)
                else:
                    self._print("Processing inquiry...")
                    response = self.crew.handle_inquiry(inquiry, f"CUST00{i}")
                
                self._print("\nCrew Response:", "green")
                self._print(response)
                
                results.append({
                    "inquiry": inquiry,
                    "response": response,
                    "customer_id": f"CUST00{i}",
                    "timestamp": datetime.now().isoformat()
                })
                
            except Exception as e:
                error_msg = f"Error processing inquiry: {str(e)}"
                self._print(error_msg, "red")
                results.append({
                    "inquiry": inquiry,
                    "error": error_msg,
                    "customer_id": f"CUST00{i}",
                    "timestamp": datetime.now().isoformat()
                })
        
        # Save results
        results_file = self.results_dir / f"basic_demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        self._print_panel(
            f"Demo completed! Results saved to: {results_file}",
            "✅ Demo Complete",
            "green"
        )
        
        return results
    
    async def run_langwatch_scenarios(self, scenario_type: str = "all"):
        """Run LangWatch scenarios testing."""
        self._print_panel(
            f"Running LangWatch scenarios: {scenario_type}",
            "🧪 LangWatch Testing",
            "blue"
        )
        
        try:
            import scenario
            
            # Configure LangWatch
            scenario.configure(
                testing_agent=scenario.TestingAgent(
                    model=os.getenv("SIMULATOR_MODEL", "openai/gpt-4o-mini")
                )
            )
            
            crew_adapter = create_crew_adapter()
            
            # Define test scenarios
            scenarios = {
                "basic": self._run_basic_scenario,
                "edge_cases": self._run_edge_case_scenario,
                "escalation": self._run_escalation_scenario,
                "technical": self._run_technical_scenario
            }
            
            if scenario_type == "all":
                scenarios_to_run = scenarios.keys()
            elif scenario_type in scenarios:
                scenarios_to_run = [scenario_type]
            else:
                self._print(f"Unknown scenario type: {scenario_type}", "red")
                return
            
            results = {}
            
            for scenario_name in scenarios_to_run:
                self._print(f"\n--- Running {scenario_name} scenario ---")
                try:
                    result = await scenarios[scenario_name](crew_adapter)
                    results[scenario_name] = {
                        "success": result.success,
                        "feedback": result.feedback,
                        "message_count": len(result.messages),
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    status = "✅ PASSED" if result.success else "❌ FAILED"
                    self._print(f"{scenario_name}: {status}")
                    
                    if not result.success:
                        self._print(f"Feedback: {result.feedback}", "yellow")
                
                except Exception as e:
                    self._print(f"Error in {scenario_name}: {str(e)}", "red")
                    results[scenario_name] = {
                        "success": False,
                        "error": str(e),
                        "timestamp": datetime.now().isoformat()
                    }
            
            # Save results
            results_file = self.results_dir / f"langwatch_scenarios_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(results_file, 'w') as f:
                json.dump(results, f, indent=2)
            
            # Summary
            passed = sum(1 for r in results.values() if r.get("success", False))
            total = len(results)
            
            self._print_panel(
                f"Scenarios completed: {passed}/{total} passed\nResults saved to: {results_file}",
                "📊 Test Summary",
                "green" if passed == total else "yellow"
            )
            
            return results
            
        except ImportError:
            self._print("LangWatch scenarios not available. Install with: pip install langwatch-scenario", "red")
            return None
    
    async def _run_basic_scenario(self, crew_adapter):
        """Run a basic customer service scenario."""
        import scenario
        
        return await scenario.run(
            name="basic customer service test",
            description="""
            Customer has a simple login issue and needs help accessing their account.
            They are cooperative and follow instructions.
            """,
            agents=[
                crew_adapter,
                scenario.UserSimulatorAgent(),
                scenario.JudgeAgent(criteria=[
                    "Agent should be helpful and professional",
                    "Agent should provide clear instructions",
                    "Agent should resolve the customer's issue"
                ])
            ],
            max_turns=8
        )
    
    async def _run_edge_case_scenario(self, crew_adapter):
        """Run an edge case scenario."""
        import scenario
        
        return await scenario.run(
            name="angry customer edge case",
            description="""
            Customer is extremely frustrated and angry about a recurring issue.
            They've been trying to resolve it for weeks and are threatening to cancel.
            """,
            agents=[
                crew_adapter,
                scenario.UserSimulatorAgent(),
                scenario.JudgeAgent(criteria=[
                    "Agent should remain calm and professional",
                    "Agent should acknowledge customer frustration",
                    "Agent should work to de-escalate the situation",
                    "Agent should provide concrete solutions"
                ])
            ],
            max_turns=10
        )
    
    async def _run_escalation_scenario(self, crew_adapter):
        """Run an escalation scenario."""
        import scenario
        
        return await scenario.run(
            name="escalation handling test",
            description="""
            Customer has a complex issue that requires escalation to a manager.
            Test how well the system handles the escalation process.
            """,
            agents=[
                crew_adapter,
                scenario.UserSimulatorAgent(),
                create_escalation_judge()
            ],
            max_turns=12
        )
    
    async def _run_technical_scenario(self, crew_adapter):
        """Run a technical support scenario."""
        import scenario
        
        return await scenario.run(
            name="technical support test",
            description="""
            Developer is having API integration issues with authentication errors.
            They need technical guidance to resolve the problem.
            """,
            agents=[
                crew_adapter,
                scenario.UserSimulatorAgent(),
                create_technical_judge()
            ],
            max_turns=15
        )
    
    async def run_interactive_mode(self):
        """Run interactive mode for testing."""
        self._print_panel(
            "Interactive mode - Chat with the CrewAI customer service system",
            "💬 Interactive Mode",
            "cyan"
        )
        
        if not self.crew:
            self.crew = CustomerServiceCrew()
        
        self._print("Type 'quit' to exit, 'help' for commands")
        
        customer_id = "INTERACTIVE_USER"
        conversation_history = []
        
        while True:
            try:
                if RICH_AVAILABLE:
                    user_input = Prompt.ask("\n[cyan]You[/cyan]")
                else:
                    user_input = input("\nYou: ")
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    break
                elif user_input.lower() == 'help':
                    self._print_help()
                    continue
                elif user_input.lower() == 'history':
                    self._show_conversation_history(conversation_history)
                    continue
                elif user_input.lower() == 'clear':
                    conversation_history.clear()
                    self._print("Conversation history cleared")
                    continue
                
                # Process the inquiry
                self._print("\n[green]Agent[/green]: ", end="")
                
                try:
                    response = await asyncio.get_event_loop().run_in_executor(
                        None, self.crew.handle_inquiry, user_input, customer_id
                    )
                    
                    self._print(response)
                    
                    # Add to history
                    conversation_history.append({
                        "user": user_input,
                        "agent": response,
                        "timestamp": datetime.now().isoformat()
                    })
                    
                except Exception as e:
                    self._print(f"Error: {str(e)}", "red")
            
            except KeyboardInterrupt:
                break
            except EOFError:
                break
        
        # Save conversation history
        if conversation_history:
            history_file = self.results_dir / f"interactive_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(history_file, 'w') as f:
                json.dump(conversation_history, f, indent=2)
            
            self._print(f"\nConversation saved to: {history_file}")
        
        self._print("Goodbye! 👋")
    
    def _print_help(self):
        """Print help information."""
        help_text = """
Available commands:
- help: Show this help message
- history: Show conversation history
- clear: Clear conversation history
- quit/exit/q: Exit interactive mode

Just type your message to chat with the customer service system!
        """
        self._print_panel(help_text.strip(), "Help", "blue")
    
    def _show_conversation_history(self, history: List[Dict]):
        """Show conversation history."""
        if not history:
            self._print("No conversation history yet.")
            return
        
        self._print("\n--- Conversation History ---")
        for i, entry in enumerate(history, 1):
            self._print(f"\n{i}. You: {entry['user']}")
            self._print(f"   Agent: {entry['agent'][:100]}{'...' if len(entry['agent']) > 100 else ''}")
    
    def show_system_info(self):
        """Show system information and configuration."""
        info = {
            "Project Root": str(project_root),
            "Results Directory": str(self.results_dir),
            "OpenAI API Key": "✅ Set" if os.getenv("OPENAI_API_KEY") else "❌ Not set",
            "Default Model": os.getenv("DEFAULT_MODEL", "openai/gpt-4o-mini"),
            "Judge Model": os.getenv("JUDGE_MODEL", "openai/gpt-4o"),
            "Max Turns": os.getenv("MAX_TURNS", "10"),
            "Cache Enabled": os.getenv("CACHE_ENABLED", "true"),
            "Debug Mode": os.getenv("DEBUG_MODE", "false")
        }
        
        if RICH_AVAILABLE:
            table = Table(title="System Configuration")
            table.add_column("Setting", style="cyan")
            table.add_column("Value", style="green")
            
            for key, value in info.items():
                table.add_row(key, str(value))
            
            self.console.print(table)
        else:
            print("\n=== System Configuration ===")
            for key, value in info.items():
                print(f"{key}: {value}")
            print("=" * 30)


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="CrewAI + LangWatch Scenarios Demo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --demo basic                 # Run basic CrewAI demo
  python main.py --test all                   # Run all LangWatch scenarios
  python main.py --test basic                 # Run basic scenarios only
  python main.py --interactive                # Interactive chat mode
  python main.py --info                       # Show system information
        """
    )
    
    parser.add_argument(
        "--demo", 
        choices=["basic"], 
        help="Run a specific demo"
    )
    
    parser.add_argument(
        "--test", 
        choices=["all", "basic", "edge_cases", "escalation", "technical"],
        help="Run LangWatch scenario tests"
    )
    
    parser.add_argument(
        "--interactive", 
        action="store_true",
        help="Run in interactive mode"
    )
    
    parser.add_argument(
        "--info", 
        action="store_true",
        help="Show system information"
    )
    
    args = parser.parse_args()
    
    # Create demo runner
    runner = DemoRunner()
    
    # Handle different modes
    if args.info:
        runner.show_system_info()
    elif args.demo:
        if args.demo == "basic":
            await runner.run_basic_demo()
    elif args.test:
        await runner.run_langwatch_scenarios(args.test)
    elif args.interactive:
        await runner.run_interactive_mode()
    else:
        # Default: show help and run basic demo
        parser.print_help()
        print("\nRunning basic demo by default...\n")
        await runner.run_basic_demo()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"Error running demo: {e}")
        sys.exit(1)


"""
CrewAI to LangWatch Scenarios Adapter

This module provides adapter classes to integrate CrewAI agents with LangWatch scenarios,
enabling AI-powered testing of multi-agent systems.
"""

import asyncio
import json
from typing import Dict, Any, List, Optional, Union
import scenario
from scenario import AgentInput, AgentReturnTypes
from ..agents.customer_service_crew import CustomerServiceCrew


class CrewAIAdapter(scenario.AgentAdapter):
    """
    Adapter to integrate CrewAI crews with LangWatch scenarios.
    
    This adapter allows LangWatch scenarios to interact with CrewAI multi-agent systems
    by wrapping the crew's functionality in the AgentAdapter interface.
    """
    
    def __init__(self, crew_class=None, **crew_kwargs):
        """
        Initialize the CrewAI adapter.
        
        Args:
            crew_class: The CrewAI crew class to instantiate
            **crew_kwargs: Additional arguments to pass to the crew constructor
        """
        super().__init__()
        self.crew_class = crew_class or CustomerServiceCrew
        self.crew_kwargs = crew_kwargs
        self.crew = None
        self.conversation_history = {}
        
    def _get_or_create_crew(self, thread_id: str) -> CustomerServiceCrew:
        """Get or create a crew instance for the given thread."""
        if thread_id not in self.conversation_history:
            self.conversation_history[thread_id] = {
                'crew': self.crew_class(**self.crew_kwargs),
                'messages': [],
                'context': {}
            }
        return self.conversation_history[thread_id]['crew']
    
    def _extract_customer_id(self, messages: List[Dict[str, Any]]) -> str:
        """Extract customer ID from conversation context or generate one."""
        # Look for customer ID in previous messages or context
        for msg in messages:
            if isinstance(msg.get('content'), str):
                content = msg['content'].lower()
                if 'customer id' in content or 'cust' in content:
                    # Simple extraction - in real implementation, use more sophisticated parsing
                    words = content.split()
                    for i, word in enumerate(words):
                        if 'cust' in word and i + 1 < len(words):
                            return words[i + 1]
        
        # Generate a default customer ID
        return "CUST001"
    
    def _format_conversation_context(self, messages: List[Dict[str, Any]]) -> str:
        """Format the conversation history for the crew."""
        context_parts = []
        
        for msg in messages:
            role = msg.get('role', 'unknown')
            content = msg.get('content', '')
            
            if role == 'user':
                context_parts.append(f"Customer: {content}")
            elif role == 'assistant':
                context_parts.append(f"Agent: {content}")
            elif role == 'system':
                context_parts.append(f"System: {content}")
        
        return "\n".join(context_parts)
    
    async def call(self, input: AgentInput) -> AgentReturnTypes:
        """
        Handle a call from LangWatch scenarios to the CrewAI crew.
        
        Args:
            input: The input from LangWatch scenarios
            
        Returns:
            The crew's response in a format compatible with LangWatch
        """
        try:
            # Get the crew for this conversation thread
            crew = self._get_or_create_crew(input.thread_id)
            
            # Extract the latest user message
            user_message = input.last_new_user_message_str()
            
            # Extract customer ID from context
            customer_id = self._extract_customer_id(input.messages)
            
            # Store conversation context
            thread_context = self.conversation_history[input.thread_id]
            thread_context['messages'].extend(input.new_messages)
            
            # If this is a judgment request, return evaluation
            if input.judgment_request:
                return await self._handle_judgment_request(input, thread_context)
            
            # Handle the inquiry through the crew
            # Run the crew in a thread pool since it might not be async
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                crew.handle_inquiry, 
                user_message, 
                customer_id
            )
            
            # Format the response for LangWatch
            formatted_response = self._format_crew_response(response)
            
            # Update conversation history
            thread_context['context']['last_response'] = formatted_response
            thread_context['context']['customer_id'] = customer_id
            
            return formatted_response
            
        except Exception as e:
            error_msg = f"Error in CrewAI adapter: {str(e)}"
            print(f"CrewAI Adapter Error: {error_msg}")
            return f"I apologize, but I encountered an error while processing your request. Please try again or contact support if the issue persists. Error: {error_msg}"
    
    def _format_crew_response(self, response: str) -> str:
        """Format the crew response for better presentation."""
        # Clean up the response if it contains crew execution details
        lines = response.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Skip lines that look like crew execution logs
            if any(skip_phrase in line.lower() for skip_phrase in [
                'agent:', 'task:', 'crew:', 'executing', 'delegating', 'final answer:'
            ]):
                continue
            
            # Keep lines that look like actual responses
            if line.strip() and not line.startswith('[') and not line.startswith('##'):
                cleaned_lines.append(line.strip())
        
        # If we have cleaned content, use it; otherwise, use original
        if cleaned_lines:
            return '\n'.join(cleaned_lines)
        
        return response
    
    async def _handle_judgment_request(self, input: AgentInput, thread_context: Dict[str, Any]) -> str:
        """Handle judgment requests from LangWatch scenarios."""
        # This would be called by a JudgeAgent to evaluate the conversation
        conversation = self._format_conversation_context(input.messages)
        
        # Return a summary for judgment
        return json.dumps({
            "conversation_summary": conversation,
            "total_messages": len(input.messages),
            "customer_id": thread_context['context'].get('customer_id', 'unknown'),
            "last_response": thread_context['context'].get('last_response', ''),
            "crew_info": thread_context['crew'].get_crew_info() if 'crew' in thread_context else {}
        })


class IndividualAgentAdapter(scenario.AgentAdapter):
    """
    Adapter for testing individual agents within a CrewAI crew.
    
    This adapter allows testing specific agents in isolation while maintaining
    access to the crew's tools and context.
    """
    
    def __init__(self, agent_role: str, crew_class=None, **crew_kwargs):
        """
        Initialize the individual agent adapter.
        
        Args:
            agent_role: The role of the specific agent to test
            crew_class: The CrewAI crew class containing the agent
            **crew_kwargs: Additional arguments for crew initialization
        """
        super().__init__()
        self.agent_role = agent_role
        self.crew_class = crew_class or CustomerServiceCrew
        self.crew_kwargs = crew_kwargs
        self.crew = None
        self.agent = None
        
    def _initialize_if_needed(self):
        """Initialize crew and agent if not already done."""
        if self.crew is None:
            self.crew = self.crew_class(**self.crew_kwargs)
            
            # Find the agent with the specified role
            for agent in self.crew.crew.agents:
                if agent.role == self.agent_role:
                    self.agent = agent
                    break
            
            if self.agent is None:
                raise ValueError(f"Agent with role '{self.agent_role}' not found in crew")
    
    async def call(self, input: AgentInput) -> AgentReturnTypes:
        """
        Handle a call to the individual agent.
        
        Args:
            input: The input from LangWatch scenarios
            
        Returns:
            The agent's response
        """
        try:
            self._initialize_if_needed()
            
            user_message = input.last_new_user_message_str()
            
            # Create a simple task for the individual agent
            # Note: This is a simplified approach - in practice, you might need
            # more sophisticated task creation based on the agent's capabilities
            
            # For now, return a simulated response based on the agent's role
            response = await self._simulate_agent_response(user_message)
            
            return response
            
        except Exception as e:
            return f"Error in individual agent adapter: {str(e)}"
    
    async def _simulate_agent_response(self, message: str) -> str:
        """Simulate an individual agent response based on its role."""
        role_responses = {
            "Customer Service Triage Specialist": f"I'll help route your inquiry: '{message}'. Let me determine the best specialist for your needs.",
            "Technical Support Specialist": f"I'll help you with this technical issue: '{message}'. Let me provide a step-by-step solution.",
            "Billing Support Specialist": f"I'll assist you with this billing matter: '{message}'. Let me review your account and resolve this.",
            "Customer Service Manager": f"I'll personally handle this escalated issue: '{message}'. Let me ensure we find the best solution for you."
        }
        
        base_response = role_responses.get(
            self.agent_role, 
            f"As a {self.agent_role}, I'll help you with: '{message}'"
        )
        
        return base_response


# Utility functions for scenario creation
def create_crew_adapter(**kwargs) -> CrewAIAdapter:
    """Create a CrewAI adapter with optional configuration."""
    return CrewAIAdapter(**kwargs)


def create_agent_adapter(agent_role: str, **kwargs) -> IndividualAgentAdapter:
    """Create an individual agent adapter for testing specific agents."""
    return IndividualAgentAdapter(agent_role, **kwargs)


# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def test_adapter():
        """Test the CrewAI adapter functionality."""
        adapter = create_crew_adapter()
        
        # Simulate a LangWatch AgentInput
        test_messages = [
            {"role": "user", "content": "I can't log into my account"}
        ]
        
        # Create a mock AgentInput (simplified for testing)
        class MockAgentInput:
            def __init__(self, messages):
                self.messages = messages
                self.new_messages = messages
                self.thread_id = "test_thread_001"
                self.judgment_request = False
                self.scenario_state = None
            
            def last_new_user_message_str(self):
                for msg in reversed(self.messages):
                    if msg.get('role') == 'user':
                        return msg.get('content', '')
                return ''
        
        mock_input = MockAgentInput(test_messages)
        
        print("Testing CrewAI Adapter...")
        response = await adapter.call(mock_input)
        print(f"Response: {response}")
    
    # Run the test
    asyncio.run(test_adapter())


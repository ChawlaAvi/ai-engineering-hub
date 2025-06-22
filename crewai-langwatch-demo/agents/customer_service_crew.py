"""
Customer Service Crew - A multi-agent system for handling customer inquiries.

This module implements a CrewAI-based customer service system with specialized agents
for different types of customer inquiries.
"""

import os
from typing import Dict, Any, List
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import json


class CustomerInquiry(BaseModel):
    """Model for customer inquiry data."""
    inquiry_type: str = Field(description="Type of inquiry (billing, technical, general)")
    priority: str = Field(description="Priority level (low, medium, high, urgent)")
    customer_id: str = Field(description="Customer identifier")
    description: str = Field(description="Detailed description of the inquiry")
    context: Dict[str, Any] = Field(default_factory=dict, description="Additional context")


class KnowledgeBaseTool(BaseTool):
    """Tool for accessing customer service knowledge base."""
    
    name: str = "knowledge_base_search"
    description: str = "Search the knowledge base for solutions to customer problems"
    
    def _run(self, query: str) -> str:
        """Search knowledge base for relevant information."""
        # Simulated knowledge base responses
        kb_responses = {
            "billing": {
                "refund": "Refunds can be processed within 5-7 business days. Customer needs to provide order number and reason for refund.",
                "payment": "Payment issues can be resolved by updating payment method in account settings or contacting billing support.",
                "subscription": "Subscription changes take effect immediately. Downgrades are prorated to the next billing cycle."
            },
            "technical": {
                "login": "Login issues: 1) Clear browser cache 2) Reset password 3) Check account status 4) Contact support if persists",
                "performance": "Performance issues: 1) Check internet connection 2) Update browser 3) Disable extensions 4) Try incognito mode",
                "integration": "API integration issues: 1) Check API key validity 2) Verify endpoint URLs 3) Review rate limits 4) Check documentation"
            },
            "general": {
                "hours": "Customer support hours: Monday-Friday 9AM-6PM EST, Saturday 10AM-4PM EST",
                "contact": "Contact options: Live chat, email support@company.com, phone 1-800-SUPPORT",
                "account": "Account management: Login to dashboard to update profile, billing, and preferences"
            }
        }
        
        query_lower = query.lower()
        for category, responses in kb_responses.items():
            for key, response in responses.items():
                if key in query_lower or category in query_lower:
                    return f"Knowledge Base Result: {response}"
        
        return "No specific knowledge base entry found. Please escalate to appropriate specialist."


class CustomerDataTool(BaseTool):
    """Tool for accessing customer data and history."""
    
    name: str = "customer_data_lookup"
    description: str = "Look up customer information and interaction history"
    
    def _run(self, customer_id: str) -> str:
        """Look up customer data."""
        # Simulated customer data
        customer_data = {
            "CUST001": {
                "name": "John Smith",
                "tier": "Premium",
                "account_status": "Active",
                "last_interaction": "2024-01-15",
                "open_tickets": 0,
                "satisfaction_score": 4.5
            },
            "CUST002": {
                "name": "Sarah Johnson",
                "tier": "Standard",
                "account_status": "Active",
                "last_interaction": "2024-01-10",
                "open_tickets": 1,
                "satisfaction_score": 3.8
            }
        }
        
        if customer_id in customer_data:
            data = customer_data[customer_id]
            return f"Customer: {data['name']}, Tier: {data['tier']}, Status: {data['account_status']}, Last Contact: {data['last_interaction']}, Open Tickets: {data['open_tickets']}, Satisfaction: {data['satisfaction_score']}/5"
        
        return f"Customer {customer_id} not found in database."


class TicketingTool(BaseTool):
    """Tool for creating and managing support tickets."""
    
    name: str = "create_ticket"
    description: str = "Create a support ticket for tracking customer issues"
    
    def _run(self, title: str, description: str, priority: str = "medium") -> str:
        """Create a support ticket."""
        ticket_id = f"TKT-{hash(title + description) % 10000:04d}"
        return f"Support ticket {ticket_id} created successfully. Priority: {priority}. Title: {title}"


class CustomerServiceCrew:
    """Main customer service crew orchestrating multiple specialized agents."""
    
    def __init__(self):
        """Initialize the customer service crew with all agents and tools."""
        self.tools = [
            KnowledgeBaseTool(),
            CustomerDataTool(),
            TicketingTool()
        ]
        
        # Initialize agents
        self.triage_agent = self._create_triage_agent()
        self.technical_agent = self._create_technical_agent()
        self.billing_agent = self._create_billing_agent()
        self.manager_agent = self._create_manager_agent()
        
        # Create the crew
        self.crew = self._create_crew()
    
    def _create_triage_agent(self) -> Agent:
        """Create the triage agent responsible for routing inquiries."""
        return Agent(
            role="Customer Service Triage Specialist",
            goal="Efficiently route customer inquiries to the appropriate specialist agent",
            backstory="""You are an experienced customer service triage specialist with 5+ years 
            of experience in routing customer inquiries. You excel at quickly understanding customer 
            needs and directing them to the right department. You're known for your ability to 
            identify urgent issues and prioritize accordingly.""",
            tools=self.tools,
            verbose=True,
            allow_delegation=True,
            max_iter=3
        )
    
    def _create_technical_agent(self) -> Agent:
        """Create the technical support agent."""
        return Agent(
            role="Technical Support Specialist",
            goal="Resolve technical issues and provide clear, actionable solutions",
            backstory="""You are a senior technical support specialist with deep expertise in 
            troubleshooting software and integration issues. You have a talent for explaining 
            complex technical concepts in simple terms and always provide step-by-step solutions. 
            You're patient, thorough, and committed to resolving issues completely.""",
            tools=self.tools,
            verbose=True,
            allow_delegation=False,
            max_iter=5
        )
    
    def _create_billing_agent(self) -> Agent:
        """Create the billing support agent."""
        return Agent(
            role="Billing Support Specialist",
            goal="Handle billing inquiries, process refunds, and resolve payment issues",
            backstory="""You are a billing support specialist with extensive experience in 
            financial customer service. You're detail-oriented, empathetic to customer concerns 
            about money, and skilled at explaining billing processes clearly. You have the 
            authority to process refunds and adjust accounts when appropriate.""",
            tools=self.tools,
            verbose=True,
            allow_delegation=False,
            max_iter=4
        )
    
    def _create_manager_agent(self) -> Agent:
        """Create the manager agent for escalations."""
        return Agent(
            role="Customer Service Manager",
            goal="Handle escalated issues and ensure customer satisfaction",
            backstory="""You are a customer service manager with 10+ years of experience in 
            customer relations. You handle the most complex and sensitive customer issues. 
            You're empowered to make exceptions, offer compensation, and ensure that every 
            customer leaves satisfied. You're diplomatic, solution-oriented, and focused on 
            long-term customer relationships.""",
            tools=self.tools,
            verbose=True,
            allow_delegation=True,
            max_iter=6
        )
    
    def _create_crew(self) -> Crew:
        """Create the customer service crew."""
        return Crew(
            agents=[self.triage_agent, self.technical_agent, self.billing_agent, self.manager_agent],
            process=Process.hierarchical,
            manager_agent=self.manager_agent,
            verbose=True
        )
    
    def handle_inquiry(self, inquiry: str, customer_id: str = "CUST001") -> str:
        """
        Handle a customer inquiry through the crew.
        
        Args:
            inquiry: The customer's inquiry or question
            customer_id: Customer identifier for context
            
        Returns:
            The crew's response to the inquiry
        """
        # Create the main task
        task = Task(
            description=f"""
            Handle the following customer inquiry:
            
            Customer ID: {customer_id}
            Inquiry: {inquiry}
            
            Steps to follow:
            1. Look up customer information to understand their context
            2. Analyze the inquiry to determine the type and priority
            3. Route to the appropriate specialist or handle directly
            4. Provide a complete, helpful response
            5. Create a ticket if needed for follow-up
            6. Ensure customer satisfaction
            
            The response should be professional, empathetic, and actionable.
            """,
            agent=self.triage_agent,
            expected_output="A complete resolution or clear next steps for the customer inquiry"
        )
        
        # Execute the task
        result = self.crew.kickoff(tasks=[task])
        return str(result)
    
    def get_crew_info(self) -> Dict[str, Any]:
        """Get information about the crew structure."""
        return {
            "agents": [
                {"role": agent.role, "goal": agent.goal} 
                for agent in self.crew.agents
            ],
            "process": str(self.crew.process),
            "tools": [tool.name for tool in self.tools]
        }


# Example usage and testing
if __name__ == "__main__":
    # Initialize the crew
    crew = CustomerServiceCrew()
    
    # Test with different types of inquiries
    test_inquiries = [
        "I can't log into my account and I have an important meeting in 30 minutes",
        "I was charged twice for my subscription this month",
        "How do I integrate your API with my application?",
        "I want to cancel my subscription and get a refund"
    ]
    
    print("=== Customer Service Crew Demo ===\n")
    
    for i, inquiry in enumerate(test_inquiries, 1):
        print(f"--- Test Inquiry {i} ---")
        print(f"Customer: {inquiry}")
        print("\nCrew Response:")
        
        try:
            response = crew.handle_inquiry(inquiry, f"CUST00{i}")
            print(response)
        except Exception as e:
            print(f"Error handling inquiry: {e}")
        
        print("\n" + "="*80 + "\n")


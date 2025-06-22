"""
Customer Service Test Scenarios

This module contains LangWatch scenarios for testing the CrewAI customer service system.
These scenarios simulate realistic customer interactions and evaluate agent performance.
"""

import pytest
import asyncio
import os
from typing import List, Dict, Any
import scenario
from scenario import AgentInput, AgentReturnTypes

# Import our adapters
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from adapters.crew_adapter import create_crew_adapter, create_agent_adapter


# Configure LangWatch scenarios
scenario.configure(
    testing_agent=scenario.TestingAgent(
        model=os.getenv("SIMULATOR_MODEL", "openai/gpt-4o-mini")
    )
)


class CustomerServiceTestSuite:
    """Test suite for customer service scenarios."""
    
    @staticmethod
    def get_crew_adapter():
        """Get a configured crew adapter for testing."""
        return create_crew_adapter()


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_basic_login_issue():
    """Test handling of a basic login issue."""
    
    crew_adapter = CustomerServiceTestSuite.get_crew_adapter()
    
    result = await scenario.run(
        name="basic login troubleshooting",
        description="""
        User is having trouble logging into their account. They're not particularly 
        tech-savvy but are cooperative and willing to follow instructions. They have 
        their login credentials ready and access to their email.
        """,
        agents=[
            crew_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(criteria=[
                "Agent should ask relevant troubleshooting questions",
                "Agent should provide clear, step-by-step instructions",
                "Agent should be patient and helpful",
                "Agent should offer multiple solutions if the first doesn't work",
                "Agent should create a ticket if the issue can't be resolved immediately"
            ])
        ],
        max_turns=8
    )
    
    assert result.success, f"Login troubleshooting scenario failed: {result.feedback}"
    assert len(result.messages) >= 4, "Conversation should have substantial interaction"


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_billing_dispute():
    """Test handling of a billing dispute."""
    
    crew_adapter = CustomerServiceTestSuite.get_crew_adapter()
    
    result = await scenario.run(
        name="billing dispute resolution",
        description="""
        Customer received a bill that's higher than expected. They're confused but not 
        angry. They have their account information and previous bills available. They 
        want to understand the charges and get them corrected if there's an error.
        """,
        agents=[
            crew_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(criteria=[
                "Agent should ask for account information to investigate",
                "Agent should review the billing details with the customer",
                "Agent should explain any unusual or high charges clearly",
                "Agent should offer solutions if there was a billing error",
                "Agent should maintain a professional and empathetic tone",
                "Agent should ensure customer understands before concluding"
            ])
        ],
        max_turns=10
    )
    
    assert result.success, f"Billing dispute scenario failed: {result.feedback}"


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_technical_api_integration():
    """Test handling of technical API integration questions."""
    
    crew_adapter = CustomerServiceTestSuite.get_crew_adapter()
    
    result = await scenario.run(
        name="API integration support",
        description="""
        Developer is trying to integrate the company's API into their application. 
        They're experiencing authentication issues and getting error codes they don't 
        understand. They're technically competent but new to this specific API.
        """,
        agents=[
            crew_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(criteria=[
                "Agent should ask about the specific error codes or messages",
                "Agent should provide technical guidance appropriate for a developer",
                "Agent should reference documentation or examples when helpful",
                "Agent should offer to escalate to technical specialists if needed",
                "Agent should ensure the developer has working code before concluding"
            ])
        ],
        max_turns=12
    )
    
    assert result.success, f"API integration scenario failed: {result.feedback}"


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_urgent_escalation():
    """Test handling of urgent issues requiring escalation."""
    
    crew_adapter = CustomerServiceTestSuite.get_crew_adapter()
    
    result = await scenario.run(
        name="urgent issue escalation",
        description="""
        Customer is experiencing a critical system outage that's affecting their business. 
        They're stressed and need immediate help. The issue is complex and likely requires 
        manager intervention or specialized technical support.
        """,
        agents=[
            crew_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(criteria=[
                "Agent should recognize the urgency of the situation",
                "Agent should gather essential information quickly",
                "Agent should escalate to appropriate specialist or manager",
                "Agent should provide immediate workarounds if possible",
                "Agent should set clear expectations for follow-up",
                "Agent should maintain calm and professional demeanor despite customer stress"
            ])
        ],
        max_turns=8
    )
    
    assert result.success, f"Urgent escalation scenario failed: {result.feedback}"


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_subscription_cancellation():
    """Test handling of subscription cancellation requests."""
    
    crew_adapter = CustomerServiceTestSuite.get_crew_adapter()
    
    result = await scenario.run(
        name="subscription cancellation with retention attempt",
        description="""
        Customer wants to cancel their subscription due to cost concerns. They've been 
        a customer for several months and generally satisfied with the service, but 
        their budget has tightened. They're open to alternatives but firm about 
        needing to reduce costs.
        """,
        agents=[
            crew_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(criteria=[
                "Agent should understand the reason for cancellation",
                "Agent should offer alternatives like downgrading or pausing service",
                "Agent should not be overly pushy with retention attempts",
                "Agent should process the cancellation if customer insists",
                "Agent should explain the cancellation process and timeline",
                "Agent should end on a positive note and leave door open for return"
            ])
        ],
        max_turns=10
    )
    
    assert result.success, f"Subscription cancellation scenario failed: {result.feedback}"


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_multi_issue_conversation():
    """Test handling of conversations with multiple related issues."""
    
    crew_adapter = CustomerServiceTestSuite.get_crew_adapter()
    
    result = await scenario.run(
        name="multiple related issues in one conversation",
        description="""
        Customer starts with a billing question but then mentions they're also having 
        login issues and wants to know about upgrading their plan. They want to handle 
        everything in one conversation rather than making multiple contacts.
        """,
        agents=[
            crew_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(criteria=[
                "Agent should acknowledge all the customer's concerns",
                "Agent should organize the conversation to address each issue systematically",
                "Agent should not get confused or lose track of the multiple issues",
                "Agent should provide complete solutions for each problem",
                "Agent should confirm all issues are resolved before ending",
                "Agent should maintain context throughout the conversation"
            ])
        ],
        max_turns=15
    )
    
    assert result.success, f"Multi-issue conversation scenario failed: {result.feedback}"


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_unclear_initial_request():
    """Test handling of vague or unclear initial requests."""
    
    crew_adapter = CustomerServiceTestSuite.get_crew_adapter()
    
    result = await scenario.run(
        name="clarifying vague customer request",
        description="""
        Customer contacts support saying "something is wrong" or "it's not working" 
        without providing specific details. They're frustrated but not sure how to 
        explain the problem clearly. Agent needs to ask good questions to understand 
        the actual issue.
        """,
        agents=[
            crew_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(criteria=[
                "Agent should ask clarifying questions to understand the problem",
                "Agent should be patient with the customer's inability to articulate clearly",
                "Agent should guide the customer through providing relevant details",
                "Agent should not make assumptions about what the problem might be",
                "Agent should eventually identify the specific issue",
                "Agent should provide appropriate solution once problem is clear"
            ])
        ],
        max_turns=12
    )
    
    assert result.success, f"Unclear request scenario failed: {result.feedback}"


# Performance and load testing scenarios
@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_concurrent_conversations():
    """Test the system's ability to handle multiple conversations simultaneously."""
    
    async def run_single_conversation(conversation_id: str):
        """Run a single conversation scenario."""
        crew_adapter = CustomerServiceTestSuite.get_crew_adapter()
        
        result = await scenario.run(
            name=f"concurrent conversation {conversation_id}",
            description=f"""
            Customer {conversation_id} has a standard billing question about their account. 
            This is part of testing concurrent conversation handling.
            """,
            agents=[
                crew_adapter,
                scenario.UserSimulatorAgent(),
                scenario.JudgeAgent(criteria=[
                    "Agent should handle the conversation normally despite concurrent load",
                    "Agent should not mix up information from other conversations",
                    "Agent should provide accurate and relevant responses"
                ])
            ],
            max_turns=6
        )
        return result
    
    # Run multiple conversations concurrently
    tasks = [
        run_single_conversation(f"CONC{i:03d}") 
        for i in range(3)  # Start with 3 concurrent conversations
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Check that all conversations succeeded
    successful_results = [r for r in results if not isinstance(r, Exception) and r.success]
    assert len(successful_results) >= 2, f"At least 2 out of 3 concurrent conversations should succeed. Got {len(successful_results)} successes."


# Integration test with all agent types
@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_full_crew_integration():
    """Test the full crew working together on a complex scenario."""
    
    crew_adapter = CustomerServiceTestSuite.get_crew_adapter()
    
    result = await scenario.run(
        name="complex multi-agent collaboration",
        description="""
        Customer has a complex issue that requires multiple types of support: they're 
        having technical problems with the API, want to upgrade their billing plan, 
        and need to escalate a previous unresolved issue. This should trigger 
        collaboration between triage, technical, billing, and manager agents.
        """,
        agents=[
            crew_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(criteria=[
                "Multiple agents should be involved in resolving the issues",
                "Agents should collaborate effectively without confusion",
                "Each specialist should handle their area of expertise",
                "The conversation should flow naturally between agents",
                "All customer issues should be addressed comprehensively",
                "The final resolution should be complete and satisfactory"
            ])
        ],
        max_turns=20
    )
    
    assert result.success, f"Full crew integration scenario failed: {result.feedback}"
    
    # Additional assertions for complex scenarios
    conversation_text = " ".join([msg.get('content', '') for msg in result.messages])
    assert len(result.messages) >= 10, "Complex scenario should have extended conversation"
    
    # Check that multiple types of issues were discussed
    issue_indicators = ['technical', 'billing', 'api', 'upgrade', 'escalate']
    discussed_issues = sum(1 for indicator in issue_indicators if indicator.lower() in conversation_text.lower())
    assert discussed_issues >= 3, f"Should discuss multiple issue types, found {discussed_issues}"


if __name__ == "__main__":
    # Run tests directly for development/debugging
    import asyncio
    
    async def run_single_test():
        """Run a single test for debugging."""
        print("Running basic login issue test...")
        await test_basic_login_issue()
        print("Test completed successfully!")
    
    # Uncomment to run a single test
    # asyncio.run(run_single_test())


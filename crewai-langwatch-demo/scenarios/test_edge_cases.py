"""
Edge Case Test Scenarios

This module contains LangWatch scenarios for testing edge cases and error conditions
in the CrewAI customer service system. These scenarios help ensure robustness
and graceful handling of unusual situations.
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
from adapters.crew_adapter import create_crew_adapter


# Configure LangWatch scenarios
scenario.configure(
    testing_agent=scenario.TestingAgent(
        model=os.getenv("SIMULATOR_MODEL", "openai/gpt-4o-mini")
    )
)


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_extremely_angry_customer():
    """Test handling of an extremely upset and angry customer."""
    
    crew_adapter = create_crew_adapter()
    
    result = await scenario.run(
        name="extremely angry customer de-escalation",
        description="""
        Customer is extremely angry and frustrated. They've been trying to resolve 
        an issue for weeks, feel ignored, and are threatening to cancel and leave 
        negative reviews. They're using strong language and are very emotional. 
        They need immediate attention and empathy.
        """,
        agents=[
            crew_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(criteria=[
                "Agent should remain calm and professional despite customer anger",
                "Agent should acknowledge the customer's frustration and apologize",
                "Agent should not take the anger personally or become defensive",
                "Agent should focus on understanding and solving the underlying issue",
                "Agent should escalate to manager if appropriate",
                "Agent should work to de-escalate the emotional situation",
                "Agent should provide concrete next steps and timeline"
            ])
        ],
        max_turns=12
    )
    
    assert result.success, f"Angry customer scenario failed: {result.feedback}"


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_language_barrier():
    """Test handling of customers with limited English proficiency."""
    
    crew_adapter = create_crew_adapter()
    
    result = await scenario.run(
        name="customer with language barrier",
        description="""
        Customer has limited English proficiency and is struggling to communicate 
        their issue clearly. They're using simple words, some grammar mistakes, 
        and occasionally mixing in words from their native language. They're 
        patient but frustrated by the communication difficulty.
        """,
        agents=[
            crew_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(criteria=[
                "Agent should be patient and understanding about language difficulties",
                "Agent should use simple, clear language in responses",
                "Agent should avoid idioms, slang, or complex technical terms",
                "Agent should confirm understanding by restating the issue",
                "Agent should offer alternative communication methods if needed",
                "Agent should not make the customer feel embarrassed about language skills",
                "Agent should still provide effective help despite communication challenges"
            ])
        ],
        max_turns=15
    )
    
    assert result.success, f"Language barrier scenario failed: {result.feedback}"


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_customer_with_unrealistic_expectations():
    """Test handling of customers with unrealistic or impossible requests."""
    
    crew_adapter = create_crew_adapter()
    
    result = await scenario.run(
        name="unrealistic customer expectations",
        description="""
        Customer is demanding something that's impossible or against company policy, 
        such as a full refund for a service they've used for months, or expecting 
        24/7 personal support for a basic plan. They believe they're entitled to 
        these things and become argumentative when told no.
        """,
        agents=[
            crew_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(criteria=[
                "Agent should clearly explain company policies and limitations",
                "Agent should remain professional when setting boundaries",
                "Agent should offer reasonable alternatives when possible",
                "Agent should not give in to unreasonable demands",
                "Agent should escalate to manager if customer becomes abusive",
                "Agent should document the interaction appropriately",
                "Agent should try to find win-win solutions within policy limits"
            ])
        ],
        max_turns=12
    )
    
    assert result.success, f"Unrealistic expectations scenario failed: {result.feedback}"


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_technical_system_failure():
    """Test handling when internal systems are down or malfunctioning."""
    
    crew_adapter = create_crew_adapter()
    
    result = await scenario.run(
        name="system failure during customer interaction",
        description="""
        Customer needs help with their account, but the agent discovers that internal 
        systems are down or returning errors. The agent can't access customer data, 
        process requests, or perform normal functions. Customer is unaware of the 
        technical issues and expects normal service.
        """,
        agents=[
            crew_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(criteria=[
                "Agent should acknowledge the system issues honestly",
                "Agent should apologize for the inconvenience",
                "Agent should provide realistic timeline for resolution",
                "Agent should offer alternative solutions or workarounds",
                "Agent should take customer information for follow-up",
                "Agent should not blame the customer or make excuses",
                "Agent should escalate to technical team if appropriate"
            ])
        ],
        max_turns=10
    )
    
    assert result.success, f"System failure scenario failed: {result.feedback}"


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_customer_security_concerns():
    """Test handling of customers worried about security and privacy."""
    
    crew_adapter = create_crew_adapter()
    
    result = await scenario.run(
        name="customer security and privacy concerns",
        description="""
        Customer is very concerned about security and privacy. They're hesitant to 
        provide personal information, suspicious of data collection, and worried 
        about account security. They need help but are paranoid about sharing details 
        or following instructions that might compromise their security.
        """,
        agents=[
            crew_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(criteria=[
                "Agent should respect customer's security concerns",
                "Agent should explain why information is needed and how it's protected",
                "Agent should offer alternative verification methods when possible",
                "Agent should not pressure customer to share information they're uncomfortable with",
                "Agent should provide clear information about company security practices",
                "Agent should escalate to security specialist if needed",
                "Agent should build trust through transparency and patience"
            ])
        ],
        max_turns=12
    )
    
    assert result.success, f"Security concerns scenario failed: {result.feedback}"


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_customer_with_disability():
    """Test handling of customers with accessibility needs."""
    
    crew_adapter = create_crew_adapter()
    
    result = await scenario.run(
        name="customer with accessibility needs",
        description="""
        Customer has a disability that affects how they interact with the service 
        (e.g., visual impairment, hearing difficulty, motor limitations). They need 
        help but also require accommodations or alternative methods to access 
        support and use the service effectively.
        """,
        agents=[
            crew_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(criteria=[
                "Agent should be respectful and sensitive to accessibility needs",
                "Agent should ask how they can best assist the customer",
                "Agent should offer alternative communication methods if helpful",
                "Agent should not make assumptions about the customer's capabilities",
                "Agent should provide information about accessibility features",
                "Agent should escalate to accessibility specialist if available",
                "Agent should ensure the customer receives equal quality of service"
            ])
        ],
        max_turns=10
    )
    
    assert result.success, f"Accessibility needs scenario failed: {result.feedback}"


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_customer_confusion_about_service():
    """Test handling of customers who are completely confused about what the service does."""
    
    crew_adapter = create_crew_adapter()
    
    result = await scenario.run(
        name="customer confused about service offering",
        description="""
        Customer signed up for the service but doesn't really understand what it does 
        or how to use it. They're asking basic questions that suggest they may have 
        signed up by mistake or have completely wrong expectations about the product. 
        They're not angry, just genuinely confused.
        """,
        agents=[
            crew_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(criteria=[
                "Agent should patiently explain what the service actually does",
                "Agent should use simple, non-technical language",
                "Agent should assess if the service meets the customer's actual needs",
                "Agent should offer appropriate onboarding or tutorial resources",
                "Agent should not make the customer feel stupid for not understanding",
                "Agent should help customer decide if they want to continue or cancel",
                "Agent should provide clear next steps based on customer's decision"
            ])
        ],
        max_turns=12
    )
    
    assert result.success, f"Service confusion scenario failed: {result.feedback}"


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_rapid_fire_questions():
    """Test handling of customers who ask many questions very quickly."""
    
    crew_adapter = create_crew_adapter()
    
    result = await scenario.run(
        name="customer with rapid-fire questions",
        description="""
        Customer is asking many different questions very quickly without waiting 
        for complete answers. They jump from topic to topic, interrupt responses, 
        and seem impatient. They have legitimate questions but their communication 
        style is overwhelming and disorganized.
        """,
        agents=[
            crew_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(criteria=[
                "Agent should remain organized despite the rapid questioning",
                "Agent should acknowledge all questions but structure responses logically",
                "Agent should politely ask customer to slow down if needed",
                "Agent should prioritize the most important or urgent questions first",
                "Agent should not get flustered or confused by the pace",
                "Agent should ensure all questions are eventually addressed",
                "Agent should maintain professional composure throughout"
            ])
        ],
        max_turns=15
    )
    
    assert result.success, f"Rapid-fire questions scenario failed: {result.feedback}"


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_customer_wants_to_speak_to_human():
    """Test handling of customers who insist on speaking to a human agent."""
    
    crew_adapter = create_crew_adapter()
    
    result = await scenario.run(
        name="customer demands human agent",
        description="""
        Customer realizes they're talking to an AI system and becomes upset. They 
        insist on speaking to a "real person" and refuse to continue with AI assistance. 
        They may be frustrated with AI in general or have had bad experiences with 
        automated systems before.
        """,
        agents=[
            crew_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(criteria=[
                "Agent should acknowledge the customer's preference respectfully",
                "Agent should explain the capabilities and limitations honestly",
                "Agent should offer to escalate to human agent if available",
                "Agent should not argue about the value of AI assistance",
                "Agent should provide information about human support availability",
                "Agent should offer to help while waiting for human agent",
                "Agent should handle the request professionally without defensiveness"
            ])
        ],
        max_turns=8
    )
    
    assert result.success, f"Human agent demand scenario failed: {result.feedback}"


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_customer_provides_wrong_information():
    """Test handling when customer provides incorrect or conflicting information."""
    
    crew_adapter = create_crew_adapter()
    
    result = await scenario.run(
        name="customer provides incorrect information",
        description="""
        Customer is providing information about their account or issue, but the 
        details don't match what's in the system or are internally inconsistent. 
        They might have the wrong account number, wrong dates, or be confusing 
        their issue with someone else's. They're not lying, just mistaken.
        """,
        agents=[
            crew_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(criteria=[
                "Agent should politely point out discrepancies without accusation",
                "Agent should help customer verify correct information",
                "Agent should ask clarifying questions to resolve conflicts",
                "Agent should not assume customer is lying or being difficult",
                "Agent should offer alternative ways to verify identity or details",
                "Agent should be patient while sorting out the confusion",
                "Agent should proceed once correct information is established"
            ])
        ],
        max_turns=12
    )
    
    assert result.success, f"Wrong information scenario failed: {result.feedback}"


# Stress testing scenarios
@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_extremely_long_conversation():
    """Test system behavior during unusually long conversations."""
    
    crew_adapter = create_crew_adapter()
    
    result = await scenario.run(
        name="extremely long customer conversation",
        description="""
        Customer has a complex issue that requires a very long conversation to resolve. 
        They keep asking follow-up questions, need detailed explanations, and the 
        conversation goes on much longer than typical. Test if the system maintains 
        context and performance over extended interactions.
        """,
        agents=[
            crew_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(criteria=[
                "Agent should maintain context throughout the long conversation",
                "Agent should not repeat information unnecessarily",
                "Agent should stay focused on resolving the customer's issues",
                "Agent should not show signs of degraded performance over time",
                "Agent should periodically summarize progress if helpful",
                "Agent should maintain professional quality throughout",
                "Agent should eventually reach a satisfactory resolution"
            ])
        ],
        max_turns=25  # Much longer than typical
    )
    
    assert result.success, f"Long conversation scenario failed: {result.feedback}"
    assert len(result.messages) >= 20, "Should have extended conversation"


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_customer_changes_mind_repeatedly():
    """Test handling of indecisive customers who change their minds frequently."""
    
    crew_adapter = create_crew_adapter()
    
    result = await scenario.run(
        name="indecisive customer changing requests",
        description="""
        Customer keeps changing their mind about what they want. They start with 
        one request, then change to something else, then back to the original, 
        then to a third option. They're not being difficult on purpose, just 
        genuinely indecisive and unsure what they really need.
        """,
        agents=[
            crew_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(criteria=[
                "Agent should remain patient with the changing requests",
                "Agent should help customer clarify their actual needs",
                "Agent should not get frustrated or confused by the changes",
                "Agent should keep track of different options discussed",
                "Agent should help customer make a final decision",
                "Agent should confirm the final choice before proceeding",
                "Agent should maintain helpful attitude throughout"
            ])
        ],
        max_turns=18
    )
    
    assert result.success, f"Indecisive customer scenario failed: {result.feedback}"


if __name__ == "__main__":
    # Run a single test for debugging
    import asyncio
    
    async def run_debug_test():
        """Run a single test for debugging purposes."""
        print("Running angry customer test...")
        await test_extremely_angry_customer()
        print("Test completed!")
    
    # Uncomment to run debug test
    # asyncio.run(run_debug_test())


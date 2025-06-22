"""
Advanced Scripted Scenarios

This module contains advanced LangWatch scenarios that use scripted interactions
to test specific conversation flows and error recovery patterns in the CrewAI system.
"""

import pytest
import asyncio
import os
from typing import List, Dict, Any
import scenario
from scenario import AgentInput, AgentReturnTypes

# Import our adapters
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from adapters.crew_adapter import create_crew_adapter


# Configure LangWatch scenarios
scenario.configure(
    testing_agent=scenario.TestingAgent(
        model=os.getenv("SIMULATOR_MODEL", "openai/gpt-4o-mini")
    )
)


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_scripted_error_recovery():
    """Test error recovery using a scripted scenario."""
    
    crew_adapter = create_crew_adapter()
    
    result = await scenario.run(
        name="scripted error recovery scenario",
        description="""
        Test how the agent recovers from providing incorrect information.
        The script will force the agent to make a mistake, then see how
        it handles the correction and recovery.
        """,
        agents=[
            crew_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(criteria=[
                "Agent should acknowledge the mistake when corrected",
                "Agent should apologize for the incorrect information",
                "Agent should provide the correct information promptly",
                "Agent should not make excuses or blame external factors",
                "Agent should ensure customer is satisfied with the correction",
                "Agent should learn from the mistake for the rest of the conversation"
            ])
        ],
        script=[
            scenario.user("I need help with my billing issue"),
            scenario.agent("I can help with that. Let me look up your account... I see you have a Premium plan for $99/month."),
            scenario.user("That's not right, I have the Basic plan for $29/month"),
            scenario.proceed()  # Let the scenario continue naturally from here
        ],
        max_turns=10
    )
    
    assert result.success, f"Error recovery scenario failed: {result.feedback}"


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_scripted_escalation_flow():
    """Test the escalation flow using scripted interactions."""
    
    crew_adapter = create_crew_adapter()
    
    result = await scenario.run(
        name="scripted escalation flow",
        description="""
        Test the escalation process by scripting the initial interaction
        and then letting the scenario play out the escalation naturally.
        """,
        agents=[
            crew_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(criteria=[
                "Agent should recognize when escalation is needed",
                "Agent should explain the escalation process to the customer",
                "Agent should gather necessary information before escalating",
                "Agent should set appropriate expectations for response time",
                "Agent should ensure smooth handoff to higher level support",
                "Agent should maintain professionalism throughout the process"
            ])
        ],
        script=[
            scenario.user("I've been trying to resolve this issue for 3 weeks and nobody has helped me!"),
            scenario.agent("I understand your frustration. Let me try to help you with this issue."),
            scenario.user("No! I've talked to 5 different agents already. I want to speak to a manager RIGHT NOW!"),
            scenario.proceed()  # Let the agent handle the escalation request
        ],
        max_turns=12
    )
    
    assert result.success, f"Escalation flow scenario failed: {result.feedback}"


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_scripted_technical_handoff():
    """Test handoff between different types of agents using scripted flow."""
    
    crew_adapter = create_crew_adapter()
    
    result = await scenario.run(
        name="scripted technical handoff",
        description="""
        Test how the system handles handoff from general support to technical
        support when the issue becomes too complex for the initial agent.
        """,
        agents=[
            crew_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(criteria=[
                "Initial agent should recognize the technical complexity",
                "Agent should explain why technical specialist is needed",
                "Handoff should be smooth with proper context transfer",
                "Technical specialist should have all necessary background",
                "Customer should not need to repeat their entire story",
                "Technical solution should be appropriate and complete"
            ])
        ],
        script=[
            scenario.user("I'm having trouble with your API integration"),
            scenario.agent("I can help with general API questions. What specific issue are you experiencing?"),
            scenario.user("I'm getting a 429 error with custom headers and webhook validation is failing intermittently"),
            scenario.proceed()  # Let the agent recognize this needs technical expertise
        ],
        max_turns=15
    )
    
    assert result.success, f"Technical handoff scenario failed: {result.feedback}"


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_scripted_billing_dispute_resolution():
    """Test billing dispute resolution with scripted customer responses."""
    
    crew_adapter = create_crew_adapter()
    
    result = await scenario.run(
        name="scripted billing dispute with evidence",
        description="""
        Customer has a billing dispute and provides specific evidence.
        Test how the agent handles the evidence and resolves the dispute.
        """,
        agents=[
            crew_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(criteria=[
                "Agent should carefully review the customer's evidence",
                "Agent should acknowledge the validity of customer's concerns",
                "Agent should investigate the billing discrepancy thoroughly",
                "Agent should provide clear explanation of what happened",
                "Agent should offer appropriate resolution (refund, credit, etc.)",
                "Agent should ensure customer is satisfied with the resolution"
            ])
        ],
        script=[
            scenario.user("I was charged $199 on January 15th but I downgraded to the $49 plan on January 10th"),
            scenario.agent("I'll help you with this billing issue. Let me look into your account."),
            scenario.user("I have the email confirmation of my downgrade and my bank statement showing the wrong charge"),
            scenario.proceed()  # Let agent handle the evidence and resolution
        ],
        max_turns=12
    )
    
    assert result.success, f"Billing dispute resolution scenario failed: {result.feedback}"


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_scripted_multi_step_troubleshooting():
    """Test multi-step troubleshooting with scripted customer responses."""
    
    crew_adapter = create_crew_adapter()
    
    result = await scenario.run(
        name="scripted multi-step troubleshooting",
        description="""
        Customer has a technical issue that requires multiple troubleshooting steps.
        Script the initial steps to test the agent's systematic approach.
        """,
        agents=[
            crew_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(criteria=[
                "Agent should follow a logical troubleshooting sequence",
                "Agent should wait for customer confirmation before proceeding to next step",
                "Agent should adapt approach based on customer's responses",
                "Agent should not skip steps or make assumptions",
                "Agent should provide clear instructions for each step",
                "Agent should eventually identify and resolve the root cause"
            ])
        ],
        script=[
            scenario.user("I can't access my dashboard, it just shows a blank page"),
            scenario.agent("I'll help you troubleshoot this. First, can you try refreshing the page?"),
            scenario.user("I tried that already, still blank"),
            scenario.agent("Let's try clearing your browser cache. Can you do that and try again?"),
            scenario.user("Okay, I cleared the cache but it's still not working"),
            scenario.proceed()  # Let agent continue with more advanced troubleshooting
        ],
        max_turns=15
    )
    
    assert result.success, f"Multi-step troubleshooting scenario failed: {result.feedback}"


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_scripted_customer_education():
    """Test customer education scenario with scripted learning progression."""
    
    crew_adapter = create_crew_adapter()
    
    result = await scenario.run(
        name="scripted customer education flow",
        description="""
        Customer needs to learn how to use a feature properly. Test how
        the agent educates them step by step with scripted responses
        showing learning progression.
        """,
        agents=[
            crew_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(criteria=[
                "Agent should assess customer's current knowledge level",
                "Agent should provide education at appropriate pace",
                "Agent should check understanding before moving to next concept",
                "Agent should use clear, non-technical language",
                "Agent should provide examples and practical applications",
                "Agent should ensure customer can apply the knowledge independently"
            ])
        ],
        script=[
            scenario.user("I don't understand how to use the reporting feature"),
            scenario.agent("I'd be happy to help you learn the reporting feature. What type of reports are you trying to create?"),
            scenario.user("I want to see how many users visited my site last month"),
            scenario.agent("Great! That's a traffic report. Let me walk you through creating one step by step."),
            scenario.user("Okay, I'm ready to learn"),
            scenario.proceed()  # Let agent provide the education
        ],
        max_turns=18
    )
    
    assert result.success, f"Customer education scenario failed: {result.feedback}"


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_scripted_policy_explanation():
    """Test policy explanation with scripted customer pushback."""
    
    crew_adapter = create_crew_adapter()
    
    result = await scenario.run(
        name="scripted policy explanation with pushback",
        description="""
        Customer wants something that goes against company policy.
        Script their pushback to test how agent explains and enforces policies.
        """,
        agents=[
            crew_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(criteria=[
                "Agent should clearly explain the relevant policy",
                "Agent should remain firm but empathetic about policy limits",
                "Agent should explain the reasoning behind the policy",
                "Agent should offer alternative solutions within policy bounds",
                "Agent should not make exceptions that violate policy",
                "Agent should escalate to manager if customer becomes abusive"
            ])
        ],
        script=[
            scenario.user("I want a full refund for my annual subscription that I've been using for 8 months"),
            scenario.agent("I understand you'd like a refund. Let me explain our refund policy for annual subscriptions."),
            scenario.user("I don't care about your policy, I want my money back! Other companies would give me a refund!"),
            scenario.agent("I understand your frustration. Our policy exists to be fair to all customers, but let me see what options we have."),
            scenario.user("That's not good enough! I'm going to leave negative reviews everywhere!"),
            scenario.proceed()  # Let agent handle the escalating situation
        ],
        max_turns=12
    )
    
    assert result.success, f"Policy explanation scenario failed: {result.feedback}"


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_scripted_feature_request_handling():
    """Test how agent handles feature requests with scripted customer persistence."""
    
    crew_adapter = create_crew_adapter()
    
    result = await scenario.run(
        name="scripted feature request handling",
        description="""
        Customer is requesting a feature that doesn't exist. Script their
        persistence to test how agent handles feature requests appropriately.
        """,
        agents=[
            crew_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(criteria=[
                "Agent should acknowledge the feature request positively",
                "Agent should explain current capabilities and limitations",
                "Agent should offer workarounds or alternative solutions",
                "Agent should explain how to submit formal feature requests",
                "Agent should not promise features that don't exist",
                "Agent should maintain helpful attitude despite limitations"
            ])
        ],
        script=[
            scenario.user("I need the system to automatically generate reports and email them to my team every morning"),
            scenario.agent("That sounds like a useful feature. Let me check what automation options we currently have available."),
            scenario.user("I really need this to work automatically. Can you just turn it on for me?"),
            scenario.agent("I understand how helpful that would be. Currently, our system doesn't have that specific automation feature."),
            scenario.user("But I really need this! Isn't there any way to make it work?"),
            scenario.proceed()  # Let agent handle the persistent request
        ],
        max_turns=12
    )
    
    assert result.success, f"Feature request handling scenario failed: {result.feedback}"


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_scripted_account_security_incident():
    """Test handling of account security incidents with scripted urgency."""
    
    crew_adapter = create_crew_adapter()
    
    result = await scenario.run(
        name="scripted account security incident",
        description="""
        Customer believes their account has been compromised. Script the
        urgency and concern to test security incident response.
        """,
        agents=[
            crew_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(criteria=[
                "Agent should treat security concerns with appropriate urgency",
                "Agent should ask relevant security questions to assess the situation",
                "Agent should provide immediate security recommendations",
                "Agent should escalate to security team if needed",
                "Agent should help secure the account quickly",
                "Agent should provide follow-up security guidance"
            ])
        ],
        script=[
            scenario.user("URGENT: I think someone hacked my account! I'm seeing activity I didn't do!"),
            scenario.agent("I understand this is urgent and concerning. Let me help you secure your account immediately."),
            scenario.user("There are charges I didn't make and my password was changed! What do I do?!"),
            scenario.proceed()  # Let agent handle the security incident
        ],
        max_turns=10
    )
    
    assert result.success, f"Security incident scenario failed: {result.feedback}"


# Performance testing with scripted scenarios
@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_scripted_rapid_context_switching():
    """Test rapid context switching with scripted topic changes."""
    
    crew_adapter = create_crew_adapter()
    
    result = await scenario.run(
        name="scripted rapid context switching",
        description="""
        Customer rapidly switches between different topics and issues.
        Script the switches to test agent's ability to maintain context.
        """,
        agents=[
            crew_adapter,
            scenario.UserSimulatorAgent(),
            scenario.JudgeAgent(criteria=[
                "Agent should handle rapid topic changes gracefully",
                "Agent should maintain context for each separate issue",
                "Agent should not get confused by the switching",
                "Agent should address each topic appropriately",
                "Agent should organize the conversation effectively",
                "Agent should ensure all issues are resolved"
            ])
        ],
        script=[
            scenario.user("I need help with billing"),
            scenario.agent("I can help with billing questions. What specific billing issue are you experiencing?"),
            scenario.user("Actually, first I need to reset my password"),
            scenario.agent("Of course, I can help with password reset. Let me guide you through that process."),
            scenario.user("Wait, before that, is your API down? I'm getting errors"),
            scenario.proceed()  # Let agent handle the rapid switching
        ],
        max_turns=15
    )
    
    assert result.success, f"Rapid context switching scenario failed: {result.feedback}"


if __name__ == "__main__":
    # Run a single test for debugging
    import asyncio
    
    async def run_debug_test():
        """Run a single test for debugging purposes."""
        print("Running scripted error recovery test...")
        await test_scripted_error_recovery()
        print("Test completed!")
    
    # Uncomment to run debug test
    # asyncio.run(run_debug_test())


"""
Custom Judge Agents for CrewAI Customer Service Evaluation

This module contains specialized judge agents that evaluate specific aspects
of customer service interactions with domain-specific criteria and expertise.
"""

import json
import re
from typing import Dict, Any, List, Optional
import scenario
from scenario import AgentInput, AgentReturnTypes


class CustomerServiceQualityJudge(scenario.AgentAdapter):
    """
    Specialized judge for evaluating customer service quality.
    
    This judge focuses on soft skills, empathy, professionalism,
    and overall customer experience quality.
    """
    
    def __init__(self, model: str = "openai/gpt-4o"):
        """Initialize the customer service quality judge."""
        super().__init__()
        self.model = model
        self.evaluation_criteria = [
            "Empathy and emotional intelligence",
            "Professional tone and language",
            "Active listening and acknowledgment",
            "Clear and helpful communication",
            "Problem-solving approach",
            "Customer satisfaction focus"
        ]
    
    async def call(self, input: AgentInput) -> AgentReturnTypes:
        """Evaluate the customer service quality of the conversation."""
        conversation = self._extract_conversation(input.messages)
        
        evaluation_prompt = f"""
        You are an expert customer service quality evaluator. Analyze this customer service conversation and provide a detailed evaluation.

        CONVERSATION:
        {conversation}

        EVALUATION CRITERIA:
        {chr(10).join(f"- {criterion}" for criterion in self.evaluation_criteria)}

        Please provide:
        1. Overall quality score (1-10)
        2. Detailed analysis for each criterion
        3. Specific examples from the conversation
        4. Areas for improvement
        5. What the agent did well

        Format your response as JSON with the following structure:
        {{
            "overall_score": <1-10>,
            "criterion_scores": {{
                "empathy": <1-10>,
                "professionalism": <1-10>,
                "listening": <1-10>,
                "communication": <1-10>,
                "problem_solving": <1-10>,
                "customer_focus": <1-10>
            }},
            "detailed_analysis": "...",
            "positive_examples": ["..."],
            "areas_for_improvement": ["..."],
            "recommendation": "..."
        }}
        """
        
        # In a real implementation, you would call an LLM here
        # For this demo, we'll provide a structured evaluation
        return self._generate_quality_evaluation(conversation)
    
    def _extract_conversation(self, messages: List[Dict[str, Any]]) -> str:
        """Extract and format the conversation for evaluation."""
        conversation_parts = []
        for msg in messages:
            role = msg.get('role', 'unknown')
            content = msg.get('content', '')
            
            if role == 'user':
                conversation_parts.append(f"CUSTOMER: {content}")
            elif role == 'assistant':
                conversation_parts.append(f"AGENT: {content}")
        
        return "\n\n".join(conversation_parts)
    
    def _generate_quality_evaluation(self, conversation: str) -> str:
        """Generate a quality evaluation based on conversation analysis."""
        # Analyze conversation for quality indicators
        empathy_score = self._evaluate_empathy(conversation)
        professionalism_score = self._evaluate_professionalism(conversation)
        communication_score = self._evaluate_communication(conversation)
        
        overall_score = (empathy_score + professionalism_score + communication_score) / 3
        
        evaluation = {
            "overall_score": round(overall_score, 1),
            "criterion_scores": {
                "empathy": empathy_score,
                "professionalism": professionalism_score,
                "listening": self._evaluate_listening(conversation),
                "communication": communication_score,
                "problem_solving": self._evaluate_problem_solving(conversation),
                "customer_focus": self._evaluate_customer_focus(conversation)
            },
            "detailed_analysis": self._generate_detailed_analysis(conversation),
            "positive_examples": self._extract_positive_examples(conversation),
            "areas_for_improvement": self._identify_improvements(conversation),
            "recommendation": self._generate_recommendation(overall_score)
        }
        
        return json.dumps(evaluation, indent=2)
    
    def _evaluate_empathy(self, conversation: str) -> float:
        """Evaluate empathy shown in the conversation."""
        empathy_indicators = [
            "understand", "sorry", "apologize", "frustrating", "difficult",
            "appreciate", "thank you", "I can see", "I realize"
        ]
        
        score = 5.0  # Base score
        for indicator in empathy_indicators:
            if indicator.lower() in conversation.lower():
                score += 0.5
        
        return min(10.0, score)
    
    def _evaluate_professionalism(self, conversation: str) -> float:
        """Evaluate professionalism in the conversation."""
        professional_indicators = [
            "please", "thank you", "I'll help", "let me", "I can assist"
        ]
        unprofessional_indicators = [
            "whatever", "I don't know", "not my problem", "can't help"
        ]
        
        score = 7.0  # Base score
        for indicator in professional_indicators:
            if indicator.lower() in conversation.lower():
                score += 0.3
        
        for indicator in unprofessional_indicators:
            if indicator.lower() in conversation.lower():
                score -= 1.0
        
        return max(1.0, min(10.0, score))
    
    def _evaluate_communication(self, conversation: str) -> float:
        """Evaluate communication clarity and effectiveness."""
        # Simple heuristic based on response length and structure
        agent_responses = re.findall(r'AGENT: (.+?)(?=CUSTOMER:|$)', conversation, re.DOTALL)
        
        if not agent_responses:
            return 5.0
        
        avg_length = sum(len(response.split()) for response in agent_responses) / len(agent_responses)
        
        # Score based on response length (not too short, not too long)
        if 10 <= avg_length <= 50:
            return 8.0
        elif 5 <= avg_length < 10 or 50 < avg_length <= 100:
            return 6.0
        else:
            return 4.0
    
    def _evaluate_listening(self, conversation: str) -> float:
        """Evaluate active listening skills."""
        listening_indicators = [
            "you mentioned", "you said", "I understand that", "to clarify",
            "let me make sure", "if I understand correctly"
        ]
        
        score = 6.0
        for indicator in listening_indicators:
            if indicator.lower() in conversation.lower():
                score += 0.5
        
        return min(10.0, score)
    
    def _evaluate_problem_solving(self, conversation: str) -> float:
        """Evaluate problem-solving approach."""
        problem_solving_indicators = [
            "let me check", "I'll investigate", "here's what we can do",
            "solution", "resolve", "fix", "help you with"
        ]
        
        score = 5.0
        for indicator in problem_solving_indicators:
            if indicator.lower() in conversation.lower():
                score += 0.4
        
        return min(10.0, score)
    
    def _evaluate_customer_focus(self, conversation: str) -> float:
        """Evaluate customer-focused approach."""
        customer_focus_indicators = [
            "for you", "your needs", "your experience", "your satisfaction",
            "what works best", "your preference"
        ]
        
        score = 6.0
        for indicator in customer_focus_indicators:
            if indicator.lower() in conversation.lower():
                score += 0.3
        
        return min(10.0, score)
    
    def _generate_detailed_analysis(self, conversation: str) -> str:
        """Generate detailed analysis of the conversation."""
        return f"The conversation shows {'good' if len(conversation) > 200 else 'limited'} engagement between agent and customer. The agent demonstrates professional communication and attempts to address customer concerns systematically."
    
    def _extract_positive_examples(self, conversation: str) -> List[str]:
        """Extract positive examples from the conversation."""
        examples = []
        if "I understand" in conversation:
            examples.append("Agent showed empathy with 'I understand'")
        if "let me help" in conversation:
            examples.append("Agent offered proactive assistance")
        if "thank you" in conversation:
            examples.append("Agent maintained polite communication")
        
        return examples or ["Agent maintained professional tone throughout"]
    
    def _identify_improvements(self, conversation: str) -> List[str]:
        """Identify areas for improvement."""
        improvements = []
        if "sorry" not in conversation.lower():
            improvements.append("Could show more empathy and acknowledgment of customer concerns")
        if len(re.findall(r'AGENT:', conversation)) < 3:
            improvements.append("Could engage more actively in problem-solving")
        
        return improvements or ["Continue maintaining current service quality"]
    
    def _generate_recommendation(self, score: float) -> str:
        """Generate recommendation based on overall score."""
        if score >= 8.0:
            return "Excellent customer service quality. Continue current approach."
        elif score >= 6.0:
            return "Good customer service with room for improvement in empathy and communication."
        else:
            return "Customer service quality needs significant improvement. Focus on empathy, professionalism, and problem-solving."


class TechnicalAccuracyJudge(scenario.AgentAdapter):
    """
    Specialized judge for evaluating technical accuracy and competence.
    
    This judge focuses on technical knowledge, accuracy of solutions,
    and appropriateness of technical guidance.
    """
    
    def __init__(self, model: str = "openai/gpt-4o"):
        """Initialize the technical accuracy judge."""
        super().__init__()
        self.model = model
    
    async def call(self, input: AgentInput) -> AgentReturnTypes:
        """Evaluate the technical accuracy of the conversation."""
        conversation = self._extract_conversation(input.messages)
        
        # Analyze technical content
        technical_score = self._evaluate_technical_accuracy(conversation)
        solution_quality = self._evaluate_solution_quality(conversation)
        guidance_clarity = self._evaluate_guidance_clarity(conversation)
        
        evaluation = {
            "technical_accuracy_score": technical_score,
            "solution_quality_score": solution_quality,
            "guidance_clarity_score": guidance_clarity,
            "overall_technical_score": (technical_score + solution_quality + guidance_clarity) / 3,
            "technical_issues_identified": self._identify_technical_issues(conversation),
            "solution_completeness": self._evaluate_solution_completeness(conversation),
            "recommendation": self._generate_technical_recommendation(conversation)
        }
        
        return json.dumps(evaluation, indent=2)
    
    def _extract_conversation(self, messages: List[Dict[str, Any]]) -> str:
        """Extract conversation for technical analysis."""
        return "\n".join([f"{msg.get('role', 'unknown')}: {msg.get('content', '')}" for msg in messages])
    
    def _evaluate_technical_accuracy(self, conversation: str) -> float:
        """Evaluate technical accuracy of information provided."""
        # Look for technical terms and assess accuracy
        technical_terms = ["API", "authentication", "error", "code", "integration", "configuration"]
        
        score = 7.0  # Base score
        for term in technical_terms:
            if term.lower() in conversation.lower():
                score += 0.2  # Bonus for technical engagement
        
        # Check for common technical mistakes (simplified)
        if "restart your computer" in conversation.lower() and "API" in conversation:
            score -= 2.0  # Inappropriate solution for API issues
        
        return max(1.0, min(10.0, score))
    
    def _evaluate_solution_quality(self, conversation: str) -> float:
        """Evaluate the quality of technical solutions provided."""
        solution_indicators = [
            "step by step", "first", "then", "next", "finally",
            "check", "verify", "test", "try"
        ]
        
        score = 6.0
        for indicator in solution_indicators:
            if indicator.lower() in conversation.lower():
                score += 0.3
        
        return min(10.0, score)
    
    def _evaluate_guidance_clarity(self, conversation: str) -> float:
        """Evaluate clarity of technical guidance."""
        clarity_indicators = [
            "here's how", "follow these steps", "you need to",
            "make sure", "ensure that", "double-check"
        ]
        
        score = 6.0
        for indicator in clarity_indicators:
            if indicator.lower() in conversation.lower():
                score += 0.4
        
        return min(10.0, score)
    
    def _identify_technical_issues(self, conversation: str) -> List[str]:
        """Identify any technical issues in the conversation."""
        issues = []
        
        if "API" in conversation and "key" not in conversation.lower():
            issues.append("API discussion without mentioning authentication keys")
        
        if "error" in conversation.lower() and "code" not in conversation.lower():
            issues.append("Error discussion without requesting error codes")
        
        return issues
    
    def _evaluate_solution_completeness(self, conversation: str) -> str:
        """Evaluate completeness of solutions provided."""
        if "step" in conversation.lower() and len(conversation.split("step")) > 2:
            return "Complete - Multi-step solution provided"
        elif "try" in conversation.lower():
            return "Partial - Basic troubleshooting suggested"
        else:
            return "Incomplete - No clear solution provided"
    
    def _generate_technical_recommendation(self, conversation: str) -> str:
        """Generate technical recommendation."""
        if "API" in conversation:
            return "Good technical engagement. Consider providing more specific API documentation references."
        else:
            return "Maintain technical accuracy and provide step-by-step solutions."


class EscalationAppropriatenessJudge(scenario.AgentAdapter):
    """
    Specialized judge for evaluating escalation decisions.
    
    This judge focuses on when and how escalations are handled,
    ensuring appropriate escalation timing and process.
    """
    
    def __init__(self, model: str = "openai/gpt-4o"):
        """Initialize the escalation appropriateness judge."""
        super().__init__()
        self.model = model
    
    async def call(self, input: AgentInput) -> AgentReturnTypes:
        """Evaluate escalation appropriateness in the conversation."""
        conversation = self._extract_conversation(input.messages)
        
        escalation_analysis = {
            "escalation_needed": self._assess_escalation_need(conversation),
            "escalation_timing": self._evaluate_escalation_timing(conversation),
            "escalation_process": self._evaluate_escalation_process(conversation),
            "customer_satisfaction_with_escalation": self._evaluate_escalation_satisfaction(conversation),
            "escalation_score": self._calculate_escalation_score(conversation),
            "recommendations": self._generate_escalation_recommendations(conversation)
        }
        
        return json.dumps(escalation_analysis, indent=2)
    
    def _extract_conversation(self, messages: List[Dict[str, Any]]) -> str:
        """Extract conversation for escalation analysis."""
        return "\n".join([f"{msg.get('role', 'unknown')}: {msg.get('content', '')}" for msg in messages])
    
    def _assess_escalation_need(self, conversation: str) -> Dict[str, Any]:
        """Assess whether escalation was needed."""
        escalation_triggers = [
            "manager", "supervisor", "escalate", "higher level",
            "weeks", "months", "frustrated", "angry", "unacceptable"
        ]
        
        triggers_found = [trigger for trigger in escalation_triggers if trigger in conversation.lower()]
        
        return {
            "escalation_warranted": len(triggers_found) >= 2,
            "triggers_identified": triggers_found,
            "severity_level": "high" if len(triggers_found) >= 3 else "medium" if len(triggers_found) >= 1 else "low"
        }
    
    def _evaluate_escalation_timing(self, conversation: str) -> str:
        """Evaluate timing of escalation."""
        if "manager" in conversation.lower():
            # Count interactions before escalation
            parts = conversation.split("manager")
            if len(parts) > 1:
                pre_escalation = parts[0]
                interaction_count = pre_escalation.count("AGENT:")
                
                if interaction_count <= 2:
                    return "Too early - should attempt resolution first"
                elif interaction_count <= 5:
                    return "Appropriate timing"
                else:
                    return "Too late - should have escalated sooner"
        
        return "No escalation occurred"
    
    def _evaluate_escalation_process(self, conversation: str) -> Dict[str, Any]:
        """Evaluate the escalation process quality."""
        process_elements = {
            "explanation_provided": "escalate" in conversation.lower() or "manager" in conversation.lower(),
            "expectations_set": "will contact" in conversation.lower() or "within" in conversation.lower(),
            "information_gathered": "account" in conversation.lower() or "details" in conversation.lower(),
            "professional_handoff": "transfer" in conversation.lower() or "connect" in conversation.lower()
        }
        
        return process_elements
    
    def _evaluate_escalation_satisfaction(self, conversation: str) -> str:
        """Evaluate customer satisfaction with escalation handling."""
        satisfaction_indicators = ["thank you", "appreciate", "helpful"]
        dissatisfaction_indicators = ["still not", "waste of time", "ridiculous"]
        
        if any(indicator in conversation.lower() for indicator in satisfaction_indicators):
            return "Satisfied with escalation process"
        elif any(indicator in conversation.lower() for indicator in dissatisfaction_indicators):
            return "Dissatisfied with escalation process"
        else:
            return "Neutral - no clear satisfaction indicators"
    
    def _calculate_escalation_score(self, conversation: str) -> float:
        """Calculate overall escalation handling score."""
        need_assessment = self._assess_escalation_need(conversation)
        timing = self._evaluate_escalation_timing(conversation)
        process = self._evaluate_escalation_process(conversation)
        
        score = 5.0  # Base score
        
        # Adjust based on appropriateness
        if need_assessment["escalation_warranted"] and "manager" in conversation.lower():
            score += 2.0  # Correctly escalated when needed
        elif not need_assessment["escalation_warranted"] and "manager" not in conversation.lower():
            score += 1.0  # Correctly didn't escalate when not needed
        
        # Adjust based on timing
        if timing == "Appropriate timing":
            score += 1.0
        elif timing.startswith("Too"):
            score -= 1.0
        
        # Adjust based on process quality
        process_score = sum(1 for element in process.values() if element)
        score += process_score * 0.5
        
        return max(1.0, min(10.0, score))
    
    def _generate_escalation_recommendations(self, conversation: str) -> List[str]:
        """Generate recommendations for escalation handling."""
        recommendations = []
        
        need_assessment = self._assess_escalation_need(conversation)
        if need_assessment["escalation_warranted"] and "manager" not in conversation.lower():
            recommendations.append("Should have escalated to manager given customer frustration level")
        
        if "manager" in conversation.lower() and not any(phrase in conversation.lower() for phrase in ["will contact", "within"]):
            recommendations.append("Should set clear expectations for escalation timeline")
        
        if not recommendations:
            recommendations.append("Escalation handling was appropriate for this situation")
        
        return recommendations


# Factory functions for creating custom judges
def create_quality_judge(**kwargs) -> CustomerServiceQualityJudge:
    """Create a customer service quality judge."""
    return CustomerServiceQualityJudge(**kwargs)


def create_technical_judge(**kwargs) -> TechnicalAccuracyJudge:
    """Create a technical accuracy judge."""
    return TechnicalAccuracyJudge(**kwargs)


def create_escalation_judge(**kwargs) -> EscalationAppropriatenessJudge:
    """Create an escalation appropriateness judge."""
    return EscalationAppropriatenessJudge(**kwargs)


# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def test_custom_judges():
        """Test the custom judge functionality."""
        # Create sample conversation
        sample_messages = [
            {"role": "user", "content": "I'm having trouble with my account and I'm really frustrated!"},
            {"role": "assistant", "content": "I understand your frustration and I'm here to help. Let me look into your account issue right away."},
            {"role": "user", "content": "This has been going on for weeks! I want to speak to a manager!"},
            {"role": "assistant", "content": "I completely understand why you'd want to escalate this. Let me gather some information and connect you with my manager who can provide additional assistance."}
        ]
        
        # Create mock input
        class MockAgentInput:
            def __init__(self, messages):
                self.messages = messages
                self.thread_id = "test"
                self.judgment_request = True
        
        mock_input = MockAgentInput(sample_messages)
        
        # Test quality judge
        quality_judge = create_quality_judge()
        quality_result = await quality_judge.call(mock_input)
        print("Quality Judge Result:")
        print(quality_result)
        print("\n" + "="*50 + "\n")
        
        # Test escalation judge
        escalation_judge = create_escalation_judge()
        escalation_result = await escalation_judge.call(mock_input)
        print("Escalation Judge Result:")
        print(escalation_result)
    
    # Run the test
    asyncio.run(test_custom_judges())


# Architecture Overview

This document provides a detailed overview of the CrewAI + LangWatch Scenarios demo architecture.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    LangWatch Scenarios Layer                    │
├─────────────────┬─────────────────┬─────────────────────────────┤
│ UserSimulator   │   JudgeAgent    │     Custom Judges           │
│ Agent           │                 │  - Quality Judge            │
│                 │                 │  - Technical Judge          │
│                 │                 │  - Escalation Judge         │
└─────────────────┴─────────────────┴─────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Adapter Layer                                │
├─────────────────────────────────────────────────────────────────┤
│  CrewAI Adapter                                                 │
│  - Message formatting                                           │
│  - State management                                             │
│  - Error handling                                               │
│  - Conversation history                                         │
└─────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CrewAI Multi-Agent System                    │
├─────────────────┬─────────────────┬─────────────────────────────┤
│ Triage Agent    │ Technical Agent │    Billing Agent            │
│ - Route inquiries│ - API issues   │    - Payment issues         │
│ - Prioritize    │ - Troubleshoot  │    - Refunds               │
│ - Delegate      │ - Integration   │    - Subscriptions         │
└─────────────────┴─────────────────┴─────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Manager Agent                                │
├─────────────────────────────────────────────────────────────────┤
│  - Handle escalations                                           │
│  - Complex issue resolution                                     │
│  - Customer satisfaction                                        │
│  - Policy exceptions                                            │
└─────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Tools & Knowledge Base                       │
├─────────────────┬─────────────────┬─────────────────────────────┤
│ Knowledge Base  │ Customer Data   │    Ticketing System        │
│ Tool            │ Tool            │    Tool                     │
└─────────────────┴─────────────────┴─────────────────────────────┘
```

## Component Details

### 1. LangWatch Scenarios Layer

The top layer handles AI-powered testing and evaluation:

#### UserSimulatorAgent
- Simulates realistic customer behavior
- Adapts to different scenarios and personalities
- Generates natural conversation flows
- Responds to agent actions appropriately

#### JudgeAgent
- Evaluates conversation quality
- Applies success criteria
- Provides detailed feedback
- Determines pass/fail status

#### Custom Judges
- **Quality Judge**: Evaluates empathy, professionalism, communication
- **Technical Judge**: Assesses technical accuracy and solution quality
- **Escalation Judge**: Reviews escalation timing and process

### 2. Adapter Layer

The adapter layer bridges LangWatch and CrewAI:

#### CrewAI Adapter
```python
class CrewAIAdapter(scenario.AgentAdapter):
    async def call(self, input: AgentInput) -> AgentReturnTypes:
        # Extract user message
        user_message = input.last_new_user_message_str()
        
        # Get crew for this conversation
        crew = self._get_or_create_crew(input.thread_id)
        
        # Process through CrewAI
        response = crew.handle_inquiry(user_message, customer_id)
        
        # Format for LangWatch
        return self._format_crew_response(response)
```

Key responsibilities:
- **Message Translation**: Converts between LangWatch and CrewAI message formats
- **State Management**: Maintains conversation state across turns
- **Error Handling**: Gracefully handles failures and exceptions
- **Context Preservation**: Ensures conversation context is maintained

### 3. CrewAI Multi-Agent System

The core multi-agent system with specialized roles:

#### Agent Hierarchy
```
Manager Agent (Orchestrator)
├── Triage Agent (Router)
├── Technical Agent (Specialist)
├── Billing Agent (Specialist)
└── [Future agents can be added here]
```

#### Agent Roles

**Triage Agent**
- **Role**: Customer Service Triage Specialist
- **Goal**: Efficiently route customer inquiries to appropriate specialists
- **Capabilities**: 
  - Analyze inquiry type and priority
  - Route to appropriate specialist
  - Handle simple inquiries directly
  - Escalate when necessary

**Technical Agent**
- **Role**: Technical Support Specialist
- **Goal**: Resolve technical issues with clear, actionable solutions
- **Capabilities**:
  - API troubleshooting
  - Integration support
  - Step-by-step guidance
  - Error code interpretation

**Billing Agent**
- **Role**: Billing Support Specialist
- **Goal**: Handle billing inquiries and payment issues
- **Capabilities**:
  - Process refunds
  - Explain billing charges
  - Manage subscriptions
  - Handle payment disputes

**Manager Agent**
- **Role**: Customer Service Manager
- **Goal**: Handle escalated issues and ensure satisfaction
- **Capabilities**:
  - Complex issue resolution
  - Policy exceptions
  - Customer retention
  - Final decision authority

### 4. Tools & Knowledge Base

Shared tools available to all agents:

#### Knowledge Base Tool
```python
class KnowledgeBaseTool(BaseTool):
    def _run(self, query: str) -> str:
        # Search knowledge base for relevant information
        # Return structured response with solutions
```

#### Customer Data Tool
```python
class CustomerDataTool(BaseTool):
    def _run(self, customer_id: str) -> str:
        # Look up customer information and history
        # Return customer context and preferences
```

#### Ticketing Tool
```python
class TicketingTool(BaseTool):
    def _run(self, title: str, description: str, priority: str) -> str:
        # Create support ticket for tracking
        # Return ticket ID and status
```

## Data Flow

### 1. Scenario Execution Flow

```
1. LangWatch creates scenario with description and criteria
2. UserSimulatorAgent generates initial customer message
3. Message sent to CrewAI Adapter
4. Adapter extracts message and context
5. CrewAI processes through appropriate agents
6. Response formatted and returned to LangWatch
7. JudgeAgent evaluates the interaction
8. Process repeats until scenario completion
```

### 2. Message Flow

```
UserSimulator → LangWatch → Adapter → CrewAI → Tools → CrewAI → Adapter → LangWatch → Judge
```

### 3. State Management

Each conversation maintains:
- **Thread ID**: Unique identifier for conversation
- **Message History**: Complete conversation log
- **Customer Context**: Customer ID, preferences, history
- **Agent State**: Current agent handling the conversation
- **Tool Results**: Results from tool executions

## Integration Patterns

### 1. Adapter Pattern
The adapter pattern allows seamless integration between different frameworks:
- **Interface Compliance**: Implements LangWatch's AgentAdapter interface
- **Format Translation**: Converts between message formats
- **Error Isolation**: Prevents errors from propagating between systems

### 2. Observer Pattern
Custom judges observe conversations and provide evaluations:
- **Non-intrusive**: Don't affect conversation flow
- **Specialized**: Each judge focuses on specific aspects
- **Extensible**: New judges can be added easily

### 3. Strategy Pattern
Different testing strategies can be applied:
- **Basic Scenarios**: Standard conversation flows
- **Scripted Scenarios**: Controlled conversation paths
- **Edge Case Scenarios**: Unusual or difficult situations

## Scalability Considerations

### 1. Horizontal Scaling
- **Stateless Adapters**: Each adapter instance is independent
- **Thread Isolation**: Conversations don't interfere with each other
- **Load Distribution**: Multiple adapter instances can handle concurrent scenarios

### 2. Performance Optimization
- **Caching**: Scenario results can be cached for deterministic testing
- **Async Processing**: All operations are asynchronous
- **Resource Management**: Proper cleanup of conversation state

### 3. Monitoring and Observability
- **Logging**: Comprehensive logging at all levels
- **Metrics**: Performance and success rate tracking
- **Tracing**: End-to-end request tracing

## Security Considerations

### 1. Data Privacy
- **Customer Data**: Simulated data only, no real customer information
- **API Keys**: Secure storage and rotation of API keys
- **Conversation Logs**: Proper handling and retention policies

### 2. Access Control
- **Environment Isolation**: Separate environments for testing and production
- **Permission Management**: Proper access controls for different components
- **Audit Logging**: Track all system interactions

## Extension Points

### 1. Adding New Agents
```python
# Create new agent
new_agent = Agent(
    role="New Specialist",
    goal="Handle specific type of inquiry",
    backstory="...",
    tools=shared_tools
)

# Add to crew
crew.agents.append(new_agent)
```

### 2. Adding New Judges
```python
class CustomJudge(scenario.AgentAdapter):
    async def call(self, input: AgentInput) -> AgentReturnTypes:
        # Custom evaluation logic
        return evaluation_result
```

### 3. Adding New Tools
```python
class NewTool(BaseTool):
    name: str = "new_tool"
    description: str = "Description of what the tool does"
    
    def _run(self, input: str) -> str:
        # Tool implementation
        return result
```

## Best Practices

### 1. Agent Design
- **Single Responsibility**: Each agent has a clear, focused role
- **Clear Boundaries**: Well-defined handoff points between agents
- **Consistent Interface**: All agents use the same tool interface

### 2. Testing Strategy
- **Comprehensive Coverage**: Test happy paths, edge cases, and error conditions
- **Realistic Scenarios**: Use scenarios that reflect real-world usage
- **Continuous Testing**: Integrate testing into development workflow

### 3. Error Handling
- **Graceful Degradation**: System continues to function when components fail
- **Clear Error Messages**: Provide actionable error information
- **Recovery Mechanisms**: Automatic retry and fallback strategies

This architecture provides a robust, scalable foundation for AI agent testing while maintaining clear separation of concerns and extensibility for future enhancements.


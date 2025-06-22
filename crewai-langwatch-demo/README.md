# CrewAI + LangWatch Scenarios Demo

A comprehensive demonstration of how to use **LangWatch Scenarios** to test **CrewAI** multi-agent systems through AI-powered simulation testing.

## 🎯 What This Demo Shows

This demo showcases:
- **Multi-Agent System**: A customer service automation system built with CrewAI
- **AI-Powered Testing**: Using LangWatch scenarios to test agent behavior with AI simulators
- **Realistic Scenarios**: Edge cases, escalations, and complex multi-turn conversations
- **Advanced Testing**: Scripted scenarios, custom judges, and performance monitoring

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Input    │───▶│   CrewAI Agents  │◀───│ LangWatch Tests │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │                          │
                              ▼                          ▼
                       ┌──────────────┐         ┌──────────────┐
                       │ Triage Agent │         │ User Simulator│
                       │ Tech Agent   │         │ Judge Agent   │
                       │ Billing Agent│         │ Custom Judges │
                       │ Manager Agent│         └──────────────┘
                       └──────────────┘
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repo-url>
cd crewai-langwatch-demo

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your API keys
```

### 2. Basic Usage

```bash
# Run a simple demo
python main.py --demo basic

# Run all test scenarios
python main.py --test all

# Interactive mode
python main.py --interactive
```

### 3. Run with pytest

```bash
# Run all tests
pytest scenarios/ -v

# Run specific scenario
pytest scenarios/test_customer_service.py -v -s
```

## 📋 Demo Scenarios

### 1. **Happy Path Customer Service**
- User asks about billing issue
- System routes to billing agent
- Agent resolves issue efficiently

### 2. **Technical Support Escalation**
- Complex technical issue
- Multiple agent collaboration
- Escalation to manager when needed

### 3. **Edge Cases & Error Recovery**
- Unclear user requests
- System handles ambiguity
- Graceful error recovery

### 4. **Multi-Turn Conversations**
- Extended conversations
- Context maintenance
- Natural flow management

## 🧪 Testing Features

### LangWatch Scenarios Integration
- **UserSimulatorAgent**: Simulates realistic user behavior
- **JudgeAgent**: Evaluates conversation quality and success criteria
- **Custom Judges**: Domain-specific evaluation criteria
- **Scenario Caching**: Deterministic testing for CI/CD

### Advanced Testing
- **Scripted Scenarios**: Controlled conversation flows
- **Performance Monitoring**: Response times and resource usage
- **Edge Case Generation**: Automatic discovery of failure modes
- **Regression Testing**: Ensure improvements don't break existing functionality

## 📁 Project Structure

```
crewai-langwatch-demo/
├── agents/                 # CrewAI agent implementations
│   ├── customer_service_crew.py
│   ├── triage_agent.py
│   ├── technical_agent.py
│   └── billing_agent.py
├── adapters/              # LangWatch integration adapters
│   ├── crew_adapter.py
│   └── agent_adapter.py
├── scenarios/             # Test scenarios
│   ├── test_customer_service.py
│   ├── test_edge_cases.py
│   ├── advanced/
│   └── judges/
├── docs/                  # Documentation
├── examples/              # Jupyter notebook examples
├── cli/                   # Command-line interface
└── main.py               # Demo runner
```

## 🎓 Learning Objectives

After exploring this demo, you'll understand:

1. **Multi-Agent Architecture**: How to design and implement collaborative AI agent systems
2. **AI Testing Paradigms**: Using AI agents to test other AI agents
3. **Scenario-Based Testing**: Creating realistic test scenarios for complex AI systems
4. **Integration Patterns**: Connecting different AI frameworks effectively
5. **Production Readiness**: Testing strategies for deploying AI agents in production

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key
- `DEFAULT_MODEL`: Model for main agents (default: gpt-4o-mini)
- `JUDGE_MODEL`: Model for evaluation (default: gpt-4o)
- `MAX_TURNS`: Maximum conversation turns (default: 10)

### Customization
- Modify agent roles and goals in `agents/`
- Add new test scenarios in `scenarios/`
- Create custom judges in `scenarios/judges/`
- Adjust evaluation criteria for your use case

## 📊 Results and Analytics

The demo provides:
- **Test Results**: Pass/fail status with detailed feedback
- **Conversation Logs**: Full conversation transcripts
- **Performance Metrics**: Response times and token usage
- **Quality Scores**: Evaluation results from judge agents
- **Trend Analysis**: Performance over time

## 🤝 Contributing

This demo is part of the AI Engineering Hub. Contributions welcome!

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Submit a pull request

## 📚 Further Reading

- [LangWatch Scenarios Documentation](https://scenario.langwatch.ai/)
- [CrewAI Documentation](https://docs.crewai.com/)
- [AI Agent Testing Best Practices](./docs/best-practices.md)
- [Advanced Integration Patterns](./docs/advanced-patterns.md)

## 🆘 Troubleshooting

Common issues and solutions:

1. **API Key Issues**: Ensure your `.env` file is properly configured
2. **Model Availability**: Check that your API keys have access to the specified models
3. **Rate Limits**: Adjust `MAX_TURNS` if hitting rate limits
4. **Memory Issues**: Use caching for large test suites

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.


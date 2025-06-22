# Setup Guide

This guide will help you set up and run the CrewAI + LangWatch Scenarios demo on your local machine.

## Prerequisites

Before you begin, ensure you have the following:

- **Python 3.8+** installed on your system
- **OpenAI API key** (required for LLM interactions)
- **Git** for cloning the repository
- **Terminal/Command Prompt** access

## Step 1: Clone the Repository

```bash
git clone <repository-url>
cd ai-engineering-hub/crewai-langwatch-demo
```

## Step 2: Create Virtual Environment

It's recommended to use a virtual environment to avoid conflicts with other Python projects:

### Using venv (recommended)
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Using conda
```bash
conda create -n crewai-langwatch python=3.9
conda activate crewai-langwatch
```

## Step 3: Install Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

### Core Dependencies Installed
- **crewai**: Multi-agent framework
- **langwatch-scenario**: AI testing framework
- **openai**: OpenAI API client
- **litellm**: Multi-LLM provider support
- **python-dotenv**: Environment variable management
- **rich**: Beautiful console output
- **pytest**: Testing framework

## Step 4: Environment Configuration

### Create Environment File
Copy the example environment file and configure it:

```bash
cp .env.example .env
```

### Edit the .env File
Open `.env` in your favorite text editor and configure the following:

```bash
# Required: OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Optional: LangWatch Configuration
LANGWATCH_API_KEY=your_langwatch_api_key_here
LANGWATCH_ENDPOINT=https://app.langwatch.ai

# Optional: Model Configuration
DEFAULT_MODEL=openai/gpt-4o-mini
JUDGE_MODEL=openai/gpt-4o
SIMULATOR_MODEL=openai/gpt-4o-mini

# Optional: Testing Configuration
MAX_TURNS=10
CACHE_ENABLED=true
DEBUG_MODE=false

# Optional: Logging
LOG_LEVEL=INFO
```

### Getting Your OpenAI API Key

1. Go to [OpenAI's website](https://platform.openai.com/)
2. Sign up or log in to your account
3. Navigate to the API section
4. Create a new API key
5. Copy the key and paste it in your `.env` file

⚠️ **Important**: Keep your API key secure and never commit it to version control.

## Step 5: Verify Installation

Test that everything is set up correctly:

```bash
python main.py --info
```

You should see output showing your system configuration. Look for:
- ✅ OpenAI API Key: Set
- All other configuration values

## Step 6: Run Your First Demo

### Basic Demo
Run the basic CrewAI demonstration:

```bash
python main.py --demo basic
```

This will:
- Initialize the customer service crew
- Run several test inquiries
- Show agent responses
- Save results to the `results/` directory

### Interactive Mode
Try the interactive chat mode:

```bash
python main.py --interactive
```

This allows you to chat directly with the customer service system.

## Step 7: Run LangWatch Scenarios

### Install LangWatch Scenarios
If you haven't already, ensure LangWatch scenarios is installed:

```bash
pip install langwatch-scenario
```

### Run Basic Scenarios
```bash
python main.py --test basic
```

### Run All Scenarios
```bash
python main.py --test all
```

### Run with pytest
```bash
pytest scenarios/ -v
```

## Step 8: Explore the Jupyter Notebook

Launch Jupyter and explore the interactive examples:

```bash
jupyter notebook examples/basic_usage.ipynb
```

The notebook provides a step-by-step walkthrough of all features.

## Troubleshooting

### Common Issues and Solutions

#### 1. Import Errors
**Problem**: `ModuleNotFoundError` when running scripts

**Solution**: 
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`
- Check Python path: `python -c "import sys; print(sys.path)"`

#### 2. API Key Issues
**Problem**: Authentication errors or "API key not found"

**Solution**:
- Verify `.env` file exists and contains `OPENAI_API_KEY=your_key`
- Check that the key is valid on OpenAI's platform
- Ensure no extra spaces or quotes around the key

#### 3. Model Access Issues
**Problem**: "Model not found" or permission errors

**Solution**:
- Verify your OpenAI account has access to the specified models
- Try using `gpt-3.5-turbo` instead of `gpt-4` models
- Check your OpenAI usage limits and billing status

#### 4. LangWatch Scenarios Issues
**Problem**: Scenarios fail to run or import errors

**Solution**:
- Ensure `langwatch-scenario` is installed: `pip install langwatch-scenario`
- Check that all dependencies are compatible
- Try running a simple scenario first

#### 5. Performance Issues
**Problem**: Slow response times or timeouts

**Solution**:
- Reduce `MAX_TURNS` in your `.env` file
- Use faster models like `gpt-3.5-turbo`
- Check your internet connection
- Monitor OpenAI API rate limits

#### 6. Memory Issues
**Problem**: Out of memory errors during testing

**Solution**:
- Reduce the number of concurrent scenarios
- Clear conversation history regularly
- Use `CACHE_ENABLED=true` to avoid redundant API calls

### Getting Help

If you encounter issues not covered here:

1. **Check the logs**: Look in the console output for detailed error messages
2. **Enable debug mode**: Set `DEBUG_MODE=true` in your `.env` file
3. **Review the documentation**: Check the [architecture guide](architecture.md)
4. **Search existing issues**: Look for similar problems in the repository issues
5. **Create an issue**: If you find a bug, please report it with:
   - Your operating system and Python version
   - Complete error message
   - Steps to reproduce the issue
   - Your configuration (without API keys)

## Advanced Configuration

### Custom Models

You can use different models for different components:

```bash
# Use different models for different purposes
DEFAULT_MODEL=openai/gpt-4o-mini          # Main agents
JUDGE_MODEL=openai/gpt-4o                 # Evaluation (more capable)
SIMULATOR_MODEL=openai/gpt-3.5-turbo      # User simulation (faster)
```

### Using Other LLM Providers

The demo supports multiple LLM providers through LiteLLM:

```bash
# Anthropic Claude
DEFAULT_MODEL=anthropic/claude-3-sonnet-20240229

# Google Gemini
DEFAULT_MODEL=gemini/gemini-pro

# Local models (Ollama)
DEFAULT_MODEL=ollama/llama2
```

### Performance Tuning

For better performance:

```bash
# Enable caching for deterministic results
CACHE_ENABLED=true

# Reduce conversation length
MAX_TURNS=6

# Use faster models
DEFAULT_MODEL=openai/gpt-3.5-turbo
```

### Development Mode

For development and debugging:

```bash
# Enable detailed logging
DEBUG_MODE=true
LOG_LEVEL=DEBUG

# Disable caching to see fresh results
CACHE_ENABLED=false
```

## Next Steps

Once you have the demo running:

1. **Explore the Examples**: Work through the Jupyter notebook
2. **Customize Agents**: Modify agent roles and capabilities
3. **Create New Scenarios**: Add your own test scenarios
4. **Build Custom Judges**: Create domain-specific evaluation criteria
5. **Integrate with CI/CD**: Set up automated testing
6. **Scale the System**: Deploy for production use

## Directory Structure

After setup, your directory should look like:

```
crewai-langwatch-demo/
├── agents/                 # CrewAI agent implementations
├── adapters/              # LangWatch integration
├── scenarios/             # Test scenarios
├── docs/                  # Documentation
├── examples/              # Jupyter notebooks
├── results/               # Test results (created automatically)
├── .env                   # Your environment configuration
├── requirements.txt       # Python dependencies
├── main.py               # Main demo runner
└── README.md             # Project overview
```

## Security Best Practices

1. **Never commit API keys**: Always use `.env` files and add them to `.gitignore`
2. **Rotate keys regularly**: Change your API keys periodically
3. **Monitor usage**: Keep track of your API usage and costs
4. **Use environment-specific keys**: Different keys for development, testing, and production
5. **Limit key permissions**: Use keys with minimal required permissions

## Support

For additional support:
- 📚 [Documentation](../README.md)
- 🏗️ [Architecture Guide](architecture.md)
- 💡 [Best Practices](best-practices.md)
- 🐛 [Issue Tracker](https://github.com/your-repo/issues)

Happy building! 🚀


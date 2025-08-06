# Random Topic Summary Flow

A simple CrewAI Flow that generates a random topic, then generates a summary for that topic using OpenAI's API, and finally logs the result in a file.

## Prerequisites

- Python 3.10+
- Install dependencies:
  ```bash
  pip install crewai openai python-dotenv pydantic
  ```

- Set `OPENAI_API_KEY` environment variable or create a `.env` file with:
  ```
  OPENAI_API_KEY=your_openai_api_key
  ```

## Usage

```bash
python -m random_topic_summary_flow.main
```

The flow will generate a random topic, summarize it, and save the output to `topic_summary.txt`.
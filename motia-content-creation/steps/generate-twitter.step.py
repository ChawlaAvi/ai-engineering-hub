import os
import json
from pydantic import BaseModel, HttpUrl
from ollama import AsyncClient
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class GenerateInput(BaseModel):
    requestId: str
    url: HttpUrl
    title: str
    content: str
    timestamp: int

config = {
    'type': 'event',
    'name': 'TwitterGenerate',
    'description': 'Generates Twitter content',
    'subscribes': ['generate-content'],
    'emits': ['twitter-schedule'],
    'input': GenerateInput.model_json_schema(),
    'flows': ['content-generation']
}

async def handler(input, context):
    try:
        with open("prompts/twitter-prompt.txt", "r", encoding='utf-8') as f:
            twitterPromptTemplate = f.read()
        
        twitterPrompt = twitterPromptTemplate.replace('{{title}}', input['title']).replace('{{content}}', input['content'])

        context.logger.info("🔄 Twitter content generation started...")

        ollama_client = AsyncClient()
        response = await ollama_client.chat(model=os.getenv('OLLAMA_MODEL'), messages=[{'role': 'user', 'content': twitterPrompt}])

        try:
            twitter_content = json.loads(response.message.content)
        except Exception:
            twitter_content = {'text': response.message.content}

        context.logger.info(f"🎉 Twitter content generated successfully!")

        await context.emit({
            'topic': 'twitter-schedule',
            'data': {
                'requestId': input['requestId'],
                'url': input['url'],
                'title': input['title'],
                'content': twitter_content,
                'generatedAt': datetime.now().isoformat(),
                'originalUrl': input['url']
            }
        })
    except Exception as e:
        context.logger.error(f"❌ Content generation failed: {e}")
        raise e
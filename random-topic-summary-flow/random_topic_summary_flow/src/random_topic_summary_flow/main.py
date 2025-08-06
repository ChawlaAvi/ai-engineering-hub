#!/usr/bin/env python
import asyncio
import random
import os
import openai
from dotenv import load_dotenv
from pydantic import BaseModel
from crewai.flow import Flow, listen, start

load_dotenv()


class TopicState(BaseModel):
    topic: str = ""
    summary: str = ""


class TopicFlow(Flow[TopicState]):

    @start()
    def generate_topic(self):
        print("Generating random topic")
        topics = [
            "Artificial Intelligence",
            "Machine Learning",
            "Natural Language Processing",
            "Robotics",
            "Computer Vision",
            "Data Science",
            "Reinforcement Learning",
            "Deep Learning",
            "Neural Networks",
            "Generative Models",
        ]
        self.state.topic = random.choice(topics)
        print(f"Topic generated: {self.state.topic}")

    @listen(generate_topic)
    def generate_summary(self):
        print(f"Generating summary for topic: {self.state.topic}")
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Provide a concise summary for the topic: {self.state.topic}"}
            ]
        )
        self.state.summary = response.choices[0].message.content.strip()
        print("Summary generated")

    @listen(generate_summary)
    def log_results(self):
        print("Logging topic and summary to file")
        with open("topic_summary.txt", "w") as f:
            f.write(f"Topic: {self.state.topic}\n")
            f.write("Summary:\n")
            f.write(self.state.summary + "\n")
        print("Results logged to topic_summary.txt")


def kickoff():
    flow = TopicFlow()
    asyncio.run(flow.kickoff_async())


if __name__ == "__main__":
    kickoff()
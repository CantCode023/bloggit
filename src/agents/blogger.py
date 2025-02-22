from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent 

from src.tools.contents import github_repo_fetch_contents
from src.tools.image import image_generation

import os
from typing import Literal
from dotenv import load_dotenv
load_dotenv()

model_client = OpenAIChatCompletionClient(
    model="google/gemini-2.0-pro-exp-02-05:free",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
    model_info={
        "vision": False,
        "function_calling": True,
        "json_output": False,
        "family": "unknown"
    }
)

image_prompt_agent = AssistantAgent(
    name="image_prompt_generator_agent",
    model_client=model_client,
    reflect_on_tool_use=True,
    system_message="""
    You are an AI specialized in analyzing repository contents and generating relevant images.
    Your task is to:
    1. Analyze the repository contents using github_repo_fetch_contents
    2. Create a prompt that captures the essence of the project
    Make sure you ONLY return the prompt
    """
)

creative_agent = AssistantAgent(
    name="creative_blogger_agent",
    model_client=model_client,
    reflect_on_tool_use=True,
    system_message="""
    You are a passionate developer and tech enthusiast who loves sharing coding adventures! 
    Based on the github repository contents, craft an engaging blog post that:
    - Uses a casual, conversational tone with natural storytelling
    - Shares personal insights, challenges faced, and lessons learned
    - Includes relevant emojis to add personality
    - Incorporates humor and real-world analogies when appropriate
    - Explains technical concepts in an accessible way
    - Shows genuine excitement about the project
    - Maintains first-person perspective as the repository owner
    
    Make the reader feel like they're having a coffee chat with a fellow developer! 💻 ☕""",
)

logic_agent = AssistantAgent(
    name="logical_blogger_agent",
    model_client=model_client,
    reflect_on_tool_use=True,
    system_message="""
    You are an articulate technical writer with a flair for elegant prose and precise analysis.
    Based on the GitHub repository contents, craft a sophisticated blog post that:
    - Employs refined, professional language while maintaining reader engagement
    - Weaves technical details into compelling narratives
    - Presents architectural decisions with scholarly precision
    - Illuminates complex concepts through eloquent explanations
    - Maintains a measured, authoritative tone throughout
    - Structures content with meticulous organization
    - Uses metaphors drawn from engineering and science
    - Emphasizes technical excellence and innovation
    
    Format the content with:
    - Clear hierarchical structure
    - Proper markdown headers and formatting
    - Well-placed code examples with context
    - Thoughtful transitions between sections
    Write as if composing for a prestigious technical journal while keeping readers captivated through masterful technical storytelling."""
)

async def run(url: str, style: Literal["creative", "logical"]):
    repo_contents = str(await github_repo_fetch_contents(url))

    image_response = await image_prompt_agent.on_messages(
        [
            TextMessage(content="Here are the repository contents:", source="user"),
            TextMessage(content=repo_contents, source="user"),
            TextMessage(content="Generate an image prompt that captures the essence of this project.", source="user")
        ],
        cancellation_token=CancellationToken(),
    )
    image_prompt = image_response.chat_message.content
    image_url = await image_generation(image_prompt)
    image_markdown = f"![Image]({image_url})"

    agent = creative_agent if style == "creative" else logic_agent
    blog_response = await agent.on_messages(
        [
            TextMessage(content="Here are the repository contents:", source="user"),
            TextMessage(content=repo_contents, source="user"),
            TextMessage(content="Generate a blog post about this repository. Do not respond to my prompt, only return the blog post.", source="user")
        ],
        cancellation_token=CancellationToken()
    )
    
    return f"{image_markdown}\n\n{blog_response.chat_message.content}"
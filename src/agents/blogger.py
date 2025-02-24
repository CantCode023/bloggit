from autogen_agentchat.messages import ModelClientStreamingChunkEvent, TextMessage
from autogen_core import CancellationToken

from src.agents.image import image_prompt_agent
from src.agents.creative import creative_agent
from src.agents.logical import logic_agent

from src.tools.contents import github_repo_fetch_contents
from src.tools.image import image_generation

from typing import Literal
import asyncio
import nest_asyncio
nest_asyncio.apply()

async def run_tools(url: str):
    repo_contents = str(await github_repo_fetch_contents(url))

    image_response = await image_prompt_agent.on_messages(
        [
            TextMessage(content="Here are the repository contents:", source="user"),
            TextMessage(content=repo_contents, source="user"),
        ],
        cancellation_token=CancellationToken(),
    )
    image_prompt = image_response.chat_message.content
    image_url = ""
    if isinstance(image_prompt, str):
        image_url = await image_generation(image_prompt)
    image_markdown = f"![Image]({image_url})"

    return image_markdown, repo_contents

def get_agent(style: Literal["creative", "logical"]):
    return creative_agent if style == "creative" else logic_agent

async def stream_blog(repo_contents: str, style: Literal["creative", "logical"]):
    agent = get_agent(style)

    async for chunk in agent.on_messages_stream([
        TextMessage(content="Here are the repository contents:", source="user"),
        TextMessage(content=repo_contents, source="user"),
    ], cancellation_token=CancellationToken()):
        if isinstance(chunk, ModelClientStreamingChunkEvent) and chunk.content:
            yield chunk.content
            await asyncio.sleep(0.01)
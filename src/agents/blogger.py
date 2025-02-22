from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken

from src.agents.image import image_prompt_agent
from src.agents.creative import creative_agent
from src.agents.logical import logic_agent

from src.tools.contents import github_repo_fetch_contents
from src.tools.image import image_generation

from typing import Literal

async def run(url: str, style: Literal["creative", "logical"]):
    repo_contents = str(await github_repo_fetch_contents(url))

    image_response = await image_prompt_agent.on_messages(
        [
            TextMessage(content="Here are the repository contents:", source="user"),
            TextMessage(content=repo_contents, source="user"),
        ],
        cancellation_token=CancellationToken(),
    )
    image_prompt = image_response.chat_message.content
    image_url=""
    if isinstance(image_prompt, str):
        image_url = image_generation(image_prompt)
    image_markdown = f"![Image]({image_url})"

    agent = creative_agent if style == "creative" else logic_agent
    blog_response = await agent.on_messages(
        [
            TextMessage(content="Here are the repository contents:", source="user"),
            TextMessage(content=repo_contents, source="user"),
        ],
        cancellation_token=CancellationToken()
    )
    
    return f"{image_markdown}\n\n{blog_response.chat_message.content}"
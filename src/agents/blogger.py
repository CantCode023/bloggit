from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent 

import os
from dotenv import load_dotenv
load_dotenv()

model_client = OpenAIChatCompletionClient(
    model="deepseek/deepseek-chat:free",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
    model_info={
        "vision": False,
        "function_calling": True,
        "json_output": False,
        "family": "unknown"
    }
)

agent = AssistantAgent(
    name="blogger_agent",
    model_client=model_client,
    tools=[],
    reflect_on_tool_use=True,
    system_message="Based on the github repository contents, generate a blog about the project.",
)
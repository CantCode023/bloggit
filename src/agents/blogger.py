from autogen_core.models import UserMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
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

from src.agents.client import model_client
from autogen_agentchat.agents import AssistantAgent 

image_prompt_agent = AssistantAgent(
    name="image_prompt_generator_agent",
    model_client=model_client,
    system_message="""
    You are an AI specialized in analyzing repository contents and generating relevant images.
    Your task is to: Create a prompt that captures the essence of the project
    Make sure you ONLY return the prompt.
    """
)
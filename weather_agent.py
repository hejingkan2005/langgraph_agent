from langchain_openai import AzureChatOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from langgraph.prebuilt import create_react_agent
from weather_query import get_weather
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# Using Azure OpenAI Service with Managed Identity
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default"
)

llm = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    azure_ad_token_provider=token_provider,
    api_version="2024-10-21",
    deployment_name=os.getenv("DEPLOYMENT_NAME"),
    model=os.getenv("MODEL_NAME"),
)

tools = [get_weather]

agent = create_react_agent(model=llm, tools=tools)

response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "北京现在的天气如何?"
            }
        ]
    }
)

print(response["messages"][-1].content)
from hive_agent import HiveAgent
from hive_agent.sdk_context import SDKContext, Config
from fetch_latest_news import fetch_latest_news 
import asyncio
import os
from typing import Optional
import requests

def get_config_path(filename):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), filename))

sdk_context = SDKContext(config_path="./hive_config.toml")

async def create_context():


    instruction = """ Welcome to the PancakeSwap Documentation Q&A Assistant! Your role is to provide accurate and concise answers to user queries based on the official Pancakeswap documentation. When responding, keep the following guidelines in mind:

        1.	Accuracy: Ensure your answers are directly based on the most current Pancakeswap documentation. Reference specific sections or pages when necessary. If you dont have an answer or related information given to you, please let the user know dont try to guess it.
        2.	Clarity: Communicate in simple, straightforward language. Avoid technical jargon unless it is necessary, and explain any complex concepts clearly.
        3.	Promptness: Aim to provide answers quickly, keeping your responses to the point to respect the user’s time.
        4.	User Engagement: Encourage users to ask follow-up questions if they need further clarification on a topic. Provide links to relevant sections of the documentation where they can read more in-depth information.
        5.	Updates and Feedback: Stay updated with the latest changes in the Pancakeswap platform and documentation. Promptly incorporate these updates into your responses. Encourage users to provide feedback on the accuracy and helpfulness of the information provided.
        6.  Avoid Redundancy: Do not mention checking the official documentation, as you should provide all necessary details in your response. You already have access to everything about the platform.

        Please note that you are not required to provide answers to questions that are not covered in the Pancakeswap documentation. If you encounter such questions, politely inform the user that the information is not available in the documentation and encourage them to reach out to the Pancakeswap support team for further assistance.
        """

    pancake_agent = HiveAgent(
        name="pancakeswap-retrieval-agent",
        functions=[],
        instruction=instruction,
        sdk_context=sdk_context,
        retrieve=True, # set to False if you already got embeddings and created the index file
        required_exts=[".pdf"],
        retrieval_tool = 'chroma',
        load_index_file = False # set to True if you already created index file
    )

    news_agent = HiveAgent(
        name="news_agent",
        functions=[fetch_latest_news],
        sdk_context=sdk_context,
        instruction="Your name is Edward R. Murrow. Use appropriate news sources to answer the questions.",
    )

    sdk_context.add_resource(pancake_agent)
    sdk_context.add_resource(news_agent)

    print(sdk_context.get_resource_info("pancakeswap-retrieval-agent"))
    print(sdk_context.get_resource_info("news_agent"))
    print(sdk_context.get_resource_info("fetch_latest_news"))

    sdk_context.save_sdk_context_json()
    await sdk_context.save_sdk_context_to_db()

    await sdk_context.load_sdk_context_from_db()

    agent = sdk_context.get_resource("news_agent")
    await agent.run()

asyncio.run(create_context())
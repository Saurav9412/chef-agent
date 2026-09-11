from pprint import pprint
from utils import (
    extract_recipe_info, 
    get_placeholders, 
    get_gemini, 
    get_groq,
    intent_to_prompt_context
)
from models import UserInputSchema
from tools import search_recipe_in_web
import random, logging
from logging_config import setup_logging
from langchain.agents import create_agent
import os

print("Tracing: ", os.getenv("LANGSMITH_TRACING"))
print("Langsmith Project: ", os.getenv("LANGSMITH_PROJECT"))
print("LangSmith API key: ", bool(os.getenv("LANGSMITH_API_KEY")))

setup_logging()

logger = logging.getLogger(__name__)

def main():
    logger.info("Starting recipe extraction application")

    placeholders = get_placeholders()
    try:
        _ = random.randint(0, len(placeholders))

        user_request = input(placeholders[_])
        extracted_info = extract_recipe_info(
            UserInputSchema(
                prompt = user_request
            )
        )
        sm = """U are a helpful agent please try to search for recipes for now using the tool given on;ly use it if needed"""
        agent = create_agent(
            get_groq(),
            tools=[search_recipe_in_web],
            system_prompt=sm
        )
        logger.info(f"{extracted_info = }\n")
        context = intent_to_prompt_context(extracted_info)
        logger.info(f"parsed intent: {context}")
        history = {
            "messages":[
                {
                    "role": "user",
                    "content": context
                }
            ]
        }
        response = agent.invoke(
            history
        )
        pprint(response)
    except Exception as e:
        logger.error(f"Application failed during execution: {str(e)}", exc_info=True)
    
if __name__=="__main__":
    main()
from pprint import pprint
from utils import extract_recipe_info, get_placeholders
from models import UserInputSchema
import random, logging
from logging_config import setup_logging

setup_logging()

logger = logging.getLogger(__name__)

def main(prompt: UserInputSchema):
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
        pprint(extracted_info)
    except Exception as e:
        logger.error(f"Application failed during execution: {str(e)}", exc_info=True)
    
if __name__=="__main__":
    main()
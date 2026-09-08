import os
import logging
from dotenv import load_dotenv
from langchain_tavily import TavilySearch
from logging_config import setup_logging

load_dotenv()
setup_logging()

logger = logging.getLogger(__name__)

def search_web_tavily(
    search_query: str,
    max_results: int 
) -> dict:
    tool = TavilySearch(
    max_results=1,
    topic="general",
    # include_answer=False,
    # include_raw_content=False,
    # include_images=False,
    # include_image_descriptions=False,
    # search_depth="basic",
    # time_range="day",
    # include_domains=None,
    # exclude_domains=None,
    # country=None
    # include_favicon=False
    # include_usage=False
)
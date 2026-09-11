import os
import logging
from dotenv import load_dotenv
from langchain_tavily import TavilySearch
from logging_config import setup_logging
from typing import Literal, List
from langchain_core.tools import tool

load_dotenv()
setup_logging()

logger = logging.getLogger(__name__)

@tool
def search_recipe_in_web(
    search_query: str,
    max_results:int=5,
    topic:Literal["general","news","finance"]="general",
    include_answer:bool=False,
    include_raw_content:bool=False,
    include_images:bool=False,
    include_image_descriptions:bool=False,
    search_depth:Literal["basic","advanced"]="basic",
    time_range:Literal["day","week","month","year"]=None,
    include_domains:List[str]=None,
    exclude_domains:List[str]=None
) -> dict[str: any]:
    """    
    Search the web broadly for recipe pages matching the user's recipe intent.

    Use this tool when external recipe information is needed, especially when
    the user asks to find, discover, compare, or recommend recipes from the web,
    or when the request depends on recipes that may vary by source.

    This is a DISCOVERY tool. It returns candidate recipe pages, titles,
    snippets, URLs, and relevance scores. It does NOT guarantee that the
    complete recipe, ingredient quantities, or cooking instructions are present
    in the search result.

    Build keywords from the user's extracted recipe intent rather than passing
    the entire conversation. Include the dish, important ingredients, cuisine,
    dietary requirements, and other meaningful constraints.

    Do NOT use this tool when the user only asks for a generic recipe that can
    be generated reliably from existing culinary knowledge and no current,
    source-specific, or web-based information is required.

    Args:
        max_results: Maximum number of search results to return. Default is 5.
        topic: Type of search vertical to execute. Options are "general", "news", or "finance". Default is "general".
        include_answer: Whether to include a short text answer or summary generated from the results. Default is False.
        include_raw_content: Whether to return the full, raw HTML or parsed body content of the search results. Default is False.
        include_images: Whether to include image URLs in the search output. Default is False.
        include_image_descriptions: Whether to extract and include text descriptions or alt-text for discovered images. Default is False.
        search_depth: The thoroughness of the search engine crawling. Options are "basic" or "advanced". Default is "basic".
        time_range: Filters results published within a specific window. Options are "day", "week", "month", "year", or None. Default is None.
        include_domains: A strict list of specific domain strings to restrict the search to. Default is None.
        exclude_domains: A list of specific domain strings to completely block or filter out from results. Default is None.


    Returns:
        A dictionary containing the generated search query and normalized
        candidate recipe results. Each result contains the title, URL, snippet,
        and Tavily relevance score.
    """
    TAVILY = TavilySearch(
        api_key = os.getenv("TAVILY_API_KEY"),
        max_results=max_results,
        topic=topic,
        include_answer=include_answer,
        include_raw_content=include_raw_content,
        include_images=include_images,
        include_image_descriptions=include_image_descriptions,
        search_depth=search_depth,
        time_range=time_range,
        include_domains=include_domains,
        exclude_domains=exclude_domains
    )

    results = TAVILY.invoke(
        {
            "query":search_query
        }
    )
    return results
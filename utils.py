import requests
import os, json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from prompts import *
from models import *

load_dotenv()

def intent_to_prompt_context(
        intent: RecipeSearchIntent
    ) -> str:
    data = intent.model_dump(exclude_none=True)
    data = {k:v for k,v in data.items() if v not in ("",[],None)}
    return json.dumps(data, indent=2)

def extract_recipe_info(user_query: UserInputSchema) -> RecipeSearchIntent:
    """
    Extracts structured recipe search intent from the user's query.
    
    Args:
        user_query (UserInputSchema): The user's recipe request.
        
    Returns:
        RecipeSearchIntent: Structured information about the user's recipe search intent.
    
    """
    structured_groq = get_groq().with_structured_output(
        RecipeSearchIntent,
        include_raw=False
    )
    structured_gemini = get_gemini().with_structured_output(
        RecipeSearchIntent,
        include_raw=False
    )
    llm = structured_groq.with_fallbacks([structured_gemini])

    chain = extraction_prompt | llm
    return chain.invoke({"user_input": user_query.prompt})

def get_groq(
        temperature: float|None = 0.6,
        top_p: float|None = 0.9,
        max_output_tokens: int|None = 1024
    ) -> ChatGroq:
    return ChatGroq(
        model = os.getenv("GROQ_MODEL"),
        api_key = os.getenv("GROQ_API_KEY"),
        temperature = temperature
    )

def get_available_models_groq():
    api_key = os.getenv("GROQ_API_KEY")
    url = "https://api.groq.com/openai/v1/models"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers).json()

    for item in response["data"]:
        print(item["id"], "\n")

def get_gemini(
        temperature: float|None = 0.3,
        top_p: float|None = 0.7,
        max_output_tokens: int|None =  1024
    ) -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        model = os.getenv("GEMINI_MODEL"),
        api_key = os.getenv("GEMINI_API_KEY")
    )

def get_placeholders() -> list:
    placeholders = [
        # 🍳 Simple / general
        "What would you like to cook today?",
        "What ingredients do you have?",
        "Tell me what you're craving...",
        "What can I help you cook?",
        "Ask me for a recipe...",

        # 🥦 Ingredient-based

        "I have chicken, rice, and broccoli...",
        "I have eggs, tomatoes, and bread. What can I make?",
        "What can I make with the ingredients in my fridge?",
        "I have some leftover vegetables. Any ideas?",
        "Here are my ingredients: ...",

        ### 🎯 Preference-based

        "Give me a high-protein dinner for 2",
        "Suggest a quick vegetarian meal",
        "I want something under 500 calories",
        "Give me an easy Italian recipe",
        "I need a gluten-free dinner idea",

        # 🧑‍🍳 More natural / fun

        "Chef, what's for dinner?",
        "Surprise me with something delicious!",
        "Help me turn my leftovers into dinner",
        "I'm hungry... what should I make?",
        "Let's cook something!",

        # 📸 Multimodal

        "Take a photo of your fridge and I'll find recipe ideas",
        "Show me what's in your fridge...",
        "Upload a photo of your ingredients",
        "Tell me what you have, or show me a photo",
        "Got ingredients? Let's turn them into a meal.",
        "What would you like to cook today?",
        "What ingredients do you have?",
        "I have chicken, rice, and broccoli...",
        "Give me a high-protein dinner for 2",
        "What can I make with what's in my fridge?",
        "I'm craving something Italian...",
        "Help me use up my leftovers",
        "Give me a quick vegetarian recipe",
        "Chef, what's for dinner?",
        "Tell me what you're craving..."
    ]

    return placeholders
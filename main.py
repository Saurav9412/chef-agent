import os
from dotenv import load_dotenv, set_key
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from pprint import pprint

load_dotenv()


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

def get_gemini(
        temperature: float|None = 0.3,
        top_p: float|None = 0.7,
        max_output_tokens: int|None =  1024
    ) -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        model = os.getenv("GEMINI_MODEL"),
        api_key = os.getenv("GEMINI_API_KEY")
    )


extraction_prompt = ChatPromptTemplate([
    (
        "system", """
You are a recipe-query understanding system. Extract structured recipe search information from the user's request. 
Rules: 
- Extract only information explicitly stated or strongly implied. 
- Do not invent ingredients. 
- If the user asks for a specific dish, put it in dish. 
- If the user lists ingredients, put them in ingredients. 
- Separate dietary preferences from hard restrictions. 
- If something is unknown, leave it null or empty. 
- Preserve important cooking preferences.
"""),
   (
       "user", "{user_input}"
   )
])


class UserInputSchema(BaseModel):
    prompt: str = Field(
        ...,
        description=(
            "The user's recipe request. It may contain ingredients, "
            "dietary restrictions, cuisine preferences, a specific dish, "
            "servings, or other cooking preferences."
        )
    )

class RecipeSearchIntent(BaseModel):
    ingredients : list[str] = Field(
        default_factory=list,
        description = "Ingredients the user has or wants to use."
    )

    dish : str|None = Field(
        default_factory = None,
        description = "Specific dish the user wants to prepare, if any."
    )

    dietary_restrictions : list[str] = Field(
        default_factory = list,
        description = "Dietary preferences such as high-protein or low-carb."
    )

    cuisine : str|None = Field(
        default_factory = None,
        description = "Cuisine preference, e.g., Italian, Mexican, etc."
    )

    serving_size : int|None = Field(
        default_factory = None,
        description = "Number of servings the user wants to prepare."
    )

    additional_preferences : list[str] = Field(
        default_factory = list,
        description = "Any other cooking preferences or constraints, such as quick, easy, spicy, etc"
    )

class Recipe(BaseModel):
    title : str = Field(
        ...,
        description = "The title of the recipe."
    )

    description : str = Field(
        ...,
        description = "A brief description of the recipe."
    )

    ingredients : list[str] = Field(
        ...,
        description = "List of ingredients required for the recipe."
    )

    instructions : str = Field(
        ...,
        description = "Step-by-step instructions for preparing the recipe."
    )

    servings : int = Field(
        ...,
        description = "Number of servings the recipe yields."
    )

    macros : dict[str, float] = Field(
        ...,
        description = "Nutritional information, including calories, protein, carbs, and fats."
    )

    tips : list[str] = Field(
        default_factory=list,
        description = "Additional tips or variations for the recipe."
    )


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
        include_raw=True
    )
    structured_gemini = get_gemini().with_structured_output(
        RecipeSearchIntent,
        include_raw=True
    )
    llm = structured_groq.with_fallbacks([structured_gemini])

    chain = extraction_prompt | llm
    return chain.invoke({"user_input": user_query.prompt})


def main(prompt: UserInputSchema):
    model = ChatGroq(
        model = "qwen/qwen3.8-27b",
        api_key = os.getenv("GROQ_API_KEY"),
        temperature = 0.6   
    )
    # agent = create_agent(model)
    structured = model.with_structured_output(
        RecipeSearchIntent,
        include_raw=True
    )
    result = structured.invoke(prompt.prompt)
    pprint.pprint(result)
    return result

if __name__=="__main__":
    prompt = input("User: ")
    pprint(extract_recipe_info(UserInputSchema(prompt = prompt)))
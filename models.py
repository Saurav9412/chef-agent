from enum import Enum
from pydantic import BaseModel, Field
from typing import List


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
        default = None,
        description = "Specific dish the user wants to prepare, if any."
    )

    dietary_restrictions : list[str] = Field(
        default_factory = list,
        description = "Dietary preferences such as high-protein or low-carb."
    )

    cuisine : str|None = Field(
        default = None,
        description = "Cuisine preference, e.g., Italian, Mexican, etc."
    )

    serving_size : int|None = Field(
        default = None,
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

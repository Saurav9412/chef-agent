from langchain_core.prompts import ChatPromptTemplate


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
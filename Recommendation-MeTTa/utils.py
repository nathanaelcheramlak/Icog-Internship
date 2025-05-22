import os
import google.generativeai as genai
from dotenv import load_dotenv

# Config
load_dotenv()
api_key = os.getenv('API_KEY')
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

def get_metta_query_from_llm(user_input):
    system_prompt = """
            You are an expert in generating MeTTa queries for recipe recommendation.
            Given a user's natural language input, generate a valid atom expression that:
            1. Defines their ingredients using (my-ing (...)).
            2. Example: (my-ing (tomato bread ketchup))
            3. If a specific ingredient is two or more letters use '-' to separate the words

            Only return valid MeTTa expression. Do not explain anything.
        """

    # Combine system prompt and user input
    full_prompt = f"{system_prompt}\n\nUser input: {user_input}"
    
    response = model.generate_content(full_prompt)
    
    return response.text.strip()

def make_output_human_friendly(metta_output, user_request):
    if not metta_output:
        return "Sorry, no matching recipes found."

    all_recipes = []
    all_recipe_names = []

    for recipe in metta_output:
        name, time, diet = recipe
        all_recipe_names.append(name)
        all_recipes.append(f"{name}: Takes {time}, Diet: {diet}")
    
    prompt = f"""
    You are a recipe assistant.

    You will be given:
    - A list of possible recipes the user can make based on their ingredients.
    - The user's dietary preference and ingredient list.

    Your task:
    - In the first sentence, list all the recipes the user can make **with their cooking times** (e.g., With the provided ingredients, you can make A (5m), B (10m), and C (15m)).
    - Then, based on their diet preference, recommend the best two recipes from the list.
    - If the user given recipe matches exactly with a food prioritize it. But else
    - Use the cooking time to prioritize quicker recipes if multiple match the diet.
    - Format your response **exactly** like this:

    "With the provided ingredients, you can make A (5m), B (10m), and C (15m)."

    Only use the recipe names and times from the list. Do not invent any. Be clear and concise.
    Only if diet preference exists, take that into consideration and recommend from the recipes given.

    Food options:
    {chr(10).join(all_recipes)}

    User request:
    {user_request}
    """


    response = model.generate_content(prompt)
    return response.text.strip()

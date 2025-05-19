from hyperon import MeTTa
from utils import get_metta_query_from_llm, make_output_human_friendly


def main():
    recipes = [
        "(food PBJ (ingredients bread peanut-butter jam) 5m vegan)",
        "(food BLT (ingredients bread lettuce tomato) 10m vegan)",
        "(food Salad (ingredients lettuce tomato cucumber) 25m vegetarian)",
        "(food Bread (ingredients bread) 1m non-vegan)",
        "(food Veggie-Wrap (ingredients tortilla lettuce tomato cucumber hummus) 8m vegan)",
        "(food Grilled-Cheese (ingredients bread cheese butter) 6m vegetarian)",
        "(food Fruit-Salad (ingredients apple banana grapes) 4m vegan)",
        "(food Avocado-Toast (ingredients bread avocado) 5m vegan)",
        "(food Egg-Sandwich (ingredients bread egg cheese) 7m non-vegan)",
        "(food Stir-Fry (ingredients broccoli bell-pepper tofu soy-sauce) 15m vegan)",
        "(food Pancakes (ingredients flour egg milk) 12m non-vegan)",
        "(food Oatmeal (ingredients oats almond-milk banana) 10m vegan)",
        "(food Tuna-Sandwich (ingredients bread tuna mayo) 9m non-vegan)",
        "(food Hummus-Plate (ingredients hummus carrot cucumber pita) 6m vegan)",
        "(food Pasta (ingredients pasta tomato-sauce) 20m vegetarian)",
        "(food Chicken-Wrap (ingredients tortilla chicken lettuce sauce) 12m non-vegan)",
        "(food Rice-Bowl (ingredients rice beans corn avocado) 18m vegan)",
        "(food Cheese-Quesadilla (ingredients tortilla cheese) 7m vegetarian)",
        "(food Lentil-Soup (ingredients lentils carrot onion) 30m vegan)",
        "(food Yogurt-Parfait (ingredients yogurt granola berries) 5m vegetarian)"
    ]

    metta = MeTTa()

    try:
        # Prompt the user
        print(f'{'*' * 10} Welcome to RecRecommendations  {'*' * 10}')
        user_input = input('Enter your ingredients below \n')

        # Add recipe atoms to the space
        recipe_atoms = metta.parse_all(' '.join(recipes))
        for recipe_atom in recipe_atoms:
            metta.space().add_atom(recipe_atom)


        # Add users ingredients to the space
        metta_query = get_metta_query_from_llm(user_input)

        user_ingredients = metta.parse_single(metta_query)
        metta.space().add_atom(user_ingredients)

        # Execute MeTTa Code
        metta.run("""
            ; Checks if an ingredient exists in a pool of ingredients
            ; Returns 1 if found else 0
            (= (find_ingredient $ing ()) 0)
            (= (find_ingredient $ing $ingredients) (
                if (== (car-atom $ingredients) $ing) 1 (find_ingredient $ing (cdr-atom $ingredients))
            ))
        """)

        metta.run("""
            ; Count common ingredients
            (= (count-common-ingredients $x ()) 0)
            (= (count-common-ingredients $available-ingredients $all-ingredients) (
                + (find_ingredient (car-atom $all-ingredients) $available-ingredients) (count-common-ingredients $available-ingredients (cdr-atom $all-ingredients)))
            )
        """)

        metta.run("""
            ; Count ingredients
            (= (count-ingredients ()) 0)
            (= (count-ingredients $ingredients) (
                + 1 (count-ingredients (cdr-atom $ingredients))
            ))
        """)

        metta.run("""
            ; Iterate over all the foods and find matches
            (= (get-foods) (match &self (food $name $ingredients $cooking-time $diet-type) (
                if (<= (count-ingredients (cdr-atom $ingredients)) (match &self (my-ing $ing) (count-common-ingredients $ing (cdr-atom $ingredients))))
                ($name $cooking-time $diet-type)
                ()
            )))
        """)

        recipes = metta.run("!(get-foods)")

        def format_recipe(recipes):
            return [str(food).split(' ') for food in recipes[0] if str(food) not in ['()', '', 'Nil']]

        recipes = format_recipe(recipes)

        output = make_output_human_friendly(recipes, user_input)
        print('\nRecommendation: ', output)

    finally:
        # Explicit cleanup
        if 'metta' in locals():
            del metta


if __name__ == "__main__":
    main()
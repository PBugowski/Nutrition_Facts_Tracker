def generate_prompt_nutrition(product_name):
    prompt = f"""
        You are expert dietitian. 
        
        Your role today is to assist in providing essential data concerning nutritional 
        values of food products.
        
        Instructions for Task completion:
        - Your output should include only a JSON dictionary,
        - Your output should not include any ` or word json,
        
        - Dictionary should include the following key-value pairs:
        product_name: "{product_name}",
        energy_value: "here include desired value in kcal per 100 gram of a product",
        proteins: "here include desired value in grams per 100 gram of a product",
        total_fats: "here include desired value in grams per 100 gram of a product",
        saturated_fats: "here include desired value in grams per 100 gram of a product",
        carbohydrates: "here include desired value in grams per 100 gram of a product",
        sugars: "here include desired value in grams per 100 gram of a product",
        cholesterol: "here include desired value in milligrams per 100 gram of a product",
        fiber: "here include desired value in grams per 100 gram of a product"
        - Values of energy_value, proteins, total_fats, saturated_fats, carbohydrates,
        sugars, cholesterol and fiber should only consist integers.
        """
    return prompt


def generate_prompt_training(intensity, trained_part, level_of_experience):
    prompt = f"""
        You are expert gym instructor.
        
        Your role today is to present a {intensity} training for {trained_part}. 
        It is important that the training should be adjusted for a {level_of_experience} gym goer
        and consist of 5 exercises.
        
        Instructions for Task completion:
        - Your output should include only a JSON dictionary,
        - Your output should not include any ` or word json,
        - Values in key-value pairs should be provided in polish,
        
        - Dictionary should include the following key-value pairs:
        training_name: return "{intensity} - {level_of_experience} - {trained_part}",
        kcal_burnt: "here include expected value of burnt kcal while training",
        exercise_1: "name of the first exercise"
        exercise_1_sets: "number of sets for the first exercise"
        exercise_1_reps: "number of repetitions in each set for the first exercise"
        exercise_2: "name of the second exercise"
        exercise_2_sets: "number of sets for the second exercise"
        exercise_2_reps: "number of repetitions in each set for the second exercise"
        exercise_3: "name of the third exercise"
        exercise_3_sets: "number of sets for the third exercise"
        exercise_3_reps: "number of repetitions in each set for the third exercise"
        exercise_4: "name of the fourth exercise"
        exercise_4_sets: "number of sets for the fourth exercise"
        exercise_4_reps: "number of repetitions in each set for the fourth exercise"
        exercise_5: "name of the fifth exercise"
        exercise_5_sets: "number of sets for the fifth exercise"
        exercise_5_reps: "number of repetitions in each set for the fifth exercise"
        - Values of kcal_burnt, exercise_1_sets, exercise_1_reps, exercise_2_sets, exercise_2_reps,
        exercise_3_sets, exercise_3_reps, exercise_4_sets, exercise_4_reps, exercise_5_sets and
        exercise_5_reps should only consist integers without any additional description.
        - Provide a description of each of the exercises. Add them to a json dictionary in key-value pairs:
        exercise_1_description: “content”
        exercise_2_description: “content”
        exercise_3_description: “content”
        exercise_4_description: “content”
        exercise_5_description: “content”
    """
    return prompt

import os, json, random, unicodedata
from pathlib import Path


def normalize_to_ascii(text):
    """
    Convert Unicode characters to closest ASCII equivalent.
    """
    if isinstance(text, str):
        return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    elif isinstance(text, list):
        return [normalize_to_ascii(item) for item in text]    
    elif isinstance(text, dict):
        return {normalize_to_ascii(k): normalize_to_ascii(v) for k, v in text.items()}
    return text


def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))


def extract_questions(json_filename="questions"):   
    with open(json_filename + ".json", 'r') as f:
        data = json.load(f)
        questions = []
        for item in data:
            questions.append(item["question"])
        
    with open(json_filename + "_list.txt", 'w') as f:
        for question in questions:
            f.write(question + "\n")


def extract_categories(json_filename="categories"):
    with open(json_filename + ".json", 'r') as f:
        data = json.load(f)
        categories = []
        for item in data:
            print(item)
            categories.append(item)
    
    print(categories)
        
    with open(json_filename + "_list.txt", 'w') as f:
        for category in categories:
            f.write(category + "\n")


def insert_quizzes_to_categorised_questions(json_filename="questions_categorised"):
    """
    Generate quizzes from categorized questions and save them to a new JSON file.
    """
    output_data = {}
    total_quiz_count = 0

    with open(json_filename + ".json", 'r') as f:
        data = json.load(f)
        for category, questions_in_category in data.items():
            num_quizzes_for_category = clamp(3 * len(questions_in_category) // 4, 1, 15)            
            category_quizzes_list = []            
            shuffled_source_questions = questions_in_category.copy()
            random.shuffle(shuffled_source_questions)            
            for _ in range(num_quizzes_for_category):
                current_quiz_question_texts = []
                total_quiz_count += 1
                num_questions_for_quiz = random.choice([3, 5, 8])                
                for _ in range(num_questions_for_quiz):
                    if not shuffled_source_questions:
                        shuffled_source_questions = questions_in_category.copy()
                        random.shuffle(shuffled_source_questions)
                    question_text = shuffled_source_questions.pop(0)
                    current_quiz_question_texts.append(question_text)                
                formatted_quiz_questions = [{"text": q_text} for q_text in current_quiz_question_texts]
                quiz_object = {
                    "name": "",
                    "description": "",
                    "questions": formatted_quiz_questions
                }
                category_quizzes_list.append(quiz_object)            
            output_data[category] = category_quizzes_list            
    print(f"Generated {total_quiz_count} quizzes for {len(data)} categories.")
            
    output_filename = "quizzes_categorised.json" 
    with open(output_filename, 'w') as outfile:
        json.dump(output_data, outfile, indent=4)
    print(f"Saved quizzes to {output_filename}")


def split_quizzes_into_files(json_filename="quizzes_categorised"):
    """
    Generate quiz names and descriptions for each quiz in the JSON file.
    """
    # Output folder to save JSON files
    output_path = "quizzes"
    Path(output_path).mkdir(exist_ok=True)
    print("Starting file generation...\n")

    with open(json_filename + ".json", 'r') as f:
        data = json.load(f)
        for category, quizzes in data.items():
            category_output_data = {category: quizzes}
            output_filename = os.path.join(output_path, category.replace(" ", "_").replace("&", "and") + ".json")
            
            with open(output_filename, 'w') as outfile:
                json.dump(category_output_data, outfile, indent=4)
            print(f"Saved {category} quizzes to {output_filename}")
        

def generate_quiz_details(quiz):
    """
    """


def create_quiz_names_and_descriptions():
    """
    Generate quiz names and descriptions for each quiz in the JSON file.
    """
    # Output folder to save JSON files
    input_path = "quizzes"
    Path(input_path).mkdir(exist_ok=True)
    print("Starting name generation...\n")

    # open each file in the input path one by one
    for filename in os.listdir(input_path):
        if filename.endswith(".json"):
            with open(os.path.join(input_path, filename), 'r') as f:
                data = json.load(f)
                for category, quizzes in data.items():
                    for quiz in quizzes:
                        name, description = generate_quiz_details(quiz)
                        quiz["name"] = name
                        quiz["description"] = description
            
            # Save the updated quizzes back to the file
            with open(os.path.join(input_path, filename), 'w') as outfile:
                json.dump(data, outfile, indent=4)
                print(f"Updated {filename} with quiz names and descriptions.")


def run():
    #extract_questions()
    #extract_categories()
    #insert_quizzes_to_categorised_questions()
    #split_quizzes_into_files()

    create_quiz_names_and_descriptions()
     



if __name__ == "__main__": 
    run()



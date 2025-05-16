import re, os, json, random, unicodedata, time
from pathlib import Path
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate


# Create a prompt template for generating quizzes and questions
PROMPT_TEMPLATE = ChatPromptTemplate.from_template(
"""
You are a quiz generator. 
Create unique names and unique descriptions for the following sets of quizzes.
                                                   
All quizzes are for the category "{category}".
The quiz name should be unique and creative, based on the quiz questions.
The quiz description should be a short summary of the quiz, 2-4 sentences long.

The quizzes and their questions are supplied in the following JSON format:
{{
  "name": "",
  "description": "",
  "questions": [
    {{
      "text": "question 1",
    }},
    {{
      "text": "question 2",
    }},
    ...
  ]
}}

Return the same json format with the new quiz names and descriptions inserted, and no other changes:
{{
  "name": "<insert the quiz name here>",
  "description": "<insert the quiz description here>",
  "questions": [
    {{
      "text": "question 1",
    }},
    {{
      "text": "question 2",
    }},
    ...
  ]
}}
    
Return only the JSON, with no explanation or additional text. 
Do not include code blocks or any Markdown formatting.

Here is the JSON:
{json_data}
""")


def extract_json(text):
    """
    Attempt to extract the first JSON object from text.
    """
    try:
        # Extract the first {...} block
        match = re.search(r'\{[\s\S]*\}', text)

        # If a match is found, parse it as JSON
        return json.loads(match.group(0)) if match else None

    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")

    return None


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
        

def generate_quiz_details(category, json_data):
    """
    """
    llm = OllamaLLM(model="gemma3:12b")

    prompt = PROMPT_TEMPLATE.format_messages(
        category=category,
        json_data=json.dumps(json_data, indent=4)
    )

    try:
        # Invoke the LLM with the prompt and get the response which should be in JSON format
        response = llm.invoke(prompt)
        quiz_json = extract_json(response)

        # If the response is not valid JSON, skip this quiz
        if not quiz_json:
            print(f"Failed to parse JSON from response.")
            return

        # Convert all Unicode characters to ASCII
        quiz_json = normalize_to_ascii(quiz_json)
        return quiz_json

    except Exception as e:
        # If we get an error, print it and the response so we can see what went wrong
        # and continue to the next quiz
        print(f"Error generating quiz details: {e}")
        print(f"Raw response:\n{response}...\n")


def create_quiz_names_and_descriptions():
    """
    Generate quiz names and descriptions for each quiz in the JSON file.
    """
    # Output folder to save JSON files
    input_path = "quizzes"
    Path(input_path).mkdir(exist_ok=True)
    print("Starting name generation...\n")

    start_time = time.time()  # Record start time

    # open each file in the input path one by one
    for filename in os.listdir(input_path):
        if filename.endswith(".json"):
            file_start_time = time.time() # Record start time for this file
            with open(os.path.join(input_path, filename), 'r') as f:
                data = json.load(f)
                for category, _ in data.items():
                    pass

                print(f"Generating quiz names and descriptions for {category}...")
                new_data = generate_quiz_details(category, data)
            
            if new_data:
                with open(os.path.join(input_path, filename), 'w') as outfile:
                    json.dump(new_data, outfile, indent=4)
                    file_end_time = time.time() # Record end time for this file
                    file_duration_seconds = file_end_time - file_start_time
                    file_minutes = int(file_duration_seconds // 60)
                    file_seconds = int(file_duration_seconds % 60)
                    print(f" - Updated {filename}, took {file_minutes}m {file_seconds}s.")

    end_time = time.time()  # Record end time
    total_duration_seconds = end_time - start_time
    total_minutes = int(total_duration_seconds // 60)
    total_seconds = int(total_duration_seconds % 60)
    print(f"\nFinished name generation. Total time: {total_minutes}m {total_seconds}s.")


def patch_quiz_details():

    question_details_lookup = {}

    with open("questions_with_hints.json", 'r') as f:
        data = json.load(f)
        for item in data:
            question_details_lookup[item["question"]] = item

    input_path = "quizzes"
    Path(input_path).mkdir(exist_ok=True)

    for filename in os.listdir(input_path):
        if filename.endswith(".json"):

            with open(os.path.join(input_path, filename), 'r') as f:
                data = json.load(f)

                quizzes = data.items()[0][1]
                
                for quiz in quizzes:
                    for question in quiz["questions"]:
                        question_text = question["text"]
                        
                        source = question_details_lookup[question_text]
                        if source:
                            print(f"Updated question: {question_text}")
                            question.update(source)
                        else:
                            print(f"Question not found in lookup: {question_text}")

                with open(os.path.join(input_path, filename), 'w') as outfile:
                    json.dump(data, outfile, indent=4)
                    print(f"Updated {filename} with question details.")             


def run():
    #extract_questions()
    #extract_categories()
    
    #insert_quizzes_to_categorised_questions()
    #split_quizzes_into_files()

    #create_quiz_names_and_descriptions()
     
    patch_quiz_details()



if __name__ == "__main__": 
    run()



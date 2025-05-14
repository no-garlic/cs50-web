import re
import os
import json
import random
from pathlib import Path
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import unicodedata


def extract_json(text):
    """
    Attempt to extract the first JSON object from text.
    """
    try:
        # Extract the first {...} block
        match = re.search(r'\{[\s\S]*\}', text)
        if match:
            return json.loads(match.group(0))
    except json.JSONDecodeError as e:
        print(f"   ⚠️ JSON decode error: {e}")
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


# Read categories from categories.json file
with open('categories.json', 'r') as f:
    categories_data = json.load(f)
    CATEGORIES = list(categories_data.keys())

# Initialize the LLM
llm = OllamaLLM(model="gemma3:12b")

# Prompt template
PROMPT_TEMPLATE = ChatPromptTemplate.from_template("""
You are a quiz generator. 
Create a unique multiple choice quiz in the category "{category}" that does not duplicate any of these quiz names: {existing_titles}.

The quiz should include:
1. A unique and creative name.
2. A short description (2-4 sentences).
3. A list of {num_questions} multiple choice questions, each with:
    - Question text
    - A hint to show the user if they ask for help
    - 4 answer options
    - The correct option number (1, 2, 3, or 4) for the solution
                                                   
You must use this list of correct option numbers for the solutions: {correct_options}, each question you generate will use the next number in the list for the solution.
The questions should be challenging and engaging, suitable for a quiz format. 
The quiz should be in English.
Make sure to include a variety of topics within the category. 
The quiz should be fun and interesting, with a good mix of easy and hard questions.                                                

Return the quiz in JSON format following this structure:
{{
  "name": "...",
  "description": "...",
  "questions": [
    {{
      "text": "...",
      "hint": "...",
      "option1": "...",
      "option2": "...",
      "option3": "...",
      "option4": "...",
      "solution": "..."
    }},
    ...
  ]
}}
    
Return only the JSON, with no explanation or additional text. 
Do not include code blocks or any Markdown formatting.                                              
""")

# Directory to save JSON files
OUTPUT_DIR = "quizzes"
Path(OUTPUT_DIR).mkdir(exist_ok=True)

print("🚀 Starting quiz generation...\n")

# Main loop
for category in CATEGORIES:
    print(f"📚 Category: {category}")
    filename = os.path.join(OUTPUT_DIR, category.replace(" ", "_").replace("&", "and") + ".json")

    # Load existing data if it exists
    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = json.load(f)
        print(f"➡️  Loaded existing file: {filename}")
    else:
        data = {category: []}
        print(f"🆕 Creating new file: {filename}")

    existing_titles = [quiz["name"] for quiz in data[category]]
    num_quizzes_to_generate = random.randint(5, 15) - len(data[category])
    if num_quizzes_to_generate <= 0 or len(existing_titles) >= 5:
        print("   No new quizzes needed.")
        continue

    print(f"🔄 Generating {num_quizzes_to_generate} new quizzes...")

    for i in range(num_quizzes_to_generate):
        num_questions = random.choice([5, 8, 10])

        correct_options = []
        last_correct_option = 0

        for _ in range(num_questions):
            correct_option = random.randint(1, 4)
            while correct_option == last_correct_option:
                correct_option = random.randint(1, 4)
            last_correct_option = correct_option
            correct_options.append(correct_option)

        correct_options_str = ", ".join(map(str, correct_options))
        print(f"   ✏️ Generating quiz {i+1}/{num_quizzes_to_generate} with {num_questions} questions...")

        prompt = PROMPT_TEMPLATE.format_messages(
            category=category,
            existing_titles=existing_titles,
            num_questions=num_questions,
            correct_options=f"[{correct_options_str}]",
        )
        try:
            response = llm.invoke(prompt)
            quiz_json = extract_json(response)

            if not quiz_json:
                print(f"   ❌ Failed to parse JSON from response.")
                continue

            # Normalize all Unicode characters to ASCII
            quiz_json = normalize_to_ascii(quiz_json)

            if quiz_json["name"] in existing_titles:
                print(f"   ⚠️ Skipped duplicate: {quiz_json['name']}")
                continue

            # Append the new quiz and save immediately
            data[category].append(quiz_json)
            existing_titles.append(quiz_json["name"])
            print(f"   ✅ Added quiz: {quiz_json['name']}")

            # Save updated file immediately after each quiz
            with open(filename, "w") as f:
                json.dump(data, f, indent=4)
            print(f"   💾 Saved updated file: {filename}")

        except Exception as e:
            print(f"   ❌ Error generating quiz: {e}")
            print(f"   🧠 Raw response:\n{response}...\n")
            continue

print("🎉 Quiz generation complete.")

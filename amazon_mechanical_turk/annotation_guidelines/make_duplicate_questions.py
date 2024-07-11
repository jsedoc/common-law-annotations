"""
Create N questions per HIT
"""

# 1. Read in the base questions HTML
# 2. Duplicate with different ID's
# 3. Read base instructions
# 4. Merge instructions + questions into one html file


PATH = "commonlaw/amazon_mechanical_turk/annotation_guidelines/"
GROUP_NO = 5
ANNOTATION_GUIDELINE_FILE_NAME = f"amt_guideline_group{GROUP_NO}.html"
SOURCE_FILE_NAME = "prompt_response.html"  # HTML for prompt-response question
FOOTER_FILE_NAME = "amt_footer.html"
# Number of total prompt-responses (including attention checks)
NUMBER_OF_QUESTIONS = 55
ATTENTION_CHECKS = [7, 17, 27, 37, 47]
DEST_FILE_NAME = f"final_guidelines/prompt_response_group{GROUP_NO}_{NUMBER_OF_QUESTIONS}prompts.html"

STRINGS_TO_REPLACE = [
    "amt_idx",
    "prompt",
    "response",
    "appropriateness",
    "info-content",
    "humanlikeness",
]

questions = []  # List of duplicate questions with updated variable names

with open(PATH + SOURCE_FILE_NAME, encoding='utf-8') as file:
    base_html = file.read()

# Generate N number of prompt-response pairs

for question_id in range(NUMBER_OF_QUESTIONS):
    target_html = base_html

    # Place attention check
    if question_id in ATTENTION_CHECKS:

        # Create unique attention check ids, (0,1,2,...,)
        attention_check_id = ATTENTION_CHECKS.index(question_id)
        # Replace AMT variable strings with proper ids
        # ie. prompt -> 1_prompt
        for string_to_replace in STRINGS_TO_REPLACE:
            target_html = target_html.replace(
                string_to_replace, f"attention_check_" + string_to_replace + f"_{attention_check_id}")

        target_html = target_html.replace('id="q"', f'id="q{question_id}"')
        target_html = target_html.replace(
            '>Question</h3>', f'>Question {question_id+1}</h3>')

        questions.append(target_html)

        continue

    # Replace AMT variable strings with proper ids
    # ie. prompt -> 1_prompt
    for string_to_replace in STRINGS_TO_REPLACE:
        target_html = target_html.replace(
            string_to_replace, str(question_id) + "_" + string_to_replace)

    target_html = target_html.replace('id="q"', f'id="q{question_id}"')
    target_html = target_html.replace(
        '>Question</h3>', f'>Question {question_id+1}</h3>')

    questions.append(target_html)

# Read annotation guideline
with open(PATH + ANNOTATION_GUIDELINE_FILE_NAME, encoding='utf-8') as file:
    guideline_html = file.read()

# Read footer
with open(PATH + FOOTER_FILE_NAME, encoding='utf-8') as file:
    footer_html = file.read()

with open(PATH + DEST_FILE_NAME, "w", encoding='utf-8') as file:
    file.write(guideline_html)
    for question in questions:
        file.write(question + "\n")
    file.write(footer_html)

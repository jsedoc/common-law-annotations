# Annotation Guidelines

- `make_duplicate_questions.py` : Script to create `html` annotation guidelines used in Amazon Mechanical Turk. Uses the following files to generate the final guideline
- `prompt_response.html` : Template file containing one prompt/response item. Code in this file is repeated to generated however many questions neeeded.
- `amt_footer.html` : Contains the footer portion of the `html`.
- *Final guideline generated in `/final_guidelines`*
- `/final_guidelines` : Destination directory for the Amazon Mechanical Turk annotation guidelines, made in `html`.

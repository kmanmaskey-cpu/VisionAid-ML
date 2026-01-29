import pdfplumber
import re
import json

# 1. SETUP - Minimal and direct
file_path = r"C:\Users\User\OneDrive\Documents\ML\CBSE\DATA\science_2024.pdf.pdf"
output_path = r"C:\Users\User\OneDrive\Documents\ML\CBSE\science_TEST.json"


# 2. GET TEXT - No layout=True (it sometimes causes weird spacing)
full_text = ""
with pdfplumber.open(file_path) as pdf:
    for page in pdf.pages:
        full_text += "\n" + (page.extract_text() or "") + "\n"

# 3. SPLIT QUESTIONS - Simple 'Newline + Number + Space'
# This is the most reliable pattern for CBSE papers
regex_pattern = r'\n(\d{1,2})\s+'
parts = re.split(regex_pattern, full_text)

# 4. BUILD DATA
final_quiz = []
unique_ids = set()

AR_OPTIONS = [
    "Both Assertion (A) and Reason (R) are true and (R) is the correct explanation of (A).",
    "Both Assertion (A) and Reason (R) are true but (R) is not the correct explanation of (A).",
    "Assertion (A) is true but (R) is false.",
    "Assertion (A) is false but (R) is true."
]


# Index 1 is the first number, Index 2 is the text, etc.
for i in range(1, len(parts), 2):
    num = int(parts[i])
    text = parts[i+1].strip()
    
    if 1 <= num <= 20 and num not in unique_ids:
        # If it's an Assertion-Reason question, give it the standard options

        if num == 3:
            question_text = "Mild non-corrosive basic salt is:"
            options = ["Ca(OH)2", "NaCl", "NaOH", "NaHCO3"]
        elif num == 5:
            question_text = "Which one of the following correctly represents Sodium oxide?"
            options = ["Na2O", "NaO2", "Na2O2", "NaO"]
        elif num >= 17:
            question_text = text
            options = AR_OPTIONS
        else:
            # Normal MCQ logic
            option_parts = re.split(r'\s[a-d][\)\.]\s', text)
            question_text = option_parts[0]
            options = option_parts[1:]
        
        final_quiz.append({
            "number": num,
            "question": question_text.strip(),
            "options": [opt.strip() for opt in options]
        })
        unique_ids.add(num)

# Use a fresh variable name to ensure no data collisions
with open(output_path, "w", encoding='utf-8') as f:
    json_string = json.dumps(final_quiz, indent=4)
    f.write(json_string)
    f.flush() # Forces Windows to write the bits to disk NOW
print(f"DONE! Found {len(final_quiz)} unique questions.")
print(f"Check this specific file: {output_path}")
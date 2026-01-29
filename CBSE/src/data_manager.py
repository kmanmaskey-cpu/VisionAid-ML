import random
# Import your data manager to use get_questions
import data_manager

import json
import os

# Define the file paths clearly
DATA_FILE = r"C:\Users\User\OneDrive\Documents\ML\CBSE\DATA\science_TEST.json"
MASTERY_FILE = r"C:\Users\User\OneDrive\Documents\ML\CBSE\DATA\mastery.json"

def load_json_file(filename):
    """Safely loads a JSON file or returns an empty dictionary if not found."""
    if not os.path.exists(filename):
        return {}
    with open(filename, 'r') as f:
        return json.load(f)

def save_updated_weight(question_id, new_weight):
    """
    Updates a single question's weight in the file.
    Note: This is 'safe' but slow if used inside a loop.
    """
    mastery_data = load_json_file(MASTERY_FILE)
    mastery_data[str(question_id)] = new_weight
    
    with open(MASTERY_FILE, 'w') as f:
        json.dump(mastery_data, f, indent=4)

# Configuration for the adaptive algorithm
WRONG_PENALTY = 7
RIGHT_REWARD = 2
DEFAULT_WEIGHT = 10 # Neutral starting point

def calculate_new_weight(current_weight, is_correct):
    """Calculates the mathematical shift in weight."""
    if is_correct:
        return max(1, current_weight - RIGHT_REWARD)
    return min(50, current_weight + WRONG_PENALTY)

def update_mastery(mastery_data, question_id, is_correct):
    """Updates the dictionary and prepares it for saving."""
    q_id_str = str(question_id)
    # Start new questions at 10 so they are tested early
    current_weight = mastery_data.get(q_id_str, DEFAULT_WEIGHT)
    
    new_weight = calculate_new_weight(current_weight, is_correct)
    mastery_data[q_id_str] = new_weight
    return mastery_data

def get_smart_questions(all_questions, mastery_data, num_to_pick=5):
    """Selects high-weight questions to focus on weak spots."""
    weighted_list = []
    
    for q in all_questions:
        q_id = str(q['number'])
        weight = mastery_data.get(q_id, DEFAULT_WEIGHT)
        weighted_list.append((q, weight))
    
    # Sort by weight descending (Hardest first)
    weighted_list.sort(key=lambda x: x[1], reverse=True)
    
    # Pick the top N and shuffle them for variety
    top_questions = [item[0] for item in weighted_list[:num_to_pick]]
    random.shuffle(top_questions)
    return top_questions

def get_question_map(all_questions):
    """Creates a fast lookup table: { 'number': question_dict }."""
    return {str(q['number']): q for q in all_questions}

def calculate_session_stats(session_results):
    """Summarizes performance [True, False, True] -> stats dict."""
    total = len(session_results)
    correct = sum(session_results)
    percentage = (correct / total) * 100 if total > 0 else 0
    
    return {
        "total": total,
        "correct": correct,
        "percentage": round(percentage, 2)
    }

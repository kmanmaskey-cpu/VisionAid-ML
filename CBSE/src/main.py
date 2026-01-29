from data_manager import load_json_file , save_updated_weight , MASTERY_FILE, DATA_FILE
from engine import calculate_new_weight, get_smart_questions
from engine import calculate_session_stats


def run_quiz(session_questions): # Pass questions in here
    print(f"\n--- Starting Session with {len(session_questions)} questions ---")
    total = len(session_questions)
    score = 0
    
    # We still need mastery to update weights after each answer
    mastery = load_json_file(MASTERY_FILE) 

    for q in session_questions:
        print(f"\nQuestion {q['number']}: {q['question']}")
        
        # --- PASTE THE NEW LOGIC HERE ---
        # 1. Display options with letters
        labels = ['a', 'b', 'c', 'd']
        for label, opt in zip(labels, q['options']):
            print(f"  {label}) {opt}")

        # 2. Create the map and get input
        answer_map = dict(zip(labels, q['options']))
        ans = input("\nYour answer: ").lower().strip()

        # 3. Handle letter vs. full text
        if ans in answer_map:
            chosen_text = answer_map[ans]
        else:
            chosen_text = ans
        # Check logic ✅
        is_correct = chosen_text.strip().lower() == q['correct'].lower()
        
        # 3. Calculate and Save 💾
        # Get the current weight from our mastery dictionary
        current_w = mastery.get(str(q['number']), 10)
        new_w = calculate_new_weight(current_w, is_correct)
        save_updated_weight(q['number'], new_w)
        
        # Ask the Brain for the new weight
        new_w = calculate_new_weight(current_w, is_correct)
        
        # Ask the Librarian to save it
        save_updated_weight(q['number'], new_w)
        
        if is_correct:
            print(f"✅ Correct! New weight: {new_w}")
            score += 1
        else: 
            print(f"❌ Wrong! You chose '{chosen_text}', but the correct answer was '{q['correct']}'")
            print(f"Weight increased to: {new_w}")

    percentage = (score / total) * 100
    print(f"QUIZ FINISHED")
    print(f"Final Score: {score}/{total} ({percentage}%)")

if __name__ == "__main__":
    questions = load_json_file(DATA_FILE)
    mastery = load_json_file(MASTERY_FILE)

    print("--- QUIZ SYSTEM ---")
    print("1. Normal Mode (All questions in order)")
    print("2. Smart Adaptive Mode (Focus on weak areas)")
    choice = input("Select (1/2): ")

    if choice == '1':
        # Normal: Just pass the whole list (or a slice like questions[:10])
        run_quiz(questions) 

        
    elif choice == '2':
        # Adaptive: Use your engine to pick the "Smart" questions
        smart_q = get_smart_questions(questions, mastery, num_to_pick=5)
        run_quiz(smart_q)
        
    else:
        print("Invalid choice!")
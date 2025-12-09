# Simple helper to standardize grading
def grade_answer(student_input, correct_key, strategy="exact"):
    """
    Grading Strategies:
    - 'exact': A vs B (Case insensitive)
    - 'essay': Always returns 'pending'
    """
    
    if strategy == "essay":
        return False, "pending"

    if strategy == "exact":
        # Convert both to string, strip spaces, lower case
        s_clean = str(student_input).strip().lower()
        k_clean = str(correct_key).strip().lower()
        
        is_correct = (s_clean == k_clean)
        return is_correct, "graded"
        
    return False, "unknown_strategy"
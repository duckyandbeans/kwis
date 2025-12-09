from http.server import BaseHTTPRequestHandler
import json
from core.db import get_db
from core.graders import grade_answer
from firebase_admin import firestore

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_len = int(self.headers.get('Content-Length', 0))
        data = json.loads(self.rfile.read(content_len))
        
        student_id = data.get('student_id')
        quiz_id = data.get('quiz_id')
        answers = data.get('answers') # Dict of {q1: "A", q2: "text"}

        db = get_db()
        
        # 1. Fetch Answer Key
        quiz_doc = db.collection('content_quizzes').document(quiz_id).get()
        if not quiz_doc.exists:
            self.send_error(404, "Quiz not found")
            return

        quiz_data = quiz_doc.to_dict()
        key = quiz_data.get('answer_key', {})
        
        # 2. Grade
        mcq_score = 0
        mcq_total = 0
        needs_review = False
        feedback_map = {}

        for q_id, q_info in key.items():
            # q_info example: {"type": "exact", "correct": "B", "points": 10}
            q_type = q_info.get('type', 'exact')
            correct_val = q_info.get('correct')
            points = q_info.get('points', 10)
            
            student_val = answers.get(q_id, "")
            
            is_correct, status = grade_answer(student_val, correct_val, q_type)
            
            if status == "pending":
                needs_review = True
                feedback_map[q_id] = "PENDING"
            elif is_correct:
                mcq_score += points
                mcq_total += points
                feedback_map[q_id] = "CORRECT"
            else:
                mcq_total += points # Still add to total possible
                feedback_map[q_id] = "WRONG"

        # 3. Save Log
        log_data = {
            "student_ref": f"users_students/{student_id}",
            "quiz_id": quiz_id,
            "answers": answers,
            "score_mcq": mcq_score,
            "status": "review_needed" if needs_review else "completed",
            "timestamp": firestore.SERVER_TIMESTAMP
        }
        db.collection('log_submissions').add(log_data)

        # 4. Respond
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {
            "mcq_score": mcq_score,
            "feedback": feedback_map,
            "message": "Saved successfully"
        }
        self.wfile.write(json.dumps(response).encode('utf-8'))
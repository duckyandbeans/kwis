from http.server import BaseHTTPRequestHandler
import json
from api.core.db import get_db

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_len = int(self.headers.get('Content-Length', 0))
        data = json.loads(self.rfile.read(content_len))
        
        input_code = data.get('code', '').strip()
        
        # 1. Query DB for active quizzes with this code
        db = get_db()
        quizzes = db.collection('content_quizzes').where('teacher_code', '==', input_code).stream()
        
        found_quiz = None
        for q in quizzes:
            q_data = q.to_dict()
            if q_data.get('active', True):
                found_quiz = q.id
                break
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        if found_quiz:
            # Redirect logic: if code is "QUIZ1", go to kwis.html?id=quiz_1
            # For simplicity, we assume your HTML file handles the ID
            response = {"valid": True, "quiz_id": found_quiz}
        else:
            response = {"valid": False}
            
        self.wfile.write(json.dumps(response).encode('utf-8'))
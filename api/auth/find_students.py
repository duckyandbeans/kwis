from http.server import BaseHTTPRequestHandler
import json
# Import the db helper we just made
from core.db import get_db

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # 1. Read Data
            content_len = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_len)
            data = json.loads(body)
            
            grade = str(data.get('grade', '')).strip()
            cls = str(data.get('class_id', '')).strip() # Using 'class_id' from frontend
            num = str(data.get('number', '')).strip()

            # 2. Reconstruct ID (e.g., "XI_D_15")
            # Note: We split class_id "XI D" -> we need just "D" if your frontend sends "XI D"
            # Let's assume frontend sends strictly the letter "D" for class_id to match your CSV logic
            # If frontend sends "XI D", we split it:
            if " " in cls:
                cls = cls.split(" ")[-1]

            student_id = f"{grade}_{cls}_{num}"
            
            # 3. Check DB
            db = get_db()
            doc_ref = db.collection('users_students').document(student_id)
            doc = doc_ref.get()

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            if doc.exists:
                student_data = doc.to_dict()
                response = {
                    "found": True,
                    "name": student_data.get('name'),
                    "id": student_id
                }
            else:
                response = {"found": False, "debug_id": student_id}
            
            self.wfile.write(json.dumps(response).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode('utf-8'))
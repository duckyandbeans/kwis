from http.server import BaseHTTPRequestHandler
import csv
import io
from api.core.db import get_db

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        db = get_db()
        
        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Student ID', 'Quiz ID', 'MCQ Score', 'Status', 'Raw Answers'])
        
        # Get all submissions (ordered by time)
        logs = db.collection('log_submissions').order_by('timestamp', direction='DESCENDING').stream()
        
        for log in logs:
            d = log.to_dict()
            # Clean up ID for display (users_students/XI_D_1 -> XI_D_1)
            s_ref = d.get('student_ref', '')
            s_id = s_ref.split('/')[-1] if '/' in s_ref else s_ref
            
            writer.writerow([
                s_id,
                d.get('quiz_id'),
                d.get('score_mcq'),
                d.get('status'),
                str(d.get('answers'))
            ])
            
        # Send File
        self.send_response(200)
        self.send_header('Content-Type', 'text/csv')
        self.send_header('Content-Disposition', 'attachment; filename="all_grades.csv"')
        self.end_headers()
        self.wfile.write(output.getvalue().encode('utf-8'))
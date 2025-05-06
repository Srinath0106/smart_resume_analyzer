from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from resume_parser import parse_resume
from gemini_api import get_resume_feedback
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB limit
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx', 'txt', 'png', 'jpg', 'jpeg'}

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'resume' not in request.files:
        return jsonify({'error': 'No resume file uploaded'}), 400

    file = request.files['resume']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Supported formats: PDF, DOCX, TXT, PNG, JPG, JPEG'}), 400

    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Extract resume text
        resume_text = parse_resume(filepath)
        if not resume_text.strip():
            return jsonify({'error': 'Could not extract text from the file. Please try another file.'}), 400

        # Optional: get job description
        job_desc = request.form.get('job_description', '')

        # Call Gemini AI for comprehensive analysis
        feedback = get_resume_feedback(resume_text, job_desc)
        
        # Process feedback into structured format
        analysis = process_feedback(feedback, resume_text, job_desc)
        
        # Generate ATS score (simulated - in real app, this would be more sophisticated)
        ats_score = generate_ats_score(resume_text, job_desc)
        
        # Generate keyword analysis
        keywords = analyze_keywords(resume_text, job_desc)
        
        # Combine all results
        result = {
            'ats_score': ats_score,
            'summary': analysis.get('summary', ''),
            'job_fit': analysis.get('job_fit', ''),
            'improvements': analysis.get('improvements', ''),
            'keywords': keywords,
            'detailed_feedback': analysis.get('detailed_feedback', feedback)
        }

        # Clean up uploaded file
        if os.path.exists(filepath):
            os.remove(filepath)

        return jsonify(result)

    except Exception as e:
        # Clean up in case of error
        if 'filepath' in locals() and os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

def process_feedback(feedback, resume_text, job_desc):
    """Process the raw feedback into structured sections"""
    # This is a simplified version - in a real app you'd use more sophisticated parsing
    sections = {
        'summary': '',
        'job_fit': '',
        'improvements': '',
        'detailed_feedback': feedback
    }
    
    # Try to extract sections from feedback
    if "Overall Assessment:" in feedback:
        parts = feedback.split("Overall Assessment:")
        if len(parts) > 1:
            sections['summary'] = parts[1].split("Job Fit Analysis:")[0].strip()
    
    if "Job Fit Analysis:" in feedback:
        parts = feedback.split("Job Fit Analysis:")
        if len(parts) > 1:
            sections['job_fit'] = parts[1].split("Improvement Suggestions:")[0].strip()
    
    if "Improvement Suggestions:" in feedback:
        parts = feedback.split("Improvement Suggestions:")
        if len(parts) > 1:
            sections['improvements'] = parts[1].split("Detailed Feedback:")[0].strip()
    
    return sections

def generate_ats_score(resume_text, job_desc):
    """Generate a simulated ATS score based on resume content"""
    # In a real app, this would be more sophisticated analysis
    base_score = random.randint(40, 80)  # Base score between 40-80
    
    # Increase score if job description is provided and matches are found
    if job_desc:
        matching_keywords = analyze_keywords(resume_text, job_desc)
        match_count = sum(1 for kw in matching_keywords if kw['match'])
        base_score += min(20, match_count * 2)  # Add up to 20 points for matches
    
    return min(95, base_score)  # Cap at 95%

def analyze_keywords(resume_text, job_desc):
    """Analyze keywords from job description against resume"""
    if not job_desc:
        return []
    
    # Simple keyword extraction (in real app, use NLP)
    job_keywords = set()
    for word in job_desc.lower().split():
        if len(word) > 4 and word.isalpha():  # Simple filter for meaningful words
            job_keywords.add(word)
    
    # Check which keywords appear in resume
    resume_lower = resume_text.lower()
    keywords = []
    for kw in job_keywords:
        keywords.append({
            'term': kw.capitalize(),
            'match': kw in resume_lower
        })
    
    return keywords

if __name__ == '__main__':
    app.run(debug=True)
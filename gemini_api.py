import google.generativeai as genai
from datetime import datetime

# Configure Gemini
genai.configure(api_key="AIzaSyBzMG730F9Q2Ohapk5QpPUAJlQ8ArVRbsQ")

# Initialize Gemini model
model = genai.GenerativeModel('models/gemini-1.5-flash')

def get_resume_feedback(resume_text, job_desc):
    # Generate timestamp for the analysis
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Enhanced prompt with more specific instructions and structured output
    prompt = f"""
    **Resume Analysis Request** (Generated on: {timestamp})
    
    **Role**: You are a professional HR recruiter with 10+ years of experience in technical hiring.
    
    **Task**: Analyze the following resume and provide comprehensive, structured feedback. 
    Compare it with the provided job description (if available) and suggest improvements.
    
    **Resume Text**:
    {resume_text[:20000]}  # Limiting to first 20k chars to avoid token limits
    
    **Job Description**:
    {job_desc if job_desc else "Not provided"}
    
    **Analysis Guidelines**:
    1. Provide a clear, structured response with the following sections:
       - Overall Assessment (2-3 sentence summary)
       - Job Fit Analysis (how well the resume matches the job description)
       - Improvement Suggestions (specific, actionable recommendations)
       - Detailed Feedback (comprehensive analysis)
    2. Focus on:
       - ATS optimization (formatting, keywords, structure)
       - Content quality (achievements vs responsibilities)
       - Relevance to job description
       - Readability and clarity
    3. Be specific and provide examples where possible
    4. Use bullet points for clear readability
    5. Highlight critical issues first
    
    **Output Format**:
    ### Overall Assessment:
    [Brief summary of resume quality and main strengths/weaknesses]
    
    ### Job Fit Analysis:
    [Analysis of how well the resume matches the job description]
    - Key matches
    - Potential gaps
    - Relevance score (1-10)
    
    ### Improvement Suggestions:
    [Specific, actionable recommendations]
    - Formatting improvements
    - Content enhancements
    - Keyword optimization
    - Other suggestions
    
    ### Detailed Feedback:
    [Comprehensive section-by-section analysis]
    - Contact Information
    - Summary/Objective
    - Work Experience
    - Skills
    - Education
    - Other Sections
    
    **Important**: If the resume appears to be incomplete or incorrectly parsed, mention this first.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating feedback: {str(e)}\n\nPlease try again later."
Smart Resume Analyzer
A powerful, AI-driven project that analyzes resumes to evaluate candidate skills, experience, and match percentage for job descriptions. This tool helps recruiters filter out the best-fit candidates efficiently using machine learning and natural language processing (NLP) techniques.

🚀 Features
📄 Resume Parsing (PDF, DOCX)

🧠 Skill & Experience Extraction

🔍 Matching Score with Job Description

📊 Generate Candidate Fit Report

💾 Supports multiple file formats

🖥️ Simple and clean web interface Flask

🔥 Fast and lightweight, suitable for small and large datasets

📂 Project Structure

smart_resume_analyzer/
├── app.py
├── resume_parser.py
├── gemini_api.py
├── requirements.txt
├── README.md
└── templates/intex.html

⚙️ Technologies Used
Python 🐍

NLP: SpaCy / NLTK

Machine Learning: Scikit-learn

PDF & DOCX Parsing: PyPDF2, python-docx

Web Framework:  Flask 

Pandas & NumPy for data handling

📦 Installation

Clone the repository

git clone https://github.com/srinath0106/smart_resume_analyzer.git

cd smart_resume_analyzer

Create a virtual environment (optional but recommended)

python -m venv resumeanalyzer

source resumeanalyzer/bin/activate  

Install dependencies

pip install -r requirements.txt

🚀 Usage
Run the analyzer (command-line version)
python app.py



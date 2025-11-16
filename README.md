# AI-based PM Internship Allocation (Flask + Tailwind + JS)
This project is a simple, self-contained Flask web application that demonstrates
an AI-like (rule-based/scoring) allocation system matching candidates to product-management internships.

## Features
- Flask backend (`app.py`) with SQLite (SQLAlchemy) storage
- Simple matching algorithm (skill overlap + experience)
- Upload candidates and internships via forms (or use sample data)
- View matches and export results
- Tailwind CSS via CDN for styling, plus custom CSS
- Vanilla JavaScript for small UI interactions

## Run locally
1. Create virtualenv and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate    # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```
2. Initialize database and run:
   ```
   export FLASK_APP=app.py
   flask run --reload
   ```
   Or run:
   ```
   python app.py
   ```
3. Open http://127.0.0.1:5000

## Notes
- This project uses a simple rule-based matching algorithm for demonstration.
- You can extend the "AI" part by integrating a real ML model or API.

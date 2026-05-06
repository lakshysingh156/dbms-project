# ResumeIQ Pro - Automated Resume Shortlisting System

A professional full-stack web implementation of your DBMS project report with:

- Candidate profile management
- Job posting management
- Automated application scoring and shortlisting
- Dashboard analytics and reports
- Deployment-ready setup

## Tech Stack

- Python
- Flask
- SQLite
- HTML + Jinja templates
- Custom modern CSS UI

## Local Run

1. Open terminal in project root.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start app:
   ```bash
   python app.py
   ```
4. Open:
   `http://127.0.0.1:5000`

## Deployment (Render/Railway)

### Render

1. Push this folder to GitHub.
2. Create a new **Web Service** on Render.
3. Use:
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
4. Add environment variable:
   - `SECRET_KEY=your_strong_secret`
5. Deploy.

## Scoring Logic

- Skill fit weight: 70%
- Experience fit weight: 30%
- Shortlist threshold: 60+

## Suggested Demo Flow

1. Add a few candidates with different skills.
2. Add job postings.
3. Create applications and run evaluation.
4. Show Dashboard and Reports for ranked output.

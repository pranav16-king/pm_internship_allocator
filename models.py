from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    skills = db.Column(db.String(400))
    experience = db.Column(db.Float, default=0.0)

class Internship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    required_skills = db.Column(db.String(400))
    level = db.Column(db.String(50))

class MatchResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, nullable=False)
    internship_id = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Float, nullable=False)

def init_db(app):
    with app.app_context():
        db.create_all()
        # sample data if empty
        if Candidate.query.count() == 0:
            c1 = Candidate(name='Alice', skills='product management, communication, roadmap, analytics', experience=1.5)
            c2 = Candidate(name='Bob', skills='python, data analysis, analytics, product', experience=0.8)
            c3 = Candidate(name='Carol', skills='ux, research, product management, communication', experience=2.0)
            db.session.add_all([c1,c2,c3])
        if Internship.query.count() == 0:
            i1 = Internship(title='PM Intern - Analytics', required_skills='analytics, data analysis, product', level='Intern')
            i2 = Internship(title='PM Intern - UX Research', required_skills='ux, research, product management', level='Intern')
            db.session.add_all([i1,i2])
        db.session.commit()

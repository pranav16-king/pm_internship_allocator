from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
from flask_sqlalchemy import SQLAlchemy
import os, csv, io
from models import db, Candidate, Internship, MatchResult, init_db
from match import run_matching
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    init_db(app)

@app.route('/')
def index():
    candidates = Candidate.query.all()
    internships = Internship.query.all()
    return render_template('index.html', candidates=candidates, internships=internships)

@app.route('/candidates', methods=['GET','POST'])
def candidates_view():
    if request.method == 'POST':
        name = request.form['name']
        skills = request.form['skills']
        exp = float(request.form.get('experience', 0) or 0)
        candidate = Candidate(name=name, skills=skills, experience=exp)
        db.session.add(candidate)
        db.session.commit()
        return redirect(url_for('candidates_view'))
    candidates = Candidate.query.all()
    return render_template('candidates.html', candidates=candidates)

@app.route('/internships', methods=['GET','POST'])
def internships_view():
    if request.method == 'POST':
        title = request.form['title']
        skills = request.form['skills']
        level = request.form.get('level','Intern')
        internship = Internship(title=title, required_skills=skills, level=level)
        db.session.add(internship)
        db.session.commit()
        return redirect(url_for('internships_view'))
    internships = Internship.query.all()
    return render_template('internships.html', internships=internships)

@app.route('/match', methods=['GET','POST'])
def match_view():
    if request.method == 'POST':
        # run matching and store results
        results = run_matching()
        # Save results
        MatchResult.query.delete()
        db.session.commit()
        for r in results:
            m = MatchResult(candidate_id=r['candidate_id'], internship_id=r['internship_id'], score=r['score'])
            db.session.add(m)
        db.session.commit()
        return redirect(url_for('match_view'))
    matches = MatchResult.query.all()
    enriched = []
    for m in matches:
        c = Candidate.query.get(m.candidate_id)
        i = Internship.query.get(m.internship_id)
        enriched.append({'candidate': c, 'internship': i, 'score': m.score})
    return render_template('match.html', matches=enriched)

@app.route('/export_matches')
def export_matches():
    matches = MatchResult.query.all()
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['candidate','internship','score'])
    for m in matches:
        c = Candidate.query.get(m.candidate_id)
        i = Internship.query.get(m.internship_id)
        cw.writerow([c.name, i.title, m.score])
    output = io.BytesIO()
    output.write(si.getvalue().encode())
    output.seek(0)
    return send_file(output, mimetype='text/csv', as_attachment=True, download_name='matches.csv')

if __name__ == '__main__':
    app.run(debug=True)

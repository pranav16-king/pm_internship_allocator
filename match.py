from models import Candidate, Internship
from models import db
import re

def normalize_skills(s):
    if not s: return set()
    parts = re.split('[,;|]', s.lower())
    return set([p.strip() for p in parts if p.strip()])

def score_pair(candidate, internship):
    cskills = normalize_skills(candidate.skills)
    iskills = normalize_skills(internship.required_skills)
    overlap = cskills.intersection(iskills)
    # basic scoring: overlap count + experience weight
    score = len(overlap) * 10 + min(candidate.experience, 3) * 5
    return score

def run_matching():
    results = []
    candidates = Candidate.query.all()
    internships = Internship.query.all()
    # Simple greedy assignment: for each candidate pick best internship
    for c in candidates:
        best = None
        best_score = -1
        for i in internships:
            s = score_pair(c, i)
            if s > best_score:
                best = i
                best_score = s
        if best is not None:
            results.append({'candidate_id': c.id, 'internship_id': best.id, 'score': round(best_score,2)})
    return results

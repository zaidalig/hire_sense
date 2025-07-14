# hire_sense/utils/resume_parser.py
import re
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_skills(resume_text):
    skills = ["Python", "Java", "Machine Learning", "Data Science", "Django", "React"]
    skill_found = []

    for skill in skills:
        if skill.lower() in resume_text.lower():
            skill_found.append(skill)
    
    return skill_found

def extract_name_and_education(resume_text):
    doc = nlp(resume_text)
    name = None
    education = None

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text
        elif ent.label_ == "ORG":
            education = ent.text

    return name, education


# resumes/utils/resume_parser.py
from core.models import Resume

def save_parsed_resume(resume_text, user):
    name, education = extract_name_and_education(resume_text)
    skills = extract_skills(resume_text)

    # Save extracted resume details to the core Resume model
    resume = Resume.objects.create(
        user=user,
        file=None,  # Since the file is already uploaded, we don't need to save it again.
        parsed_skills=", ".join(skills),
        parsed_education=education,
        parsed_experience="",  # Extract experience similarly if needed
        status='pending',  # Default status
    )
    resume.save()
    return resume

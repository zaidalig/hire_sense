from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from core.models import Job

def match_resume_to_job(resume_text, job_descriptions):
    """Match resume with job descriptions based on similarity scores."""
    # Combine resume text with job descriptions
    vectorizer = TfidfVectorizer(stop_words='english')

    all_texts = job_descriptions + [resume_text]
    tfidf_matrix = vectorizer.fit_transform(all_texts)

    # Compute cosine similarity between resume and all job descriptions
    similarity_scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

    return similarity_scores.flatten()

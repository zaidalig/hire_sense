# resumes/utils/bert_matching.py
from transformers import BertTokenizer, BertModel
import torch
from sklearn.metrics.pairwise import cosine_similarity

# Load the pre-trained BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

def get_bert_embeddings(text):
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512)
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1)  # Mean pooling for sentence embeddings

def match_resume_to_job(resume_text, job_description):
    resume_embedding = get_bert_embeddings(resume_text)
    job_embedding = get_bert_embeddings(job_description)

    similarity = cosine_similarity(resume_embedding.detach().numpy(), job_embedding.detach().numpy())
    return similarity[0][0]

def recommend_jobs(resume_text, job_descriptions):
    job_scores = []

    for job in job_descriptions:
        score = match_resume_to_job(resume_text, job["description"])
        job_scores.append((job["id"], score))

    # Sort by similarity score
    job_scores.sort(key=lambda x: x[1], reverse=True)
    return job_scores[:5]  # Return top 5 recommended jobs

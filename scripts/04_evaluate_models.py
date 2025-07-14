import joblib
from sklearn.metrics import classification_report
from transformers import T5ForConditionalGeneration, T5Tokenizer

# Evaluate Job Categorization Model
job_categorization_model = joblib.load('./models/job_categorization_model.pkl')

# Load the evaluation data (we'll use the test data from the preprocessed data)
import pandas as pd
test_data = pd.read_csv('./dataset/cleaned_resume_data.csv')
X_test = test_data['cleaned_text']
y_test = test_data['job_role']

# Vectorize the test data for evaluation
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
X_test_tfidf = vectorizer.fit_transform(X_test)

# Predict job categories on the test data
y_pred = job_categorization_model.predict(X_test_tfidf)

# Print classification report for Job Categorization
print("Job Categorization Model Evaluation:")
print(classification_report(y_test, y_pred))

# Evaluate Resume Suggestions Model
print("\nEvaluating Resume Suggestions Model...")

# Load the T5 model and tokenizer for suggestions
resume_suggestions_model = T5ForConditionalGeneration.from_pretrained("./models/t5_resume_suggestions_model")
tokenizer = T5Tokenizer.from_pretrained("./models/t5_resume_suggestions_model")

# Example of evaluating suggestions for a resume
resume_text = "Your resume text goes here"  # Sample resume text
input_text = f"resume: {resume_text}"
input_ids = tokenizer(input_text, return_tensors="pt").input_ids

# Generate suggestion for the resume
output = resume_suggestions_model.generate(input_ids, max_length=50, num_beams=5, early_stopping=True)
suggestion = tokenizer.decode(output[0], skip_special_tokens=True)

print(f"Suggested Improvement: {suggestion}")

print("\nModel Training and Evaluation Completed!")

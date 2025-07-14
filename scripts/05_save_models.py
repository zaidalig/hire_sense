import joblib
from transformers import T5ForConditionalGeneration, T5Tokenizer

# Save Job Categorization Model
job_categorization_model = joblib.load('./models/job_categorization_model.pkl')
joblib.dump(job_categorization_model, './models/job_categorization_model.pkl')
print("Job Categorization Model saved.")

# Save Resume Suggestions Model
resume_suggestions_model = T5ForConditionalGeneration.from_pretrained("./models/t5_resume_suggestions_model")
tokenizer = T5Tokenizer.from_pretrained("./models/t5_resume_suggestions_model")

# Save models
resume_suggestions_model.save_pretrained('./models/t5_resume_suggestions_model')
tokenizer.save_pretrained('./models/t5_resume_suggestions_model')
print("Resume Suggestions Model saved.")

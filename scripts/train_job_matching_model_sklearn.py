import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib
import os

# Load the cleaned updated resume dataset for job matching
job_matching_data = pd.read_csv('./dataset/cleaned_updated_resume_dataset.csv')

# Check the data
print(f"Total samples: {len(job_matching_data)}")
print(job_matching_data.head())

# Feature and target
X = job_matching_data['cleaned_resume']  # Resume text (cleaned)
y = job_matching_data['cleaned_category']  # Job category (cleaned)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Vectorize the text data using TfidfVectorizer
vectorizer = TfidfVectorizer(max_features=5000)  # You can adjust max_features as needed
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Initialize and train the Logistic Regression model
model = LogisticRegression(max_iter=1000)  # You can tweak max_iter if needed
model.fit(X_train_tfidf, y_train)

# Evaluate the model
y_pred = model.predict(X_test_tfidf)
print(classification_report(y_test, y_pred))

# Ensure the models directory exists
models_directory = './models'
if not os.path.exists(models_directory):
    os.makedirs(models_directory)

# Save the trained model and vectorizer
joblib.dump(model, os.path.join(models_directory, 'job_matching_model_sklearn.pkl'))
joblib.dump(vectorizer, os.path.join(models_directory, 'tfidf_vectorizer_sklearn.pkl'))

print("Job matching model trained and saved.")

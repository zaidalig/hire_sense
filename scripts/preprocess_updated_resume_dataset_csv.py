import pandas as pd
import re

# Function to clean text data
def preprocess_text(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'\W', ' ', text)  # Remove non-alphanumeric characters
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with single space
    return text

# Function to process the UpdatedResumeDataSet CSV
def process_updated_resume_dataset_csv(file_path):
    print(f"Processing CSV file: {file_path}")
    
    # Load CSV
    data = pd.read_csv(file_path)
    
    # Check if the required columns exist
    if 'Resume' not in data.columns or 'Category' not in data.columns:
        print("Necessary columns ('Resume', 'Category') not found. Skipping this dataset.")
        return pd.DataFrame()  # Return an empty DataFrame if required columns are missing
    
    # Clean the resume text
    data['cleaned_resume'] = data['Resume'].apply(preprocess_text)
    
    # Clean the Category (convert it to lowercase for consistency)
    data['cleaned_category'] = data['Category'].apply(lambda x: x.lower())
    
    return data[['cleaned_resume', 'cleaned_category']]

# --- Define the path to the 'UpdatedResumeDataSet.csv' ---
csv_file_path = './dataset/UpdatedResumeDataSet.csv'  # Adjust to your folder structure

# Process the CSV file
cleaned_data = process_updated_resume_dataset_csv(csv_file_path)

# --- Save the Cleaned Data ---
if not cleaned_data.empty:
    cleaned_data.to_csv('./dataset/cleaned_updated_resume_dataset.csv', index=False)
    print("CSV data preprocessed and saved to 'cleaned_updated_resume_dataset.csv'")
else:
    print("No valid CSV data to save.")

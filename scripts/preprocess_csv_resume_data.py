import pandas as pd
import os
import re
from bs4 import BeautifulSoup

# Function to clean text data
def preprocess_text(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'\W', ' ', text)  # Remove non-alphanumeric characters
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with single space
    return text

# Function to extract text from HTML content
def extract_text_from_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text()

# Function to process CSV files in the 'resume' folder
def process_csv_files(folder_path, possible_columns=['Resume_str', 'Resume_html']):
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    all_data = []
    
    for csv_file in csv_files:
        file_path = os.path.join(folder_path, csv_file)
        print(f"Processing CSV file: {csv_file}")
        
        # Load CSV
        data = pd.read_csv(file_path)
        
        # Dynamically check if any column contains resume HTML content
        valid_column = None
        for col in possible_columns:
            if col in data.columns:
                valid_column = col
                break
        
        if valid_column is None:
            print(f"None of the columns ({', '.join(possible_columns)}) found in {csv_file}. Skipping this dataset.")
            continue
        
        # Extract and clean resume text from HTML
        data['cleaned_text'] = data[valid_column].apply(lambda x: preprocess_text(extract_text_from_html(x)))
        
        # Add job category (you can modify based on your dataset)
        if 'Category' in data.columns:  # Adjust this based on your dataset column name for the job role
            all_data.append(data[['cleaned_text', 'Category']])  # Modify as per column availability
        else:
            print(f"Category column not found in {csv_file}. Skipping this dataset.")
            continue
    
    if all_data:
        return pd.concat(all_data, ignore_index=True)
    else:
        return pd.DataFrame()  # Return an empty DataFrame if no valid data

# --- Define the path to the 'resume' folder ---
csv_folder_path = './dataset/snehaan/resume/'  # Adjust to your folder structure

# Process the CSV files in the folder
csv_data = process_csv_files(csv_folder_path, possible_columns=['Resume_str', 'Resume_html'])

# --- Save the Combined Cleaned Data ---
if not csv_data.empty:
    csv_data.to_csv('./dataset/cleaned_csv_resume_data_with_html.csv', index=False)
    print("CSV data preprocessed and saved to 'cleaned_csv_resume_data_with_html.csv'")
else:
    print("No valid CSV data to save.")

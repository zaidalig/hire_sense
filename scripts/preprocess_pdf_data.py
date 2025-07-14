import os
import re
import pandas as pd
from PyPDF2 import PdfReader

# Function to clean text data
def preprocess_text(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'\W', ' ', text)  # Remove non-alphanumeric characters
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with single space
    return text

# Function to extract text from PDFs
def extract_pdf_text(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

# Function to process PDF files in the given folder
def process_pdf_files(folder_path):
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
    all_data = []
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        print(f"Processing PDF file: {pdf_file}")
        
        # Extract text from the PDF
        pdf_text = extract_pdf_text(pdf_path)
        
        # Clean the text
        cleaned_text = preprocess_text(pdf_text)
        
        # For simplicity, assign a job role (this can be adjusted)
        job_role = "Unknown"  # You can modify this part based on your requirement
        
        all_data.append({"cleaned_text": cleaned_text, "job_role": job_role})
    
    # Convert the list to a DataFrame and return
    return pd.DataFrame(all_data)

# --- Define the path to the PDF folder ---
pdf_folder_path = './dataset/snehaan/data/data/'  # Adjust to your folder structure

# Process the PDF files in the folder
pdf_data = process_pdf_files(pdf_folder_path)

# Save the cleaned data to a new CSV file
pdf_data.to_csv('./dataset/cleaned_pdf_data.csv', index=False)
print("PDF data preprocessed and saved to 'cleaned_pdf_data.csv'")

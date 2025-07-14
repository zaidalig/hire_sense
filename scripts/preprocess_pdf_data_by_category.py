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
def process_pdf_files_by_category(base_folder_path):
    all_data = []
    
    # Loop over each subfolder (category) inside the base folder
    for category in os.listdir(base_folder_path):
        category_folder_path = os.path.join(base_folder_path, category)
        
        if os.path.isdir(category_folder_path):  # Check if it's a folder
            print(f"Processing category: {category}")
            
            # Process PDF files inside the category folder
            pdf_files = [f for f in os.listdir(category_folder_path) if f.endswith('.pdf')]
            
            for pdf_file in pdf_files:
                pdf_path = os.path.join(category_folder_path, pdf_file)
                print(f"Processing PDF file: {pdf_file}")
                
                # Extract text from the PDF
                pdf_text = extract_pdf_text(pdf_path)
                
                # Clean the extracted text
                cleaned_text = preprocess_text(pdf_text)
                
                # Store the cleaned text along with the category as the job role
                all_data.append({"cleaned_text": cleaned_text, "job_role": category})
    
    # Convert the list to a DataFrame and return
    return pd.DataFrame(all_data)

# --- Define the path to the base folder containing categorized subfolders ---
pdf_base_folder_path = './dataset/snehaan/data/data/'  # Adjust to your folder structure

# Process the PDF files in the base folder
pdf_data = process_pdf_files_by_category(pdf_base_folder_path)

# Check if the DataFrame is empty before saving
if not pdf_data.empty:
    # Save the cleaned data to a new CSV file
    pdf_data.to_csv('./dataset/cleaned_pdf_data_by_category.csv', index=False)
    print("PDF data preprocessed and saved to 'cleaned_pdf_data_by_category.csv'")
else:
    print("No valid PDF data to save.")

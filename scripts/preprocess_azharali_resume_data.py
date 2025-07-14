from datasets import load_dataset
import pandas as pd
import re

# Function to clean text data
def preprocess_text(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'\W', ' ', text)  # Remove non-alphanumeric characters
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with single space
    return text

# Load the AzharAli05 Resume Screening Dataset from Hugging Face
dataset = load_dataset("AzharAli05/Resume-Screening-Dataset")

# Check the structure of the dataset
print(f"Dataset keys: {dataset.keys()}")
print(f"First few entries of the train set: {dataset['train'][0]}")

# Preprocess the text data
def preprocess_azharali_data(dataset):
    # Process only the 'train' dataset
    print(f"Processing 'train' dataset...")

    data = dataset['train']
        
    # Extracting and cleaning the resume text
    data = data.map(lambda x: {'cleaned_text': preprocess_text(x['Resume'])})

    # Optional: Save the cleaned dataset (could be useful for later steps)
    cleaned_file_path = "./dataset/cleaned_azharali_train.csv"
    data.to_csv(cleaned_file_path, index=False)
    print(f"Cleaned train dataset saved to {cleaned_file_path}")

    return dataset

# Preprocess the dataset
cleaned_dataset = preprocess_azharali_data(dataset)

print("AzharAli05 Resume Screening Dataset processed and cleaned.")

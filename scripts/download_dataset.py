from datasets import load_dataset

# Load the dataset
dataset = load_dataset("AzharAli05/Resume-Screening-Dataset")

# Specify the directory where you want to save the dataset locally
output_dir = "./Resume_Screening_Dataset"

# Save the dataset to a local directory
dataset.save_to_disk(output_dir)

print(f"Dataset saved locally at {output_dir}")

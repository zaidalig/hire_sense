from transformers import T5ForConditionalGeneration, T5Tokenizer

def suggest_improvements(resume_text):
    """Generate resume improvement suggestions using a pre-trained model."""
    model = T5ForConditionalGeneration.from_pretrained('./models/t5_resume_suggestions_model')
    tokenizer = T5Tokenizer.from_pretrained('./models/t5_resume_suggestions_model')

    inputs = tokenizer(f"suggest improvements for resume: {resume_text}", return_tensors="pt")
    outputs = model.generate(inputs['input_ids'], max_length=150)
    suggestion = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return suggestion

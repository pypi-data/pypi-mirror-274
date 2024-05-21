import json
import spacy
import argparse
from pdfminer.high_level import extract_text
import os
from spacy.language import Language
import warnings

# Suppress specific warnings
warnings.filterwarnings("ignore", message="torch.utils._pytree._register_pytree_node is deprecated")

# Construct the absolute path to the 'model-best' directory
model_path = os.path.join(os.path.dirname(__file__), 'model-best')

# Load the spaCy model once
try:
    nlp = spacy.load(model_path)
except ValueError:
    # In case the transformer is not registered, let's add it manually
    @Language.factory("transformer")
    def create_transformer_component(nlp, name):
        from spacy_transformers import Transformer
        return Transformer(nlp.vocab)
    
    nlp = spacy.load(model_path)

def pdf_to_text(filepath):
    """
    Extracts text from a PDF file.

    :param filepath: Path to the PDF file
    :return: Extracted text as a string
    """
    return extract_text(filepath)

def extract_entities(text, nlp):
    """
    Extracts entities from the text using a spaCy model.

    :param text: Input text
    :param nlp: spaCy NLP model
    :return: Dictionary of entities
    """
    doc = nlp(text)
    
    # Initialize a dictionary to hold entity lists
    entities = {
        'first_name': [],
        'last_name': [],
        'email': [],
        'phone': [],
        'country': [],
        'state': [],
        'city': [],
        'pincode': [],
        'college_name': [],
        'education': [],
        'designation': [],
        'position_held': [],
        'companies_worked': [],
        'projects_worked': [],
        'skills': [],
        'total_experience': [],
        'language': [],
        'linkedin': [],
        'github': []
    }
    
    # Populate the dictionary with entities from the document
    for ent in doc.ents:
        label = ent.label_.lower()
        if label in entities:
            entities[label].append(ent.text)
    
    # Remove duplicates by converting lists to sets and back to lists
    for key in entities:
        entities[key] = list(set(entities[key]))
    
    return entities

def parse_resume(filepath, nlp):
    """
    Converts a PDF file to a JSON object with extracted entities.

    :param filepath: Path to the PDF file
    :param nlp: spaCy NLP model
    :return: JSON object with extracted entities
    """
    text = pdf_to_text(filepath)
    entities = extract_entities(text, nlp)
    entities_json = json.dumps(entities, indent=4)
    return entities_json

def main():
    parser = argparse.ArgumentParser(description="Parse a resume PDF file and extract entities.")
    parser.add_argument("filepath", type=str, help="Path to the resume PDF file.")
    args = parser.parse_args()
    
    parsed_resume = parse_resume(args.filepath, nlp)
    print(parsed_resume)

if __name__ == "__main__":
    main()

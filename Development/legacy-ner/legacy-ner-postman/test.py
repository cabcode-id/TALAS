
import json
import spacy
from googletrans import Translator
from rapidfuzz import fuzz
from spacy.util import load_model_from_path
from pathlib import Path
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import re 

# Load Spacy Models
nlp = spacy.load("en_core_web_sm")  # English language model
model_path = Path("model")  # Adjust if necessary
nlp_custom = load_model_from_path(model_path)

translator = Translator()

# Mock Data
feedback_data = [
    {"id": 1, "content": "Calon gubernur (cagub)-calon wakil gubernur (cawagub) Ridwan Kamil-Suswono menyoroti kesehatan mental di Jakarta. Menurut Ridwan Kamil, Jakarta menduduki peringkat ke-9 sebagai kota paling stres di dunia. Dia mengutip data Dinas Kesehatan (Dinkes) Jakarta yang menunjukkan bahwa penderita skizofrenia, jumlahnya lebih banyak dari pasien pneumonia, diare, diabetes hingga DBD."},
    {"id": 2, "content": "Kementerian Perhubungan tidak mewajibkan rapid test COVID-19 untuk perjalanan darat lintas daerah, kecuali untuk tujuan Bali."},
]

# Valid labels
VALID_LABELS = [
    'PERSON', 'ORGANIZATION', 'LOCATION', 'ORG', 'GPE', 'LOC', 'EVENT', 'PRODUCT', 'LAW', 'WORK_OF_ART', 
    'NORP', 'FAC'
]
factory = StopWordRemoverFactory()
STOPWORDS = set(factory.get_stop_words())

# Function to detect words with capitalized first letters
def exclude_capitalized_words(text):
    capitalized_words = re.findall(r'\b[A-Z][a-zA-Z]*\b', text)
    placeholders = {word: f"__PLACEHOLDER_{i}__" for i, word in enumerate(capitalized_words)}
    
    for word, placeholder in placeholders.items():
        text = text.replace(word, placeholder)
    
    return text, placeholders

def restore_capitalized_words(text, placeholders):
    for word, placeholder in placeholders.items():
        text = text.replace(placeholder, word)
    
    return text

# Function to normalize and clean up the text
def normalize_text(text):
    return re.sub(r'\s+', '', text.lower())


def annotate_data():
    annotated_data = []
    
    for record in feedback_data:
        try:
            text, placeholders = exclude_capitalized_words(record["content"])
            text_en = translator.translate(text, src='id', dest='en').text
            doc_default = nlp(text_en)
            doc_custom = nlp_custom(record["content"])

            keyword = []

            # Extract entities using the default English model
            for ent in doc_default.ents:
                if len(ent.text) > 2 and ent.label_ in VALID_LABELS:
                    translated_entity = translator.translate(ent.text, src='en', dest='id').text
                    if translated_entity.lower() not in STOPWORDS and translated_entity in record["content"] and \
                            not any(fuzz.ratio(translated_entity.lower(), existing_ent['text'].lower()) > 80 for existing_ent in keyword):
                        start = record["content"].index(translated_entity)
                        end = start + len(translated_entity)
                        keyword.append({
                            "start": start,
                            "end": end,
                            "label": ent.label_,
                            "text": translated_entity,
                            "source": "default"
                        })

            # Extract entities using the custom Indonesian model
            for ent in doc_custom.ents:
                if len(ent.text) > 2 and ent.label_ in VALID_LABELS:
                    if not any(fuzz.ratio(ent.text.lower(), existing_ent['text'].lower()) > 80 for existing_ent in keyword):
                        start = record["content"].index(ent.text)
                        end = start + len(ent.text)
                        keyword.append({
                            "start": start,
                            "end": end,
                            "label": ent.label_,
                            "text": ent.text,
                            "source": "custom"
                        })

            text_en = restore_capitalized_words(text_en, placeholders)

            annotated_data.append({
                'id': record["id"],
                'content': record["content"],
                'keyword': keyword,  
            })

        except Exception as e:
            print(f"Error processing record {record['id']}: {str(e)}")

    return json.dumps(annotated_data, indent=2, ensure_ascii=False)

# Run the test and print the output
if __name__ == "__main__":
    result = annotate_data()
    print(result)

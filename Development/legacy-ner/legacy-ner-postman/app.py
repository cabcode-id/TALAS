import json
import spacy
from flask import Flask, request, jsonify
from spacy.training.example import Example
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from googletrans import Translator
from collections import Counter
import re
from rapidfuzz import fuzz
from database import db
from models import Feedback
from config import Config

# Setup Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)

# Load Spacy Models
nlp = spacy.load("en_core_web_sm")  # English language model
nlp_custom = spacy.load("spacy model")  # Custom trained model
translator = Translator()

# Validating entities (filtering rules)
VALID_LABELS = [
    'PERSON', 'ORGANIZATION', 'LOCATION', 'ORG', 'GPE', 'LOC', 'EVENT', 'PRODUCT', 'LAW', 'WORK_OF_ART', 
    'NORP', 'FAC'
]

# Using stopwords from Sastrawi
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

# Function to calculate the top 10 keywords from the list
def calculate_top_keywords(keyword):
    normalized_counter = Counter()
    original_map = {}

    for entity in keyword:
        norm_text = normalize_text(entity)
        if norm_text not in STOPWORDS:
            normalized_counter[norm_text] += 1
            original_map[norm_text] = entity

    top_keywords = normalized_counter.most_common(10)
    return [{"keyword": original_map[key], "count": count} for key, count in top_keywords]

# Route to annotate raw data and extract entities
@app.route('/annotate', methods=['GET'])
def annotate_data():
    feedback_data = Feedback.query.filter(Feedback.keyword == None).all() 
    annotated_data = []

    for record in feedback_data:
        try:
            text, placeholders = exclude_capitalized_words(record.content)
            text_en = translator.translate(text, src='id', dest='en').text
            doc_default = nlp(text_en)
            doc_custom = nlp_custom(record.content)

            keyword = []

            # Extract entities from the default model (en_core_web_sm) and translate to Indonesian
            for ent in doc_default.ents:
                if len(ent.text) > 2 and ent.label_ in VALID_LABELS:
                    translated_entity = translator.translate(ent.text, src='en', dest='id').text
                    if translated_entity.lower() not in STOPWORDS and translated_entity in record.content and \
                            not any(fuzz.ratio(translated_entity.lower(), existing_ent['text'].lower()) > 80 for existing_ent in keyword):
                        start = record.content.index(translated_entity)
                        end = start + len(translated_entity)
                        keyword.append({
                            "start": start,
                            "end": end,
                            "label": ent.label_,
                            "text": translated_entity
                        })

            # Extract entities from the custom model (spacy model in Indonesian)
            for ent in doc_custom.ents:
                if len(ent.text) > 2 and ent.label_ in VALID_LABELS:
                    if not any(fuzz.ratio(ent.text.lower(), existing_ent['text'].lower()) > 80 for existing_ent in keyword):
                        start = record.content.index(ent.text)
                        end = start + len(ent.text)
                        keyword.append({
                            "start": start,
                            "end": end,
                            "label": ent.label_,
                            "text": ent.text
                        })

            text_en = restore_capitalized_words(text_en, placeholders)

            # Save the annotations in the database
            record.keyword = json.dumps(keyword)
            db.session.commit()

            annotated_data.append({
                'id': record.id,
                'content': record.content,
                'keyword': keyword,  
            })

        except Exception as e:
            print(f"Error processing record {record.id}: {str(e)}")

    return jsonify(annotated_data)

# Route to calculate the top 10 keywords from all keyword columns
@app.route('/top_keywords', methods=['GET'])
def top_keywords():
    feedback_data = Feedback.query.filter(Feedback.keyword.isnot(None)).all()  
    all_keyword = []

    for record in feedback_data:
        try:
            keyword = json.loads(record.keyword)  

            for entity in keyword:
                if entity['text'].lower() not in STOPWORDS:
                    all_keyword.append(entity['text'])

        except Exception as e:
            print(f"Error processing record {record.id}: {str(e)}")

    top_keywords = calculate_top_keywords(all_keyword)

    return jsonify(top_keywords)

if __name__ == '__main__':
    app.run(debug=True)

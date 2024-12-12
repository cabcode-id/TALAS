from flask import Flask, request, render_template, redirect
import spacy
import json
from mysql.connector import connect, Error

app = Flask(__name__)

# Path to the spaCy model
MODEL_PATH = "spacy model"
nlp = spacy.load(MODEL_PATH)

# Function to connect to the MySQL database
def connect_db():
    """Establishes a connection to the MySQL database."""
    try:
        return connect(
            host="localhost",
            user="root",
            password="",
            database="ner_feedback"
        )
    except Error as e:
        print(f"Error while connecting to the database: {e}")
        return None

@app.route('/')
def index():
    """Renders the home page."""
    return render_template("ner_home.html")

@app.route('/process', methods=["POST"])
def process_text():
    """Processes the input text, applies spaCy NLP model, and extracts named entities."""
    text = request.form["input_data"]
    doc = nlp(text)
    entities_data = [(ent.text, ent.label_) for ent in doc.ents]
    return render_template("ner_home.html", input_text=text, results=entities_data)

@app.route('/report', methods=["POST"])
def report():
    """Handles the feedback submission, updates entities, and stores them in the database."""
    text = request.form["input_text"]
    corrected_entities = request.form.getlist("corrected_entities[]")
    entity_labels = request.form.getlist("entity_labels[]")
    removed_entities = request.form.getlist("removed_entities[]")
    action = request.form.get("action")

    # Filter out removed entities
    filtered_entities = [
        corrected_entities[i] for i in range(len(corrected_entities))
        if corrected_entities[i] not in removed_entities
    ]

    if action == "change":
        # Save feedback and update spaCy model with corrected entities
        feedback_data = {
            "text": text,
            "corrected_entities": filtered_entities,
            "entity_labels": [entity_labels[i] for i in range(len(corrected_entities)) if corrected_entities[i] not in removed_entities]
        }
        save_feedback_to_database(feedback_data)
        update_entity_ruler(feedback_data)
    
    # Save the corrected keywords to the database
    save_keywords_to_database(text, filtered_entities)

    return render_template("article.html", text=text, keywords=filtered_entities)

@app.route('/clear', methods=["POST"])
def clear_data():
    """Clears the input data and renders the home page again."""
    return render_template("ner_home.html")

def save_keywords_to_database(text, keywords):
    """Saves the extracted keywords (patterns only) to the database."""
    conn = connect_db()
    if not conn:
        print("Failed to connect to the database!")
        return

    try:
        cursor = conn.cursor()
        keywords_json = json.dumps(keywords)
        query = "INSERT INTO feedback (text, entities) VALUES (%s, %s)"
        cursor.execute(query, (text, keywords_json))
        conn.commit()
        print("Keywords successfully saved.")
    except Error as e:
        print(f"Error while saving keywords: {e}")
    finally:
        conn.close()

def save_feedback_to_database(feedback_data):
    """Saves detailed feedback, including corrected entities, to the database."""
    conn = connect_db()
    if not conn:
        print("Failed to connect to the database!")
        return

    try:
        cursor = conn.cursor()
        feedback_json = json.dumps(feedback_data['corrected_entities'])
        query = "INSERT INTO feedback (text, corrected_entities) VALUES (%s, %s)"
        cursor.execute(query, (feedback_data['text'], feedback_json))
        conn.commit()
        print("Feedback successfully saved.")
    except Error as e:
        print(f"Error while saving feedback: {e}")
    finally:
        conn.close()

def update_entity_ruler(feedback_data):
    """Updates the spaCy EntityRuler with new patterns based on the feedback."""
    ruler = nlp.get_pipe("entity_ruler") if "entity_ruler" in nlp.pipe_names else nlp.add_pipe("entity_ruler", last=True)
    patterns = [{"label": feedback_data['entity_labels'][i], "pattern": feedback_data['corrected_entities'][i]}
                for i in range(len(feedback_data['corrected_entities']))]
    ruler.add_patterns(patterns)
    nlp.to_disk(MODEL_PATH)

@app.route('/article/<int:id>')
def view_article(id):
    """Views a specific article and its associated keywords based on the article ID."""
    conn = connect_db()
    if not conn:
        return "Failed to connect to the database!"

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT text, entities FROM feedback WHERE id = %s", (id,))
        article = cursor.fetchone()
        if not article:
            return "Article not found!"
        
        # Load the saved keywords (patterns) from the database
        keywords = json.loads(article['entities'])
        return render_template("article.html", text=article['text'], keywords=keywords)
    except Error as e:
        print(f"Error retrieving article: {e}")
        return "Error retrieving article!"
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

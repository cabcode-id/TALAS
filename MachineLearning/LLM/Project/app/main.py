# Standard libraries
import sys
import pickle
import numpy as np
import pandas as pd
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0' # resolves warning

# Third-party libraries
import tensorflow as tf
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import nest_asyncio
import swifter
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import re
from keras.preprocessing.sequence import pad_sequences
from tensorflow.keras import preprocessing
import networkx as nx
from sklearn.metrics.pairwise import cosine_similarity

# Internal imports
from llama_index.core import Settings, Document, VectorStoreIndex, SummaryIndex
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
sys.modules['keras.src.preprocessing'] = preprocessing
nest_asyncio.apply() # async patch for nested event loops

app = Flask(__name__)

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
Settings.llm = OpenAI(model='chatgpt-4o-latest')
Settings.embed_model = OpenAIEmbedding(model="text-embedding-ada-002")

def loadClusterModel():
    try:
        with open('app/model/cluster/kmeans_8_cluster.pkl', 'rb') as f:
            kmeans = pickle.load(f)
    except FileNotFoundError:
        with open('model/cluster/kmeans_8_cluster.pkl', 'rb') as f:
            kmeans = pickle.load(f)
    return kmeans

def loadModel(model_path, model_name):
    try:
        with open(f"{model_path}/{model_name}_tokenizer.pkl", 'rb') as f:
            tokenizer = pickle.load(f)
    except FileNotFoundError:
        model_path = 'app/' + model_path
        with open(f"{model_path}/{model_name}_tokenizer.pkl", 'rb') as f:
            tokenizer = pickle.load(f)

    interpreter = tf.lite.Interpreter(model_path=f"{model_path}/{model_name}.tflite")
    interpreter.allocate_tensors()
    return tokenizer, interpreter

# Load Models
kmeans = loadClusterModel()
bias_tokenizer, bias_interpreter = loadModel('model/bias', 'bias')
hoax_tokenizer, hoax_interpreter = loadModel('model/hoax', 'hoax')
ideology_tokenizer, ideology_interpreter = loadModel('model/ideology', 'ideology')

# Load Stopword and Stemmer
stopword_factory = StopWordRemoverFactory()
stopword = stopword_factory.create_stop_word_remover()
stemmer_factory = StemmerFactory()
stemmer = stemmer_factory.create_stemmer()

def preprocessText(text):
    text = str(text)

    # change text to lowercase
    text = text.lower()

    # change link with http/https patterns
    text = re.sub(r'http\S+', '', text)

    # remove hashtag and username
    text = re.sub(r'(@\w+|#\w+)', '', text)

    # remove character other than a-z and A-Z
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)

    # replace new line '\n' with space
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\t', ' ', text)

    # remove stopword with sastrawi library
    text = stopword.remove(text)

    # do stemming with sastrawi library
    text = stemmer.stem(text)

    # removing more than one space
    text = re.sub(r'\s{2,}', ' ', text)

    return text

@app.route('/cleaned', methods=['POST'])
def cleaned():
    try:
        input_data = request.json

        if 'content' not in input_data:
            return jsonify({"error": "Invalid input, 'content' field is required"}), 400

        content = input_data['content']

        if isinstance(content, str): 
            cleaned = preprocessText(content)
            return jsonify({"cleaned": cleaned})

        elif isinstance(content, list): 
            if not all(isinstance(item, str) for item in content):
                return jsonify({"error": "All items in the 'content' list must be strings"}), 400

            df = pd.DataFrame({'content': content})
            df['cleaned'] = df['content'].swifter.apply(preprocessText)
            return jsonify({"cleaned": df['cleaned'].tolist()})

        else:  # Invalid type
            return jsonify({"error": "'content' must be either a string or a list of strings"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def predictWithModel(newsText, tokenizer, interpreter, maxLen):
    new_sequences = tokenizer.texts_to_sequences([newsText])
    new_padded = pad_sequences(new_sequences, maxlen=maxLen, padding='post', truncating='post')
    new_padded = new_padded.astype('float32')

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    interpreter.set_tensor(input_details[0]['index'], new_padded)
    interpreter.invoke()

    predictions = interpreter.get_tensor(output_details[0]['index'])
    return predictions

def predictBias(newsText):
    predictions = predictWithModel(newsText, bias_tokenizer, bias_interpreter, 30)
    return [1 if pred > 0.5 else 0 for pred in predictions][0]

def predictHoax(newsText):
    predictions = predictWithModel(newsText, hoax_tokenizer, hoax_interpreter, 100)
    return float(predictions[0])

def predictIdeology(newsText):
    predictions =  predictWithModel(newsText, ideology_tokenizer, ideology_interpreter, 100)
    return [1 if pred > 0.75 else 0 for pred in predictions][0]

def completeDf(df):
    for col in ['bias', 'hoax', 'ideology', 'embedding', 'cleaned']:
        if col not in df.columns:
            df[col] = None

    mask = df['cleaned'].isnull() | (df['cleaned'] == '')

    df.loc[mask, 'cleaned'] = df.loc[mask, 'content'].swifter.apply(preprocessText)

    df['embedding'] = df.apply(
        lambda row: row['embedding'] if isinstance(row.get('embedding'), (list, np.ndarray)) else Settings.embed_model.get_text_embedding(row['content']),
        axis=1
    )

    df['bias'] = df.swifter.apply(
        lambda row: row['bias'] if pd.notnull(row['bias']) else predictBias([row['cleaned']]),
        axis=1
    )

    df['hoax'] = df.swifter.apply(
        lambda row: row['hoax'] if pd.notnull(row['hoax']) else predictHoax([row['cleaned']]),
        axis=1
    )

    df['ideology'] = df.swifter.apply(
        lambda row: row['ideology'] if pd.notnull(row['ideology']) else predictIdeology([row['cleaned']]),
        axis=1
    )

    return df

def create_documents(df):
    documents = []
    for index, row in df.iterrows():
        metadata = {'title': row['title']}

        if 'bias' in row and not pd.isnull(row['bias']):
            metadata['bias'] = 'biased' if row['bias'] == 1 else 'not biased'

        if 'hoax' in row and not pd.isnull(row['hoax']):
            metadata['hoax'] = row['hoax']

        if 'ideology' in row and not pd.isnull(row['ideology']):
            metadata['ideology'] = 'liberalism' if row['ideology'] == 1 else 'conservative'

        document = Document(
            text=row['content'],
            doc_id=str(index),
            metadata=metadata,
            embedding=row['embedding']
        )
        documents.append(document)
    return documents


def create_summary(documents):
    if(documents == []):
        return "No articles written in this perspective."
    
    summarizeQuery = """
    Create a short, detailed, and factual summary of the articles.
    For more context for you, chatgpt, information regarding: 
    it's bias (0: not biased/neutral, 1: biased), 
    hoax (0: is factual, 1: has hoax), 
    and whether it's ideology (liberal or conservative)
    which are all detected using machine learning models are also included.
    Do NOT discuss about the article's hoax, bias, or political view. 
    Do NOT rely on previous knowledge.
    Use Indonesian language. 
    """

    summary_index = SummaryIndex.from_documents(documents, use_async=True)
    summary_query_engine = summary_index.as_query_engine(llm=Settings.llm, response_mode='tree_summarize')
    summary = summary_query_engine.query(summarizeQuery)
    return summary.response

def create_analysis(query_engine):
    compareQuery = """
    I have a collection of articles classified as either liberal or conservative. These articles all discuss the same event but from differing perspectives.
    Your task is to analyze a given query and generate a response summarizing how articles from each perspective address the topic. 
    
    Ensure the response follows this structure:
    Liberal: [Summarize key points using the language and tone of liberal articles. If no liberal perspective exists, only explain that there are no liberal perspectives.]
    Conservative: [Summarize key points using the language and tone of conservative articles. If no conservative perspective exists, only explain that there are no conservative perspectives.]
    
    Follow these guidelines:
    Derive all information directly from the provided articles—do not rely on prior knowledge or external context.
    Keep summaries concise, factual, and reflective of the language and tone used in the articles. Avoid being too wordy.
    Highlight notable phrases or specific terminology unique to each perspective to showcase differences in framing or emphasis.
    Only include sections for perspectives present in the articles. If only one perspective is available, summarize that side alone.
    Format responses as concise paragraphs. Do not include editorial commentary, personal interpretation, or merge perspectives into one.
    Use Indonesian language.
    """
    response = query_engine.query(compareQuery)
    return response.response

@app.route('/cluster', methods=['POST'])
def predict_cluster():
    try:
        input_data = request.json
        if 'content' not in input_data:
            return jsonify({"error": "Invalid input, 'content' field is required"}), 400

        content = input_data['content']
        
        embedding = Settings.embed_model.get_text_embedding(content)
        embedding = np.array(embedding, dtype=np.float32).reshape(1, -1)

        cluster = kmeans.predict(embedding)[0]

        return jsonify({"cluster": int(cluster)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/bias', methods=['POST'])
def biasAPI():
    try:
        input_data = request.json
        if 'content' not in input_data:
            return jsonify({"error": "Invalid input, 'content' field is required"}), 400

        content = input_data['content']
        
        bias = predictBias(content)

        return jsonify({"bias": bias})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/hoax', methods=['POST'])
def hoaxAPI():
    try:
        input_data = request.json
        if 'content' not in input_data:
            return jsonify({"error": "Invalid input, 'content' field is required"}), 400

        content = input_data['content']
        
        bias = predictHoax(content)

        return jsonify({"hoax": bias})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/ideology', methods=['POST'])
def ideologyAPI():
    try:
        input_data = request.json
        if 'content' not in input_data:
            return jsonify({"error": "Invalid input, 'content' field is required"}), 400

        content = input_data['content']
        
        bias = predictIdeology(content)

        return jsonify({"ideology": bias})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def summarize_article(documents):
    document_liberalism = [doc for doc in documents if doc.metadata['ideology'] == 'liberalism']
    document_conservative = [doc for doc in documents if doc.metadata['ideology'] == 'conservative']

    summary_liberalism = create_summary(document_liberalism)
    summary_conservative = create_summary(document_conservative)

    return summary_liberalism, summary_conservative
    
def analyze_article(documents):
    query_engine = VectorStoreIndex.from_documents(documents).as_query_engine(llm=Settings.llm)

    analysis = create_analysis(query_engine)

    return analysis

def getClusters(df):
    X = np.array(df['embedding'].to_list(), dtype=np.float32)
    clusters = kmeans.predict(X)
    modeCluster = np.bincount(clusters).argmax()
    return int(modeCluster)

def getTitle(documents):
    query_engine = VectorStoreIndex.from_documents(documents).as_query_engine(llm=Settings.llm)
    titleQuery = """
    From the following articles, generate a single article title that summarizes the content of all articles.
    Be as factual, neutral, and objective as possible.
    Do not use prior knowledge.
    Include the important subjects in the title if there are any. 
    Use Indonesian language.
    """
    response = query_engine.query(titleQuery)
    return response.response

def dfEmbedding(df):
    df['embedding'] = df.apply(
        lambda row: row['embedding'] if isinstance(row['embedding'], (list, np.ndarray)) else Settings.embed_model.get_text_embedding(row['content']),
        axis=1
    )

    return df

@app.route('/embedding', methods=['POST'])
def get_embedding():
    try:
        data = request.get_json()
        
        if isinstance(data, dict):  # If a single article is provided, wrap it in a list
            data = [data]
        elif not isinstance(data, list):  # If it's not a list or dict, return an error
            return jsonify({"error": "Input must be a list of news articles or a single article"}), 400
        
        df = pd.DataFrame(data)
        
        if 'content' not in df.columns:
            return jsonify({"error": "Input must contain 'content' field"}), 400
            
        df['embedding'] = df.apply(
            lambda row: row['embedding'] if isinstance(row.get('embedding'), (list, np.ndarray)) else Settings.embed_model.get_text_embedding(row['content']),
            axis=1
        )

        # Return embeddings
        return jsonify({"embedding": df['embedding'].tolist()}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/title', methods=['POST'])
def title():
    try:
        data = request.get_json()
        
        if not isinstance(data, list):
            return jsonify({"error": "Input must be a list of news articles"}), 400
        
        df = pd.DataFrame(data)

        for col in ['title', 'content', 'embedding']:
            if col not in df.columns:
                return jsonify({"error": f"Input must contain {col} field"}), 400
            
        df = dfEmbedding(df) # incase any empty ones

        documents = create_documents(df)
        title = getTitle(documents)

        response = {
            'title': title,
            'embedding': df['embedding'].tolist()
        }
        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@app.route('/modeCluster', methods=['POST'])
def modeCluster():
    try:
        data = request.get_json()
        
        if not isinstance(data, list):
            return jsonify({"error": "Input must be a list of news articles"}), 400
        
        df = pd.DataFrame(data)

        for col in ['title', 'content', 'embedding']:
            if col not in df.columns:
                return jsonify({"error": f"Input must contain {col} field"}), 400
            
        df = dfEmbedding(df) # incase any empty ones
        modeCluster = getClusters(df)

        response = {
            'modeCluster': modeCluster,
        }
        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@app.route('/summary', methods=['POST'])
def summary():
    try:
        data = request.get_json()
        
        if not isinstance(data, list):
            return jsonify({"error": "Input must be a list of news articles"}), 400
        
        df = pd.DataFrame(data)
        
        for col in ['title', 'content', 'embedding']:
            if col not in df.columns:
                return jsonify({"error": f"Input must contain {col} field"}), 400
            
        df = completeDf(df) # incase any empty ones

        documents = create_documents(df)
        summary_liberalism, summary_conservative = summarize_article(documents)

        response = {
            'summary_liberalism': summary_liberalism,
            'summary_conservative': summary_conservative,
            'cleaned': df['cleaned'].tolist()
        }
        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        
        if not isinstance(data, list):
            return jsonify({"error": "Input must be a list of news articles"}), 400
        
        df = pd.DataFrame(data)

        for col in ['title', 'content', 'embedding']:
            if col not in df.columns:
                return jsonify({"error": f"Input must contain {col} field"}), 400

        df = completeDf(df)
        documents = create_documents(df)
        analysis = analyze_article(documents)

        response = {
            'analyze': analysis,
        }
        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/separate', methods=['POST'])
def separate():
    try:
        data = request.get_json()

        if not isinstance(data, list):
            return jsonify({"error": "Input must be a list of news articles"}), 400
        
        df = pd.DataFrame(data)

        for col in ['title', 'content', 'embedding']:
            if col not in df.columns:
                return jsonify({"error": f"Input must contain {col} field"}), 400
            
        df = dfEmbedding(df)

        embeddings = np.array(df['embedding'].to_list(), dtype=np.float32)

        similarity_threshold = 0.9

        similarity_matrix = cosine_similarity(embeddings)

        G = nx.Graph()
        for i in range(len(similarity_matrix)):
            for j in range(i + 1, len(similarity_matrix)):
                if similarity_matrix[i, j] >= similarity_threshold:
                    G.add_edge(i, j)

        clusters = [list(component) for component in nx.connected_components(G)]

        cluster_indices = [-1] * len(df)

        # Assign a unique cluster index to each group
        current_cluster_index = 0
        for cluster in clusters:
            for idx in cluster:
                cluster_indices[idx] = current_cluster_index
            current_cluster_index += 1

        # For unclustered items, assign them unique indices starting from current_cluster_index
        for idx, cluster_index in enumerate(cluster_indices):
            if cluster_index == -1:
                cluster_indices[idx] = current_cluster_index
                current_cluster_index += 1

        # Return the cluster indices
        return jsonify({"separate": cluster_indices}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400



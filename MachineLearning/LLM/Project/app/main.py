# Standard libraries
import sys
import pickle
import numpy as np
import pandas as pd
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0' # resolves warning

import json

# Third-party libraries
import tensorflow as tf
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import nest_asyncio

# Internal imports
from llama_index.core import Settings, Document, VectorStoreIndex, SummaryIndex
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.query_engine import SubQuestionQueryEngine
from llama_index.core.callbacks import CallbackManager, LlamaDebugHandler
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI

from keras.preprocessing.sequence import pad_sequences
from tensorflow.keras import preprocessing
sys.modules['keras.src.preprocessing'] = preprocessing

# async patch for nested event loops
nest_asyncio.apply()

app = Flask(__name__)

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

Settings.embed_model = OpenAIEmbedding(model="text-embedding-ada-002")

try:
    with open('app/model/cluster/kmeans_8_cluster.pkl', 'rb') as f:
        kmeans = pickle.load(f)
except FileNotFoundError:
    with open('model/cluster/kmeans_8_cluster.pkl', 'rb') as f:
        kmeans = pickle.load(f)

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

bias_tokenizer, bias_interpreter = loadModel('model/bias', 'bias')
hoax_tokenizer, hoax_interpreter = loadModel('model/hoax', 'hoax')
ideology_tokenizer, ideology_interpreter = loadModel('model/ideology', 'ideology')

@app.route('/cluster', methods=['POST'])
def predict_cluster():
    try:
        Settings.llm = OpenAI(model='chatgpt-4o-latest', temperature=0.5)

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

def predict_with_model(news_text, tokenizer, interpreter, max_len):
    new_sequences = tokenizer.texts_to_sequences([news_text])
    new_padded = pad_sequences(new_sequences, maxlen=max_len, padding='post')
    new_padded = new_padded.astype('float32')

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    interpreter.set_tensor(input_details[0]['index'], new_padded)
    interpreter.invoke()

    predictions = interpreter.get_tensor(output_details[0]['index'])
    return predictions

def predictBias(news_text):
    predictions = predict_with_model(news_text, bias_tokenizer, bias_interpreter, 30)
    return [1 if pred > 0.5 else 0 for pred in predictions][0]

def predictHoax(news_text):
    predictions = predict_with_model(news_text, hoax_tokenizer, hoax_interpreter, 100)
    return float(predictions[0])

def predictIdeology(news_text):
    predictions =  predict_with_model(news_text, ideology_tokenizer, ideology_interpreter, 100)
    return [1 if pred > 0.5 else 0 for pred in predictions][0]

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

def completeDf(df):
    for col in ['embedding', 'bias', 'hoax', 'ideology']:
        if col not in df.columns:
            df[col] = None

    df['embedding'] = df.apply(
        lambda row: row['embedding'] if isinstance(row['embedding'], (list, np.ndarray)) else Settings.embed_model.get_text_embedding(row['content']),
        axis=1
    )

    df['bias'] = df.apply(
        lambda row: row['bias'] if pd.notnull(row['bias']) else predictBias([row['content']]),
        axis=1
    )

    df['hoax'] = df.apply(
        lambda row: row['hoax'] if pd.notnull(row['hoax']) else predictHoax([row['content']]),
        axis=1
    )

    df['ideology'] = df.apply(
        lambda row: row['ideology'] if pd.notnull(row['ideology']) else predictIdeology([row['content']]),
        axis=1
    )

    return df

def create_documents(df):
    documents = []
    for index, row in df.iterrows():
        document = Document(
            text=row['content'],
            doc_id=str(index),
            metadata={
            'title': row['title'],
            'bias': 'biased' if row['bias'] == 1 else 'not biased',
            'hoax': row['hoax'],
            'ideology': 'liberalism' if row['ideology'] == 1 else 'conservative'
            },
            embedding=row['embedding']
        )
        documents.append(document)
    return documents

def create_summary(documents):
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
    summary_query_engine = summary_index.as_query_engine(llm=Settings.llm)

    summary = summary_query_engine.query(summarizeQuery)

    return summary.response

@app.route('/summarize', methods=['POST'])
def summarize_article():
    try:
        Settings.llm = OpenAI(model='chatgpt-4o-latest', temperature=0.5)

        data = request.get_json()
        
        if not isinstance(data, list):
            return jsonify({"error": "Input must be a list of news articles"}), 400
        
        df = pd.DataFrame(data)
        if 'content' not in df.columns: 
            return jsonify({"error": "Input must contain 'title' and 'content' fields"}), 400
        
        elif df['content'].isnull().any() or not all(isinstance(c, str) and c.strip() for c in df['content']):
            return jsonify({"error": "Each article must have a non-empty 'content' field"}), 400
        
        df = completeDf(df)

        documents = create_documents(df)

        summary = create_summary(documents)

        response = {
            'summary': summary,
            'embedding': df['embedding'].tolist(),
            'bias': df['bias'].tolist(),
            'hoax': df['hoax'].tolist(),
            'ideology': df['ideology'].tolist()
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

def queryEngineMaker(documents):
    query_engine = VectorStoreIndex.from_documents(documents).as_query_engine(llm=Settings.llm)
    # query_engine_tools = [
    # QueryEngineTool(
    #     query_engine=query_engine,
    #     metadata=ToolMetadata(
    #         name="news_articles",
    #         description="News Articles of the same topic with bias, hoax, and liberalism_conservative labelled.",
    #     ),
    # ),
    # ]
    # query_engine = SubQuestionQueryEngine.from_defaults(
    #     query_engine_tools = query_engine_tools
    # )
    return query_engine

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

@app.route('/analyze', methods=['POST'])
def analyze_article():
    try:
        Settings.llm = OpenAI(model='chatgpt-4o-latest')

        data = request.get_json()
        
        if not isinstance(data, list):
            return jsonify({"error": "Input must be a list of news articles"}), 400
        
        df = pd.DataFrame(data)

        if 'title' not in df.columns or 'content' not in df.columns:
            return jsonify({"error": "Input must contain 'title' and 'content' fields"}), 400
        
        elif df['content'].isnull().any() or not all(isinstance(c, str) and c.strip() for c in df['content']):
            return jsonify({"error": "Each article must have a non-empty 'content' field"}), 400
        
        df = completeDf(df)

        documents = create_documents(df)

        query_engine = queryEngineMaker(documents)

        analysis = create_analysis(query_engine)

        response = {
            'analysis': analysis,
            'embedding': df['embedding'].tolist(),
            'bias': df['bias'].tolist(),
            'hoax': df['hoax'].tolist(),
            'ideology': df['ideology'].tolist()
        }

        return jsonify(response), 200  
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400
        



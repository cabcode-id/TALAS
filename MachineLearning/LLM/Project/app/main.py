# Standard libraries
import sys
import pickle
import numpy as np
import pandas as pd
import os
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

with open('app/model/cluster/kmeans_8_cluster.pkl', 'rb') as f:
    kmeans = pickle.load(f)


def loadModel(path, model_name):
    with open(path + model_name + '_tokenizer.pkl', 'rb') as f:
        tokenizer = pickle.load(f)
    interpreter = tf.lite.Interpreter(model_path=path + model_name + '.tflite')
    interpreter.allocate_tensors()
    return tokenizer, interpreter

bias_tokenizer, bias_interpreter = loadModel('app/model/bias/', 'bias')
hoax_tokenizer, hoax_interpreter = loadModel('app/model/hoax/', 'hoax')
liberalism_conservative_tokenizer, liberalism_conservative_interpreter = loadModel('app/model/liberalism_conservative/', 'liberalism_conservative')

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
    new_sequences = tokenizer.texts_to_sequences(news_text)
    new_padded = pad_sequences(new_sequences, maxlen=max_len, padding='post')
    new_padded = new_padded.astype('float32')

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    interpreter.set_tensor(input_details[0]['index'], new_padded)
    interpreter.invoke()

    predictions = interpreter.get_tensor(output_details[0]['index'])
    return [1 if pred > 0.5 else 0 for pred in predictions][0]

def predict(df):
    df['bias'] = df['content'].apply(lambda x: predict_with_model([x], bias_tokenizer, bias_interpreter, 30))
    df['hoax'] = df['content'].apply(lambda x: predict_with_model([x], hoax_tokenizer, hoax_interpreter, 100))
    df['liberalism_conservative'] = df['content'].apply(lambda x: predict_with_model(
        [x], liberalism_conservative_tokenizer, liberalism_conservative_interpreter, 100
        ))
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
            'hoax': 'hoax' if row['hoax'] == 1 else 'not hoax',
            'liberalism_conservative': 'liberalism' if row['liberalism_conservative'] == 1 else 'conservative'
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
    and whether it is liberal or conservative (0 is liberal, 1 is conservative)
    which are all detected using machine learning models are also included.
    Do NOT discuss about the article's hoax, bias, or political view. 
    Do NOT rely on previous knowledge. 
    Use Indonesian language. 
    """
    summary_index = SummaryIndex.from_documents(documents, use_async=True)
    summary_query_engine = summary_index.as_query_engine(llm=Settings.llm)

    summary = summary_query_engine.query(summarizeQuery)

    print(summary)
    return summary.response

@app.route('/summarize', methods=['POST'])
def summarize_article():
    try:
        Settings.llm = OpenAI(model='chatgpt-4o-latest', temperature=0.5)

        data = request.get_json()
        
        if not isinstance(data, list):
            return jsonify({"error": "Input must be a list of news articles"}), 400
        
        df = pd.DataFrame(data)
        if 'title' not in df.columns or 'content' not in df.columns:
            return jsonify({"error": "Input must contain 'title' and 'content' fields"}), 400
        
        if 'embedding' not in df.columns:
            df['embedding'] = df['content'].apply(lambda x: Settings.embed_model.get_text_embedding(x))

        df = predict(df)

        documents = create_documents(df)

        summary = create_summary(documents)

        response = {
            'summary': summary
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

def queryEngineMaker(documents):
    query_engine = VectorStoreIndex.from_documents(documents).as_query_engine(llm=Settings.llm)
    query_engine_tools = [
    QueryEngineTool(
        query_engine=query_engine,
        metadata=ToolMetadata(
            name="news_articles",
            description="News Articles of the same topic with bias, hoax, and liberalism_conservative labelled.",
        ),
    ),
    ]
    query_engine = SubQuestionQueryEngine.from_defaults(
        query_engine_tools = query_engine_tools
    )
    return query_engine

def create_analysis(query_engine):
    compareQuery = """
    You will act as a text analysis and comparison expert to help me analyze a collection of articles classified as liberal or conservative. These articles all address the same topic or event. Your task is to:

    Identify linguistic patterns in liberal and conservative sources, analyzing key phrases, tone, and stylistic choices.
    Compare how each perspective frames the topic, including their choice of focus, emotional appeals, or omitted details.
    Summarize the themes unique to each perspective and explain how these differences reveal underlying priorities or ideological leanings.
    Include direct quotes from the articles to illustrate your analysis and provide concrete examples.
    Highlight specific instances of emotionally charged language, identifying how they shape the narrative or influence the reader's perception.
    Present your findings in a clear and structured format, using sections or bullet points where appropriate. Do not use markdowns. Ensure the analysis is thorough and uses examples to make the findings actionable.

    """
    response = query_engine.query(compareQuery)
    return response.response

@app.route('/analyze', methods=['POST'])
def analyze_article():
    try:
        Settings.llm = OpenAI(model='gpt-4o')
        data = request.get_json()
        
        if not isinstance(data, list):
            return jsonify({"error": "Input must be a list of news articles"}), 400
        
        df = pd.DataFrame(data)
        if 'title' not in df.columns or 'content' not in df.columns:
            return jsonify({"error": "Input must contain 'title' and 'content' fields"}), 400
        
        if 'embedding' not in df.columns:
            df['embedding'] = df['content'].apply(lambda x: Settings.embed_model.get_text_embedding(x))

        df = predict(df)

        documents = create_documents(df)

        query_engine = queryEngineMaker(documents)

        analysis = create_analysis(query_engine)

        response = {
            'analysis': analysis
        }

        return jsonify(response), 200  
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    

        



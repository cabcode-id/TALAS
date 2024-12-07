from app.main import app  
import json
import os

def test_predict_endpoint(test_data):
    """Test the /cluster endpoint."""
    with app.test_client() as client:
        response = client.post(
            '/cluster',
            data=json.dumps(test_data),
            content_type='application/json'
        )

        print("Status Code:", response.status_code)
        print("Response JSON:", response.json)

        assert response.status_code == 200 
        assert "cluster" in response.json 

def test_summarize_endpoint(test_data):
    """Test the /summarize endpoint."""
    with app.test_client() as client:
        response = client.post(
            '/summarize',
            data=json.dumps(test_data),
            content_type='application/json'
        )

        print("Status Code:", response.status_code)
        print("Response JSON:", response.json)
        assert response.status_code == 200  
        assert "summary" in response.json

        # embedding = response.json.get('embedding', [])
        # bias = response.json.get('bias', [])
        # hoax = response.json.get('hoax', [])
        # ideology = response.json.get('ideology', [])

        # for idx, article in enumerate(test_data):
        #     article['embedding'] = embedding[idx] if idx < len(embedding) else None
        #     article['bias'] = bias[idx] if idx < len(bias) else None
        #     article['hoax'] = hoax[idx] if idx < len(hoax) else None
        #     article['ideology'] = ideology[idx] if idx < len(ideology) else None

        # def save_test_data_to_json(test_data, filename='temp_data.json'):
        #     with open(filename, 'w') as f:
        #         json.dump(test_data, f, indent=4)

        # save_test_data_to_json(test_data)

def test_analyze_endpoint(test_data):
    """Test the /analyze endpoint."""
    with app.test_client() as client:

        response = client.post(
            '/analyze',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        print("Status Code:", response.status_code)
        print("Response JSON:", response.json)
        assert response.status_code == 200  
        assert "analysis" in response.json

def test_bias_endpoint(test_data):
    """Test the /bias endpoint."""
    with app.test_client() as client:
        response = client.post(
            '/bias',
            data=json.dumps(test_data),
            content_type='application/json'
        )

        print("Status Code:", response.status_code)
        print("Response JSON:", response.json)

        assert response.status_code == 200 
        assert "bias" in response.json

def test_hoax_endpoint(test_data):
    """Test the /hoax endpoint."""
    with app.test_client() as client:
        response = client.post(
            '/hoax',
            data=json.dumps(test_data),
            content_type='application/json'
        )

        print("Status Code:", response.status_code)
        print("Response JSON:", response.json)

        assert response.status_code == 200 
        assert "hoax" in response.json

def test_ideology_endpoint(test_data):
    """Test the /ideology endpoint."""
    with app.test_client() as client:
        response = client.post(
            '/ideology',
            data=json.dumps(test_data),
            content_type='application/json'
        )

        print("Status Code:", response.status_code)
        print("Response JSON:", response.json)

        assert response.status_code == 200 
        assert "ideology" in response.json

test_data = {
    "content": "Jakarta - Seorang polisi Brigadir J tewas ditembak oleh polisi lainnya, Bharada E. Brigadir J merupakan personel yang bertugas di Propam Polri."
}

test_predict_endpoint(test_data)
test_bias_endpoint(test_data)
test_hoax_endpoint(test_data)
test_ideology_endpoint(test_data)

# with open('test_data.json') as f:
#     test_data = json.load(f)

with open('temp_data.json') as f:
    test_data = json.load(f)

test_summarize_endpoint(test_data)

test_analyze_endpoint(test_data)


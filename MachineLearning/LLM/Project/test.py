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

        # embedding = response.json.get('embedding', [])
        # cleaned = response.json.get('cleaned', [])
        # bias = response.json.get('bias', [])
        # hoax = response.json.get('hoax', [])
        # ideology = response.json.get('ideology', [])

        # for idx, article in enumerate(test_data):
        #     article['embedding'] = embedding[idx] if idx < len(embedding) else None
        #     article['cleaned'] = cleaned[idx] if idx < len(cleaned) else None
        #     article['bias'] = bias[idx] if idx < len(bias) else None
        #     article['hoax'] = hoax[idx] if idx < len(hoax) else None
        #     article['ideology'] = ideology[idx] if idx < len(ideology) else None

        # def save_test_data_to_json(test_data, filename='temp_data.json'):
        #     with open(filename, 'w') as f:
        #         json.dump(test_data, f, indent=4)

        # save_test_data_to_json(test_data)

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

def test_separate_endpoint(test_data):
    """Test the /separate endpoint."""
    with app.test_client() as client:
        response = client.post(
            '/separate',
            data=json.dumps(test_data),
            content_type='application/json'
        )

        print("Status Code:", response.status_code)
        print("Response JSON:", response.json)

        assert response.status_code == 200 
        assert "clusters" in response.json # {[1,2,3], [4,5,6], [7,8,9]}

def test_title_endpoint(test_data):
    """Test the /title endpoint."""
    with app.test_client() as client:
        response = client.post(
            '/title',
            data=json.dumps(test_data),
            content_type='application/json'
        )

        print("Status Code:", response.status_code)
        print("Response JSON:", response.json)

        assert response.status_code == 200 
        assert "title" in response.json

def test_modeCluster_endpoint(test_data):
    """Test the /modeCluster endpoint."""
    with app.test_client() as client:
        response = client.post(
            '/modeCluster',
            data=json.dumps(test_data),
            content_type='application/json'
        )

        print("Status Code:", response.status_code)
        print("Response JSON:", response.json)

        assert response.status_code == 200 
        assert "modeCluster" in response.json

def test_summary_endpoint(test_data):
    """Test the /summary endpoint."""
    with app.test_client() as client:
        response = client.post(
            '/summary',
            data=json.dumps(test_data),
            content_type='application/json'
        )

        print("Status Code:", response.status_code)
        print("Response JSON:", response.json)

        assert response.status_code == 200 
        assert "summary_liberalism" in response.json
        assert "summary_conservative" in response.json

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

test_data = {
    {
        "title": "Sistem Ekonomi yang Gagal: Kenapa Pemuda Terjebak dalam Kejahatan?",
        "content": "Kasus perampokan yang melibatkan seorang pemuda di Jakarta mencerminkan kegagalan sistem ekonomi yang tidak menyediakan peluang bagi generasi muda. Ketimpangan pendapatan terus meningkat, membuat banyak orang terpaksa mengambil jalan pintas untuk bertahan hidup."
    }
}

# test_predict_endpoint(test_data)
# test_bias_endpoint(test_data)
# test_hoax_endpoint(test_data)
# test_ideology_endpoint(test_data)

# with open('sameExample2.json') as f:
#     test_data = json.load(f)

# test_title_endpoint(test_data)
# test_modeCluster_endpoint(test_data)
# test_summary_endpoint(test_data)
# test_analyze_endpoint(test_data)





# // alurnya setelah title besar dibuat,itu langsung disummarize 
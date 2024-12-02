from app.main import app  
import json
import requests

def test_predict_endpoint():
    """Test the /cluster endpoint."""
    with app.test_client() as client:
        test_data = {
            "content": "Jakarta - Seorang polisi Brigadir J tewas ditembak oleh polisi lainnya, Bharada E. Brigadir J merupakan personel yang bertugas di Propam Polri."
        }

        response = client.post(
            '/cluster',
            data=json.dumps(test_data),
            content_type='application/json'
        )

        print("Status Code:", response.status_code)
        print("Response JSON:", response.json)

        assert response.status_code == 200 
        assert "cluster" in response.json 

def test_summarize_endpoint():
    """Test the /summarize endpoint."""
    with app.test_client() as client:
        test_data = [
            {
                "title": "The Impact of Climate Change on Global Ecosystems",
                "content": "Climate change is increasingly affecting ecosystems across the globe. Rising temperatures, changing rainfall patterns, and extreme weather events are disrupting biodiversity. Many species are migrating to new areas or becoming endangered. Urgent action is needed to reduce greenhouse gas emissions to mitigate further damage to our ecosystems."
            },
            {
                "title": "Scientists Warn About Accelerating Global Warming",
                "content": "Recent studies show that global warming is accelerating at an alarming rate. Rising CO2 levels in the atmosphere are contributing to faster melting of polar ice caps, leading to rising sea levels. Experts urge governments to take immediate action to curb emissions and implement policies that address climate change."
            },
            {
                "title": "How Climate Change Is Affecting Agriculture",
                "content": "Farmers around the world are struggling to adapt to the changing climate. Droughts, floods, and unpredictable weather patterns are making it harder to grow crops. Climate change poses a serious threat to food security, and agricultural practices must evolve to cope with these challenges. Sustainability and innovation in farming are crucial."
            },
            {
                "title": "The Role of Renewable Energy in Combating Climate Change",
                "content": "Renewable energy sources such as solar, wind, and hydroelectric power are key to reducing carbon emissions. Investing in renewable energy infrastructure is essential for transitioning to a carbon-neutral economy. These energy sources offer a sustainable alternative to fossil fuels, which contribute to climate change."
            },
            {
                "title": "Climate Change and Human Health: A Growing Threat",
                "content": "Climate change is not just an environmental issue; it’s a public health crisis. Rising temperatures are leading to more heatwaves, which can cause heat-related illnesses. Changing weather patterns also contribute to the spread of diseases like malaria and dengue fever. Governments need to prioritize health policies that address these risks."
            }
        ]

        response = client.post(
            '/summarize',
            data=json.dumps(test_data),
            content_type='application/json'
        )

        print("Status Code:", response.status_code)
        print("Response JSON:", response.json)

        assert response.status_code == 200 
        assert "summary" in response.json

def test_analyze_endpoint():
    """Test the /analyze endpoint."""
    with app.test_client() as client:
        test_data = [
            {
                "title": "The Impact of Climate Change on Global Ecosystems",
                "content": "Climate change is increasingly affecting ecosystems across the globe. Rising temperatures, changing rainfall patterns, and extreme weather events are disrupting biodiversity. Many species are migrating to new areas or becoming endangered. Urgent action is needed to reduce greenhouse gas emissions to mitigate further damage to our ecosystems."
            },
            {
                "title": "Scientists Warn About Accelerating Global Warming",
                "content": "Recent studies show that global warming is accelerating at an alarming rate. Rising CO2 levels in the atmosphere are contributing to faster melting of polar ice caps, leading to rising sea levels. Experts urge governments to take immediate action to curb emissions and implement policies that address climate change."
            },
            {
                "title": "How Climate Change Is Affecting Agriculture",
                "content": "Farmers around the world are struggling to adapt to the changing climate. Droughts, floods, and unpredictable weather patterns are making it harder to grow crops. Climate change poses a serious threat to food security, and agricultural practices must evolve to cope with these challenges. Sustainability and innovation in farming are crucial."
            },
            {
                "title": "The Role of Renewable Energy in Combating Climate Change",
                "content": "Renewable energy sources such as solar, wind, and hydroelectric power are key to reducing carbon emissions. Investing in renewable energy infrastructure is essential for transitioning to a carbon-neutral economy. These energy sources offer a sustainable alternative to fossil fuels, which contribute to climate change."
            },
            {
                "title": "Climate Change and Human Health: A Growing Threat",
                "content": "Climate change is not just an environmental issue; it’s a public health crisis. Rising temperatures are leading to more heatwaves, which can cause heat-related illnesses. Changing weather patterns also contribute to the spread of diseases like malaria and dengue fever. Governments need to prioritize health policies that address these risks."
            }
        ]

        response = client.post(
            '/analyze',
            data=json.dumps(test_data),
            content_type='application/json'
        )

        print("Status Code:", response.status_code)
        print("Response JSON:", response.json)

        assert response.status_code == 200  
        assert "analysis" in response.json

# test_predict_endpoint()
# test_summarize_endpoint()
test_analyze_endpoint()
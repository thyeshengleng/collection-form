import requests

def fetch_data_from_api():
    api_url = "https://your-api-endpoint.com/api/debtor"
    response = requests.get(api_url)
    return response.json() 
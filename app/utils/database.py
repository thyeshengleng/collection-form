import pandas as pd
import requests
from config.settings import WORKER_URL

def load_records():
    try:
        response = requests.get(f"{WORKER_URL}/api/form")
        if response.status_code == 200:
            data = response.json()
            return pd.DataFrame(data) if data else pd.DataFrame()
    except:
        return pd.DataFrame()

# Rest of your database functions... 
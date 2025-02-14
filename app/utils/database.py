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

def save_records(df):
    try:
        records = df.to_dict('records')
        requests.post(f"{WORKER_URL}/api/form", json=records)
    except:
        st.error("Failed to save data")

def create_record(form_data):
    df = load_records()
    form_data = {k: str(v) for k, v in form_data.items()}
    new_df = pd.DataFrame([form_data])
    df = pd.concat([df, new_df], ignore_index=True)
    save_records(df)
    return df

def update_record(index, form_data):
    df = load_records()
    form_data = {k: str(v) for k, v in form_data.items()}
    for key, value in form_data.items():
        df.at[index, key] = value
    save_records(df)
    return df

def delete_record(index):
    df = load_records()
    df = df.drop(index)
    df = df.reset_index(drop=True)
    save_records(df)
    return df

# Rest of your database functions... 
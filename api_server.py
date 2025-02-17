from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pyodbc
import pandas as pd
from typing import List
import json
from datetime import datetime

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    conn_str = (
        'DRIVER={SQL Server};'
        'SERVER=DESKTOP-RMNV9QV\\A2006;'
        'DATABASE=AED_AssignmentOne;'
        'UID=sa;'
        'PWD=oCt2005-ShenZhou6_A2006;'
        'Trusted_Connection=no;'
    )
    return pyodbc.connect(conn_str)

@app.get("/api/debtor")
async def get_debtors():
    try:
        conn = get_db_connection()
        query = """
            SELECT TOP 1000 
                AccNo,
                CompanyName,
                RegisterNo,
                Address1,
                Address2,
                Address3,
                Address4,
                PostCode,
                Phone1,
                Phone2,
                EmailAddress,
                WebURL,
                NatureOfBusiness,
                IsActive
            FROM Debtor
            ORDER BY CompanyName
        """
        df = pd.read_sql(query, conn)
        conn.close()
        
        # Convert DataFrame to JSON
        return df.to_dict(orient='records')
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 
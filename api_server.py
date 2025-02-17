from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pyodbc
import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    try:
        conn_str = (
            'DRIVER={SQL Server};'
            'SERVER=DESKTOP-RMNV9QV\\A2006;'
            'DATABASE=AED_AssignmentOne;'
            'UID=sa;'
            'PWD=oCt2005-ShenZhou6_A2006;'
            'Trusted_Connection=no;'
        )
        logger.info("Attempting database connection...")
        conn = pyodbc.connect(conn_str)
        logger.info("Database connection successful!")
        return conn
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        raise

@app.get("/api/debtor")
async def get_debtors():
    try:
        logger.info("API endpoint called: /api/debtor")
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
        logger.info("Executing SQL query...")
        df = pd.read_sql(query, conn)
        conn.close()
        logger.info(f"Query returned {len(df)} rows")
        
        # Convert DataFrame to JSON
        return df.to_dict(orient='records')
        
    except Exception as e:
        logger.error(f"Error in get_debtors: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting FastAPI server...")
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="info") 
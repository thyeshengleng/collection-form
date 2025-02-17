from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pyodbc
import pandas as pd
import logging
import os

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
        # Get database credentials from environment variables
        server = os.getenv('DB_SERVER', 'DESKTOP-RMNV9QV\\A2006')
        database = os.getenv('DB_NAME', 'AED_AssignmentOne')
        username = os.getenv('DB_USER', 'sa')
        password = os.getenv('DB_PASSWORD', 'oCt2005-ShenZhou6_A2006')
        
        conn_str = (
            'DRIVER={SQL Server};'
            f'SERVER={server};'
            f'DATABASE={database};'
            f'UID={username};'
            f'PWD={password};'
            'Trusted_Connection=no;'
        )
        logger.info("Attempting database connection...")
        conn = pyodbc.connect(conn_str)
        logger.info("Database connection successful!")
        return conn
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        raise

@app.get("/")
async def root():
    return {"message": "API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

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
        
        return df.to_dict(orient='records')
        
    except Exception as e:
        logger.error(f"Error in get_debtors: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv('PORT', 8001))
    logger.info(f"Starting FastAPI server on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info") 
from fastapi import FastAPI
from sqlalchemy import create_engine, text
import pandas as pd


# Connection details
user = 
password = 
host = 
port = 
database = 

# Create the engine
engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}')


app = FastAPI()

@app.get("/data")
async def read_data():
    query = 'SELECT count(*) FROM SRC_ATM_TRANS limit 5'
    with engine.connect() as connection:
        result = connection.execute(text(query))
        # Convert the result to a DataFrame
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
        print(df)
    return df.to_dict(orient='records')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

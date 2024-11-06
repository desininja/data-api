from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from sqlalchemy import create_engine
import os

app = Flask(__name__)

# Load sensitive information from environment variables
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'market_star_schema')

# Singleton database connection class
class DatabaseConnection:
    _engine = None  # Singleton engine instance

    @classmethod
    def get_engine(cls):
        if cls._engine is None:
            # Create the engine if it doesn't exist
            connection_string = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
            cls._engine = create_engine(connection_string, pool_recycle=3600)
        return cls._engine

    @staticmethod
    def query_function(query):
        engine = DatabaseConnection.get_engine()

        try:
            with engine.connect() as connection:
                df = pd.read_sql(query, connection)
                # Directly return the data as a JSON-ready dictionary
                return df.to_dict(orient="records")

        except Exception as e:
            # Log the error in production instead of returning it
            print("Error:", e)
            return {"error": "Could not fetch data from the database"}

# Route to retrieve data
@app.route('/data', methods=['GET'])
def get_data():
    try:
        query = """
            SELECT pd.Product_category AS product_category,
                   SUM(mff.profit) AS total_profit
            FROM market_fact_full AS mff
            INNER JOIN prod_dimen AS pd ON pd.prod_id = mff.prod_id
            GROUP BY 1
            ORDER BY 2 DESC;
        """
        result = DatabaseConnection.query_function(query)
        
        if "error" in result:
            return jsonify(result), 500  # Return error message if query fails
        return jsonify(result)  # Return JSON response without extra nesting

    except Exception as e:
        # Log the exception in production logs
        print("Error:", e)
        return jsonify(error="An internal server error occurred"), 500

# Entry point
if __name__ == '__main__':
    # Run with debug=False in production for security
    app.run(debug=True)

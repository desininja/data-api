from sqlalchemy import create_engine
import pandas as pd

# Database connection parameters
username = ''  # replace with your MySQL username
password = ''  # replace with your MySQL password
host = 'localhost'          # 'localhost' can also be used
database = 'market_star_schema'   # replace with your database name

# Create the connection string
connection_string = f"mysql+pymysql://{username}:{password}@{host}/{database}"

# Create the SQLAlchemy engine
engine = create_engine(connection_string)

# Define your SQL query
query = "select pd.Product_category as product_category \
	   ,sum(mff.profit) as total_profit \
from market_fact_full as mff \
inner join prod_dimen as pd on pd.prod_id = mff.prod_id \
group by 1 \
order by 2 DESC;" 

# Execute the query and load the data into a Pandas DataFrame
try:
    with engine.connect() as connection:
        df = pd.read_sql(query, connection)
        print(df)  # Display the DataFrame

except Exception as e:
    print("Error reading data from MySQL table:", e)



import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:8102@localhost:3306/finance_etl")
df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
df.to_sql('test_table', con=engine, if_exists='replace', index=False)
print("Success")
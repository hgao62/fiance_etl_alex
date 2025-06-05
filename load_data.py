from sqlalchemy import create_engine
import pandas as pd

user_name = "root"  # database username
password = "8102"   # database password
host = "localhost"  # database host (e.g., localhost or an IP address)
port = "3306"       # database port (default for MySQL is 3306)
db_name = "finance_etl" # database name
    # Create the database engine
MYSQL_CONNECTION_STRING = f"mysql+pymysql://{user_name}:{password}@{host}:{port}/{db_name}"

ENGINE = create_engine(
    MYSQL_CONNECTION_STRING,
    pool_size=5,             # Number of persistent connections
    max_overflow=10,         # Extra connections above pool_size
    pool_recycle=1800,       # Recycle after 30 minutes
    pool_pre_ping=True       # Ping before using (avoids broken pipe)
)
def create_table_if_not_exists(df: pd.DataFrame, table_name: str, engine=ENGINE):
    dtype_map = {
        "int64": "INT",
        "float64": "FLOAT",
        "object": "VARCHAR(255)",
        "datetime64[ns]": "DATETIME",
        "bool": "BOOLEAN"
    }

    columns = []
    for col, dtype in df.dtypes.items():
        sql_type = dtype_map.get(str(dtype), "VARCHAR(255)")
        columns.append(f"`{col}` {sql_type}")

    ddl = f"CREATE TABLE IF NOT EXISTS `{table_name}` (\n  {', '.join(columns)}\n);"

    with engine.connect() as conn:
        conn.execute(text(ddl))
        print(f"✅ Ensured table `{table_name}` exists.")


def save_df_to_db(df: pd.DataFrame, table_name: str, engine=ENGINE, replace=False):
    if df.empty:
        print(f"⚠️ DataFrame is empty, skipping insert to {table_name}")
        return

    create_table_if_not_exists(df, table_name, engine)
    columns = list(df.columns)
    col_names = ", ".join(f"`{col}`" for col in columns)
    placeholders = ", ".join(["%s"] * len(columns))  # %s for pymysql
    insert_sql = f"INSERT INTO `{table_name}` ({col_names}) VALUES ({placeholders})"
    data = df.to_records(index=False).tolist()

    raw_conn = engine.raw_connection()  
    try:
        cursor = raw_conn.cursor()
        if replace:
            cursor.execute(f"DELETE FROM `{table_name}`")
        cursor.executemany(insert_sql, data)
        raw_conn.commit()
        print(f"✅ Bulk inserted {len(data)} rows into `{table_name}`.")
    finally:
        cursor.close()
        raw_conn.close()


if __name__ == "__main__":
    df = pd.DataFrame({
    "id": [1, 2, 3],
    "name": ["Alice", "Bob", "Charlie"]
})

    save_df_to_db(df, "my_table", replace=True)

from sqlalchemy import create_engine
import pandas as pd

def save_df_to_db(
    df, table_name, if_exists="append", dtype=None,
) -> None:
    """
    Function to send a dataframe to SQL database.

    Args:
        df: DataFrame to be sent to the SQL database.
        table_name: Name of the table in the SQL database.
        if_exists: Action to take if the table already exists in the SQL database.
                   Options: "fail", "replace", "append" (default: "append").
        dtype: Dictionary of column names and data types to be used when creating the table (default: None).


    Returns:
        None. This function logs a note in the log file to confirm that data has been sent to the SQL database.
    """
    user_name = "root"  # database username
    password = "8102"   # database password
    host = "localhost"  # database host (e.g., localhost or an IP address)
    port = "3306"       # database port (default for MySQL is 3306)
    db_name = "test_db" # database name
    # Create the database engine
    ENGINE = create_engine(f"mysql+mysqlconnector://{user_name}:{password}@{host}:{port}/{db_name}")


    # Save the DataFrame to the database
    df.to_sql(
        name=table_name,
        con=ENGINE,
        if_exists=if_exists,
        index=False,  # Do not save the DataFrame index as a column in the database
        dtype=dtype,  # Specify column data types if provided
    )


# data = {
#     "Date": ["2025-01-01", "2025-01-02", "2025-01-03"],
#     "Open": [150.0, 152.5, 155.0],
#     "High": [155.0, 157.5, 160.0],
#     "Low": [148.0, 150.5, 153.0],
#     "Close": [154.0, 156.5, 159.0],
#     "Volume": [1000000, 1200000, 1100000],
#     "Dividends": [0.0, 0.0, 0.0],
#     "Stock Splits": [0, 0, 0],
# }
# df = pd.DataFrame(data)

# save_df_to_db(df, "test_table")


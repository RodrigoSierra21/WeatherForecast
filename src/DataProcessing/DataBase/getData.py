import sqlite3
import pandas as pd


def get_table_names(conn):
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_names = [row[0] for row in cursor.fetchall()]

    # Step 5: Close the cursor and connection
    cursor.close()

    return table_names


def get_rows(num_rows, database_path, table_name):
    conn = sqlite3.connect(database_path)

    # Create the SQL query to fetch the last n rows
    query = f"""
        SELECT * 
        FROM "{table_name}" 
        ORDER BY rowid DESC 
        LIMIT ?
    """

    # Execute the query and fetch the last n rows
    df = pd.read_sql(query, conn, params=(num_rows,))

    # Close the connection
    conn.close()

    # Return the resulting DataFrame
    return df


def get_rows_by_week_index(week_index, table_name):
    conn = sqlite3.connect("./Datasets/Databases/DataDistributionShiftDatabase.db")

    # Create the SQL query to fetch the entire row based on the column value
    query = f"""
        SELECT * 
        FROM "{table_name}" 
        WHERE "week_of_year" = ?
    """

    # Execute the query and fetch the result
    cursor = conn.cursor()
    cursor.execute(query, (week_index,))

    # Fetch all matching rows
    rows = cursor.fetchall()

    # Close the connection
    cursor.close()
    conn.close()

    return rows

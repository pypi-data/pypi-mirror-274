import pandas as pd
import snowflake.connector

def query_to_dataframe(cur, path_to_script):

    with open(path_to_script, 'r') as query_file:
        sql_query = query_file.read()

    cur.execute(sql_query)
    result = cur.fetchall()

    # Convert result to DataFrame
    df = pd.DataFrame(result, columns=[desc[0] for desc in cur.description])

    return df
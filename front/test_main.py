import csv
import psycopg2
from psycopg2 import sql

def infer_data_type(value):
    try:
        int(value)
        return 'INTEGER'
    except ValueError:
        try:
            float(value)
            return 'NUMERIC'
        except ValueError:
            return 'TEXT'

def create_table_from_csv(csv_file, table_name, db_params):
    # Read the CSV file to get column names and infer data types
    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)
        first_row = next(csv_reader)
        data_types = [infer_data_type(value) for value in first_row]

    # Generate CREATE TABLE statement
    columns = [f"{header} {data_type}" for header, data_type in zip(headers, data_types)]
    create_table_sql = sql.SQL("CREATE TABLE {} ({})").format(
        sql.Identifier(table_name),
        sql.SQL(', ').join(map(sql.SQL, columns))
    )

    # Connect to the database
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    # Create the table
    cur.execute(create_table_sql)

    # Prepare INSERT statement
    insert_columns = [sql.Identifier(header) for header in headers]
    insert_values = [sql.Placeholder() for _ in headers]
    insert_sql = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
        sql.Identifier(table_name),
        sql.SQL(', ').join(insert_columns),
        sql.SQL(', ').join(insert_values)
    )

    # Import data
    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header
        for row in csv_reader:
            # Convert values to appropriate Python types
            converted_row = []
            for value, data_type in zip(row, data_types):
                if data_type == 'INTEGER':
                    converted_row.append(int(float(value)) if value else None)
                elif data_type == 'NUMERIC':
                    converted_row.append(float(value) if value else None)
                else:
                    converted_row.append(value)
            cur.execute(insert_sql, converted_row)

    # Commit changes and close connection
    conn.commit()
    cur.close()
    conn.close()

# Example usage
db_params = {
    'dbname': 'hakatoni',
    'user': 'postgres',
    'password': 'P-Qlolik123',
    'host': 'localhost'
}

create_table_from_csv('video_stat.csv', 'lol', db_params)
import os
import csv
import pymysql
import glob
from scraper_config import OUTPUT_DIR

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Change this to your MySQL password
    'database': 'news',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def connect_to_database():
    """Establish connection to the MySQL database"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        print("Successfully connected to the database!")
        return connection
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def get_all_csv_files():
    """Get all CSV files from the output directory"""
    csv_pattern = os.path.join(OUTPUT_DIR, '*.csv')
    return glob.glob(csv_pattern)

def upload_csv_to_db(csv_file, connection):
    """Upload data from a CSV file to the database"""
    try:
        # Get the CSV filename without extension for logging
        filename = os.path.basename(csv_file)
        print(f"Processing {filename}...")

        # Read the CSV file
        with open(csv_file, 'r', encoding='utf-8') as f:
            csv_reader = csv.reader(f)
            headers = next(csv_reader)  # Get column names from first row
            
            cursor = connection.cursor()
            
            # Get the current maximum ID from the articles table
            cursor.execute("SELECT MAX(id) as max_id FROM articles")
            result = cursor.fetchone()
            current_max_id = result['max_id'] if result['max_id'] is not None else 0
            
            # Process each row in the CSV
            for row in csv_reader:
                if len(row) != len(headers):
                    print(f"Skipping row with incorrect number of columns: {row}")
                    continue
                
                # Create dict of column names and values
                data = dict(zip(headers, row))
                
                # Build the SQL query dynamically based on the CSV columns
                # Exclude 'id' from the columns if it exists in the CSV headers
                filtered_headers = [h for h in headers if h.lower() != 'id']
                columns = ', '.join(filtered_headers)
                columns = 'id, ' + columns  # Add id as the first column
                
                placeholders = ', '.join(['%s'] * (len(filtered_headers) + 1))  # +1 for the id field
                
                # Get values for existing columns (excluding id)
                values = [data[header] for header in filtered_headers]
                
                # Increment max_id for the new record
                current_max_id += 1
                values = [current_max_id] + values  # Add the new id as the first value
                
                query = f"INSERT INTO articles ({columns}) VALUES ({placeholders})"
                
                try:
                    cursor.execute(query, values)
                except Exception as e:
                    print(f"Error inserting row: {e}")
            
            # Commit the transaction
            connection.commit()
            print(f"Successfully uploaded data from {filename}")
            
    except Exception as e:
        print(f"Error processing file {csv_file}: {e}")

def main():
    """Main function to run the database upload process"""
    # Connect to the database
    connection = connect_to_database()
    if not connection:
        return
    
    # Get all CSV files
    csv_files = get_all_csv_files()
    if not csv_files:
        print("No CSV files found in the output directory.")
        return
    
    print(f"Found {len(csv_files)} CSV files to process.")
    
    # Process each CSV file
    for csv_file in csv_files:
        upload_csv_to_db(csv_file, connection)
    
    # Close the database connection
    connection.close()
    print("Database connection closed.")

if __name__ == "__main__":
    main()
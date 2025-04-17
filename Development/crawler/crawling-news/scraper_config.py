import os

# Define the output directory for all scrapers
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scraped_data')

# Create the directory if it doesn't exist
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def get_output_path(filename):
    """Get the full path for a file in the output directory"""
    return os.path.join(OUTPUT_DIR, filename)
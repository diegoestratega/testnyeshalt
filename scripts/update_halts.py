import requests
import csv
import json
import os
from datetime import datetime
import pytz

# NYSE Official CSV Endpoint
CSV_URL = "https://www.nyse.com/api/trade-halts/current/download"
OUTPUT_FILE = "data/halts.json"

def fetch_halts():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(CSV_URL, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse CSV content
        decoded_content = response.content.decode('utf-8')
        cr = csv.DictReader(decoded_content.splitlines())
        
        data = list(cr)
        
        # Add metadata
        output = {
            "last_updated": datetime.now(pytz.timezone('US/Eastern')).strftime("%Y-%m-%d %H:%M:%S ET"),
            "count": len(data),
            "data": data
        }
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(output, f, indent=2)
            
        print(f"Successfully updated {len(data)} halt records.")
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        exit(1)

if __name__ == "__main__":
    fetch_halts()

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
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(CSV_URL, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Parse CSV content with BOM handling
        decoded_content = response.content.decode('utf-8-sig')
        lines = decoded_content.splitlines()
        
        # Robust CSV Reading
        reader = csv.DictReader(lines)
        
        # Normalize headers (strip spaces)
        if reader.fieldnames:
            reader.fieldnames = [name.strip() for name in reader.fieldnames]

        clean_data = []
        for row in reader:
            clean_row = {}
            for k, v in row.items():
                if k: # Only keep valid keys
                    # Strip whitespace from Key AND Value
                    clean_row[k.strip()] = v.strip() if v else ""
            
            # Save row if it has a Symbol
            if 'Symbol' in clean_row:
                clean_data.append(clean_row)
        
        # Metadata
        output = {
            "last_updated": datetime.now(pytz.timezone('US/Eastern')).strftime("%Y-%m-%d %H:%M:%S ET"),
            "count": len(clean_data),
            "data": clean_data
        }
        
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(output, f, indent=2)
            
        print(f"Successfully updated {len(clean_data)} halt records.")
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        exit(1)

if __name__ == "__main__":
    fetch_halts()

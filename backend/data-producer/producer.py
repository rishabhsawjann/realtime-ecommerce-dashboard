import os
import json
import random
import time
import requests
from datetime import datetime

# Configurable API endpoint
API_URL = os.environ.get('SALES_API_URL', 'http://localhost:3000/sales')

PRODUCTS = [
    {'id': 'P001', 'category': 'Electronics'},
    {'id': 'P002', 'category': 'Books'},
    {'id': 'P003', 'category': 'Clothing'},
    {'id': 'P004', 'category': 'Home'},
    {'id': 'P005', 'category': 'Toys'},
]
LOCATIONS = ['CA', 'NY', 'TX', 'FL', 'WA', 'IL', 'MA', 'GA', 'NC', 'OH']

CUSTOMERS = [f'C{str(i).zfill(4)}' for i in range(1, 101)]


def generate_sale():
    product = random.choice(PRODUCTS)
    sale = {
        'product_id': product['id'],
        'category': product['category'],
        'price': round(random.uniform(10, 500), 2),
        'location': random.choice(LOCATIONS),
        'customer_id': random.choice(CUSTOMERS),
        'timestamp': datetime.utcnow().isoformat(),
    }
    return sale


def main():
    print(f"Sending sales data to {API_URL}")
    while True:
        sale = generate_sale()
        try:
            response = requests.post(API_URL, json=sale, timeout=5)
            if response.status_code == 200:
                print(f"[OK] {sale}")
            else:
                print(f"[ERROR] {response.status_code}: {response.text}")
        except Exception as e:
            print(f"[EXCEPTION] {e}")
        time.sleep(random.uniform(0.5, 2.0))  # Random interval between sales


if __name__ == '__main__':
    main() 
import os
import csv
from datetime import datetime

class CSVHandler:
    def __init__(self, output_dir='../data/csv', file_name='output.csv'):
        self.output_dir = output_dir
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.file_name = f'{file_name}_{timestamp}.csv'
        self.file_path = os.path.join(self.output_dir, self.file_name)
        os.makedirs(self.output_dir, exist_ok=True)
        if not os.path.exists(self.file_path):
            with open(self.file_path, mode='w', newline='', encoding='utf-8-sig') as file:
                writer = csv.DictWriter(file, fieldnames=['title', 'address', 'price', 'area'])
                writer.writeheader()

    def save_data(self, data):
        with open(self.file_path, mode='a', newline='', encoding='utf-8-sig') as file:
            writer = csv.DictWriter(file, fieldnames=data.keys())
            writer.writerow(data)

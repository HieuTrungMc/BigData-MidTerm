import os
from datetime import datetime

class TXTHandler:
    def __init__(self, output_dir='../data/txt', file_name='output.txt'):
        self.output_dir = output_dir
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.file_name = f'${file_name}_{timestamp}.csv'        
        self.file_path = os.path.join(self.output_dir, self.file_name)
        
        os.makedirs(self.output_dir, exist_ok=True)
        open(self.file_path, mode='w', encoding='utf-8').close()

    def save_data(self, data):
        with open(self.file_path, mode='a', encoding='utf-8') as file:
            file.write(f"Dự án: {data.get('title', 'N/A')}\n")
            file.write(f"Giá: {data.get('price', 'N/A')}\n")
            file.write(f"Địa chỉ: {data.get('address', 'N/A')}\n")
            file.write(f"Diện tích: {data.get('area', 'N/A')}\n")
            file.write("-" * 40 + "\n")

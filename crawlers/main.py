import scrapy
from scrapy.crawler import CrawlerProcess
from crawlers.spiders.batdongsan import BatdongsanSpider
import threading
import time
from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import json_util
import json


app = Flask(__name__)

def get_mongo_client():
    uri = 'mongodb+srv://hieutrungmc:verysafe@cluster0.0bbrp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
    client = MongoClient(uri)
    return client

@app.route('/batdongsan', methods=['GET'])
def get_buildings():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        
        client = get_mongo_client()
        db = client['batdongsan']
        collection = db['thongtin']
        
        skip = (page - 1) * per_page
        
        total = collection.count_documents({})
        buildings = list(collection.find({}).skip(skip).limit(per_page))
        
        buildings_json = json.loads(json_util.dumps(buildings))
        
        client.close()
        
        return jsonify({
            'success': True,
            'count': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page,
            'buildings': buildings_json
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Server error',
            'message': str(e)
        }), 500

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

@app.route('/health', methods=['GET'])
def health_check():
    try:
        # Test MongoDB connection
        client = get_mongo_client()
        client.admin.command('ping')
        client.close()
        return jsonify({'status': 'healthy', 'mongodb': 'connected'}), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'mongodb': 'disconnected', 'error': str(e)}), 500

def run_crawler():
    while True:
        process = CrawlerProcess(settings={
            "SCRAPY_SETTINGS_MODULE": "crawlers.settings"
        })
        process.crawl(BatdongsanSpider)
        process.start()
        process = None
        time.sleep(3600) 

if __name__ == '__main__':
    crawler_thread = threading.Thread(target=run_crawler)
    crawler_thread.daemon = True 
    crawler_thread.start()
    
    app.run(host='0.0.0.0', port=3000, debug=False)

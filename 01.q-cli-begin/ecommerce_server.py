#!/usr/bin/env python3
import json
import boto3
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import os

class EcommerceHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.dynamodb = boto3.client('dynamodb', region_name='us-east-1')
        super().__init__(*args, **kwargs)
    
    def do_HEAD(self):
        # HEAD 요청을 GET과 동일하게 처리하되 body는 보내지 않음
        self.do_GET()
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)
        
        if path == '/':
            self.serve_html()
        elif path == '/api/categories':
            self.get_categories(query_params)
        elif path == '/api/products':
            self.get_products(query_params)
        elif path == '/api/customers':
            self.get_customers(query_params)
        elif path == '/api/orders':
            self.get_orders(query_params)
        else:
            self.send_error(404)
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        path = self.path
        
        if path == '/api/categories':
            self.create_category(data)
        elif path == '/api/products':
            self.create_product(data)
        elif path == '/api/customers':
            self.create_customer(data)
        elif path == '/api/orders':
            self.create_order(data)
        else:
            self.send_error(404)
    
    def do_PUT(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        path = self.path
        
        if path.startswith('/api/categories/'):
            category_id = path.split('/')[-1]
            self.update_category(category_id, data)
        elif path.startswith('/api/products/'):
            product_id = path.split('/')[-1]
            self.update_product(product_id, data)
        elif path.startswith('/api/customers/'):
            customer_id = path.split('/')[-1]
            self.update_customer(customer_id, data)
        elif path.startswith('/api/orders/'):
            order_id = path.split('/')[-1]
            self.update_order(order_id, data)
        else:
            self.send_error(404)
    
    def do_DELETE(self):
        path = self.path
        
        if path.startswith('/api/categories/'):
            category_id = path.split('/')[-1]
            self.delete_category(category_id)
        elif path.startswith('/api/products/'):
            product_id = path.split('/')[-1]
            self.delete_product(product_id)
        elif path.startswith('/api/customers/'):
            customer_id = path.split('/')[-1]
            self.delete_customer(customer_id)
        elif path.startswith('/api/orders/'):
            order_id = path.split('/')[-1]
            self.delete_order(order_id)
        else:
            self.send_error(404)
    
    def serve_html(self):
        try:
            with open('/home/ec2-user/ecommerce.html', 'r', encoding='utf-8') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            if self.command != 'HEAD':  # HEAD 요청시에는 body를 보내지 않음
                self.wfile.write(content.encode('utf-8'))
        except FileNotFoundError:
            self.send_error(404, "HTML file not found")
    
    def send_json_response(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    # Categories CRUD
    def get_categories(self, query_params=None):
        try:
            if query_params and 'search' in query_params:
                # 카테고리 이름 및 설명으로 검색
                search_term = query_params['search'][0].lower()
                response = self.dynamodb.scan(TableName='Categories')
                items = []
                for item in response['Items']:
                    category_name = item['name']['S'].lower()
                    category_desc = item['description']['S'].lower()
                    if search_term in category_name or search_term in category_desc:
                        items.append({
                            'category_id': item['category_id']['S'],
                            'name': item['name']['S'],
                            'description': item['description']['S']
                        })
            else:
                response = self.dynamodb.scan(TableName='Categories')
                items = []
                for item in response['Items']:
                    items.append({
                        'category_id': item['category_id']['S'],
                        'name': item['name']['S'],
                        'description': item['description']['S']
                    })
            self.send_json_response(items)
        except Exception as e:
            self.send_json_response({'error': str(e)}, 500)
    
    def create_category(self, data):
        try:
            self.dynamodb.put_item(
                TableName='Categories',
                Item={
                    'category_id': {'S': data['category_id']},
                    'name': {'S': data['name']},
                    'description': {'S': data['description']}
                }
            )
            self.send_json_response({'success': True})
        except Exception as e:
            self.send_json_response({'error': str(e)}, 500)
    
    def update_category(self, category_id, data):
        try:
            self.dynamodb.update_item(
                TableName='Categories',
                Key={'category_id': {'S': category_id}},
                UpdateExpression='SET #n = :name, description = :desc',
                ExpressionAttributeNames={'#n': 'name'},
                ExpressionAttributeValues={
                    ':name': {'S': data['name']},
                    ':desc': {'S': data['description']}
                }
            )
            self.send_json_response({'success': True})
        except Exception as e:
            self.send_json_response({'error': str(e)}, 500)
    
    def delete_category(self, category_id):
        try:
            self.dynamodb.delete_item(
                TableName='Categories',
                Key={'category_id': {'S': category_id}}
            )
            self.send_json_response({'success': True})
        except Exception as e:
            self.send_json_response({'error': str(e)}, 500)
    
    # Products CRUD
    def get_products(self, query_params):
        try:
            if 'search' in query_params:
                # 간단한 검색 기능 (이름으로 검색)
                search_term = query_params['search'][0].lower()
                response = self.dynamodb.scan(TableName='Products')
                items = []
                for item in response['Items']:
                    product_name = item['name']['S'].lower()
                    if search_term in product_name:
                        items.append(self.format_product(item))
            else:
                response = self.dynamodb.scan(TableName='Products')
                items = [self.format_product(item) for item in response['Items']]
            self.send_json_response(items)
        except Exception as e:
            self.send_json_response({'error': str(e)}, 500)
    
    def format_product(self, item):
        return {
            'product_id': item['product_id']['S'],
            'name': item['name']['S'],
            'price': int(item['price']['N']),
            'stock': int(item['stock']['N']),
            'brand': item['brand']['S'],
            'category_id': item['category_id']['S']
        }
    
    def create_product(self, data):
        try:
            self.dynamodb.put_item(
                TableName='Products',
                Item={
                    'product_id': {'S': data['product_id']},
                    'name': {'S': data['name']},
                    'description': {'S': data['description']},
                    'price': {'N': str(data['price'])},
                    'stock': {'N': str(data['stock'])},
                    'brand': {'S': data['brand']},
                    'model': {'S': data['model']},
                    'category_id': {'S': data['category_id']}
                }
            )
            self.send_json_response({'success': True})
        except Exception as e:
            self.send_json_response({'error': str(e)}, 500)
    
    def update_product(self, product_id, data):
        try:
            self.dynamodb.update_item(
                TableName='Products',
                Key={'product_id': {'S': product_id}},
                UpdateExpression='SET #n = :name, description = :desc, price = :price, stock = :stock, brand = :brand, model = :model, category_id = :cat_id',
                ExpressionAttributeNames={'#n': 'name'},
                ExpressionAttributeValues={
                    ':name': {'S': data['name']},
                    ':desc': {'S': data['description']},
                    ':price': {'N': str(data['price'])},
                    ':stock': {'N': str(data['stock'])},
                    ':brand': {'S': data['brand']},
                    ':model': {'S': data['model']},
                    ':cat_id': {'S': data['category_id']}
                }
            )
            self.send_json_response({'success': True})
        except Exception as e:
            self.send_json_response({'error': str(e)}, 500)
    
    def delete_product(self, product_id):
        try:
            self.dynamodb.delete_item(
                TableName='Products',
                Key={'product_id': {'S': product_id}}
            )
            self.send_json_response({'success': True})
        except Exception as e:
            self.send_json_response({'error': str(e)}, 500)
    
    # Customers CRUD
    def get_customers(self, query_params):
        try:
            if 'search' in query_params:
                search_term = query_params['search'][0].lower()
                response = self.dynamodb.scan(TableName='Customers')
                items = []
                for item in response['Items']:
                    customer_name = item['name']['S'].lower()
                    if search_term in customer_name:
                        items.append(self.format_customer(item))
            else:
                response = self.dynamodb.scan(TableName='Customers')
                items = [self.format_customer(item) for item in response['Items']]
            self.send_json_response(items)
        except Exception as e:
            self.send_json_response({'error': str(e)}, 500)
    
    def format_customer(self, item):
        return {
            'customer_id': item['customer_id']['S'],
            'name': item['name']['S'],
            'email': item['email']['S'],
            'phone': item['phone']['S'],
            'address': item['address']['S'],
            'created_date': item['created_date']['S']
        }
    
    def create_customer(self, data):
        try:
            self.dynamodb.put_item(
                TableName='Customers',
                Item={
                    'customer_id': {'S': data['customer_id']},
                    'name': {'S': data['name']},
                    'email': {'S': data['email']},
                    'phone': {'S': data['phone']},
                    'address': {'S': data['address']},
                    'membership_level': {'S': data['membership_level']},
                    'created_date': {'S': data['created_date']}
                }
            )
            self.send_json_response({'success': True})
        except Exception as e:
            self.send_json_response({'error': str(e)}, 500)
    
    def update_customer(self, customer_id, data):
        try:
            self.dynamodb.update_item(
                TableName='Customers',
                Key={'customer_id': {'S': customer_id}},
                UpdateExpression='SET #n = :name, email = :email, phone = :phone, address = :address, membership_level = :level, created_date = :date',
                ExpressionAttributeNames={'#n': 'name'},
                ExpressionAttributeValues={
                    ':name': {'S': data['name']},
                    ':email': {'S': data['email']},
                    ':phone': {'S': data['phone']},
                    ':address': {'S': data['address']},
                    ':level': {'S': data['membership_level']},
                    ':date': {'S': data['created_date']}
                }
            )
            self.send_json_response({'success': True})
        except Exception as e:
            self.send_json_response({'error': str(e)}, 500)
    
    def delete_customer(self, customer_id):
        try:
            self.dynamodb.delete_item(
                TableName='Customers',
                Key={'customer_id': {'S': customer_id}}
            )
            self.send_json_response({'success': True})
        except Exception as e:
            self.send_json_response({'error': str(e)}, 500)
    
    # Orders CRUD
    def get_orders(self, query_params):
        try:
            if 'search' in query_params:
                # 주문 ID, 고객 ID, 상태로 검색
                search_term = query_params['search'][0].lower()
                response = self.dynamodb.scan(TableName='Orders')
                items = []
                for item in response['Items']:
                    order_id = item['order_id']['S'].lower()
                    customer_id = item['customer_id']['S'].lower()
                    status = item['status']['S'].lower()
                    if search_term in order_id or search_term in customer_id or search_term in status:
                        items.append(self.format_order(item))
            elif 'customer_id' in query_params:
                # 특정 고객의 주문 조회
                customer_id = query_params['customer_id'][0]
                response = self.dynamodb.query(
                    TableName='Orders',
                    IndexName='CustomerIndex',
                    KeyConditionExpression='customer_id = :cid',
                    ExpressionAttributeValues={':cid': {'S': customer_id}}
                )
                items = [self.format_order(item) for item in response['Items']]
            else:
                response = self.dynamodb.scan(TableName='Orders')
                items = [self.format_order(item) for item in response['Items']]
            self.send_json_response(items)
        except Exception as e:
            self.send_json_response({'error': str(e)}, 500)
    
    def format_order(self, item):
        items_list = []
        for order_item in item['items']['L']:
            item_data = {
                'product_id': order_item['M']['product_id']['S'],
                'quantity': int(order_item['M']['quantity']['N'])
            }
            # price 또는 unit_price 필드 처리
            if 'price' in order_item['M']:
                item_data['price'] = int(order_item['M']['price']['N'])
            elif 'unit_price' in order_item['M']:
                item_data['price'] = int(order_item['M']['unit_price']['N'])
            
            # 추가 필드들 처리
            if 'product_name' in order_item['M']:
                item_data['product_name'] = order_item['M']['product_name']['S']
            if 'original_price' in order_item['M']:
                item_data['original_price'] = int(order_item['M']['original_price']['N'])
            if 'discount_rate' in order_item['M']:
                item_data['discount_rate'] = float(order_item['M']['discount_rate']['N'])
                
            items_list.append(item_data)
        
        order_data = {
            'order_id': item['order_id']['S'],
            'customer_id': item['customer_id']['S'],
            'order_date': item['order_date']['S'],
            'total_amount': int(item['total_amount']['N']),
            'status': item['status']['S'],
            'items': items_list
        }
        
        # 추가 필드들 처리
        if 'payment_method' in item:
            order_data['payment_method'] = item['payment_method']['S']
        if 'shipping_address' in item:
            order_data['shipping_address'] = item['shipping_address']['S']
        if 'estimated_delivery' in item:
            order_data['estimated_delivery'] = item['estimated_delivery']['S']
        if 'is_prime_day_order' in item:
            order_data['is_prime_day_order'] = item['is_prime_day_order']['BOOL']
            
        return order_data
    
    def create_order(self, data):
        try:
            items_list = []
            for item in data['items']:
                items_list.append({
                    'M': {
                        'product_id': {'S': item['product_id']},
                        'quantity': {'N': str(item['quantity'])},
                        'price': {'N': str(item['price'])}
                    }
                })
            
            self.dynamodb.put_item(
                TableName='Orders',
                Item={
                    'order_id': {'S': data['order_id']},
                    'customer_id': {'S': data['customer_id']},
                    'order_date': {'S': data['order_date']},
                    'total_amount': {'N': str(data['total_amount'])},
                    'status': {'S': data['status']},
                    'items': {'L': items_list}
                }
            )
            self.send_json_response({'success': True})
        except Exception as e:
            self.send_json_response({'error': str(e)}, 500)
    
    def update_order(self, order_id, data):
        try:
            items_list = []
            for item in data['items']:
                items_list.append({
                    'M': {
                        'product_id': {'S': item['product_id']},
                        'quantity': {'N': str(item['quantity'])},
                        'price': {'N': str(item['price'])}
                    }
                })
            
            self.dynamodb.update_item(
                TableName='Orders',
                Key={'order_id': {'S': order_id}},
                UpdateExpression='SET customer_id = :cust_id, order_date = :date, total_amount = :amount, #s = :status, items = :items',
                ExpressionAttributeNames={'#s': 'status'},
                ExpressionAttributeValues={
                    ':cust_id': {'S': data['customer_id']},
                    ':date': {'S': data['order_date']},
                    ':amount': {'N': str(data['total_amount'])},
                    ':status': {'S': data['status']},
                    ':items': {'L': items_list}
                }
            )
            self.send_json_response({'success': True})
        except Exception as e:
            self.send_json_response({'error': str(e)}, 500)
    
    def delete_order(self, order_id):
        try:
            self.dynamodb.delete_item(
                TableName='Orders',
                Key={'order_id': {'S': order_id}}
            )
            self.send_json_response({'success': True})
        except Exception as e:
            self.send_json_response({'error': str(e)}, 500)

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8000), EcommerceHandler)
    print("이커머스 관리 서버가 http://0.0.0.0:8000 에서 실행 중입니다...")
    server.serve_forever()

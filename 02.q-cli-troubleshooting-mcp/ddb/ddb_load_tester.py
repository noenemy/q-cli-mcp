#!/usr/bin/env python3
"""
DynamoDB Load Tester for Amazon Prime Day Simulation
이커머스 Prime Day 시나리오를 시뮬레이션하는 통합 부하 테스트 도구

Usage:
    python3 ddb_load_tester.py --demo          # 30초 데모 테스트 (5개 스레드)
    python3 ddb_load_tester.py --full          # 5분 실제 테스트 (20개 스레드)
    python3 ddb_load_tester.py --custom        # 사용자 정의 설정

Features:
- 대량 상품 조회 요청 (Products table scan/query)
- 대량 주문 생성 시도 (Orders table write)
- 동시 실행 (멀티스레딩)
- Decimal 타입 사용 (Float 사용 안함)
- 실시간 모니터링 및 통계
"""

import boto3
import threading
import time
import random
import uuid
import argparse
from datetime import datetime, timedelta
from decimal import Decimal
import json
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from botocore.exceptions import ClientError
import sys
import os

# 로깅 설정
def setup_logging():
    """로깅 설정"""
    log_dir = '/home/ec2-user/ddb'
    os.makedirs(log_dir, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f'{log_dir}/load_test.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()

class DynamoDBLoadTester:
    def __init__(self, region='us-east-1', test_duration=300, num_threads=20):
        """DynamoDB Load Tester 초기화"""
        self.region = region
        self.dynamodb = boto3.client('dynamodb', region_name=region)
        self.test_duration = test_duration
        self.num_threads = num_threads
        self.start_time = None
        
        # 통계 데이터
        self.stats = {
            'product_queries': 0,
            'product_query_errors': 0,
            'order_creates': 0,
            'order_create_errors': 0,
            'throttled_requests': 0,
            'total_requests': 0,
            'start_time': None,
            'end_time': None
        }
        self.stats_lock = threading.Lock()
        
        # 테스트 데이터
        self.product_ids = []
        self.customer_ids = []
        self.category_ids = []
        
        logger.info(f"DynamoDB Load Tester 초기화 완료 - Region: {region}, Duration: {test_duration}초, Threads: {num_threads}")
    
    def load_test_data(self):
        """테스트에 필요한 기존 데이터 로드"""
        try:
            # Products 테이블에서 product_id 목록 가져오기
            response = self.dynamodb.scan(
                TableName='Products',
                ProjectionExpression='product_id'
            )
            self.product_ids = [item['product_id']['S'] for item in response['Items']]
            
            # Customers 테이블에서 customer_id 목록 가져오기
            response = self.dynamodb.scan(
                TableName='Customers',
                ProjectionExpression='customer_id'
            )
            self.customer_ids = [item['customer_id']['S'] for item in response['Items']]
            
            # Categories 테이블에서 category_id 목록 가져오기
            response = self.dynamodb.scan(
                TableName='Categories',
                ProjectionExpression='category_id'
            )
            self.category_ids = [item['category_id']['S'] for item in response['Items']]
            
            logger.info(f"테스트 데이터 로드 완료 - Products: {len(self.product_ids)}, "
                       f"Customers: {len(self.customer_ids)}, Categories: {len(self.category_ids)}")
            
        except Exception as e:
            logger.error(f"테스트 데이터 로드 실패: {str(e)}")
            raise
    
    def update_stats(self, operation, success=True, throttled=False):
        """통계 데이터 업데이트"""
        with self.stats_lock:
            self.stats['total_requests'] += 1
            
            if throttled:
                self.stats['throttled_requests'] += 1
            
            if operation == 'product_query':
                if success:
                    self.stats['product_queries'] += 1
                else:
                    self.stats['product_query_errors'] += 1
            elif operation == 'order_create':
                if success:
                    self.stats['order_creates'] += 1
                else:
                    self.stats['order_create_errors'] += 1
    
    def simulate_product_query(self, thread_id):
        """상품 조회 시뮬레이션 - Prime Day 대량 조회 패턴"""
        query_types = ['scan_all', 'query_by_category', 'get_specific_product']
        
        while time.time() - self.start_time < self.test_duration:
            try:
                query_type = random.choice(query_types)
                
                if query_type == 'scan_all':
                    # 전체 상품 스캔 (Prime Day 메인 페이지)
                    response = self.dynamodb.scan(
                        TableName='Products',
                        Limit=random.randint(10, 50)  # 페이지네이션 시뮬레이션
                    )
                    
                elif query_type == 'query_by_category':
                    # 카테고리별 상품 조회 (에어컨, 난방기 등)
                    if self.category_ids:
                        category_id = random.choice(self.category_ids)
                        response = self.dynamodb.query(
                            TableName='Products',
                            IndexName='CategoryIndex',
                            KeyConditionExpression='category_id = :cat_id',
                            ExpressionAttributeValues={
                                ':cat_id': {'S': category_id}
                            },
                            Limit=random.randint(5, 20)
                        )
                
                elif query_type == 'get_specific_product':
                    # 특정 상품 조회 (상품 상세 페이지)
                    if self.product_ids:
                        product_id = random.choice(self.product_ids)
                        response = self.dynamodb.get_item(
                            TableName='Products',
                            Key={'product_id': {'S': product_id}}
                        )
                
                self.update_stats('product_query', success=True)
                
                # Prime Day 트래픽 패턴 시뮬레이션 (빠른 연속 요청)
                time.sleep(random.uniform(0.01, 0.1))
                
            except ClientError as e:
                error_code = e.response['Error']['Code']
                if error_code in ['ProvisionedThroughputExceededException', 'ThrottlingException']:
                    self.update_stats('product_query', success=False, throttled=True)
                    logger.warning(f"Thread-{thread_id}: 상품 조회 스로틀링 발생 - {error_code}")
                    time.sleep(random.uniform(0.1, 0.5))  # 백오프
                else:
                    self.update_stats('product_query', success=False)
                    logger.error(f"Thread-{thread_id}: 상품 조회 오류 - {str(e)}")
            
            except Exception as e:
                self.update_stats('product_query', success=False)
                logger.error(f"Thread-{thread_id}: 상품 조회 예외 - {str(e)}")
    
    def simulate_order_creation(self, thread_id):
        """주문 생성 시뮬레이션 - Prime Day 대량 주문 패턴"""
        order_statuses = ['PENDING', 'CONFIRMED']
        payment_methods = ['CARD', 'BANK_TRANSFER']
        
        while time.time() - self.start_time < self.test_duration:
            try:
                if not self.customer_ids or not self.product_ids:
                    time.sleep(0.1)
                    continue
                
                # Prime Day 주문 데이터 생성
                order_id = f"ORD{int(time.time())}{random.randint(1000, 9999)}"
                customer_id = random.choice(self.customer_ids)
                selected_products = random.sample(
                    self.product_ids, 
                    min(random.randint(1, 3), len(self.product_ids))
                )
                
                # 주문 아이템 생성 (Decimal 사용)
                items_list = []
                total_amount = Decimal('0')
                
                for product_id in selected_products:
                    quantity = random.randint(1, 5)
                    # Prime Day 할인가 시뮬레이션
                    unit_price = Decimal(str(random.randint(50000, 2000000)))
                    discount_rate = Decimal(str(random.uniform(0.1, 0.5)))  # 10-50% 할인
                    discounted_price = unit_price * (Decimal('1') - discount_rate)
                    
                    items_list.append({
                        'M': {
                            'product_id': {'S': product_id},
                            'product_name': {'S': f'Prime Day Special - {product_id}'},
                            'quantity': {'N': str(quantity)},
                            'unit_price': {'N': str(int(discounted_price))},
                            'original_price': {'N': str(int(unit_price))},
                            'discount_rate': {'N': str(discount_rate)}
                        }
                    })
                    total_amount += discounted_price * quantity
                
                # 주문 생성
                order_item = {
                    'order_id': {'S': order_id},
                    'customer_id': {'S': customer_id},
                    'order_date': {'S': datetime.utcnow().isoformat() + 'Z'},
                    'status': {'S': random.choice(order_statuses)},
                    'total_amount': {'N': str(int(total_amount))},
                    'shipping_address': {'S': f'Prime Day 배송지 - {random.randint(1, 1000)}'},
                    'payment_method': {'S': random.choice(payment_methods)},
                    'items': {'L': items_list},
                    'is_prime_day_order': {'BOOL': True},
                    'estimated_delivery': {'S': (datetime.utcnow() + timedelta(days=1)).isoformat() + 'Z'}
                }
                
                # DynamoDB에 주문 저장
                self.dynamodb.put_item(
                    TableName='Orders',
                    Item=order_item
                )
                
                self.update_stats('order_create', success=True)
                
                # Prime Day 주문 폭주 패턴 시뮬레이션
                time.sleep(random.uniform(0.05, 0.2))
                
            except ClientError as e:
                error_code = e.response['Error']['Code']
                if error_code in ['ProvisionedThroughputExceededException', 'ThrottlingException']:
                    self.update_stats('order_create', success=False, throttled=True)
                    logger.warning(f"Thread-{thread_id}: 주문 생성 스로틀링 발생 - {error_code}")
                    time.sleep(random.uniform(0.2, 1.0))  # 더 긴 백오프
                else:
                    self.update_stats('order_create', success=False)
                    logger.error(f"Thread-{thread_id}: 주문 생성 오류 - {str(e)}")
            
            except Exception as e:
                self.update_stats('order_create', success=False)
                logger.error(f"Thread-{thread_id}: 주문 생성 예외 - {str(e)}")
    
    def worker_thread(self, thread_id):
        """워커 스레드 - 상품 조회와 주문 생성을 동시 실행"""
        logger.info(f"Thread-{thread_id}: 부하 테스트 시작")
        
        # 각 스레드에서 상품 조회와 주문 생성을 동시에 실행
        with ThreadPoolExecutor(max_workers=2) as executor:
            # 상품 조회 태스크
            query_future = executor.submit(self.simulate_product_query, thread_id)
            # 주문 생성 태스크
            order_future = executor.submit(self.simulate_order_creation, thread_id)
            
            # 두 태스크 완료 대기
            for future in as_completed([query_future, order_future]):
                try:
                    future.result()
                except Exception as e:
                    logger.error(f"Thread-{thread_id}: 워커 스레드 오류 - {str(e)}")
        
        logger.info(f"Thread-{thread_id}: 부하 테스트 완료")
    
    def print_real_time_stats(self):
        """실시간 통계 출력"""
        while time.time() - self.start_time < self.test_duration:
            time.sleep(10)  # 10초마다 통계 출력
            
            with self.stats_lock:
                elapsed_time = time.time() - self.start_time
                total_requests = self.stats['total_requests']
                rps = total_requests / elapsed_time if elapsed_time > 0 else 0
                
                logger.info(f"""
=== Prime Day Load Test 실시간 통계 ===
경과 시간: {elapsed_time:.1f}초 / {self.test_duration}초
총 요청 수: {total_requests}
초당 요청 수 (RPS): {rps:.2f}
상품 조회 성공: {self.stats['product_queries']}
상품 조회 실패: {self.stats['product_query_errors']}
주문 생성 성공: {self.stats['order_creates']}
주문 생성 실패: {self.stats['order_create_errors']}
스로틀링 발생: {self.stats['throttled_requests']}
성공률: {((self.stats['product_queries'] + self.stats['order_creates']) / total_requests * 100):.2f}% (총 요청 대비)
=====================================
                """)
    
    def run_load_test(self):
        """메인 부하 테스트 실행"""
        logger.info("=== Amazon Prime Day DynamoDB Load Test 시작 ===")
        logger.info(f"테스트 설정: {self.num_threads}개 스레드, {self.test_duration}초 동안 실행")
        
        # 테스트 데이터 로드
        self.load_test_data()
        
        # 테스트 시작 시간 기록
        self.start_time = time.time()
        self.stats['start_time'] = datetime.utcnow().isoformat()
        
        # 스레드 풀 생성 및 실행
        with ThreadPoolExecutor(max_workers=self.num_threads + 1) as executor:
            # 워커 스레드들 시작
            worker_futures = []
            for i in range(self.num_threads):
                future = executor.submit(self.worker_thread, i + 1)
                worker_futures.append(future)
            
            # 실시간 통계 출력 스레드 시작
            stats_future = executor.submit(self.print_real_time_stats)
            
            # 모든 스레드 완료 대기
            for future in as_completed(worker_futures + [stats_future]):
                try:
                    future.result()
                except Exception as e:
                    logger.error(f"스레드 실행 오류: {str(e)}")
        
        # 테스트 완료
        self.stats['end_time'] = datetime.utcnow().isoformat()
        self.print_final_stats()
        logger.info("=== Amazon Prime Day DynamoDB Load Test 완료 ===")
    
    def print_final_stats(self):
        """최종 통계 출력"""
        total_time = time.time() - self.start_time
        total_requests = self.stats['total_requests']
        successful_requests = self.stats['product_queries'] + self.stats['order_creates']
        failed_requests = self.stats['product_query_errors'] + self.stats['order_create_errors']
        
        logger.info(f"""
╔══════════════════════════════════════════════════════════════╗
║                   PRIME DAY LOAD TEST 최종 결과                ║
╠══════════════════════════════════════════════════════════════╣
║ 테스트 시간: {total_time:.2f}초                                    ║
║ 총 요청 수: {total_requests:,}개                                  ║
║ 평균 RPS: {total_requests/total_time:.2f}                        ║
║                                                              ║
║ 📊 상품 조회 (Product Queries)                                 ║
║   성공: {self.stats['product_queries']:,}개                      ║
║   실패: {self.stats['product_query_errors']:,}개                 ║
║                                                              ║
║ 🛒 주문 생성 (Order Creation)                                  ║
║   성공: {self.stats['order_creates']:,}개                        ║
║   실패: {self.stats['order_create_errors']:,}개                  ║
║                                                              ║
║ ⚠️  스로틀링: {self.stats['throttled_requests']:,}개              ║
║ ✅ 전체 성공률: {(successful_requests/total_requests*100):.2f}%   ║
║ ❌ 전체 실패율: {(failed_requests/total_requests*100):.2f}%       ║
╚══════════════════════════════════════════════════════════════╝
        """)
        
        # 결과를 파일로도 저장
        result_file = '/home/ec2-user/ddb/load_test_result.json'
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, indent=2, ensure_ascii=False)
        
        logger.info(f"상세 결과가 {result_file}에 저장되었습니다.")

def show_help():
    """도움말 출력"""
    help_text = """
🚀 DynamoDB Load Tester for Amazon Prime Day

사용법:
    python3 ddb_load_tester.py [옵션]

옵션:
    --demo          30초 데모 테스트 (5개 스레드)
    --full          5분 실제 테스트 (20개 스레드) - 기본값
    --custom        사용자 정의 설정
    --help, -h      이 도움말 출력

예시:
    python3 ddb_load_tester.py --demo
    python3 ddb_load_tester.py --full
    python3 ddb_load_tester.py --custom

특징:
    ✅ 동시 실행: 상품 조회와 주문 생성을 동시에 수행
    ✅ 멀티스레딩: 높은 동시성으로 실제 Prime Day 트래픽 시뮬레이션
    ✅ Decimal 타입: 정확한 금액 계산
    ✅ 실시간 모니터링: 10초마다 통계 출력
    ✅ 스로틀링 감지: DynamoDB 한계 도달 시 자동 처리

주의사항:
    ⚠️  이 테스트는 DynamoDB에 높은 부하를 가합니다
    💰 Provisioned 모드에서 스로틀링이 발생할 수 있습니다
    📊 CloudWatch에서 실시간 메트릭 모니터링을 권장합니다
    """
    print(help_text)

def get_custom_settings():
    """사용자 정의 설정 입력"""
    print("\n=== 사용자 정의 설정 ===")
    
    try:
        duration = int(input("테스트 시간 (초, 기본값 300): ") or "300")
        threads = int(input("스레드 수 (기본값 20): ") or "20")
        
        if duration <= 0 or threads <= 0:
            raise ValueError("양수를 입력해주세요.")
        
        print(f"\n설정 확인:")
        print(f"  테스트 시간: {duration}초")
        print(f"  스레드 수: {threads}개")
        
        confirm = input("\n이 설정으로 진행하시겠습니까? (y/N): ")
        if confirm.lower() != 'y':
            print("테스트가 취소되었습니다.")
            return None, None
        
        return duration, threads
        
    except ValueError as e:
        print(f"잘못된 입력입니다: {e}")
        return None, None
    except KeyboardInterrupt:
        print("\n테스트가 취소되었습니다.")
        return None, None

def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(description='DynamoDB Load Tester for Amazon Prime Day', add_help=False)
    parser.add_argument('--demo', action='store_true', help='30초 데모 테스트')
    parser.add_argument('--full', action='store_true', help='5분 실제 테스트')
    parser.add_argument('--custom', action='store_true', help='사용자 정의 설정')
    parser.add_argument('--help', '-h', action='store_true', help='도움말 출력')
    
    args = parser.parse_args()
    
    # 도움말 출력
    if args.help or len(sys.argv) == 1:
        show_help()
        return
    
    try:
        if args.demo:
            print("🎯 데모 테스트 모드 (30초, 5개 스레드)")
            tester = DynamoDBLoadTester(region='us-east-1', test_duration=30, num_threads=5)
            
        elif args.custom:
            duration, threads = get_custom_settings()
            if duration is None or threads is None:
                return
            
            print(f"🔧 사용자 정의 테스트 ({duration}초, {threads}개 스레드)")
            tester = DynamoDBLoadTester(region='us-east-1', test_duration=duration, num_threads=threads)
            
        else:  # --full 또는 기본값
            print("🚀 실제 Prime Day 테스트 (5분, 20개 스레드)")
            print("⚠️  주의: 이 테스트는 DynamoDB에 높은 부하를 가합니다.")
            print("💰 비용: Provisioned 모드에서 스로틀링이 발생할 수 있습니다.")
            
            if not args.full:  # 명시적으로 --full을 지정하지 않은 경우 확인
                response = input("\n계속 진행하시겠습니까? (y/N): ")
                if response.lower() != 'y':
                    print("테스트가 취소되었습니다.")
                    return
            
            tester = DynamoDBLoadTester(region='us-east-1', test_duration=300, num_threads=20)
        
        # 부하 테스트 실행
        tester.run_load_test()
        
    except KeyboardInterrupt:
        logger.info("사용자에 의해 테스트가 중단되었습니다.")
    except Exception as e:
        logger.error(f"부하 테스트 실행 중 오류 발생: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
  

# DynamoDB Load Tester for Amazon Prime Day

## 개요
Amazon Prime Day를 시뮬레이션하는 통합 DynamoDB 부하 테스트 도구입니다.
대량의 상품 조회와 주문 생성을 동시에 수행하여 실제 이커머스 환경의 부하를 재현합니다.

## 스크립트 작성 프롬프트
이커머스 Amazon Prime Day를 예상하고 us-east-1 리전에 있는 DynamoDB의 테이블에 부하를 주려고 합니다.
1) 짧은 시간 대량의 상품 조회 요청과 
2) 대량의 주문 생성 시도가 발생하며
3) 위의 두 가지는 동시에 일어납니다.
4) Float type은 사용하지 않고 Decimal 만 사용합니다.
5) 20개 스레드, 5분간 테스트 예정입니다.
Load Tester를 위한 스크립트를 Python 으로 만들어 주세요. 
파일명과 위치는 /home/ec2-user/ddb/ddb_load_tester.py 입니다.

## 주요 특징
- ✅ **통합 스크립트**: 모든 기능이 하나의 파일에 포함
- ✅ **동시 실행**: 상품 조회와 주문 생성을 동시에 수행
- ✅ **멀티스레딩**: 최대 20개 스레드로 높은 동시성 구현
- ✅ **Decimal 타입**: Float 대신 Decimal 사용으로 정확한 금액 계산
- ✅ **실시간 모니터링**: 10초마다 실시간 통계 출력
- ✅ **스로틀링 감지**: DynamoDB 스로틀링 발생 시 자동 감지 및 백오프
- ✅ **Prime Day 시나리오**: 할인가, 대량 주문 등 실제 시나리오 반영

## 파일 구조
```
/home/ec2-user/ddb/
├── ddb_load_tester.py      # 통합 Load Tester (메인 파일)
├── load_test.log          # 테스트 실행 로그
├── load_test_result.json  # 테스트 결과 JSON
└── README.md             # 이 파일
```

## 사용법

### 1. 도움말 확인
```bash
cd /home/ec2-user/ddb
python3 ddb_load_tester.py --help
```

### 2. 데모 테스트 (30초, 5개 스레드)
```bash
cd /home/ec2-user/ddb
python3 ddb_load_tester.py --demo
```

### 3. 실제 Prime Day 테스트 (5분, 20개 스레드)
```bash
cd /home/ec2-user/ddb
python3 ddb_load_tester.py --full
```

### 4. 사용자 정의 설정
```bash
cd /home/ec2-user/ddb
python3 ddb_load_tester.py --custom
```

### 5. 기본 실행 (확인 후 5분 테스트)
```bash
cd /home/ec2-user/ddb
python3 ddb_load_tester.py
```

## 명령어 옵션

| 옵션 | 설명 | 스레드 수 | 테스트 시간 |
|------|------|-----------|-------------|
| `--demo` | 데모 테스트 | 5개 | 30초 |
| `--full` | 실제 Prime Day 테스트 | 20개 | 5분 |
| `--custom` | 사용자 정의 설정 | 사용자 입력 | 사용자 입력 |
| `--help`, `-h` | 도움말 출력 | - | - |

## 테스트 시나리오

### 상품 조회 패턴
1. **전체 상품 스캔**: Prime Day 메인 페이지 시뮬레이션
2. **카테고리별 조회**: 에어컨, 난방기 등 카테고리 필터링
3. **특정 상품 조회**: 상품 상세 페이지 접근

### 주문 생성 패턴
1. **Prime Day 할인가**: 10-50% 할인 적용
2. **다중 상품 주문**: 1-3개 상품 동시 주문
3. **빠른 배송**: 익일 배송 설정
4. **Decimal 정확도**: 모든 금액 계산에 Decimal 사용

## 모니터링 지표

### 실시간 통계 (10초마다 출력)
- 경과 시간 / 총 테스트 시간
- 총 요청 수 및 초당 요청 수 (RPS)
- 상품 조회 성공/실패 수
- 주문 생성 성공/실패 수
- 스로틀링 발생 횟수
- 전체 성공률

### 최종 결과
- 테스트 총 시간 및 평균 RPS
- 각 작업별 성공/실패 통계
- 스로틀링 발생 현황
- 전체 성공률 및 실패율

## 예시 실행 결과

### 데모 테스트 결과 예시
```
╔══════════════════════════════════════════════════════════════╗
║                   PRIME DAY LOAD TEST 최종 결과                ║
╠══════════════════════════════════════════════════════════════╣
║ 테스트 시간: 48.98초                                    ║
║ 총 요청 수: 1,296개                                  ║
║ 평균 RPS: 26.46                        ║
║                                                              ║
║ 📊 상품 조회 (Product Queries)                                 ║
║   성공: 670개                      ║
║   실패: 5개                 ║
║                                                              ║
║ 🛒 주문 생성 (Order Creation)                                  ║
║   성공: 621개                        ║
║   실패: 0개                  ║
║                                                              ║
║ ⚠️  스로틀링: 5개              ║
║ ✅ 전체 성공률: 99.61%   ║
║ ❌ 전체 실패율: 0.39%       ║
╚══════════════════════════════════════════════════════════════╝
```

## 주의사항

### DynamoDB 비용
- **Provisioned Mode**: RCU/WCU 2로 설정된 상태에서 스로틀링 발생 가능
- **스로틀링 시**: 자동 백오프로 재시도하지만 테스트 시간이 길어질 수 있음
- **모니터링**: CloudWatch에서 실시간 메트릭 확인 권장

### 테스트 환경
- **리전**: us-east-1 고정
- **테이블**: Categories, Products, Customers, Orders 필요
- **권한**: DynamoDB 읽기/쓰기 권한 필요

## 결과 분석

### 성공적인 테스트 지표
- **높은 RPS**: 50+ 요청/초
- **낮은 오류율**: 5% 미만
- **적절한 스로틀링**: 전체 요청의 10% 미만

### 문제 상황 대응
- **높은 스로틀링**: RCU/WCU 증가 고려
- **높은 오류율**: 네트워크 또는 권한 문제 확인
- **낮은 RPS**: 스레드 수 또는 테스트 로직 조정

## 로그 파일
- **실행 로그**: `/home/ec2-user/ddb/load_test.log`
- **결과 JSON**: `/home/ec2-user/ddb/load_test_result.json`

## 고급 사용법

### 스크립트 내부 설정 변경
```python
# ddb_load_tester.py 파일 내에서 직접 수정 가능
tester = DynamoDBLoadTester(
    region='us-east-1',
    test_duration=600,  # 10분으로 변경
    num_threads=30      # 30개 스레드로 변경
)
```

### 시나리오 커스터마이징
- `simulate_product_query()`: 상품 조회 패턴 수정
- `simulate_order_creation()`: 주문 생성 패턴 수정
- 할인율, 주문 수량, 배송 옵션 등 조정 가능

## 문제 해결

### 일반적인 오류
1. **ModuleNotFoundError**: `pip3 install boto3` 실행
2. **권한 오류**: IAM 역할에 DynamoDB 권한 확인
3. **테이블 없음**: DynamoDB 테이블 존재 여부 확인

### 성능 최적화
1. **스레드 수 조정**: 시스템 리소스에 맞게 조정
2. **백오프 전략**: 스로틀링 발생 시 대기 시간 조정
3. **배치 크기**: 스캔/쿼리 Limit 값 조정

## 라이센스
이 도구는 교육 및 테스트 목적으로 제작되었습니다.

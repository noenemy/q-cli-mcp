```
Application Load Balancer, 두 개의 t3.medium EC2 인스턴스, 그리고 RDS db.t3.medium MySQL 데이터베이스를 포함한 간단한 웹 애플리케이션의 비용 분석을 loaded된 MCP 서버를 이용해서 작성해 주세요. 월 730시간 사용과 약 100GB의 중간 수준의 데이터 전송량을 가정하고, 예상 비용을 /home/ec2-user/cost-analysis디렉토리에 PDF 형식으로 변환해 주시기 바랍니다.
```
<img width="1461" height="532" alt="Screenshot 2025-07-17 at 5 03 54 AM" src="https://github.com/user-attachments/assets/7adbd69e-a077-4e0a-9cda-1b42bc18ec2f" />

아래와 같은 pdf 결과물을 보실 수 있습니다. <br>
<img width="1024" height="948" alt="image" src="https://github.com/user-attachments/assets/c29b959e-1b39-4255-8b6e-efa7fde98313" />

Example 1: Analyze a serverless application
```
API Gateway, Lambda, 그리고 DynamoDB를 사용하는 서버리스 애플리케이션의 비용 분석을 작성해 주세요. 월 100만 건의 API 호출, 평균 Lambda 실행 시간 200ms(512MB 메모리), 그리고 10GB의 DynamoDB 스토리지와 월 500만 건의 읽기 요청 및 100만 건의 쓰기 요청을 가정합니다. 예상 비용을 PDF 형식으로 변환해 주시기 바랍니다.
```

Example 2: Analyze multi-tier architectures
```
CloudFront와 ALB를 포함한 프레젠테이션 계층, Fargate를 사용하는 ECS의 애플리케이션 계층, 그리고 Aurora PostgreSQL의 데이터 계층으로 구성된 3계층 웹 애플리케이션의 비용 분석을 작성해 주세요. 각각 1 vCPU와 2GB 메모리를 가진 2개의 Fargate 태스크, 100GB 스토리지가 있는 Aurora db.r5.large 인스턴스, 그리고 10을 포함한 Application Load Balancer의 비용을 포함해 주시기 바랍니다.
```

<img width="1024" height="797" alt="image" src="https://github.com/user-attachments/assets/1ee71c4e-11ac-46d5-bbbf-8c717631e6fd" />

Example 3: Compare deployment options
```
EC2 시작 유형과 Fargate 시작 유형을 사용하는 ECS에서 컨테이너화된 애플리케이션 실행 비용을 비교해 주세요. 각각 1 vCPU와 2GB 메모리가 필요한 4개의 컨테이너가 한 달 동안 24/7 실행된다고 가정합니다. EC2의 경우 t3.medium 인스턴스를 사용합니다. 이 워크로드에 대해 어떤 옵션이 더 비용 효율적인지 추천해 주시고, 예상 비용을 HTML 웹페이지 형식으로 변환해 주시기 바랍니다.
```
```
마이크로서비스 아키텍처를 사용하는 e-commerce 플랫폼의 비용 분석을 작성해 주세요. 제품 카탈로그, 장바구니, 결제, 결제 처리, 주문 관리 및 사용자 인증을 위한 구성 요소를 포함해 주세요. 월간 활성 사용자 50만 명, 일일 페이지뷰 200만 회, 월 5만 건의 주문과 같은 중간 수준의 트래픽을 가정합니다. 분석 시 AWS 비용 최적화 모범 사례를 따르고, 예상 비용을 PDF 형식으로 변환해 주시기 바랍니다.

주요 요점:

    마이크로서비스별 개별 비용 분석
    트래픽 패턴에 따른 리소스 산정
    AWS 비용 최적화 모범 사례 적용
    확장성을 고려한 아키텍처 설계
    각 서비스별 모니터링 및 운영 비용 포함
    데이터 전송 및 스토리지 비용 고려
    고가용성 및 재해 복구 구성 비용 반영
```

<img width="600" height="453" alt="image" src="https://github.com/user-attachments/assets/3f1e953a-fa22-465a-ba62-35667ecee80b" />

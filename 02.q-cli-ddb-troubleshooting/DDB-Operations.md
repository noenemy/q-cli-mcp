# DynamoDB를 이용하여 Prime Day 이벤트 준비하기

DynamoDB 콘솔을 통해서 설정과 테이블들을 확인해 봅시다. 특히 Capacity mode가 On demand인 것이 확인되셨나요? <br>
<img width="1348" height="605" alt="Screenshot 2025-07-18 at 5 21 55 AM" src="https://github.com/user-attachments/assets/a53d8c61-48d9-4454-a1b3-6ff493d6fc23" />

### MCP 설정에 필요한 패키지를 설치해 봅니다.
```
q chat
```

```
uvx 패키지를 설치해 줘
```

```
aws documentation mcp server 파일을 ~/.aws/amazonq/mcp.json에 추가해 줘 기존 설정은 지우지 말아줘.
```

```
aws cloudwatch mcp server 파일을 ~/.aws/amazonq/mcp.json에 추가해 줘 기존 설정은 지우지 말아줘.
```


```
aws Pricing List MCP Server 파일을 ~/.aws/amazonq/mcp.json에 추가해 줘 기존 설정은 지우지 말아줘.
```

### DynamoDB 설정 변경하기
평소 운영하는 DynamoDB가 큰 부하를 일으키지 않는다고 가정하고 아래와 같이 Provisioned Capacity를 설정해 봅니다.

```
DynamoDB의 모든 테이블들을 Provisioned Capacity Mode로 바꿔줘. WCU 3, RCU 3으로 변경해 줘.
```

관리 콘솔을 통해서 변경된 설정을 확인해 봅시다. On Demand에서 Provisioned로 바뀌었는지 확인해 봅시다.
<img width="1329" height="1065" alt="Screenshot 2025-07-18 at 5 22 58 AM" src="https://github.com/user-attachments/assets/9475aedf-874f-46bb-a255-842313ab23ae" />


### Prime Day 준비하기
이제 테이블에 로드테스트를 해 보겠습니다. Q Developer CLI가 만들어 준 파일을 이용하여 load 테스트를 해 봅시다. 이커머스의 특성상 Peak load를 테스트하기 위해서 아래와 같은 로드 테스트 시나리오를 준비해 봅니다.

```
이커머스 Prime Day를 예상하고 DynamoDB의 여러 테이블들에 부하를 줄 수 있도록  load tester를 Python으로 만들어 주고 그 파일을 ddb_load_tester.py로 만들어서 ~/ddb/에 넣어줘.
```
<img width="1676" height="757" alt="Screenshot 2025-07-18 at 5 39 16 AM" src="https://github.com/user-attachments/assets/c650fcca-e084-4d4f-8b18-7436d092b796" />


### Prime Day를 위한 Load Test하기
Load tester는 다음과 같이 완성이 되었습니다.!!!!
<img width="1255" height="487" alt="Screenshot 2025-07-18 at 5 40 13 AM" src="https://github.com/user-attachments/assets/a74e936a-1bc0-4cbb-ad53-ce1b19cfd997" />

```
 python3 /home/ec2-user/ddb/ddb_load_tester.py --table Orders --operation write --threads 100 duration 600
```

이제 테스트 해 봅시다. 테스트 시나리오는 주문 폭주 시뮬레이션이고 10분간 진행된다고 가정해 봅시다. 테스트는 10분 동안 진행이 됩니다. (잠시 커피 한잔하면서 지켜보시죠)
<img width="1277" height="128" alt="Screenshot 2025-07-18 at 5 42 29 AM" src="https://github.com/user-attachments/assets/acc5bd7c-1b84-4216-a7c7-e3ab52b9939f" />

결과는 아래와 같습니다. <br>
<img width="354" height="262" alt="2025-07-17 204202" src="https://github.com/user-attachments/assets/f2803688-6079-4a09-8e82-8fd543deb07a" />


```
CloudWatch의 Metric을 통해서 로드 테스트의 결과 보고서를 pdf 파일로 만들어서 ~/ddb-load-test-result/ 디렉토리에 생성해 줘. 그리고 터미널에도 요약 결과를 알려줘. 
```

<img width="1323" height="748" alt="Screenshot 2025-07-18 at 5 58 28 AM" src="https://github.com/user-attachments/assets/16983850-1b98-449c-a7a9-2a24e8f5b2eb" />

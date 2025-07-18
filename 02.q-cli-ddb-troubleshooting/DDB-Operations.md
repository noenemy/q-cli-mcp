# DynamoDB를 이용하여 Prime Day 이벤트 준비하기

DynamoDB 콘솔을 통해서 설정과 테이블들을 확인해 봅시다. 특히 Capacity mode가 On demand인 것이 확인되셨나요? <br>
<img width="1348" height="605" alt="Screenshot 2025-07-18 at 5 21 55 AM" src="https://github.com/user-attachments/assets/a53d8c61-48d9-4454-a1b3-6ff493d6fc23" />


### DynamoDB 설정 변경하기
평소 운영하는 DynamoDB가 큰 부하를 일으키지 않는다고 가정하고 아래와 같이 Provisioned Capacity를 설정해 봅니다.
'''
DynamoDB의 모든 테이블들을 Provisioned Capacity Mode로 바꿔줘. WCU 10, RCU 10으로 변경해 줘.
'''

관리 콘솔을 통해서 변경된 설정을 확인해 봅시다. On Demand에서 Provisioned로 바뀌었는지 확인해 봅시다.
<img width="1329" height="1065" alt="Screenshot 2025-07-18 at 5 22 58 AM" src="https://github.com/user-attachments/assets/9475aedf-874f-46bb-a255-842313ab23ae" />


### Prime Day 준비하기
이제 테이블에 로드테스트를 해 보겠습니다. Q Developer CLI가 만들어 준 파일을 이용하여 load 테스트를 해 봅시다. 이커머스의 특성상 Peak load를 테스트하기 위해서 아래와 같은 로드 테스트 시나리오를 준비해 봅니다.

‘’’
이커머스 Prime Day를 예상하고 DynamoDB의 여러 테이블들에 부하를 줄 수 있도록  load tester를 Python으로 만들어 주고 그 파일을 ddb_load_tester.py로 만들어서 ~/ddb/에 넣어줘.
‘’’
<img width="1676" height="757" alt="Screenshot 2025-07-18 at 5 39 16 AM" src="https://github.com/user-attachments/assets/c650fcca-e084-4d4f-8b18-7436d092b796" />

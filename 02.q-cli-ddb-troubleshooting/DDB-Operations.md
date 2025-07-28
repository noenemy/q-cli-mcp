# Prime Day 이벤트 준비를 위한 Load Test 로 대비하기

DynamoDB 콘솔을 통해서 설정과 테이블들을 확인해 봅시다. 특히 Capacity mode가 On demand인 것이 확인되셨나요? <br>
<img width="1348" height="605" alt="Screenshot 2025-07-18 at 5 21 55 AM" src="https://github.com/user-attachments/assets/a53d8c61-48d9-4454-a1b3-6ff493d6fc23" />

/home/ec2-user/.aws/amazonq/mcp.json 파일을 생성합니다. 그리고 본 랩의 폴더에 있는 mcp.json 파일의 내용을 입력합니다.
https://github.com/noenemy/q-cli-mcp/blob/main/02.q-cli-ddb-troubleshooting/mcp.json

<BR>

>[!NOTE]
>Python 3.9.xx 버전이 구성된 경우 아래 방법으로 3.11 이상 버전으로 업그레이드 설치 하고 pip, nodejs 버전을 확인하세요.
>이미 3.11 이상의 Python 버전 및 환경에 필요한 패키지들이 구성된 경우 아래 내용은 Skip 하셔도 좋습니다.
```SHELL
sudo yum install python3.11 -y
sudo yum install python3-pip -y
sudo ln -s /usr/bin/python3.11 /usr/bin/python

python --version
pip3 --version
node --version
npm --version
```
<BR>

>[!NOTE] AWS Credential은 Workshop Studio에서 확인하여 mcp.json 파일에 입력합니다. 
> 반드시 메모장 등에서 미리 파일을 준비하고, EC2 SSH 세션에서는 붙여넣기만 합니다.

```
vi /home/ec2-user/.aws/amazonq/mcp.json
# 붙여넣기
```

### MCP 설정에 필요한 패키지를 설치합니다.
```
q chat
```

```
uvx 패키지를 설치해 주세요
```

uvx 패키지 설치가 완료되었으면 q chat을 빠져나옵니다.
```
/quit
```

q chat을 다시 실행하고 mcp.json 에서 만든 MCP 서버가 추가된 것을 확인합니다.
```
q chat
```
```
/tools
```

### DynamoDB 설정 변경하기
평소 운영하는 DynamoDB가 큰 부하를 일으키지 않는다고 가정하고 아래와 같이 Provisioned Capacity를 설정해 봅니다.

```
DynamoDB의 모든 테이블들을 Provisioned Capacity Mode로 변경하고 WCU 2, RCU 2으로 설정해 주세요.
```

관리 콘솔을 통해서 변경된 설정을 확인해 봅시다. On Demand에서 Provisioned로 바뀌었는지 확인해 봅시다.
<img width="1329" height="1065" alt="Screenshot 2025-07-18 at 5 22 58 AM" src="https://github.com/user-attachments/assets/9475aedf-874f-46bb-a255-842313ab23ae" />


### Prime Day 준비하기
이제 테이블에 로드테스트를 해 보겠습니다. Q Developer CLI가 만들어 준 파일을 이용하여 load 테스트를 해 봅시다. 이커머스의 특성상 Peak load를 테스트하기 위해서 아래와 같은 로드 테스트 시나리오를 준비해 봅니다.

```
이커머스 Amazon Prime Day를 예상하고 DynamoDB의 여러 테이블들에 부하를 주려고 합니다.
1) 짧은 시간 대량의 상품 조회 요청과 
2) 많은 주문 데이터 생성 시도가 발생하며
3) 위의 두가지는 동시에 일어납니다.
Load Tester를 위한 스크립트를 Python 으로 만들어 주세요. 
파일명과 위치는 /home/ec2-user/ddb/ddb_load_tester.py 입니다.
```
<img width="1676" height="757" alt="Screenshot 2025-07-18 at 5 39 16 AM" src="https://github.com/user-attachments/assets/c650fcca-e084-4d4f-8b18-7436d092b796" />


### Prime Day를 위한 Load Test하기
Load tester가 완성되었다면, Q Developer CLI가 생성한 스크립트를 이용해서 부하테스트를 시작합니다. 
사용법을 꼼꼼히 읽어보고 시작합니다. 만약 부하가 충분하지 않을 것으로 생각된다면, 변경을 요청합니다.

부하를 충분히 주도록 테스트를 10분 동안 20개 쓰레드를 이용해서 진행합니다. 
(잠시 커피 한잔하면서 지켜봅니다.)
<img width="1255" height="487" alt="Screenshot 2025-07-18 at 5 40 13 AM" src="https://github.com/user-attachments/assets/a74e936a-1bc0-4cbb-ad53-ce1b19cfd997" />
<img width="1277" height="128" alt="Screenshot 2025-07-18 at 5 42 29 AM" src="https://github.com/user-attachments/assets/acc5bd7c-1b84-4216-a7c7-e3ab52b9939f" />

결과를 확인하고 옆에 동료와 비교해 봅니다.<br>
<img width="354" height="262" alt="2025-07-17 204202" src="https://github.com/user-attachments/assets/f2803688-6079-4a09-8e82-8fd543deb07a" />


부하가 충분히 발생했다면, 어떻게 대비하면 좋은지 Q Developer CLI에 질의합니다.
```
이러한 수준의 부하가 발생했을 때, 운영자가 취할 수 있는 방법을 요약 정리해주세요.
1) 사용자의 경험이 나빠지는 것을 사전에 방지하고 
2) 사전 준비를 함에도 불구하고 실제 이벤트에서 문제가 발생했을 때 조치방법. 실제 이벤트 시에는 부하가 가중될 수 있습니다.
```
요약 정리된 내용을 확인했다면 Support Case로 정확히 확인하도록 준비를 요청합니다.
```
위의 요약 정리된 내용이 정확한지 Support Case로 문의할 예정입니다.
진행한 부하테스트와 해결 방법을 문의하도록 제목과 내용을 300글자 이하로 작성해주세요. 
```

<img width="1323" height="748" alt="Screenshot 2025-07-18 at 5 58 28 AM" src="https://github.com/user-attachments/assets/16983850-1b98-449c-a7a9-2a24e8f5b2eb" />


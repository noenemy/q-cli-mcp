# CloudWatch MCP 서버를 이용하여 DDB throttling 해결하기

### CloudWatch Metric과 Logs를 이용하여 적절한 WCU, RCU를 확인하고 이를 설정하기
```
CloudWatch Metric과 Logs를 확인해서 DDB의 성능이 적절한 지 알려주고 Prime Day를 치를 때 필요한 적정한 WCU, RCU를 추천해 줘. 그리고 해당 WCU, RCU를 테이블 마다 적용해 줘.
```

Products, Orders 등 Table들의 WCU, RCU를 테스트 결과에 따라 업데이트합니다.<br>
<img width="1391" height="893" alt="Screenshot 2025-07-18 at 6 09 20 AM" src="https://github.com/user-attachments/assets/4fb6ee79-c292-4292-9104-a82408ac5023" /> <br>
<img width="1606" height="460" alt="Screenshot 2025-07-18 at 6 11 49 AM" src="https://github.com/user-attachments/assets/bad8b21a-071f-4ba7-8e6b-081a59cc086f" />

DynamoDB 콘솔에서 확인해 보시면 WCU, RCU가 변경된 것을 확인하실 수 있습니다.
￼<img width="1616" height="1024" alt="Screenshot 2025-07-18 at 6 13 13 AM" src="https://github.com/user-attachments/assets/58340ba8-5254-416c-8099-082a24655bf9" />



### PRIME Day 용량 증설로 인한 비용 비교해 보기
이제 Prime Day로 인해서 AWS 비용이 평소에 비해 얼마나 늘어날 지 예측해 보겠습니다.
```
MCP 서버 목록의 pricing 관련 MCP server를 이용해서 평소 사용하는 aws 비용과 Prime day가 3일 지속되었다고 가정하면 이로 인해 늘어난 비용을 비교 분석해서 알려줘.
```

결과는 아래와 같이 Prime Day 진행시 설정된 비용과 평소 비용을 알려주고 비교해 줍니다.
<img width="1334" height="791" alt="Screenshot 2025-07-18 at 6 17 26 AM" src="https://github.com/user-attachments/assets/b459b5c8-65d3-4e31-b872-e6004b40961d" />

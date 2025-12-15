# Lab 1. Kiro CLI(예전 이름 : Q CLI) 시작하기
## 개요 
Kiro CLI에 자연어로 지시해서 쉽고 빠르게 서비스를 만들 수 있습니다.
이 랩에서는 온라인 쇼핑 데이터를 관리하는 웹서비스를 만들어 봅니다. 데이터베이스는 DynamoDB로, 웹서비스는 EC2 Instance 에서 호스팅 합니다.

AWS에 대한 지식이 없더라도 자연어로 서비스를 구현 가능합니다.
 
**Let's go!**

* Kiro CLI와 자연어 채팅을 시작하려면 다음과 같이 실행합니다. 
```
kiro-cli
```

* 다음과 같이 입력해서 샘플 이커머스 고객 데이터를 만들어 봅니다.
```
10개의 샘플 이커머스 고객의 데이터를 만들어 주세요. 
```
출력이 어떤 모습인가요? 다른 동료와 출력 결과를 확인해 보세요.

* 이번에는 출력 결과를 명시적으로 간단하게 하기 위해 지시 내용에 다음과 같이 추가해 실행해 봅니다.
```
10개의 샘플 이커머스 고객의 데이터를 csv 형식으로 만들어 주세요. 
```
이전 출력과 어떻게 달라졌는지 확인해주세요. 여러분이 스스로 주문을 추가해보시기 바랍니다

* 출력 형식을 한국어로 지정하기 위해 다음과 같이 프롬프트에 입력해 봅니다.
```
모든 답변은 한국어로 작성해주시되, 기술 용어는 영어로 표기해주세요.
```

* Kiro CLI가 지시사항을 따르는지 다음과 같이 테스트 합니다.
```
이커머스 데이터를 관리하는 웹 애플리케이션을 만드는 가장 간단한 방법은 무엇인가요? 방법론만 설명해주세요
```
답변이 위의 지시사항 처럼 한국어로, 기술용어는 영어로 표기되었는지 확인합니다.

* Kiro CLI를 종료하기 위해서는 다음과 같이 입력합니다.  
참고) Kiro CLI 내에서 `/` 를 입력하면 다양한 커맨드를 확인할 수 있습니다.
```
/quit
```

* Kiro CLI로부터 일관된 응답을 받기 위해 Knowledge를 입력하여 응답 내용을 지시하겠습니다.
다음과 같이 markdown 파일로 입력합니다. 
```
cat > myknowledge.md << EOF
응답 시 지시사항을 명시적으로 참조해주세요.
AWS를 능숙하게 다루는 이커머스 서비스 개발자의 관점에서 답변해주세요.
서비스 구축은 최대한 간단하고 신속하게 진행해주세요.
모든 답변은 한국어로 작성해주시되, 기술 용어는 영어로 표기해주세요.
추측이 필요한 경우 반드시 이를 명시해주세요.
AWS 리소스 작업 시 us-east-1 리전을 사용해주세요.
/home/ec2-user/.kiro/settings/mcp.json 파일 수정 시 기존 내용을 보존해주세요.
Amazon, AWS 관련 MCP 서버 정보는 공식 GitHub 저장소인 https://github.com/awslabs/mcp/tree/main/src 링크만 참조해주세요.
Amazon, AWS 관련 MCP 서버 설치는 공식 링크만 사용해주세요.
DynamoDB의 describe_table의 ItemCount는 신뢰할 수 없으므로 사용을 제한해주세요.
EOF
```

* Kiro CLI에 지식 기능을 활성화 합니다.
```
kiro-cli settings chat.enableKnowledge true
```

* 이제 지시사항을 적용하기 위해 kiro-cli에 다시 접속합니다. 
```
kiro-cli
```

* 작성된 myknowledge.md 파일을 kiro-cli가 참조하도록 합니다.
```
/knowledge add --name e-commerce-developer --path myknowledge.md
```

* 위의 지식이 잘 추가 되었는지 확인합니다.
```
/knowledge show
```
현재 Agent에 myknowledge.md 파일이 지식으로 추가되어 있습니다. Kiro CLI 에서는 여러 개의 Agent을 가질 수 있고, 각 Agent마다 다른 지식을 맵핑할 수 있습니다. 자세한 내용은 [링크](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line-custom-agents.html)에서 확인 가능합니다.

* 이제 우리는 DynamoDB를 이용해서 데이터베이스를 만들 것입니다. Kiro CLI에 다음과 같이 지시합니다.
```
DynamoDB를 이용해서 이커머스 데이터베이스를 만들어주세요. 
테이블은 총 4개입니다. 1) Categories 2) Products 3) Customers 4) Orders
제품에는 에어콘과 난방기를 포함해주세요.
각 테이블마다 샘플 데이타는 테이블당 50개 이하로 만들어주세요.
```
<img width="1432" height="508" alt="Screenshot 2025-08-04 at 12 55 56 PM" src="https://github.com/user-attachments/assets/b944e4b2-ee52-4ad8-8e40-1fb87ed303f4" />


이렇게 DynamoDB에 대한 지식이 없는 누구나 쉽게 DynamoDB를 이용하여 샘플 데이타를 만들 수 있습니다.
컨텍스트 입력 전 후, Kiro CLI의 응답에 변화가 있었나요? 어떤 것인가요?

* DynamoDB에 테이블 4개가 모두 생성되었는지, 각 테이블마다 샘플 데이타가 모두 지시대로 생성되었는지 확인해 봅니다. 혹시 누락된 것이 있다면 Kiro CLI에 직접 지시해서 보완합니다.
```
DynamoDB에 테이블 4개가 모두 생성되었는지, 각 테이블마다 샘플 데이타가 있는지 확인해주세요. 
```
Kiro CLI가 지시받은 대로 작업을 했는지 확인합니다.
* 4개의 테이블과 샘플 데이타가 모두 생성되었는지 확인합니다.
* 샘플 데이타가 모두 생성되었는지 확인합니다.
AWS 콘솔에서 DynamoDB 콘솔로 이동하여 직접 확인할 수 있습니다.


* 위에 생성한 데이터베이스에 입출력과 보기 기능을 제공하는 웹서비스를 만들어 보겠습니다. 빠르게 시스템을 구축하기 위해 다음과 같이 지시사항을 입력합니다.

```
지금 있는 DynamoDB를 이용해서 이커머스 데이터베이스를 관리할 수 있는 웹서비스를 로컬에 만들어 주세요.
다음 조건들을 준수해주시기 바랍니다:
1. Python 내장 HTTP 서버(http.server)만 사용해주세요
2. 모든 UI는 단일 HTML 파일로 구현해주세요
3. JavaScript와 CSS는 HTML 파일 내에 포함해주세요
4. 모든 DynamoDB 테이블에 대해 CRUD 기능을 모두 구현해주세요
5. 모든 DynamoDB 테이블에 대해 간단한 검색 기능을 포함해주세요
6. Public IP로 접속 가능하도록 서버를 바인딩하세요
```

<BR>

>[!NOTE]
>웹서비스 구축 파일 생성에는 시간이 15분 이상 소요될 수 있습니다. 시간 절약을 위해 Kiro CLI 가 이미 구현한 웹서비스 파일을 활용해보세요.
>
>* [ecommerce_server.py](https://github.com/noenemy/q-cli-mcp/blob/main/01.q-cli-begin/ecommerce_server.py) 
>* [ecommerce.html](https://github.com/noenemy/q-cli-mcp/blob/main/01.q-cli-begin/ecommerce.html) 
<BR>

이제 Kiro CLI 는 웹 애플리케이션을 만들 것입니다.


* 완료가 되었습니까? 혹시 중간에 끊기거나 완료되지 않으면 `계속하세요` 라고 입력합니다.

* 완료가 되었다면 웹서비스의 포트를 확인합니다. (기본 포트는 8000)

<BR>

>[!NOTE]
> Workshop 환경은 8000번 포트가 Security Group에서 Inbound로 오픈되어 있지 않습니다.
> 접근을 위해서는 Inbound 규칙에 TCP 포트 8000과 sourceIP를 추가해주세요.
<BR>

완료가 되었다면 웹서비스를 실행합니다. 그리고 현재 접속한 EC2 Instance의 Public IP와 포트를 이용해서 URL로 접속합니다. `http://<publicIP>:port`
```
!python3 ecommerce_server.py
```

* 접속을 할 수 있습니까? 접속이 되지 않는다면 Kiro CLI에 질의합니다.
```
당신이 위에서 만들어 준 웹서비스로 접속이 되지 않는 원인을 점검해 주세요. 
```
* 웹서비스로 접속을 할 수 있게 되면 페이지를 둘러봅니다. 함께 랩을 진행한 웹페이지와 차이점을 비교해 봅니다.
* 웹페이지의 기능이 요구사항 대로 동작하는지 검증해 보세요.
* 시스템 구축 단계에서 요구사항이 변경된다고 가정합니다. 우리 시스템에는 `리뷰`라는 항목이 추가되어야 합니다. 데이터베이스와 웹서버 모두 변경이 필요합니다. Kiro CLI 에 요구사항을 입력합니다.
```
리뷰라는 항목이 추가되어야 합니다. 웹서비스와 다이나모 디비 모두 리뷰라는 항목이 추가되도록 변경해 주세요.
```
Kiro CLI가 데이터베이스와 웹서비스를 모두 변경하는지 검수합니다.

* 완료된 후에 웹사이트를 둘러보고 기능을 점검합니다.
* 변경하고 싶은 부분을 생각해 봅니다.
* 여러분 만의 요구사항을 자연어로 지시합니다.

[![Next](../03.mcp-server/images/next.png)](../02.q-cli-troubleshooting-mcp/01.PrimeDay_LoadTest.md)

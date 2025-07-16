# Lab.2-2. Streamable-HTTP MCP Server 와 MCP Client/MCP Host 만들어 보기


## 개요
중앙 집중식 MCP 서버를 구축하여 여러 사용자나 애플리케이션에서 공유할 수 있는 환경을 구성합니다. 이 모듈에서는 MCP(Model Context Protocol) 클라이언트 기반의 Streamlit MCP Host 챗봇을 구축하고, 이전 모듈에서 배포한 MCP 서버와의 연동 방법을 학습합니다. 이를 통해 LLM과 외부 도구 간의 상호작용을 위한 표준 프로토콜인 MCP의 클라이언트 측 구현을 실습합니다.


## MCP 서버 사용자 관점
- 편의성: AWS에서 MCP 서버를 운영하면 사용자는 복잡한 로컬 설치나 환경 설정 과정을 거칠 필요가 없습니다. 단순히 인터넷 연결만 있으면 데스크톱, 노트북, 태블릿 등 어떤 기기에서든 동일한 서비스에 접근할 수 있어 장소에 구애받지 않고 작업할 수 있습니다. 또한 서버 업데이트, 보안 패치, 백업 등의 기술적 관리 업무를 AWS가 자동으로 처리하기 때문에 사용자는 핵심 업무에만 집중할 수 있습니다.
- 보안: MCP 서버가 클라우드에서 실행되기 때문에 사용자의 개인 파일이나 시스템에 직접 접근할 수 없어 개인정보와 중요 데이터를 안전하게 보호할 수 있습니다. AWS의 엔터프라이즈급 보안 인프라와 전문적인 보안 관리 체계를 활용하여 개인이 직접 구축하기 어려운 수준의 보안을 제공받습니다. 만약 서비스에 문제가 발생하더라도 개인 시스템과 완전히 격리되어 있어 로컬 환경에는 전혀 영향을 주지 않습니다.
- 협업: 팀 전체가 동일한 AWS 기반 MCP 서버를 사용함으로써 일관된 작업 환경과 동일한 데이터 소스를 공유할 수 있어 협업 효율성이 크게 향상됩니다. 관리자가 중앙에서 모든 사용자의 권한과 설정을 통합 관리할 수 있으며, 새로운 기능이나 업데이트를 모든 팀원에게 동시에 배포하여 버전 불일치나 설정 차이로 인한 문제를 방지할 수 있습니다.


## MCP 서버 운영자 관점
- IAM 기반 세밀한 권한 제어: AWS IAM을 활용하면 MCP 서버에 필요한 최소한의 권한만을 정확히 부여할 수 있습니다. 서비스별, 리소스별로 세분화된 권한 설정이 가능하여 S3 특정 버킷에만 읽기 권한을 주거나 특정 DynamoDB 테이블에만 쓰기 권한을 부여하는 등 정밀한 접근 제어가 가능합니다.
- 네트워크 보안 강화: AWS VPC(Virtual Private Cloud)를 통해 MCP 서버를 완전히 격리된 네트워크 환경에서 운영할 수 있어 외부 위협으로부터 보호할 수 있습니다. Security Group과 Network ACL을 활용하여 필요한 트래픽만 허용하고 불필요한 접근을 차단할 수 있으며, 포트 단위까지 세밀한 네트워크 접근 제어가 가능합니다.


## 원격 MCP 서버를 구성할 때 주요 개념
MCP(Model Context Protocol)는 원격 통신을 위해 다양한 Transport 방식을 지원합니다. MCP 사양(2025-03-26)에 따르면 다음과 같은 Transport 방식이 있습니다.

**stdio**
- 실행 방식: 표준 입출력(stdin/stdout)을 통한 통신
- 사용 환경: 로컬 환경에서 주로 사용
- 특징: 클라이언트가 서버 프로세스를 직접 시작하고 관리
- 장점: 설정이 간단하고 추가 네트워크 구성이 필요 없음
- 사용 사례: 로컬 개발 환경, 단일 사용자 시나리오

**streamable HTTP**
- 실행 방식: HTTP POST와 GET을 통한 양방향 통신
- 특징:
  - 단일 엔드포인트에서 POST와 GET을 모두 지원
- Server-Sent Events (SSE)를 통한 스트리밍 지원
- 세션 관리 기능 제공
- 장점:
  - 확장성 있는 서버-클라이언트 통신
  - 세션 기반 상태 관리
  - 연결 재개 및 메시지 재전송 지원
  - 사용 사례: 클라우드 환경, 다중 사용자 시나리오

**HTTP/SSE(2024-11-05)**
- 실행 방식: HTTP를 통한 단방향 이벤트 스트림
- 엔드포인트: /sse
- 특징: 서버에서 클라이언트로의 지속적인 데이터 스트림 제공
- 장점: 표준 HTTP를 사용하여 방화벽 통과가 용이함
- 사용 사례: 중앙 집중식 서버, 여러 사용자가 공유하는 환경
- 호환성: 2025-03-26 버전과의 하위 호환성 유지

1. IDE 터미널에서 다음 명령어를 실행하여 Python 가상 환경을 생성합니다:
   ```
   uv venv --python 3.12
   source .venv/bin/activate
   ```

2. Remote weather mcp server 기동
   weather3.py

   ```
   uv run weather3.py
   ```
   
3. 다음 명령어를 실행하여 필요한 의존성 패키지를 설치합니다:
   ```
   cd client\
   uv pip install -r requirements.txt
   ```
   requriements.txt

## MCP 클라이언트 및 서버 구축하기
1. MCP Client 구현
client.py 파일에는 LangGraph ReAct 에이전트 기반의 MCPClient 클래스가 정의되어 있습니다. MCPClient 객체 초기화 시 비동기 작업 처리를 위한 AsyncExitStack과 LLM 호출을 위한 langchain-aws의 ChatBedrockConverse 인스턴스가 초기화되며, MCP 세션 및 ReAct 에이전트 변수는 초기 값으로 None이 설정됩니다.

client.py

클라이언트는 mcp 패키지의 sse_client를 통해 Streamable HTTP Transport 방식으로 MCP 서버와 연결하고, 클라이언트 세션을 초기화합니다. 이후 해당 세션에서 사용 가능한 도구(tools)를 로드하고, LangChain MCP Adapters의 load_mcp_tools 메서드를 통해 이 도구들을 LangChain 및 LangGraph와 호환되는 형식으로 변환합니다. 변환된 도구를 사용하여 LangGraph 기반의 ReAct 에이전트를 생성합니다.

터미널에서 다음 명령어를 실행하여 MCP Client를 테스트할 수 있습니다. 이때, module-02에서 배포한 MCP 서버의 URL 뒤에 /mcp/ 엔드포인트를 추가하여 명령행 인자로 전달합니다.

```
python app/streamlit-app/client.py <Your-MCP-Server-Endpoint-URL>/mcp/
```

What are the active weather alerts in Texas?와 같은 쿼리를 입력하여 응답을 확인합니다. 정상적인 응답이 반환되면 클라이언트 설정이 완료된 것입니다.


2. Streamlit 기반 MCP Host 애플리케이션 개발
app.py 파일에서는 client.py에 정의된 MCPClient 클래스를 활용하여 Streamlit 기반의 독립형(standalone) MCP Host 애플리케이션을 구현합니다.

app.py

Streamlit 애플리케이션에서는 사용할 LLM 모델 ID, AWS 리전, 그리고 MCP Server URL을 입력받아 MCPClient 객체를 생성하고 MCP Server와 연결합니다. 서버 연결이 성공하면 Streamlit의 session_state에 client 인스턴스와 사용 가능한 도구 정보를 저장합니다. 

MCP 서버와 성공적으로 연결된 후에는 사용 가능한 각 도구의 이름, 설명, 그리고 매개변수에 관한 상세 정보를 계층적 확장 컴포넌트(expander)를 통해 표시합니다.

MCP 서버와 연결이 완료되면 사용자 입력을 chat_input 컴포넌트를 통해 받아 MCPClient의 invoke_agent 메서드를 비동기적으로 호출합니다. 이때 MCPClient의 ReAct 에이전트는 사용자의 쿼리를 분석하여 적절한 도구를 선택적으로 활용하고, 도구 실행 결과를 바탕으로 최종 응답을 생성합니다.


3. 애플리케이션 확인하기

IDE 터미널에서 다음 명령어를 실행하여 Streamlit 애플리케이션을 실행합니다.

```
streamlit run app/streamlit-app/app.py
```
[streamlit](https://github.com/noenemy/q-cli-mcp/blob/main/02.mcp-server/images/streamlit-app.png) 


http://<Your-MCP-Server-Endpoint-URL>/app로 접속하여 배포된 streamlit 애플리케이션을 확인합니다. 이때 MCP Server URL에는 http://<Your-MCP-Server-Endpoint-URL>/mcp/로 기입하고 Connect 버튼으로 연결합니다.

요약

이 모듈에서는 MCP(Model Context Protocol) 라이브러리를 활용하여 MCP Client를 구현하고, 이전 모듈에서 배포한 MCP Server와 연결했습니다. 또한 LangChain MCP Adapters를 통해 MCP Server에서 제공하는 도구들을 LangChain 호환 형식으로 변환하여 LangGraph 기반 ReAct 에이전트를 구성하는 방법을 학습했습니다. 이렇게 구현된 에이전트를 Streamlit 웹 프레임워크와 통합하여 독립형 MCP Host 애플리케이션을 개발함으로써, MCP Host 애플리케이션의 기본 작동 원리를 실제로 구현하고 이해할 수 있습니다.


## 참고 자료
- [Model Context Protocol 공식 문서](https://modelcontextprotocol.io/introduction)
- [langchain-aws 라이브러리 문서](https://python.langchain.com/docs/integrations/providers/aws/) 
- [LangChain MCP Adapters 리포지토리](https://github.com/langchain-ai/langchain-mcp-adapters)
- [LangGraph 프레임워크 공식 문서](https://langchain-ai.github.io/langgraph/)

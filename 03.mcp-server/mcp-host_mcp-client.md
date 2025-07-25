# Lab.3-2. Streamable-HTTP MCP Server & MCP Client/MCP Host 구축


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
<BR>

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
<BR>

**HTTP/SSE(2024-11-05)**
- 실행 방식: HTTP를 통한 단방향 이벤트 스트림
- 엔드포인트: /sse
- 특징: 서버에서 클라이언트로의 지속적인 데이터 스트림 제공
- 장점: 표준 HTTP를 사용하여 방화벽 통과가 용이함
- 사용 사례: 중앙 집중식 서버, 여러 사용자가 공유하는 환경
- 호환성: 2025-03-26 버전과의 하위 호환성 유지
<BR>

### 1. IDE 터미널에서 다음 명령어를 실행하여 Python 가상 환경을 생성 및 실행합니다:
>가상환경 적용은 이미 적용되어 있다면 SKIP 하셔도 좋습니다. 
>가상환경 적용시 (weather) [ec2-user ... ] 와 같이 맨 앞에 프로젝트 명이 보여지게 됩니다.
>사전에 Bedrock Model Access 에서 Nova-Lite 버전에 대한 model access를 확인해주세요
   ```
   uv venv --python 3.11
   source .venv/bin/activate
   ```
<BR>

### 2. Remote weather mcp server 작성 및 기동<BR>

```bash
cd ~/weather
curl https://raw.githubusercontent.com/noenemy/q-cli-mcp/main/03.mcp-server/weather3.py --output weather3.py
```

**# 코드 : weather3.py** [weather3.py](weather3.py)
```python
"""Weather tools for MCP Streamable HTTP server using NWS API."""

import argparse
from typing import Any

import httpx
import uvicorn

from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server for Weather tools.
# If json_response is set to True, the server will use JSON responses instead of SSE streams
# If stateless_http is set to True, the server uses true stateless mode (new transport per request)
mcp = FastMCP(name="weather", json_response=False, stateless_http=False)

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"


async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {"User-Agent": USER_AGENT, "Accept": "application/geo+json"}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None


def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No specific instructions provided')}
"""


@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)


@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    # First get the forecast grid endpoint
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch forecast data for this location."

    # Get the forecast URL from the points response
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch detailed forecast."

    # Format the periods into a readable forecast
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # Only show next 5 periods
        forecast = f"""
{period['name']}:
Temperature: {period['temperature']}°{period['temperatureUnit']}
Wind: {period['windSpeed']} {period['windDirection']}
Forecast: {period['detailedForecast']}
"""
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run MCP Streamable HTTP based server")
    parser.add_argument("--port", type=int, default=8123, help="Localhost port to listen on")
    args = parser.parse_args()

    # Start the server with Streamable HTTP transport
    uvicorn.run(mcp.streamable_http_app, host="localhost", port=args.port)
```
>[!TIP]
> MCP 서버가 Streamable HTTP 전송방식을 사용하여 원격의 단일 엔드포인트에서 양방향 통신을 제공하며, Uvicorn을 통해 8123 포트에서 실행되어 더 안정적이고 효율적인 날씨 정보 서비스를 제공합니다. (테스트에서는 편의를 위해 같은 instance의 localhost로 구성).
<BR>
- Uvicorn은 비동기(ASGI) Python 웹서버로 FastAPI에 최적화. 참고) Python용 WebServer 에는 Gunicorn, uWSGI가 많이 사용되었었고
- Gunicorn은 안정적인 프로덕션용 WSGI 서버, uWSGI는 복잡한 설정이 가능한 전통적인 WSGI 서버입니다.
- Django/Flask는 주로 WSGI(Gunicorn, uWSGI)와 함께 사용되지만, Django 3.0+ 부터는 ASGI를 지원하므로 Uvicorn과도 사용 가능합니다.
* WSGI: Web Server Gateway Interface (웹 서버 게이트웨이 인터페이스, 동기식)
* ASGI: Asynchronous Server Gateway Interface (비동기 서버 게이트웨이 인터페이스)



<BR>

### 3. Weather MCP server를 기동시킵니다.
```
cd ~/weather
uv run weather3.py
```
   ![streamlit](https://github.com/noenemy/q-cli-mcp/blob/main/03.mcp-server/images/mcp_07.png)
> [!TIP]
> 기동된 weather3.py의 서비스 URL과 포트를 확인 : ex) http://localhost:8123
> [!CAUTION]
> 도전과제 : 8123포트에 대한 Secuirty Group은 구성되어 있지 않습니다. 콘솔, CLI, Q CLI를 통해서 8123포트를 접근할수 있게 수정해보세요
<BR>

### 4. 새로운 터미널에서 다음 명령어를 실행하여 client에 필요한 streamlit, langchain등의 의존성 패키지를 설치합니다:
> client 폴더는 client 코드 구분을 위해 만든 폴더로 기본 생성되어 있지 않으므로, client폴더가 없는 경우
> weather 폴더 및에 client 폴더 생성이 필요합니다.

## MCP 클라이언트 및 Host 구축하기
### 1. MCP Client 구현
client.py 파일에는 LangGraph ReAct 에이전트 기반의 MCPClient 클래스가 정의되어 있습니다. MCPClient 객체 초기화 시 비동기 작업 처리를 위한 AsyncExitStack과 LLM 호출을 위한 langchain-aws의 ChatBedrockConverse 인스턴스가 초기화되며, MCP 세션 및 ReAct 에이전트 변수는 초기 값으로 None이 설정됩니다.

```bash
cd ~/weather
source .venv/bin/activate
cd client          # 폴더 이동
curl https://raw.githubusercontent.com/noenemy/q-cli-mcp/main/03.mcp-server/client/requirements.txt --output requirements.txt
curl https://raw.githubusercontent.com/noenemy/q-cli-mcp/main/03.mcp-server/client/client.py --output client.py
```

**# 설정 : requirements.txt**
```
# 파이썬 의존성 패키지 설치를 위해 requirements.txt 작성
cat > requirements.txt << EOF 
streamlit>=1.30.0
langchain-mcp-adapters>=0.0.1
langchain-aws>=0.1.0
langgraph>=0.1.5
mcp>=0.1.0
boto3>=1.34.0
nest-asyncio>=1.6.0
EOF

# 의존썽 패키지 설치
uv pip install -r requirements.txt
```
[client/requirements.txt](client/requirements.txt)

<BR><BR>


**# 코드 : client/client.py** : [client/client.py](client/client.py)
```python
import asyncio
import sys
from contextlib import AsyncExitStack
from typing import Any, List

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_aws import ChatBedrockConverse
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
import logging

logging.basicConfig(level=logging.WARNING)
logging.getLogger('botocore').setLevel(logging.WARNING)
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('mcp').setLevel(logging.WARNING)
logging.getLogger('langchain_aws').setLevel(logging.WARNING)

class MCPClient:
    def __init__(self):
        self.exit_stack = AsyncExitStack()
        self.tools = []
        self.session = None

    async def connect_to_server(self, server_url: str):
        if not server_url.endswith('/'):
            server_url = f"{server_url}/"

        self.read, self.write, _ = await self.exit_stack.enter_async_context(
            streamablehttp_client(server_url)
        )
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.read, self.write)
        )
            
        session = await self.session.initialize()
        self.tools = await load_mcp_tools(self.session)
        self.session = session
    
    async def cleanup(self):
        """Cleanup resources"""
        if self.exit_stack:
            await self.exit_stack.aclose()

class MCPReActAgent:
    def __init__(self, model_id: str = "amazon.nova-lite-v1:0", region_name: str = "us-east-1"):
        self.model_id = model_id
        self.region_name = region_name
        self.bedrock = ChatBedrockConverse(
            model_id=self.model_id,
            region_name=self.region_name
        )
        self.mcp_client = MCPClient()

    async def connect_mcp_server(self, server_url: str):
        """Connect to MCP server and retrieve available tools"""
        
        try:

            await self.mcp_client.connect_to_server(server_url)

            print("MCP Server Connected!")
            print("[Available tools]")
            for tool in self.mcp_client.tools:
                print(f"- {tool.name}: {tool.description}")
            
            self.agent = create_react_agent(
                model=self.bedrock,
                tools=self.mcp_client.tools,
                checkpointer=MemorySaver()
            )
            
        except Exception as e:
            raise Exception(f"Failed to connect to MCP server: {e}")
    
    async def invoke_agent(self, query: str, thread_id: int = 42) -> List[Any]:
        """Execute query using the MCP agent"""
        if not self.agent:
            raise RuntimeError("Client not connected to server")
        
        response = await self.agent.ainvoke(
            {"messages": query},
            config={"configurable": {"thread_id": thread_id}}
        )
        return response["messages"]

    async def stream_agent(self, query: str, thread_id: int = 42):
        async for chunk in self.agent.astream(
            {"messages": query},
            config={"configurable": {"thread_id": thread_id}},
            stream_mode="updates"
        ):
            for value in chunk.values():
                value["messages"][-1].pretty_print()
    
    async def chat_loop(self):
        """Interactive chat loop for command-line usage"""
        print("MCP Client Started! Type your queries or 'quit' to exit.")
        
        while True:
            try:
                query = input("\nQuery: ").strip()
                if query.lower() == 'quit':
                    break                
                await self.stream_agent(query)

            except Exception as e:
                print(f"Error: {e}")

    async def cleanup(self):
        """Cleanup resources"""
        print("clean up")
        await self.mcp_client.cleanup()

async def main():
    """Command-line interface"""
    if len(sys.argv) < 2:
        print("Usage: python client.py <mcp_server_url>")
        sys.exit(1)
    
    agent = MCPReActAgent()
    
    try:
        server_url = sys.argv[1]
        await agent.connect_mcp_server(server_url)
        await agent.chat_loop()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
```
>[!TIP]
>이 코드는 MCP(Model Context Protocol) 클라이언트를 구현하여 Amazon Bedrock의 Nova-Lite-V1 모델과 LangChain 프레임워크를 통합한 대화형 AI 에이전트를 구현하고 있으며, Streamable HTTP를 통해 MCP 서버에 연결하여 사용 가능한 도구들을 불러오고, 사용자의 질의에 대해 ReAct 패턴을 기반으로 응답을 생성하는 대화형 인터페이스를 제공합니다.

mcp 패키지의 streamable_client를 통해 Streamable HTTP Transport 방식으로 MCP 서버와 연결하고, 세션을 초기화합니다. 이후 해당 세션에서 사용 가능한 도구(tools)를 로드하고 LangGraph 기반의 ReAct 에이전트를 이용해서 프롬프트를 서버로 전달합니다.

터미널에서 다음 명령어를 실행하여 MCP Client를 테스트할 수 있습니다. 이때, weather3 MCP 서버의 URL 뒤에 /mcp/ 엔드포인트를 추가하여 명령행 인자로 전달합니다.

```
python client.py <Your-MCP-Server-Endpoint-URL>/mcp/

#예시
python client.py http://localhost:8123/mcp/
```
![mcp-server](https://github.com/noenemy/q-cli-mcp/blob/main/03.mcp-server/images/mcp_08.png) 
* mcp server를 기동할때 확인하였던 mcp server URL ( http://localhost:8123/mcp/ ) 를 호출합니다.

아래와 같은 쿼리를 입력하여 응답을 확인합니다. 정상적인 응답이 반환되면 클라이언트 설정이 완료된 것입니다.
>What are the active weather alerts in Texas?
<BR>

> [!TIP]
> 그림에서 보는 것처럼 질문에 대해 텍사스, 루이지애나, 아칸소 일부 지역에서 최고 108도의 폭염주의보와 함께 텍사스 루프킨 인근 안젤리나 강 유역의 홍수 경보가 발령되었다는 것을 weather mcp 를 통해 확인할수  있습니다.
![mcp-server](https://github.com/noenemy/q-cli-mcp/blob/main/03.mcp-server/images/mcp_09.png) 
<BR>

### 2. Streamlit 기반 MCP Host 애플리케이션 개발
app.py 파일에서는 client.py에 정의된 MCPClient 클래스를 활용하여 Streamlit 기반의 독립형(standalone) MCP Host 애플리케이션을 구현합니다.

```bash
cd ~/weather/client
curl https://raw.githubusercontent.com/noenemy/q-cli-mcp/main/03.mcp-server/client/app.py --output app.py
```

**#코드 : client\app.py** : [client\app.py](client\app.py)

```python
import streamlit as st
import asyncio
from client import MCPReActAgent
import nest_asyncio

nest_asyncio.apply()

if "loop" not in st.session_state:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    print(loop)
    st.session_state.loop = loop

if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent" not in st.session_state:
    st.session_state.agent = None
    st.session_state.connected = False
    st.session_state.tools = None

st.set_page_config(page_title="Streamlit MCP Host", layout="wide")

# side bar
with st.sidebar:
    st.header("Server Setting")
    
    model_id = st.text_input("Model ID", value="amazon.nova-lite-v1:0")
    region_name = st.text_input("AWS Region", value="us-east-1")
    server_url = st.text_input("MCP Server URL", value="")

    if st.button("Connect"):
        if not st.session_state.connected:
            with st.spinner("Connecting to server..."):
                try:

                    agent = MCPReActAgent(model_id=model_id, region_name=region_name)

                    st.session_state.loop.run_until_complete(agent.connect_mcp_server(server_url))

                    st.session_state.agent = agent
                    st.session_state.connected = True
                    st.session_state.tools = agent.mcp_client.tools
                    st.success(f"Successfully connected to server: '{server_url}'")
                    
                except Exception as e:
                    st.error(f"Connection failed: {str(e)}")
        else:
            st.info("Already connected to server")

    st.subheader("Available tools")
    if st.session_state.connected:
        for tool in st.session_state.agent.mcp_client.tools:
            with st.expander(f"{tool.name}"):
                st.markdown(f"**description:** {tool.description}")
                
                st.markdown("**arguments:**")
                params = tool.args_schema.get('properties', {})
                required = tool.args_schema.get('required', [])
                
                if params:
                    param_data = []
                    for param_name, param_info in params.items():
                        param_type = param_info.get('type', '')
                        is_required = "✓" if param_name in required else ""
                        param_data.append([param_name, param_type, is_required])
                    
                    st.table({
                        "parameter": [p[0] for p in param_data],
                        "type": [p[1] for p in param_data],
                        "required": [p[2] for p in param_data]
                        })
    else:
        st.warning("Please connected to server")

# chat
st.title("Streamlit MCP Host")
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Input message..."):
    if not st.session_state.connected:
        st.error("You have to connect server first.")
    else:
        with st.chat_message("user"):
            st.write(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):

            response_placeholder = st.empty()
            try:
            
                messages = st.session_state.loop.run_until_complete(st.session_state.agent.invoke_agent(prompt))
                
                with st.expander('full messages'):
                    st.markdown(messages)

                final_message = messages[-1].content.split("</thinking>")[-1]
                response_placeholder.markdown(final_message)
                                    
                st.session_state.messages.append({"role": "assistant", "content": final_message})
                
            except Exception as e:
                st.error(f"Response failed: {str(e)}")

```

>[!TIP]
>이 코드는 Streamlit을 사용하여 MCP(Model Context Protocol) 호스트 웹 애플리케이션을 구현하고 있습니다. 사용자는 사이드바에서 Amazon Bedrock 모델 설정과 MCP 서버 연결을 구성할 수 있으며, 연결 후에는 사용 가능한 도구들의 상세 정보를 확인할 수 있습니다. 메인 화면에서는 대화형 인터페이스를 통해 사용자의 입력을 받아 MCP 에이전트로 처리하고, 응답을 스트리밍 방식으로 표시합니다. 이 애플리케이션은 비동기 처리를 위해 asyncio를 사용하며, 세션 상태를 관리하여 연결 상태와 대화 기록을 유지합니다.

Streamlit 애플리케이션에서는 사용할 LLM 모델 ID, AWS 리전, 그리고 MCP Server URL을 입력받아 MCPClient 객체를 생성하고 MCP Server와 연결합니다. 서버 연결이 성공하면 Streamlit의 session_state에 client 인스턴스와 사용 가능한 도구 정보를 저장합니다. 

MCP 서버와 성공적으로 연결된 후에는 사용 가능한 각 도구의 이름, 설명, 그리고 매개변수에 관한 상세 정보를 계층적 확장 컴포넌트(expander)를 통해 표시합니다.

MCP 서버와 연결이 완료되면 사용자 입력을 chat_input 컴포넌트를 통해 받아 MCPClient의 invoke_agent 메서드를 비동기적으로 호출합니다. 이때 MCPClient의 ReAct 에이전트는 사용자의 쿼리를 분석하여 적절한 도구를 선택적으로 활용하고, 도구 실행 결과를 바탕으로 최종 응답을 생성합니다.
<BR>

### 3.애플리케이션 확인하기

IDE 터미널에서 다음 명령어를 실행하여 Streamlit 애플리케이션을 실행합니다.

```
streamlit run app.py
```
![mcp-server](https://github.com/noenemy/q-cli-mcp/blob/main/03.mcp-server/images/mcp_10.png) 

http://3.210.201.53:8501/ 로 접속하여 배포된 streamlit 애플리케이션을 확인합니다. 이때 MCP Server URL에는 http://localhost:8123/mcp/ 로 기입하고 Connect 버튼으로 연결합니다.
![mcp-server](https://github.com/noenemy/q-cli-mcp/blob/main/03.mcp-server/images/mcp_11.png) 
<BR><BR>
쿼리를 입력해서 확인합니다.
> 텍사스의 날씨 경보를 한글로 알려주세요
<BR>

### 요약

이 모듈에서는 MCP(Model Context Protocol) 라이브러리를 활용하여 MCP Client를 구현하고, 이전 모듈에서 배포한 MCP Server와 연결했습니다. 또한 LangChain MCP Adapters를 통해 MCP Server에서 제공하는 도구들을 LangChain 호환 형식으로 변환하여 LangGraph 기반 ReAct 에이전트를 구성하는 방법을 학습했습니다. 이렇게 구현된 에이전트를 Streamlit 웹 프레임워크와 통합하여 독립형 MCP Host 애플리케이션을 개발함으로써, MCP Host 애플리케이션의 기본 작동 원리를 실제로 구현하고 이해할 수 있습니다.

<BR><BR>
## 참고 자료
- [Model Context Protocol 공식 문서](https://modelcontextprotocol.io/introduction)
- [langchain-aws 라이브러리 문서](https://python.langchain.com/docs/integrations/providers/aws/) 
- [LangChain MCP Adapters 리포지토리](https://github.com/langchain-ai/langchain-mcp-adapters)
- [LangGraph 프레임워크 공식 문서](https://langchain-ai.github.io/langgraph/)

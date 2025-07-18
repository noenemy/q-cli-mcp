<!-- Written by @skjun , 2025-07-13 -->
# Lab 2. Local환경에서 Weather API MCP Server를 만들어 보기

## 1. Python 가상 환경을 설정하고 필요한 패키지를 설치합니다.
### System requirements
> Python 3.10 or higher installed.
<BR>

### Set up your environment
**Windows**
```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
<BR>

**Mac/Linux**
```
curl -LsSf https://astral.sh/uv/install.sh | sh
uvx --version
```
<BR>

**가상환경 생성(프로젝트 구성)**
```
uv init weather  # weather 프로젝트를 앞 Lab에서 구성하였다면 skip
cd weather
```
<BR><BR>

**가상환경 적용 및 필수 패키지 설치**
```
uv venv
source .venv/bin/activate
uv add "mcp[cli]" httpx request
```
<BR><BR>

## 2.weather.py 작성
이론 시간에 filesystem mcp server 를 mcp.json 에 등록하여 file_read 등의 MCP Tool을 사용하는 것을 보셨습니다.
이번엔 공식 페이지 quick start 에 있는 mcp server를 직접 만들고 등록해서 사용하는 것을 보여 드리겠습니다.

weather.py 파일을 열어 코드를 확인합니다. 
[weather.py](https://github.com/noenemy/q-cli-mcp/blob/main/03.mcp-server/weather.py)

```python
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("weather")

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"



async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
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
    # Initialize and run the server
    mcp.run(transport='stdio')
```

> [!TIP]
>1. MCP(Model Context Protocol) 서버는 AI 모델이 데이터와 도구에 안전하게 접근할 수 있게 해주는 프로그램으로, FastMCP를 통해 쉽게 구현할 수 있습니다.
>2. FastMCP 라이브러리는 복잡한 프로토콜 처리, 스키마 생성, 유효성 검사 등을 자동화하여 개발자가 핵심 기능 구현에만 집중할 수 있게 해줍니다.
>3. 서버는 기본적으로 stdio(Standard Input/Output) 전송 방식을 사용하며, 이는 JSON-RPC 메시지를 표준 입출력 스트림을 통해 주고받는 방식으로 로컬 환경에서 Claude Desktop 같은 클라이언트와의 통신에 이상적입니다.
<BR><BR>  

> [!NOTE]
> 이 스크립트는 미국 국립 기상 서비스 API를 통해 날씨 정보를 가져오는 MCP 서버를 구현합니다. 사용자의 프롬프트로부터 날씨를 받을 때, get_alerts, get_forecast를 활용하여 위도와 경보를 파악하고 기상 정보를 가져오도록 동작합니다.

- Amazon Q Developer CLI는 두 가지 수준의 MCP 구성을 지원합니다.
  - 글로벌 구성: ~/.aws/amazonq/mcp.json - 모든 워크스페이스에 적용됩니다.
  - 워크스페이스 구성: .amazonq/mcp.json - 현재 워크스페이스에만 해당됩니다.
<BR>

**참조**  
- https://github.com/noenemy/q-cli-mcp/blob/main/03.mcp-server/mcp.json

```json
cat > ~/.aws/amazonq/mcp.json << EOF
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": [
        "--directory",
        "/home/ec2-user/weather",
        "run",
        "weather.py"
      ]
    }
  }
}
EOF
```
<BR><BR>

## 3.MCP 서버가 정상적으로 등록됐는지 Amazon Q Developer CLI를 다시 실행하고 /tools 명령어로 확인합니다.
![mcp](https://github.com/noenemy/q-cli-mcp/blob/main/03.mcp-server/images/mcp_00.png)
코드 작성과 실행 그리고 mcp.json이 정상인 경우 Amazon Q Dev. CLI를 재실행시 Loaded 메시지를 보게 된다.

![mcp](https://github.com/noenemy/q-cli-mcp/blob/main/03.mcp-server/images/mcp_01.png)
<BR><BR>
MCP tools에 기상정보와 기상경보에 대한 tool이 포함되어 있는지를 확인해 본다.

<BR><BR>  
## 4.Amazon Q Developer CLI 에서 프롬프트를 통해 MCP Tools 호출
아래와 같은 프롬프트 질문을 하나씩 입력하여 응답을 확인합니다. 
> Pormpt : 시카고의 현재 날씨를 알려주세요  
![mcp](https://github.com/noenemy/q-cli-mcp/blob/main/03.mcp-server/images/mcp_02.png)  
![mcp](https://github.com/noenemy/q-cli-mcp/blob/main/03.mcp-server/images/mcp_03.png)  

<BR>  
 
> Prompt : 텍사스의 날씨 경보를 알려주세요  
![mcp](https://github.com/noenemy/q-cli-mcp/blob/main/03.mcp-server/images/mcp_04.png)  
![mcp](https://github.com/noenemy/q-cli-mcp/blob/main/03.mcp-server/images/mcp_05.png)  

> Allow this action? Use 't' to trust (always allow) this tool for the session. [y/n/t]: 입력창이 나타나면, t를 입력합니다.

<BR><BR><BR>
## 요약 :shipit: :shipit: 
> [!NOTE]
> Summary
1. modelcontext.io quickstart 의 서버 개발
2. weather.py 작성
3. uv, node 설치
4. uv run weather
5. mcp.json 작성
6. q dev cli 에서 사용 및 확인
7. 프롬프트1
8. 프롬프트2

[![Next](images/next.png)](mcp-host_mcp-client.md)

### 참조
- Model Context IO : https://modelcontextprotocol.io/quickstart/server#python

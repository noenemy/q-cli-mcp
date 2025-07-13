# Lab3-1. Weather MCP Server

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
```
<BR>

**환경구성(프로젝트 구성)**
```
uv init weather  # weather 프로젝트를 앞 Lab에서 구성하였다면 skip
cd weather
```
<BR><BR>

## 2.Python 가상 환경을 설정하고 필요한 패키지를 설치합니다.
```
uv venv
source .venv/bin/activate
uv add "mcp[cli]" httpx
```
<BR><BR>

## 3.weather.py 파일을 열어 코드를 확인합니다.
weather.py 파일을 열어 코드를 확인합니다. [weather.py](https://github.com/noenemy/q-cli-mcp/blob/main/02.mcp-server/weather.py)
> cat weather.py
> [!INFO]
> 이 스크립트는 미국 국립 기상 서비스 API를 통해 날씨 정보를 가져오는 MCP 서버를 구현합니다. 사용자의 프롬프트로부터 날씨를 받을 때, get_alerts, get_forecast를 활용하여 위도와 경보를 파악하고 기상 정보를 가져오도록 동작합니다.

- Amazon Q Developer CLI는 두 가지 수준의 MCP 구성을 지원합니다.
  - 글로벌 구성: ~/.aws/amazonq/mcp.json - 모든 워크스페이스에 적용됩니다.
  - 워크스페이스 구성: .amazonq/mcp.json - 현재 워크스페이스에만 해당됩니다.
<BR>

**참조**  
- https://github.com/noenemy/q-cli-mcp/blob/main/02.mcp-server/mcp.json

```
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

## 4.MCP 서버가 정상적으로 등록됐는지 Amazon Q Developer CLI를 다시 실행하고 /tools 명령어로 확인합니다.
![mcp](https://github.com/noenemy/q-cli-mcp/blob/main/02.mcp-server/images/mcp_00.png)
코드 작성과 실행 그리고 mcp.json이 정상인 경우 Amazon Q Dev. CLI를 재실행시 Loaded 메시지를 보게 된다.

![mcp](https://github.com/noenemy/q-cli-mcp/blob/main/02.mcp-server/images/mcp_01.png)
<BR><BR>
MCP tools에 기상정보와 기상경보에 대한 tool이 포함되어 있는지를 확인해 본다.

## 5.Amazon Q Developer CLI를 재실행
아래와 같은 프롬프트 질문을 하나씩 입력하여 응답을 확인합니다. 
> Pormpt : 시카고의 현재 날씨를 알려주세요
![mcp](https://github.com/noenemy/q-cli-mcp/blob/main/02.mcp-server/images/mcp_02.png)  
![mcp](https://github.com/noenemy/q-cli-mcp/blob/main/02.mcp-server/images/mcp_03.png)  

<BR>  
> Prompt : 텍사의 날씨 경보를 알려주세요
![mcp](https://github.com/noenemy/q-cli-mcp/blob/main/02.mcp-server/images/mcp_04.png)  
![mcp](https://github.com/noenemy/q-cli-mcp/blob/main/02.mcp-server/images/mcp_05.png)  

> Allow this action? Use 't' to trust (always allow) this tool for the session. [y/n/t]: 입력창이 나타나면, t를 입력합니다.

<BR><BR><BR>
## 수정 중 :shipit: :shipit: 
> [!CAUTION]
> 이미지 및 워크샵 내용 작성 중입니다

목차
1. modelcontext.io quickstart 의 서버 개발
2. weather.py 작성
3. uv, node 설치
4. uv run weather
5. mcp.json 작성
6. q dev cli 에서 사용 및 확인
7. 프롬프트1
8. 프롬프트2
   
### 참조
- Model Context IO : https://modelcontextprotocol.io/quickstart/server#python

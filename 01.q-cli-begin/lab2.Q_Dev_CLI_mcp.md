# Lab 2. Amazon Q Developer CLI 로 MCP 활용하기
## 개요
Amazon Q Dev CLI 는 다양한 MCP 서버와 연동하여 확장 가능한 AI Agent 어플리케이션 입니다. 
이번 Lab 에서는 AWS 에서 제공하는 다양한 MCP 서버를 로딩하여 자연어를 통해 현재 환경을 분석하고 제안할 수 있는 예제를 수행해 보도록 하겠습니다. 

### MCP 설정에 필요한 패키지를 설치합니다.
아래와 같은 프롬프트를 입력하여 mcp 서버 실행에 필요한 환경을 구성합니다. 
```
python 3.10 이상 버전과 uvx 패키지를 설치해 주세요.
그리고 q chat에서 python 3.10 이상을 사용할 수 있도록 PATH 를 설정해주세요
```

### mcp 설정 파일을 생성합니다.
아래의 command 로 q dev cli 를 위한 mcp 설정 파일을 생성합니다.

```
touch /home/ec2-user/.aws/amazonq/mcp.json
```

파일을 생성 후 아래의 명령어로 mcp.json 파일을 편집합니다.
```
vi /home/ec2-user/.aws/amazonq/mcp.json
```

아래의 mcp 서버 설정을 copy & paste 합니다. 
```
{
  "mcpServers": {
    "awslabs.aws-pricing-mcp-server": {
      "command": "uvx",
      "args": [
         "awslabs.aws-pricing-mcp-server@latest"
      ],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR",
        "AWS_PROFILE": "default",
        "AWS_REGION": "ap-northeast-2"
      },
      "disabled": false,
      "autoApprove": []
    },
    "awslabs.cloudtrail-mcp-server": {
      "autoApprove": [],
      "disabled": false,
      "command": "uvx",
      "args": [
        "awslabs.cloudtrail-mcp-server@latest"
      ],
      "env": {
        "AWS_PROFILE": "default",
        "FASTMCP_LOG_LEVEL": "ERROR",
	      "AWS_REGION": "ap-northeast-2"
      },
      "transportType": "stdio"
    },
    "awslabs.cloudwatch-mcp-server": {
      "autoApprove": [],
      "disabled": false,
      "command": "uvx",
      "args": [
        "awslabs.cloudwatch-mcp-server@latest"
      ],
      "env": {
        "AWS_PROFILE": "default",
	      "AWS_REGION": "ap-northeast-2",
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "transportType": "stdio"
    },
    "awslabs.aws-diagram-mcp-server": {
      "command": "uvx",
      "args": ["awslabs.aws-diagram-mcp-server"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "autoApprove": [],
      "disabled": false
    }
  }
}
```
mcp 서버가 다시 로딩 되도록 하기 위해 q cli 를 종료 후 다시 시작합니다.

```
# 종료
/quit
```

```
# Q CLI 실행
q chat
```

## AWS MCP 서버 테스트
Q Dev CLI 에 로딩된 MCP 서버는 아래와 같습니다. 각 서버에 적절한 질의를 통해 원하는 결과를 얻을 수 있는지 테스트 해보도록 하겠습니다. 

```
비용 레포트를 작성하고 외부에서 웹으로 조회할 수 있도록 구성해줘
웹서버는 Python 내장 HTTP 서버(http.server)를 사용해줘

레포트에는 아래와 같은 내용을 포함해줘
- 현재 계정에서 이용중인 AWS리소스에 대해 1개월 예상 이용금액
- 현재 계정에서 서울리전의 미사용중인 자원 정보와 모두 삭제시 예상 절감금액
```

```
현재 구성된 시스템 아키텍처를 그려줘,
웹서버는 Python 내장 HTTP 서버(http.server)를 사용해줘
그리고 그려진 결과를 외부에서 웹으로 조회할 수 있도록 구성해줘
```

```
현재 계정의 24시간 동안 전체 사용자 활동을 분석해서 레포트를 작성해줘
```





# Lab 1-2. MCP와 연결하기
## 개요
Amazon Q CLI 의 응답을 살펴보면 AWS CLI를 이용해서 응답이 가능하단 것을 알 수 있습니다. AWS CLI 는 API 응답이나 batch, script에 최적화 되어 있는 반면, MCP는 자연어로 소통하는 애플리케이션에 특화된 응답을 하도록 구현되어 있습니다. Q CLI 를 이용한 개발이나 운영 환경에서 MCP를 올바르게 사용하는 것이 핵심이라고 할 수 있습니다.

그리하여 MCP에서는 AWS 문서검색, 비용 리스트 등 기존에 AWS CLI로는 불가했던 기능을 제공하고 있습니다.

이 랩에서는 AWS Pricing List MCP Server 를 설치하고 사용해 봅니다.

**Let's go!**

아래의 AWS Pricing List MCP Server 공식 Github 링크에 접속해봅니다.
```
https://github.com/awslabs/mcp/tree/main/src/aws-pricing-mcp-server
```

우리의 실습 환경에서는 기본 mcp.json 파일의 위치는 아래와 같습니다. 
```
/home/ec2-user/.amazonq/mcp.json
```

설치 방법은 크게 두 가지 입니다.
1. 직접 Github 링크의 [README.md](https://github.com/awslabs/mcp/blob/main/src/aws-pricing-mcp-server/README.md) 파일을 따라하며 설치
2. Q CLI에 설치해달라 요청하기

우리는 Lab.1-1 에서 Context에 AWS 리소스의 경우 공식 MCP를 참조하라 지시했습니다. (mycontext.md 파일을 확인해 보세요.)

MCP 서버 설치를 Q CLI에 요청합니다.
```
AWS Pricing List MCP Server 를 설치하고 mcp.json 등록까지 완료해줘
```

```
지금 서비스하는 ec2 인스턴스와 다이나모디비를 한달 간 사용한다면 비용은 얼마나 나오는가?
```

```
비즈니스가 확장되어 다이나모디비는 1백만배 확장, ec2 인스턴스 크기는 1백만배 트래픽 받아주는 정도로 증설되어야 한다면? EBS 스토리지도 그에 맞게 추가되어야 한다.
```

* 위의 금액은 매우 비효율적입니다. Q CLI도 이에 대해 언급하고 있습니다.
* 비즈니스 확장으로 인해 1백만배로 데이터와 트래픽이 확장된다면 어떻게 최적으로 설계할 수 있을까요? MCP 서버와 Q CLI를 적절히 이용하여 생각해 보세요.

이 워크샵은 MCP(Model Context Protocol) 

서버의 로컬/클라우드 배포에서부터 AWS 기반 애플리케이션 연동까지 종합적인 인프라 구축 역량을 키우기 위해 설계되었습니다. 실습을 통해 AI 모델과 외부 시스템의 연동 메커니즘을 이해하고, 실제 비즈니스 시나리오에 적용 가능한 MCP 기반 솔루션 아키텍처를 구현할 수 있습니다.


MCP 주요 개념

MCP는 Model Context Protocol의 약자로, 애플리케이션이 LLM(Large Language Model)에 컨텍스트를 제공하는 방법을 표준화하는 개방형 프로토콜입니다. 이 프로토콜은 다양한 AI 애플리케이션에서 컨텍스트를 일관되고 효율적으로 관리할 수 있게 해주는 핵심 기술로 자리잡고 있습니다. LLM의 성능과 정확성을 높이기 위해서는 적절한 컨텍스트 제공이 필수적이며, MCP는 이를 체계적으로 지원합니다.

![mcp](https://github.com/noenemy/q-cli-mcp/blob/main/03.mcp-server/images/mcp.jpg)

Claude Desktop
사용자는 Amazon Q Developer CLI 
, Claude Desktop 

과 같은 MCP 클라이언트를 통해 이러한 기능에 쉽게 접근할 수 있습니다. Amazon Q Developer CLI는 MCP 호스트 역할을 하며, 사용자의 질문을 AI 모델에 전달하고, AI 모델이 필요에 따라 MCP 서버의 도구를 호출하도록 합니다. 서버는 요청된 데이터나 기능을 처리한 후 결과를 클라이언트에 반환하고, 이 정보는 다시 AI 모델에게 전달되어 최종적으로 자연어 형태의 응답으로 사용자에게 제공됩니다.
핵심 학습 목표

    MCP 프로토콜을 이용한 AI-인프라 연동 시스템 설계


모델 컨텍스트 프로토콜(MCP)은 무엇이며 AWS MCP 서버와 어떻게 작동합니까?

모델 컨텍스트 프로토콜(MCP)은 LLM 애플리케이션과 외부 데이터 소스 및 도구 간의 원활한 통합을 지원하는 개방형 프로토콜입니다. AI 기반 IDE를 구축하거나, 채팅 인터페이스를 개선하거나, 맞춤형 AI 워크플로를 만드는 경우, MCP는 LLM을 필요한 컨텍스트에 연결하는 표준화된 방법을 제공합니다. 

모델 컨텍스트 프로토콜 README 
https://github.com/modelcontextprotocol#:~:text=The%20Model%20Context,context%20they%20need.

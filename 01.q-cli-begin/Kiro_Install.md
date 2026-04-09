https://kiro.dev/docs/cli/installation/

## glibc가 2.34이상인지 확인
ldd --version

## 리눅스 설치(x86)
curl --proto '=https' --tlsv1.2 -sSf 'https://desktop-release.q.us-east-1.amazonaws.com/latest/kirocli-x86_64-linux.zip' -o 'kirocli.zip'

## 압출 파일을 풀고
unzip kirocli.zip

## 다음 커맨드로 설치를 시작합니다.
./kirocli/install.sh

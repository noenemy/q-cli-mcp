https://kiro.dev/docs/cli/installation/
<img width="768" height="921" alt="Screenshot 2026-04-09 at 6 02 48 PM" src="https://github.com/user-attachments/assets/7d9f84b2-7d63-4837-8b83-1bb6c98e7d10" />


<img width="771" height="444" alt="Screenshot 2026-04-09 at 6 03 02 PM" src="https://github.com/user-attachments/assets/4977a244-cb13-4d9b-a3c0-bdeba13a8425" />

#### glibc가 2.34이상인지 확인
```
ldd --version
```
#### 리눅스 설치(x86)
```
curl --proto '=https' --tlsv1.2 -sSf 'https://desktop-release.q.us-east-1.amazonaws.com/latest/kirocli-x86_64-linux.zip' -o 'kirocli.zip'
```
#### 압출 파일을 풀고
```
unzip kirocli.zip
```

#### 다음 커맨드로 설치를 시작합니다.
```
./kirocli/install.sh
```

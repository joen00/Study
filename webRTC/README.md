"express": "^4.17.1",
"simple-peer-server": "^0.0.8",
"simple-peer-wrapper": "^0.0.2"

simple-peer-wrapper 13003번째 줄 수정필요  
ex)
'''javascript
    this.socket = io.connect(serverUrl, {
      query:{"private_path":simplePeerOptions['private_path'], "guest":simplePeerOptions['guest'] }
    }
    );
'''

simple-peer-server : 내부 코드 전면 수정 필요  
sample 파일 내부 파일로 복사해서 사용 가능  
socket io의 namespace를 이용하여 구현하였음(room에는 최대 2개 연결만 가능하다는 것을 명심)  


수정 필요  
현재 media stream이 inactive할 때 stream 을 null로 만드는 방식으로  
video를 이용 중인데 socket연결을 특정 지을 수 있을 수 있게 수정 필요  

# studyONE

스터디 개인 맞춤 추천시스템 :)

21.10.14 - django server create

1. 메일 인증을 하기위해서는
   back*end->main_server->main->settings.py에서
   email 설정 코드란에 private*\* 변수들을 각자의 메일과 비밀번호로 설정해야 한다.
   이때 github에는 올라가지 않도록 주의한다.
2. 채팅을 위해서는 redis 사용이 필요  
    docker run -p 6379:6379 -d redis:5  

   21.11.01 - basic function implementation

방 생성 - main/newroom  
body{  
 "owner" ,
"password" : blank ok,
"title"  
 "info":{  
 "grce_peri," : default 14, balnk ok  
 "max_user_count" : default 5, blank ok  
 "main_goal"  
 "period_renew": integer, blank ok  
 "enterence_fee": integer, blank oks  
 "meeting_days": charfield, blank ok  
 "meeting_times": charfield[0,1,2,3,3,4,6]=[일,월,화,수,목,금,토], blank ok  
 "penalty" : 0~100 blank ok  
 }  
}

방 내용 변경 - main/room/update/<int:classroompk> .
read_only_fields = ['user_count','main_goal', 'season', 'date_renew', 'total_money'] .
body{  
 "who",
"info":{ .
"grace_period" : default 14, balnk ok  
 "max_user_count" : default 5, blank ok  
 "main_goal"  
 "period_renew": integer, blank ok  
 "enterence_fee": integer, blank oks  
 "meeting_days": charfield, blank ok  
 "meeting_times": charfield, blank ok  
 "penalty" : 0~100 blank ok  
 }  
} .

좋아요 - main/interest/<int:userpk>/<int:classroompk>  
response  
200 - toggle  
400 - error

방 키워드 설정 - main/room/keyword/<int:classroompk>  
body - {"who":"room_owner_pk", "keywords":[ ... ] }  
response  
200 - success  
400 - error

방 채팅 저장 - main/room/chat/<int:classroompk>  
body - {"who":"speaker", "content": "..." }  
response  
200 - success  
400 - error

방 채팅 내역 보기 - main/room/chat/<int:classroompk>  
body - {"who":"guest", "content": "..." }  
response  
200 - json data  
400 - error

방 입장 허락/거부 - main/room/permission/<int:classroompk>  
body - {"who":"room owner pk", "guest":"guest pk" "allow": 1(allow) others(deny) }  
response  
200 - success  
400 - error

시즈별 금액 제출 여부 - main/room/submission/<int:classroompk>/<int:season>  
body - {"who":"guest pk" }  
response  
200 - NO/YES  
400 - error

1. classroom CRUD 구현
2. event 관련 함수 수정

방 서브 목표 설정 - [POST]main/oom/subgoal/<int:classroompk> .
body - {"who":"room_owner_pk", "method": CREATE, UPDATE, DELETE
"title":"...", "explain":"..." ,"attribute": "date_start": blank ok "date_end": blank ok} .

attribute : sub_goal / homework /meeting / other(import day) .
0 1 2 3 .  
방 서브 목표 조회 - [GET] main/oom/subgoal/<int:classroompk> .
body - {"who":"group user"} .

3. 유저 관심사 설정 oneuser/<int:userpk> .
   body - who, request_lis(모든 관심사의 내용이 포함되야함) .
4. 유저의 방 떠나기 oneuser/leave/<int:classroompk> .
   body - who
5. 유저 정보 조회 oneuser/keyword/<int:userpk> .

django start
python manager.py makemigrations
python manager.py migrate
python manager.py runserver
webrtc start
npm start
ehterpad start
src/bin/run.sh

django main port : 8000
webrtc main port : http(8080) https(8081) .
signaling server port : http(9000) https(9443) .
etherpad port : 9001

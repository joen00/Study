from django.contrib import admin
from django.urls import path, include
from .views import *

app_name = 'classroomapp'
urlpatterns = [
    # Read
    path(r'', ListClassRoomAPIView.as_view()),
    path('interest/<int:classroompk>', toggle_interesting),  # 방의 관심도
    path('newroom', CreateClassRoomApiView.as_view()),  # 방생성

    path('room/info/<int:classroompk>', DetailClassRoomAPIView.as_view()),  # 방 정보
    path('room/update/<int:classroompk>', change_classroom_API),  # 방 정보 업데이트
    path("room/deletion/<int:classroompk>", remove_classroom),  # 방 삭제
    path("room/leave/<int:classroompk>", leave_classroom_API),  # 방 떠나기
    path('interest/list', get_interesting_list),  # 관심있는 방 리스트
    path('room/keyword/<int:classroompk>',
         set_classroom_keywords),  # 방 키워드 받거나 설정
    path('room/subgoals/<int:classroompk>',
         ListEventAPIView.as_view()),  # 방 서브 목표 설정하거나 수정하거나 받기

    # chat
    path('room/chat/<int:classroompk>', add_chat_history),  # 방 채팅
    #path('room/chat/live/<str:room_name>/', eg, name='room'),
    path('room/chat/history/<int:classroompk>',
         get_chat_history),  # 방 채팅 기록 가져오기

    #path('room/<int:classroompk>/', testroom),
    # 입장
    path('room/join/request/<int:classroompk>', request_join_room),  # 방 입장 요청
    path('room/permission/<int:classroompk>',
         allow_or_deny_user),  # 방 입장 허락/거부
    path('room/permission/request', get_group_request_list),  # 방 입장 요청 리스트
    path('room/user/list/<int:classroompk>',
         get_user_list_of_classroom),  # 방 참여 유저 리스트

    path('room/submission/<int:classroompk>/<int:season>',
         check_submission),  # 시즌별 제출 여부 - 미사용
    path('room/money/<int:classroompk>', get_room_money),  # 미사용
    # file
    path('room/file/<int:classroompk>', RetrieveUploadFile.as_view()),  # 파일 업로드
    path('room/file/<int:classroompk>/<str:filename>', get_file),  # 파일 전송
    path('room/files/<int:classroompk>', get_roomflie_list),  # 방별 어로드한 파일 리스트

    path('room/attendtion/<int:classroompk>/<int:eventpk>',
         attendtion_update_retrieve),  # 출석 설정하거나 출석 내용 보기
    # 평가
    path('room/user/score/<int:classroompk>', rating_user),  # 유저 평가하기
    path('room/score/<int:classroompk>', rating_classroom),  # 방 평가 하기

    # rtc
    path('join/video/<int:classroompk>', video_func),  # 화상회의 입장



    # 김아영 작성 코드

    # path('first', first, name='first'),
    # path('heart', heart, name='heart'),
    # path('studyroom', studyroom, name='studyroom'),
    # path('mypage', mypage, name='mypage'),
    # path('detailroom', detailroom, name='detailroom'),
    # path('room', room, name='room'),
    #path('test', test, name='test'),


    path("eg", eg, name='eg'),
    path('test', ListClassRoomAPIView.as_view()),

]


"""
    path('room/title/<int:classroompk>',change_classroom_title),
    path('room/explain/<int:classroompk>',change_classroom_explain),
    path('room/grace-peroid/<int:classroompk>',change_grace_period),
    path('room/user/max/<int:classroompk>',change_max_users_count),
    path('room/period/<int:classroompk>',set_season_period),
    path('room/fee/<int:classroompk>',change_enterance_fee),
    path('room/penalty/<int:classroompk>',set_penalty),
"""

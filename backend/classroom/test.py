

from datetime import time
from re import T
from typing import List
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404, request, FileResponse
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.db.models import Q
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from channels.http import AsgiRequest


from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, ListCreateAPIView, UpdateAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import response
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.serializers import Serializer
from rest_framework.views import APIView

from .models import *
from .serializers import *
from agora.models import *
from .pagenations import *


from commons.groups_setter import *
from commons.user_checker import *
from commons.chat_history_handler import chat_history
from agora.models import *
from recommands.db_reader import read_user_goal
from recommands.dbtest import Id_recommendlist
from backend.settings import BASE_DIR


@api_view()
def eg(request: Request):
    queryset = ClassRoomInfo.objects.all()
    try:
        serializer = ClassRoomInfoSerializer(queryset, many=True)
        return HttpResponse("hi")
    except Exception as e:
        print(e)
        return HttpResponse("nonooo")


"""
import logging
logger = logging.getLogger('more_info')
def class_logging_decorator(func):
    def wrapper(self, *kwargs):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR',None)
        user_agent  = self.request.META.get('HTTP_USER_AGENT', "CANT_DETECTED")

        if x_forwarded_for != None:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        logger.info("IP : {0}, AGENT : {1}".format(ip, user_agent))
        return func(self, *kwargs)
    return wrapper

def func_logging_decorator(func):
    def wrapper(request, **kwargs):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR',None)
        user_agent  = request.META.get('HTTP_USER_AGENT', "CANT_DETECTED")

        if x_forwarded_for != None:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        logger.info("IP : {0}, AGENT : {1}".format(ip, user_agent))
        return func(request, **kwargs)
    return wrapper
"""


# list classRoom
class ListClassRoomAPIView(ListAPIView):
    queryset = ClassRoomBasic.objects.all()
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = ClassRoomBasicSerializer
    pagination_class = ClassRoomSetPagination

    def get_recommand(self):
        user_pk = getIdentity(self.request)
        if user_pk == -1:
            return ClassRoomBasic.objects.none()
        recoomands = Id_recommendlist(user_pk)
        if recoomands == None:
            return ClassRoomBasic.objects.none()
        else:
            add_querset = ClassRoomBasic.objects.filter(pk__in=recoomands)
            return add_querset

    def get_queryset(self):
        all_query = super().get_queryset()
        reco_quey = self.get_recommand()
        print(reco_quey)
        result = reco_quey.union(all_query, all=False)
        return result

    def list(self, request, *args, **kwargs):
        ret = super().list(request, *args, **kwargs)
        print(ret)
        return ret

# creation classRoom


class CreateClassRoomApiView(CreateAPIView):
    serializer_class = ClassRoomBasicSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request, *args, **kwargs):
        request.data.__i
        request.data['owner'] = getIdentity(self.request)
        return super().post(request, *args, **kwargs)

# detail classroom info


class DetailClassRoomAPIView(RetrieveAPIView):
    queryset = ClassRoomInfo.objects.all()
    serializer_class = ClassRoomInfoSerializer
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JSONWebTokenAuthentication]

    def get_object(self):
        classroompk = self.kwargs['classroompk']
        return get_object_or_404(ClassRoomInfo, classroombasic_pk=classroompk)

# change classroom info


@api_view(['POST'])
@login_required
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def change_classroom_API(request, classroompk):
    try:
        # check validation
        classroom = get_object_or_404(ClassRoomBasic, id=classroompk)
        classroominfo = get_object_or_404(
            ClassRoomInfo, classroombasic_pk=classroompk)
        requester = request.data.get("who", -1)

        if requester == -1:
            raise Exception("no input")
        # check authentication
        if not checkIdentity(request, requester):
            raise Exception("Not authenticated")

        if classroom.owner.id != requester:
            raise Exception("not authorized")

        # update info
        partial_data = request.data.get("info")
        serializer = ClassRoomInfoSerializer(
            classroominfo, data=partial_data, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            raise Exception(serializer.errors)
        return response.Response("SUCCESS", status=200)
    except Exception as e:
        return response.Response("ERROR", status=400)


# remove classroom
# for method protection(to use only get,post method)
# use function based view
# body {"who": --- }
@api_view(['POST'])
@login_required
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def remove_classroom(request, classroompk):
    try:
        # check validation
        classroom = get_object_or_404(ClassRoomBasic, id=classroompk)
        requester = request.data.get("who", -1)

        if requester == -1:
            raise Exception("no input")
        # check authentication
        if not checkIdentity(request, requester):
            raise Exception("Not authenticated")

        if classroom.owner.id != requester:
            raise Exception("not authorized")

        classroom.delete()

        return response.Response("SUCCESS", status=200)
    except Exception as e:
        return response.Response("ERROR", status=400)


# leave classroom
# use function based view
# body {"who": --- }
@api_view(['POST'])
@login_required
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def leave_classroom_API(request, classroompk):
    try:
        # check validation
        classroom = get_object_or_404(ClassRoomBasic, id=classroompk)
        guestpk = request.data.get("who", -1)
        if guestpk == -1:
            raise Exception("no input")
        if not checkIdentity(request, guestpk):
            raise Exception("Not authenticated")

        if is_guest_in_classroom(guestpk, classroompk):
            groups, guest = get_user_group(guestpk)
            leave_classroom(guest, classroompk, groups)
        else:
            raise Exception("Not Authorized")
        return response.Response("SUCCESS", status=200)
    except Exception as e:
        return response.Response("ERROR", status=400)


# 방의 서브 목표 관련
# CREATE 방의 서브 목표 설정
# url - classroompk
# body - who & method & other datas
# attribute ==> sub_goal / homework /meeting / other(import day)

# LIST room-event
# url - classroompk
# body - who
class ListEventAPIView(ListCreateAPIView):
    queryset = StudyEvent.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def list(self, request, *args, **kwargs):
        try:
            # check validation
            classroompk = kwargs['classroompk']
            classroom = get_object_or_404(ClassRoomBasic, id=classroompk)
            classroom_info = get_object_or_404(
                ClassRoomInfo, classroombasic_pk=classroompk)
            guestpk = request.data.get("who", -1)

            if guestpk == -1:
                raise Exception("No data")
            if not checkIdentity(request, guestpk):
                raise Exception("Not authenticated")

            if is_guest_in_classroom(guestpk, classroompk):
                self.queryset = StudyEvent.objects.filter(
                    user_pk=guestpk, room_pk=classroompk)
                return super().list(request, *args, **kwargs)
            else:
                return response.Response("Not authorized", status=400)
        except Exception as e:
            return response.Response("ERROR", status=400)

    def create(self, request, *args, **kwargs):
        try:
            # check validation
            classroompk = kwargs['classroompk']
            classroom = get_object_or_404(ClassRoomBasic, id=classroompk)
            requester = request.data.get("who", -1)
            requested_moethod = request.data.get("method", "NONE")
            if not checkIdentity(request, requester):
                raise Exception("Not authenticated")
            if requester != classroom.owner.id:  # only owner can change room-keywords
                raise Exception("not authorized")

            if requested_moethod == "NONE":  # if not input exist
                raise Exception("No method")
            # CREATE
            if requested_moethod == "CREATE":
                data = request.data.copy()
                data['user_pk'] = requester
                data['room_pk'] = classroom.id
                serializer = EventSerializer(data=data)
                if serializer.is_valid():
                    event_obj = serializer.save()
                    attendtion_add_of_event(classroom, event_obj)
                else:
                    raise Exception("serializing error")
            # UPDATE
            elif requested_moethod == "UPDATE":
                # check event value
                eventpk = request.data.get("event", -1)
                if eventpk == -1:
                    raise Exception("No subgoal info")
                subgoal = get_object_or_404(StudyEvent, id=eventpk)
                data = request.data.copy()
                data['user_pk'] = requester
                data['room_pk'] = classroom.id
                serializer = EventSerializer(subgoal, data=data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    raise Exception("serializing error")
            # DELETE
            elif requested_moethod == "DELETE":
                # check event value
                eventpk = request.data.get("event", -1)
                if eventpk == -1:
                    raise Exception("No subgoal info")
                subgoal = get_object_or_404(StudyEvent, id=eventpk)
            # 2일 지나면 삭제 불가
                start_date = subgoal.date_start
                limit_date = start_date + timezone.timedelta(days=2)
                now_date = timezone.now()
                if limit_date < now_date:
                    raise Exception("invalid days")
                else:
                    subgoal.delete()
            return response.Response("SUCCESS", status=200)
        except Exception as e:
            return response.Response("ERROR", status=400)


"""
room user list
"""

# 평점
# 평점은입장 후 바로 평가 후 1일 이후에 가능(빠른 피드백 필요)
# 평점은 기간은 4일로 설정(빠른 피드백 필요)
# 평점은 방에 속해있을 때만 가능하도록 했기 때문에(코드의 간편성)
# 방을 나가기 전에 평가를 내려달라는 공지가  필요
# body : rater / ratee /score


@api_view(['POST'])
@login_required
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def rating_user(request, classroompk):
    try:
        # check validation
        classroominfo = get_object_or_404(
            ClassRoomInfo, classroombasic_pk=classroompk)
        cur_season = classroominfo.season
        raterpk = request.data.get("rater", -1)
        rateepk = request.data.get("ratee", -1)
        score = request.data.get("score", -1)
        if rateepk == -1 or raterpk == -1 or score == -1:
            raise Exception("Not input")
        if not checkIdentity(request, raterpk):
            raise Exception("Not authenticated")
        if is_guest_in_classroom(raterpk, classroompk) == False or is_guest_in_classroom(rateepk, classroompk) == False:
            raise Exception("Not Authorized_1")

        # 입장후 1일이 지났는지
        today = timezone.now()
        rater_join_info = get_object_or_404(
            Group, user_pk=raterpk, classroombasic_pk=classroompk, season=cur_season)
        ratee_join_info = get_object_or_404(
            Group, user_pk=rateepk, classroombasic_pk=classroompk, season=cur_season)

        rater_init_rating_date = rater_join_info.date_join + \
            timezone.timedelta(days=1)
        ratee_init_rating_date = ratee_join_info.date_join + \
            timezone.timedelta(days=1)

        if rater_init_rating_date > today or ratee_init_rating_date > today:
            raise Exception("Not Authorized_2")
        # 평점을 매긴후 4일이 지났는지 or 처음 평점인지
        q = Q()
        q.add(Q(rater_pk=raterpk), q.OR)
        q.add(Q(ratee_pk=rateepk), q.OR)
        score_obj = UserScore.objects.filter(q)

        if len(score_obj) != 0:  # 평점 매긴지 4일이 안지난 우우
            score_obj = score_obj.latest('date')
            next_rating_day = score_obj.date + timezone.timedelta(days=4)
            if next_rating_day > today:
                raise Exception("Not expired")

        # 평점 추가하기
        rater = get_object_or_404(ONEUser, id=raterpk)
        ratee = get_object_or_404(ONEUser, id=rateepk)
        UserScore.objects.create(
            rater_pk=rater, ratee_pk=ratee, score=score, classroom_pk=classroompk)

        return response.Response("SUCCESS", status=400)

    except Exception as e:
        print(e)
        return response.Response("ERROR", status=400)

# 평점
# 평점은입장 후 바로 평가 후 1일 이후에 가능(빠른 피드백 필요)
# 평점은 기간은 4일로 설정(빠른 피드백 필요)
# 평점은 방에 속해있을 때만 가능하도록 했기 때문에(코드의 간편성)
# 방을 나가기 전에 평가를 내려달라는 공지가  필요
# body : rater / score / survey = "1-2,2-3, 4-5,"


@api_view(['POST'])
@login_required
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def rating_classroom(request, classroompk):
    try:
        # check validation
        classroom = get_object_or_404(ClassRoomBasic, id=classroompk)
        classroominfo = get_object_or_404(
            ClassRoomInfo, classroombasic_pk=classroompk)
        cur_season = classroominfo.season
        raterpk = request.data.get("rater", -1)
        score = request.data.get("score", -1)
        survey = request.data.get("survey", -1)
        if raterpk == -1 or score == -1 or survey:
            raise Exception("Not input")
        if not checkIdentity(request, raterpk):
            raise Exception("Not authenticated")
        if is_guest_in_classroom(raterpk, classroompk) == False:
            raise Exception("Not Authorized_1")

        # 입장후 1일이 지났는지
        today = timezone.now()
        rater_join_info = get_object_or_404(
            Group, user_pk=raterpk, classroombasic_pk=classroompk, season=cur_season)
        rater_init_rating_date = rater_join_info.date_join + \
            timezone.timedelta(days=1)
        if rater_init_rating_date > today:
            raise Exception("Not Authorized_2")

        # 평점을 매긴후 4일이 지났는지 or 처음 평점인지
        q = Q()
        q.add(Q(evaluator_pk=raterpk), q.OR)
        q.add(Q(classroombasic_pk=classroompk), q.OR)
        score_obj = ClassRoomScore.objects.filter(q)

        if len(score_obj) != 0:  # 평점 매긴지 4일이 안지난 우우
            score_obj = score_obj.latest('date')
            next_rating_day = score_obj.date + timezone.timedelta(days=4)
            if next_rating_day > today:
                raise Exception("Not expired")

        # 평점 추가하기
        rater = get_object_or_404(ONEUser, id=raterpk)
        ClassRoomScore.objects.create(
            evaluator_pk=rater, classroombasic_pk=classroom, score=score, survey=survey)
        return response.Response("SUCCESS", status=400)

    except Exception as e:
        print(e)
        return response.Response("ERROR", status=400)


######### simple function  ############
#######################################

# 좋아요 토글
@api_view(['POST'])
@login_required
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def toggle_interesting(request, classroompk):
    try:
        # get data
        classroom = get_object_or_404(ClassRoomBasic, id=classroompk)
        one_userpk = request.data.get('who', -1)

        if one_userpk == -1:
            raise Exception("not authenticated")
        if not checkIdentity(request, one_userpk):
            raise Exception("Not authenticated")
        user = get_object_or_404(ONEUser, id=one_userpk)

        try:  # if interest history exist
            data = UserInterest.objects.get(
                user_pk=one_userpk, room_pk=classroompk)
            if data.is_on == True:
                data.is_on = False
            else:
                data.is_on = True
            data.save()
        except ObjectDoesNotExist as e:  # if history not exist
            UserInterest.objects.create(user_pk=user, room_pk=classroom)
        return response.Response("toggle", status=200)
    except Exception as e:
        return response.Response("ERROR", status=400)

# 방의 키워드 설정
# url - classroompk
# body - owner & keyword_list


@api_view(['POST'])
@login_required
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def set_classroom_keywords(request: Request, classroompk):
    try:
        classroom = get_object_or_404(ClassRoomBasic, id=classroompk)
        requester = request.data.get("who", -1)
        input_keyword_list = request.data.get("keywords", [])

        if not checkIdentity(request, requester):
            raise Exception("Not authenticated")
        if requester != classroom.owner.id:  # only owner can change room-keywords
            raise Exception("not authorized")
        if len(input_keyword_list) == 0:  # not data exist
            raise Exception("no input")

        # get old room-keyword list
        keywordset = RoomKeyWord.objects.filter(room_pk=classroompk)
        list_keywordpk = [value.keyword_pk for value in keywordset]

        # remove not used keyword anymore in classroom-keyword
        for idx, obj in enumerate(list_keywordpk):
            old_keyword = obj.word
            if old_keyword not in input_keyword_list:
                keywordset[idx].delete()

        # update keywords relation
        for keyword in input_keyword_list:
            # create or get keyword-row
            if not Keyword.objects.filter(word=keyword).exists():
                input_keyword = Keyword(word=keyword)
                input_keyword.save()
            else:
                input_keyword = Keyword.objects.get(word=keyword)

            # if keyword not related with classroom
            if input_keyword not in list_keywordpk:
                RoomKeyWord.objects.create(
                    room_pk=classroom, keyword_pk=input_keyword)

        return response.Response("SUCCESS", status=200)
    except Exception as e:
        return response.Response("ERROR", status=400)

# 방의 모인 금액 분배


@api_view(['POST'])
@login_required
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def distribute_money(request):  # assert moeny(int)
    try:
        return response.Response("SUCCESS", status=200)
    except Exception as e:
        return response.Response("ERROR", status=400)


# chat 저장
# url - classroompk
# body - who(speaker)
@api_view(['POST'])
# @login_required
# @permission_classes((IsAuthenticated, ))
# @authentication_classes((JSONWebTokenAuthentication,))
def add_chat_history(request, classroompk):  # assert user-classroom-content
    try:
        # check input validation
        speakerpk = request.data.get("who", -1)
        content = request.data.get("content", '')
        if speakerpk == -1 or content == '':
            raise Exception("No input")
        if not checkIdentity(request, speakerpk):
            raise Exception("Not authenticated")

        if not Group.objects.filter(user_pk=speakerpk, classroombasic_pk=classroompk).exists():
            raise Exception("Invalid input")

        # save chat
        data = request.data.copy()
        data['user_pk'] = speakerpk
        data['classroombasic_pk'] = classroompk
        serializer = chatSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            raise Exception("serializer error")
        return response.Response("SUCCESS", status=200)
    except Exception as e:
        print(e)
        return response.Response("ERROR", status=400)

# chat 내용 보기
# url classroompk
# body who


@api_view(['POST'])
@login_required
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def get_chat_history(request, classroompk):  # assert user-classroom-content
    try:
       # check validation
        one_userpk = request.data.get("who", -1)
        if one_userpk == -1:
            raise Exception("No data")
        if not checkIdentity(request, one_userpk):
            raise Exception("Not authenticated")

        assert(type(one_userpk) == int)
        # oneuser = get_object_or_404(ONEUser, id=userpk)
        if not Group.objects.filter(user_pk=one_userpk, classroombasic_pk=classroompk).exists():
            raise Exception("Invalid input")

        # get data
        paginator = ChatHistorySetPagination()
        queryset = ChatHistory.objects.filter(
            classroombasic_pk=classroompk).order_by('-date')
        paged_queryset = paginator.paginate_queryset(queryset, request)
        serializer = chatSerializer(paged_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)
        # return response.Response(serializer.data, status=200)
        # json = JSONRenderer().render(serializer.data)
        # return HttpResponse(json, status=200)
    except Exception as e:
        return response.Response("ERROR", status=400)


# 방 입장 요청 리스트
# url - classroompk
# body - who

@api_view(['POST'])
@login_required
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def get_group_request_list(request):  # assert userpk and (YES or NO)
    try:
        # check input validation
        one_userpk = request.data.get("who", -1)
        if one_userpk == -1:
            raise Exception("No data")
        if not checkIdentity(request, one_userpk):
            raise Exception("Not authenticated")
        # get my classroom
        oneuser = get_object_or_404(ONEUser, id=one_userpk)
        my_classroom_list = ClassRoomBasic.objects.filter(owner=one_userpk)
        # set query
        q = Q()
        for value in my_classroom_list:
            q.add(Q(classroombasic_pk=value), q.OR)

        q.add(Q(state=0), q.AND)
        queryset = Group.objects.filter(q)

        paginator = DefaultSetPagination()
        paged_queryset = paginator.paginate_queryset(queryset, request)
        serializer = GroupSerializer(paged_queryset, many=True)

        return paginator.get_paginated_response(serializer.data)

    except Exception as e:
        return response.Response("ERROR", status=400)

# 방 입장 허용/거부
# url - classroompk
# body - who & guest & deny(allow)


@api_view(['POST'])
@login_required
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def allow_or_deny_user(request, classroompk):  # assert userpk and (YES or NO)
    try:
        # check input validation
        classroom = get_object_or_404(ClassRoomBasic, id=classroompk)
        classroom_info = get_object_or_404(
            ClassRoomInfo, classroombasic_pk=classroompk)

        ownerpk = request.data.get("who", -1)
        guestpk = request.data.get("guest", -1)
        is_allow = request.data.get("allow", -1)

        if not checkIdentity(request, ownerpk):
            raise Exception("Not authenticated")
        if ownerpk != classroom.owner.id:  # only owner can change room-keywords
            raise Exception("not authorized")
        if guestpk == -1 or is_allow == -1:
            raise Exception("NO input")

        # set permission
        group = get_object_or_404(
            Group, user_pk=guestpk, season=classroom_info.season)
        guest = get_object_or_404(ONEUser, id=guestpk)

        if join_classroom(guest, group, classroompk, is_allow, ClassRoomInfo.season):
            return response.Response("SUCCESS", status=200)
        else:
            raise Exception("not invalid")
    except Exception as e:
        return response.Response("ERROR", status=400)

# 시즌별 금액 제출 여부
# url - classroompk
# body - who


@api_view(['POST'])
@login_required
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def check_submission(request, classroompk, season):  # assert userpk classroom season
    try:
        # check validdation
        classroom = get_object_or_404(ClassRoomBasic, id=classroompk)
        classroom_info = get_object_or_404(
            ClassRoomInfo, classroombasic_pk=classroom)
        guestpk = request.data.get("who", -1)

        if guestpk == -1:
            raise Exception("no data")

        if not is_guest_in_classroom(guestpk, classroompk):
            raise Exception("not authorized")

        if classroom_info.season > season:
            raise Exception("invalid input")

        # check submission
        guest = get_object_or_404(Group, user_pk=guestpk)
        if guest.fee_submission == False:
            return response.Response("NO", status=200)
        else:
            return response.Response("YES", status=200)
    except Exception as e:
        return response.Response("ERROR", status=400)

# 현재 방에 모인 금액 확인
# url - classroompk
# body - who


@api_view(['POST'])
@login_required
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def get_room_money(request, classroompk):  # assert userpk classroom season
    try:
        # check validation
        classroom = get_object_or_404(ClassRoomBasic, id=classroompk)
        classroom_info = get_object_or_404(
            ClassRoomInfo, classroombasic_pk=classroom)
        guestpk = request.data.get("who", -1)

        if not checkIdentity(request, guestpk):
            raise Exception("Not authenticated")
        if guestpk == -1:
            raise Exception("no data")
        # check guest in classroom group
        groups, _ = get_user_group(guestpk)
        if classroompk not in groups:
            raise Exception("not authorized")
        return response.Response(classroom_info.total_money, status=200)

    except Exception as e:
        return response.Response("ERROR", status=400)


# 파일 업로드/개별 파일 확인
# url - classroompk
# body - who

@api_view(['GET'])
@login_required
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def get_roomflie_list(request, classroompk):
    try:
        # check validation
        classroom = get_object_or_404(ClassRoomBasic, id=classroompk)
        requesterpk = getIdentity(request)
        # check if group member
        if is_guest_in_classroom(requesterpk, classroompk):
            requester = get_object_or_404(ONEUser, id=requesterpk)
        else:
            raise Exception("Not Authorized")
        datalist = RoomFile.objects.filter(classroombasic_pk=classroompk)
        serializer = RoomFileSerializer(datalist, many=True)
        return response.Response(serializer.data, status=200)

    except Exception as e:
        print(e)
        return response.Response("ERROR", status=400)

# 요청 file 전송


@api_view(['GET'])
@login_required
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def get_file(request, classroompk, filename):
    try:
        # check validation
        classroom = get_object_or_404(ClassRoomBasic, id=classroompk)
        requesterpk = getIdentity(request)

        if is_guest_in_classroom(requesterpk, classroompk):
            # real relative url
            spk = str(classroompk)
            file_path = str(BASE_DIR) + "/" + "media" + \
                "/" + spk + "/" + filename
            # return redirect("/media/" + str(classroompk) + "/" + filename)
            return FileResponse(open(file_path, 'rb'))
            # return redirect()
        else:
            raise Exception("Not Authorized")
    except Exception as e:
        print(e)
        return response.Response("ERROR", status=400)


# file 저장
"""
{
    "who": --,
    "file" : ---
}
"""


class RetrieveUploadFile(APIView):  # assert userpk classroom season
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request, classroompk):
        try:
            # check validation
            uploaderpk = request.data.get("who", -1)
            if uploaderpk == -1:
                raise Exception("Not Authenticated")
            if not checkIdentity(request, uploaderpk):
                raise Exception("Not authenticated")
            if is_guest_in_classroom(uploaderpk, classroompk):
                # serializing setting
                value = dict()
                value['user_pk'] = uploaderpk
                value['classroombasic_pk'] = classroompk
                value['title'] = request.data['file']._get_name()
                value['attribute'] = request.data['file'].content_type
                value['file'] = request.data['file']
                serializer = RoomFileSerializer(data=value)
                if serializer.is_valid():
                    serializer.save()
                    return response.Response("SUCCESS", status=200)
                else:
                    raise Exception(serializer.errors)
            else:
                raise Exception("No data")

        except Exception as e:
            print(e)
            return response.Response("ERROR", status=400)


# 출석 update
# 이벤트별 출석 목록
"""
{
    "who": --(userpk),
    "attendance" : --(boolean),
}
"""


@api_view(['GET', "POST"])
@login_required
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def attendtion_update_retrieve(request, classroompk, eventpk):
    if request.method == "POST":
        try:
            # check validation
            attendance = request.data.get("attendance", None)
            if attendance == None:
                raise Exception("No enough data")
            guestpk = request.data.get('who', -1)
            if guestpk == -1:
                raise Exception("Not Authenticated")
            if not checkIdentity(request, guestpk):
                raise Exception("Not authenticated")
            if is_guest_in_classroom(guestpk, classroompk):
                # 기간 확인
                event = get_object_or_404(StudyEvent, id=eventpk)
                now = timezone.now()
                due = event.date_end
                if due < now:
                    raise Exception("EXPIRE DATE")
                # 참석/불참석 설정
                try:  # sub goal 생성시 sub goal에 해당되는 attendtion을 미리 생성하는데 오류가 발생하는 경우룰 대비함
                    attendtion: Attendtion = get_object_or_404(
                        Attendtion, event=eventpk, classroombasic_pk=classroompk, group_user=guestpk)
                except:
                    attendtion: Attendtion = Attendtion.objects.create(
                        event=eventpk, classroombasic_pk=classroompk, group_user=guestpk)
                attendtion.attendance = attendance
                attendtion.save()
                return response.Response("SUCCESS", status=200)
            else:
                raise Exception("Not authorized")
        except Exception as e:
            return response.Response("ERROR", status=400)
    elif request.method == "GET":
        try:
            guestpk = getIdentity(request)
            guestpk = 1
            """
            if requesterpk == -1:
                raise Exception("Not Authenthicated")
            """
            if is_guest_in_classroom(guestpk, classroompk):
                # 참석/불참석 여부 확인
                attendtion_list = Attendtion.objects.filter(
                    event=eventpk, classroombasic_pk=classroompk)
                serializer = AttendtionSerializer(attendtion_list, many=True)
                return response.Response(serializer.data, status=200)
        except Exception as e:
            return response.Response("ERROR", status=400)


"""
{
    "who": ---
}
"""


@api_view(['POST'])
@login_required
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def video_func(request, classroompk):
    guestpk = request.data.get('who', -1)

    if guestpk == -1:
        raise Exception("Not Authenticated")

    if not checkIdentity(request, guestpk):
        raise Exception("Not Authorized")

    if is_guest_in_classroom(guestpk, classroompk):
        base_url = "http://127.0.0.1:8080"
        path = "/main/room/video/" + str(classroompk) + "?who=" + str(guestpk)
        url = base_url + path
        print(url)
        return redirect(url)
    else:
        return response.Response("ERROR", status=400)


class GetSurveys(ListAPIView):
    queryset = surveyEntry.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = SurveyEntrySerializer

    def get_queryset(self):
        # select survey
        id_list = []
        # return surveyEntry.objects.filter(id_in = id__list)
        # use all survey
        return super().get_queryset()


"""
# 방의 제목 변경
# url - classroompk
# body - owner & title
@api_view(['POST'])
def change_classroom_title(request, classroompk):
    try:
        classroom = get_object_or_404(ClassRoomBasic, id=classroompk)
        requester = request.data.get("who", -1)
        input_title = request.data.get("title", "NONE")

        if requester != classroom.owner.id: # only owner can change room-keywords
            raise Exception("not authorized")
        if input_title == "NONE": # if not input exist
            raise Exception("No input")

        classroom.title = input_title
        classroom.save()

        return response.Response("SUCCESS",status=200)
    except Exception as e:
        return response.Response("ERROR", status=400)

# 방의 소개 변경
# url - classroompk
# body - owner & explain
@api_view(['POST'])
def change_classroom_explain(request,classroompk):
    try:
        classroom = get_object_or_404(ClassRoomBasic, id=classroompk)
        classroom_info = get_object_or_404(
            ClassRoomInfo, classroombasic_pk=classroompk)
        requester = request.data.get("who", -1)
        input_explain = request.data.get("explain", "NONE")

        if requester != classroom.owner.id: # only owner can change room-keywords
            raise Exception("not authorized")
        if input_explain == "NONE": # if not input exist
            raise Exception("No input")


        # change explain
        classroom_info.explain = input_explain
        classroom_info.save()

        return response.Response("SUCCESS",status=200)
    except Exception as e:
        print(e)
        return response.Response("ERROR", status=400)

# 방의 유예기간 설정/변경
# url - classroompk
# body - owner & days
@api_view(['POST'])
def change_grace_period(request, classroompk): # assert days(int) data
    try:
        classroom = get_object_or_404(ClassRoomBasic, id=classroompk)
        classroom_info = get_object_or_404(
            ClassRoomInfo, classroombasic_pk=classroompk)
        requester = request.data.get("who", -1)
        input_days = request.data.get("days", -1)

        if requester != classroom.owner.id: # only owner can change room-keywords
            raise Exception("not authorized")
        if input_days == -1: # if not input exist
            raise Exception("No input")

        assert(type(input_days)==int)
        classroom_info.grace_period = input_days
        classroom_info.save()

        return response.Response("SUCCESS",status=200)
    except Exception as e:
        return response.Response("ERROR", status=400)

# 방의 최대 인원 설정/변경
# url - classroompk
# body - owner & counts
@api_view(['POST'])
def change_max_users_count(request, classroompk): # assert count(int) data
    try:
        classroom = get_object_or_404(ClassRoomBasic, id=classroompk)
        classroom_info = get_object_or_404(
            ClassRoomInfo, classroombasic_pk=classroompk)
        requester = request.data.get("who", -1)
        input_counts = request.data.get("counts", -1)

        if requester != classroom.owner.id: # only owner can change room-keywords
            raise Exception("not authorized")
        if input_counts == -1: # if not input exist
            raise Exception("No input")

        assert(type(input_counts)==int)
        classroom_info.max_user_count = input_counts
        classroom_info.save()
        return response.Response("SUCCESS",status=200)
    except Exception as e:
        return response.Response("ERROR", status=400)


# 방의 penalty 설정
# url - classroompk
# body - owner & penalty
@api_view(['POST'])
def set_penalty(request, classroompk): # assert percentage(int)
    try:
        classroom = get_object_or_404(ClassRoomBasic, id=classroompk)
        classroom_info = get_object_or_404(
            ClassRoomInfo, classroombasic_pk=classroompk)
        requester = request.data.get("who", -1)
        input_penalty = request.data.get("penalty", -1)

        if requester != classroom.owner.id: # only owner can change room-keywords
            raise Exception("not authorized")
        if input_penalty == -1: # if not input exist
            raise Exception("No input")

        assert(type(input_penalty)==int)
        classroom_info.penalty = input_penalty
        classroom_info.save()
        return response.Response("SUCCESS",status=200)
    except Exception as e:
        return response.Response("ERROR", status=400)




# 방의 시즌별 기간 설정
# url - classroompk
# body - owner & period days
@api_view(['POST'])
def set_season_period(request, classroompk): # assert days(int)
    try: # assert changing is only allowed within one week in new season
        classroom = get_object_or_404(ClassRoomBasic, id=classroompk)
        classroom_info = get_object_or_404(
            ClassRoomInfo, classroombasic_pk=classroompk)
        requester = request.data.get("who", -1)
        input_days = request.data.get("days", -1)

        if requester != classroom.owner.id: # only owner can change room-keywords
            raise Exception("not authorized")
        if input_days == -1: # if not input exist
            raise Exception("No input")


        assert(type(input_days)==int)
        old_start_season  = classroom_info.date_renew
        new_start_season = old_start_season + \
            timezone.timedelta(days=input_days)
        limit_date = old_start_season + timezone.timedelta(days=7)
        now_date = timezone.now()
        # season period validation checking
        if now_date <= new_start_season and limit_date>=now_date:
            classroom_info.period_renew = input_days
            classroom_info.save()
        else:
            raise Exception("invalid days")

        return response.Response("SUCCESS",status=200)
    except Exception as e:
        return response.Response("ERROR", status=400)


# 방의 입장료 변경
# url - classroompk
# body - owner & fee
@api_view(['POST'])
def change_enterance_fee(request, classroompk): # assert moeny(int)
    try: # assert modification affects next season
        classroom = get_object_or_404(ClassRoomBasic, id=classroompk)
        classroom_info = get_object_or_404(
            ClassRoomInfo, classroombasic_pk=classroompk)
        requester = request.data.get("who", -1)
        input_fee = request.data.get("fee", -1)

        if requester != classroom.owner.id: # only owner can change room-keywords
            raise Exception("not authorized")
        if input_fee == -1: # if not input exist
            raise Exception("No input")

        # 새 시즌 이후 일주인 이내로만 변경
        assert(type(input_fee)==int)
        old_start_season  = classroom_info.date_renew
        limit_date = old_start_season + timezone.timedelta(days=7)
        now_date = timezone.now()
        # season period validation checking
        if limit_date>=now_date:
            classroom_info.enterence_fee = input_fee
            classroom_info.save()
        else:
            raise Exception("invalid days")

        return response.Response("SUCCESS",status=200)
    except Exception as e:
        return response.Response("ERROR", status=400)


"""


# 김아영 작성 코드
def first(request):
    return render(request, 'firstpage.html', {})


def heart(request):
    return render(request, 'heart.html', {})


def studyroom(request: Request):
    return render(request, 'studyroom.html', {})


def mypage(request):
    return render(request, 'mypage.html', {})


def detailroom(request):
    return render(request, 'detailroom.html', {})


def room(request):
    return render(request, 'room.html', {})


def test(request):
    return render(request, 'test.html', {})
        limit_date = old_start_season + timezone.timedelta(days=7)
        now_date = timezone.now()
        # season period validation checking
        if limit_date >= now_date:
            classroom_info.enterence_fee = input_fee
            classroom_info.save()
        else:
            raise Exception("invalid days")

        return response.Response("SUCCESS", status=200)
    except Exception as e:
        return response.Response("ERROR", status=400)


"""


# 김아영 작성 코드
def first(request):
    return render(request, 'firstpage.html', {})


def heart(request):
    return render(request, 'heart.html', {})


def studyroom(request: Request):
    return render(request, 'studyroom.html', {})


def mypage(request):
    return render(request, 'mypage.html', {})


def detailroom(request):
    return render(request, 'detailroom.html', {})


def room(request):
    return render(request, 'room.html', {})


def test(request):
    return render(request, 'test.html', {})

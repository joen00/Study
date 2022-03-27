from rest_framework import response

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from classroom.models import ChatHistory
from classroom.serializers import chatSerializer
from classroom.pagenations import ChatHistorySetPagination



def chat_history(request, classroompk): # assert user-classroom-content
    try:
        # get data
        classroompk = 1
        paginator = ChatHistorySetPagination()
        queryset =  ChatHistory.objects.filter(classroombasic_pk=classroompk).order_by('-date')
        paged_queryset = paginator.paginate_queryset(queryset, request)
        serializer = chatSerializer(paged_queryset, many=True)
        return serializer.data
    except Exception as e:
        print(e)
        return None

def add_chat(classpk, userpk, content): # assert user-classroom-content
    try:
        # save chat
        data = dict()
        data['content'] = content
        data['user_pk'] = userpk
        data['classroombasic_pk'] = classpk
        serializer = chatSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
            raise Exception("serializer error")
    except Exception as e:
        print(e)
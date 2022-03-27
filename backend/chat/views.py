
# Create your views here.
from commons.chat_history_handler import chat_history
from django.shortcuts import render
from rest_framework.decorators import api_view

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


@api_view()
def room(request, room_name):
    history = chat_history(request, 1)
    return render(request, 'room_zz.html', {
        'room_name': room_name,
        'history': history
    })


def chatroom(request, room_name):

    return render(request, 'chat_temp.html', {
        'room_name': room_name,
    })

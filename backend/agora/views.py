from .forms.account_forms import ONEUserLoginForm, ONEUserSignupForm, testForm
from commons.user_checker import *
from commons.groups_setter import *
from classroom.models import *
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import EmailMessage
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import PasswordResetForm
from django.views.decorators.cache import cache_control
from django.views.generic.base import TemplateView


from rest_auth.registration.views import RegisterView
import psycopg2
from django.utils.translation import ugettext_lazy as _


from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView, View
from rest_framework.request import Request
from rest_framework import response


from .serializers import ONEUserInfoSerializer
from .models import Keyword, ONEUser, UserKeyWord
from .token import *

import threading
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


class ONEUserRegisterView(RegisterView):
    def get_response_data(self, user):
        user.is_active = False
        user.save()
        # email sender
        uidb64 = urlsafe_base64_encode(force_bytes(user.id))
        token = account_activation_token.make_token(user)
        message_data = message("localhost:8000", uidb64, token)
        self.thread_maker(message_data, user.email)
        return {"detail": _("Verification e-mail sent.")}

    def email_sender(self, message, destination):
        email = EmailMessage("email 인증", message, to=[destination])
        email.send()

    def thread_maker(self, message, destination):
        thread = threading.Thread(
            target=self.email_sender, args=(message, destination))
        thread.start()


@api_view(["GET"])
def user_inactive():
    return HttpResponse("inactive")


def email_verifing(uid):
    conn_string = "host = 'localhost' dbname = 'test_db' user = 'evergreen' password = 'evergreen'"
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()

    query = "UPDATE account_emailaddress SET verified='TRUE' WHERE user_id=" + \
        str(uid)
    cur.execute(query)
    conn.commit()


class CustomActivate(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = ONEUser.objects.get(id=uid)
            if account_activation_token.check_token(user, token):
                user.is_active = True
                # email_verifing(uid)
                user.save()
                return HttpResponse("SUCCESS", status=200)
            return JsonResponse({"message": "AUTH FAIL"}, status=400)
        except Exception as e:
            print(e)
            return JsonResponse({"message": "TYPE_ERROR"}, status=400)
        except KeyError:
            print(e)
            return JsonResponse({"message": "INVALID_KEY"}, status=400)


@api_view(["GET"])
def get_all_user_info():
    pass


# get user info
class DetailONEUserAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = ONEUserInfoSerializer

    def get_object(self):
        pk = getIdentity(self.request)
        print(pk)
        data = get_object_or_404(ONEUser, id=pk)
        return data
# delete ONEUser account


@api_view(['POST'])
@login_required
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def delete_oneuser(request):
    try:
        # check input
        one_userpk = getIdentity(request)
        if one_userpk == -1:
            raise Exception("no data")
        # check authentication
        if not checkIdentity(request, one_userpk):
            raise Exception("Not authenticated")
        oneuser: ONEUser = ONEUser.objects.get(id=one_userpk)
        oneuser.delete()
        return response.Response("SUCCESS", status=200)
    except:
        print(e)
        return response.Response("ERROR", status=400)


# 방 떠나기
# url - classroompk
# body - who
@api_view(['POST'])
@login_required
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def leave_classroom(request, classroompk):
    try:
        # check validation
        classroom = get_object_or_404(ClassRoomBasic, id=classroompk)
        guestpk = getIdentity(request)
        if guestpk == -1:
            raise Exception("no input")

        if is_guest_in_classroom(guestpk, classroompk):
            groups, guest = get_user_group(guestpk)
            leave_classroom(guest, classroompk, groups)
        else:
            raise Exception("Not Authorized")
        return response.Response("SUCCESS", status=200)
        """
        # check guest in classroom group
        groups = get_user_group(one_userpk)
        if classroompk not in groups:
            raise Exception("not authorized")

        if leave_classroom(one_userpk, classroompk, groups):
            return response.Response("SUCCESS", status=200)
        else:
            raise Exception("No data")
        """
    except Exception as e:
        print(e)
        return response.Response("ERROR", status=400)


# 유저의 관심사 설정
# url - userpk
# body - who & keyword_list
@login_required
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
@api_view(['POST'])
def set_oneuser_keywords(request: Request):
    try:
        # chech input validation
        requester = getIdentity(request)
        input_keyword_list = request.data.get("keywords", [])
        if requester == -1:
            raise Exception("no data")
        oneuser = get_object_or_404(ONEUser, id=requester)

        # not data exist
        if len(input_keyword_list) == 0:
            raise Exception("no input")

        # get old user-keyword list
        keywordset = UserKeyWord.objects.filter(user_pk=requester)
        list_keywordpk = [value.keyword_pk for value in keywordset]

        # remove not used keyword anymore in user-keyword
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

            # if keyword not related with user
            if input_keyword not in list_keywordpk:
                UserKeyWord.objects.create(
                    user_pk=oneuser, keyword_pk=input_keyword)

        return response.Response("SUCCESS", status=200)
    except Exception as e:
        print(e)
        return response.Response("ERROR", status=400)


"""
class ONEUserLoginView(LoginView):
    form_class = ONEUserLoginForm
    template_name = "login_zz.html"

class ONEUserSignupView(SignupView):
    form_class =  ONEUserSignupForm
    template_name = "signup_zz.html"

class ONEUserInactiveView(AccountInactiveView):
    template_name = 'signup_inactive.html'

class ONEUserEmailVerificationSentView(EmailVerificationSentView):
    template_name = 'signup_email_varification.html'

class ONEUSerPWChangeView(PasswordChangeView):
    template_name = "pw_change.html"
    success_url = reverse_lazy("account_change_password_complete")

class ONEUserPWResetView(PasswordResetView):
    template_name = 'pw_reset.html'

class ONEUserPWResetConfirmView(PasswordResetFromKeyView):
    template_name = 'pw_reset_confirm.html'


@api_view(['GET'])
def email_cofirm_redirect(request):
    return redirect('account_login')

@api_view(['GET'])
def pw_change_complete(request):
    return render(request, 'pw_change_complete.html')

@api_view(['GET'])
def pw_reset_complete(request):
    return render(request, 'pw_reset_complete.html')

"""

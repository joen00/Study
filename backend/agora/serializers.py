import threading

# email varify
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
#from phonenumber_field import phonenumber
# serializer
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_auth.registration.serializers import RegisterSerializer
# inner
from .token import *
from .models import ONEUser, UserKeyWord
# registrations


class UserRegisterSerializer(RegisterSerializer):
    phone_number = serializers.IntegerField(required=True)
    #phone_number = PhoneNumberField()

    def save(self, request):
        user = super().save(request)
        user.phone_number = request.data['phone_number']
        user.save()
        # email varification process
        uidb64 = urlsafe_base64_encode(force_bytes(user.id))
        token = account_activation_token.make_token(user)  # from token.py
        message_data = message("localhost:8000", uidb64,
                               token)  # from token.py
        # email sending requires long-burst
        self.thread_maker(message_data, user.email)
        return user

    def email_sender(self, message, destination):
        email = EmailMessage("email 인증", message, to=[destination])
        email.send()

    def thread_maker(self, message, destination):
        thread = threading.Thread(
            target=self.email_sender, args=(message, destination))
        thread.start()


class ONEUserInfoSerializer(ModelSerializer):
    class Meta:
        model = ONEUser
        fields = ("id", "username", 'email', 'profile_image', 'fcm_id',
                  'score', 'phone_number', 'group_joined', 'user_goal')

    def to_representation(self, instance):
        represent = super().to_representation(instance)
        userkeywords = UserKeyWord.objects.filter(
            user_pk=instance.id)
        represent['keywords'] = [
            value.keyword_pk.word for value in userkeywords]
        return represent

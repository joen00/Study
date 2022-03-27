from agora.models import *
from django.db.models import fields
from django.db.models.base import Model
from django.utils import timezone

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, BaseSerializer, Serializer

from .models import *
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


# retrive room list
class ClassRoomBasicSerializer(ModelSerializer):
    class Meta:
        model = ClassRoomBasic
        fields = "__all__"

    def to_representation(self, instance):
        represent = super().to_representation(instance)  # classRoombasic
        represent.pop('password')
        return represent

    def create(self, validated_data):
        new_room = ClassRoomBasic.objects.create(**validated_data)
        owner: ONEUser = validated_data['owner']
        owner.group_joined += str(new_room.pk) + ","
        owner.save()
        # onwer's group entity
        Group.objects.create(user_pk=owner, classroombasic_pk=new_room,
                             introduction='owner', state=1, season=1, date_join=timezone.now())
        print(Group)
        # create room info
        info_data = self.initial_data['info']
        new_room_info = ClassRoomInfo.objects.create(
            classroombasic_pk=new_room, **info_data)
        return new_room


# classroom info
class ClassRoomInfoSerializer(ModelSerializer):
    class Meta:
        model = ClassRoomInfo
        fields = "__all__"
        read_only_fields = ['user_count', 'main_goal',
                            'season', 'date_renew', 'total_money']

    def days_handler(self, input):
        data = input.split(',')
        result = []
        for value_s in data:
            value_i = int(value_s)
            if value_i == 0:
                result.append("일")
            if value_i == 1:
                result.append("월")
            if value_i == 2:
                result.append("화")
            if value_i == 3:
                result.append("수")
            if value_i == 4:
                result.append("목")
            if value_i == 5:
                result.append("금")
            if value_i == 6:
                result.append("토")
        return result

    def to_representation(self, instance):
        represent = super().to_representation(instance)
        basic_data = dict(ClassRoomBasicSerializer(
            instance.classroombasic_pk).data)
        for key, value in basic_data.items():
            if key == "id":
                represent['basic_id'] = value
            else:
                represent[key] = value
        roomkeywords = RoomKeyWord.objects.filter(
            room_pk=instance.classroombasic_pk)
        represent['keywords'] = [
            value.keyword_pk.word for value in roomkeywords]
        represent['meeting_days'] = self.days_handler(
            represent['meeting_days'])
        return represent

    def update(self, instance, validated_data):
        # 시즌별 기간 설정 validation 확인
        period_renew = validated_data.get('period_renew', -1)
        if period_renew != -1:
            old_start_season = instance.date_renew
            new_start_season = old_start_season + \
                timezone.timedelta(days=period_renew)
            limit_date = old_start_season + timezone.timedelta(days=7)
            now_date = timezone.now()
            #  시즌 변경은 새 시즌 이후 7일 이내로만 변경 가능
            if now_date <= new_start_season and limit_date >= now_date:
                instance.period_renew = period_renew
                instance.save()
            else:
                raise Exception("invalid days")

        # 시즌별 입장료  validation 확인
        entrance_fee = validated_data.get('enterence_fee', -1)
        if entrance_fee >= 0:
            old_start_season = instance.date_renew
            limit_date = old_start_season + timezone.timedelta(days=7)
            now_date = timezone.now()
            print(limit_date > now_date)
            #  입장료 변경은 새 시즌 이후 7일 이내로만 변경 가능
            if limit_date >= now_date:
                instance.enterence_fee = entrance_fee
                # instance.save()
        else:
            raise Exception("invalid days")
        return super().update(instance, validated_data)


class EventSerializer(ModelSerializer):
    class Meta:
        model = StudyEvent
        fields = '__all__'


class chatSerializer(ModelSerializer):
    class Meta:
        model = ChatHistory
        fields = "__all__"

    def to_representation(self, instance):
        represent = super().to_representation(instance)
        user = ONEUser.objects.get(id=represent['user_pk'])
        represent['username'] = user.username
        return represent


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class RoomFileSerializer(ModelSerializer):
    class Meta:
        model = RoomFile
        fields = "__all__"

    def to_representation(self, instance):
        represent = super().to_representation(instance)
        # return represent
        file_url = represent['file'].split("/")[-2:]
        represent['file'] = "/main/room/file/" + '/'.join(file_url)
        return represent


class AttendtionSerializer(ModelSerializer):
    class Meta:
        model = Attendtion
        fields = "__all__"

    def to_representation(self, instance):
        represent = super().to_representation(instance)
        v = represent['group_user']
        group = Group.objects.get(id=v)
        user = ONEUser.objects.get(id=group.user_pk.id)
        represent['user_pk'] = user.id
        represent['user_name'] = user.username
        represent.pop('group_user')
        return represent


class SurveyEntrySerializer(ModelSerializer):
    class Meta:
        model = surveyEntry
        fields = "__all__"


class GroupUserListSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"

    def to_representation(self, instance):
        represent = super().to_representation(instance)
        represent['name'] = instance.user_pk.username
        return represent


class InterestSerializer(ModelSerializer):
    class Meta:
        model = UserInterest
        fields = "__all__"

from agora.models import ONEUser, StudyEvent
from django.db import models
from django.db.models import base
from django.core.validators import MinValueValidator, MaxValueValidator

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

# ClassRoomBasic table model


class ClassRoomBasic(models.Model):
    # if user-delete ClassRoomBasic delete?
    owner = models.ForeignKey(
        ONEUser, on_delete=models.CASCADE, blank=False, null=False)
    password = models.CharField(max_length=20, blank=True, null=True)
    date_register = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50, blank=False, null=False)
    score = models.FloatField(default=0, blank=True)


class ClassRoomInfo(models.Model):
    classroombasic_pk = models.OneToOneField(
        ClassRoomBasic, on_delete=models.CASCADE, blank=False, null=False)
    explain = models.TextField()
    main_image = models.ImageField(upload_to='profile', null=True, blank=True)
    grace_period = models.PositiveSmallIntegerField(
        default=14, blank=True, null=False)  # 유예기간 - days
    max_user_count = models.IntegerField(default=5, blank=True, null=False)
    user_count = models.IntegerField(default=1, blank=True, null=False)
    main_goal = models.TextField(blank=False, null=False)
    season = models.IntegerField(default=1, blank=True, null=False)
    date_renew = models.DateTimeField(
        auto_now_add=True, blank=True, null=False)  # 시작 날짜
    period_renew = models.IntegerField(validators=[MinValueValidator(
        14)], default=30, blank=True, null=False)  # default 유예기간과 동일 시즌별 지속 기간
    enterence_fee = models.IntegerField(
        validators=[MinValueValidator(0)], default=0, blank=True, null=False)
    total_money = models.IntegerField(
        validators=[MinValueValidator(0)], default=0, blank=True, null=False)
    meeting_days = models.CharField(max_length=255, blank=True, null=True)
    meeting_times = models.CharField(max_length=255, blank=True, null=True)
    penalty = models.IntegerField(validators=[MinValueValidator(
        0), MaxValueValidator(100)], default=0, blank=True, null=False)


# ClassRoomBasic 참여자/희망자 관련
# season 별로 업데이트 하도록 했으나 추후 변경 가능
class Group(models.Model):
    user_pk = models.ForeignKey(
        ONEUser, on_delete=models.CASCADE, blank=False, null=False)
    classroombasic_pk = models.ForeignKey(
        ClassRoomBasic, on_delete=models.CASCADE, blank=False, null=False)
    introduction = models.TextField(null=True, blank=True)
    # 0-request 1-accepted 2 - denyed 3-leave
    state = models.IntegerField(default=0)
    season = models.IntegerField(default=1)
    fee_submission = models.BooleanField(default=False)
    date_join = models.DateTimeField(null=True, blank=True)
    date_leave = models.DateTimeField(null=True, blank=True)


class ChatHistory(models.Model):
    user_pk = models.ForeignKey(
        ONEUser, on_delete=models.SET_DEFAULT, default="unknown", blank=False, null=False)
    classroombasic_pk = models.ForeignKey(
        ClassRoomBasic, on_delete=models.CASCADE, blank=False, null=False)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

# pk를 이용한 file path 이용시


def image_path(instance, filename):
    print
    return '/'.join([str(instance.classroombasic_pk.id), filename])


class RoomFile(models.Model):
    classroombasic_pk = models.ForeignKey(
        ClassRoomBasic, on_delete=models.CASCADE, blank=False, null=False)
    user_pk = models.ForeignKey(ONEUser, on_delete=models.SET_DEFAULT,
                                default="unknown", blank=False, null=False)  # delete protect
    file = models.FileField(upload_to=image_path, blank=True, null=True)
    title = models.CharField(max_length=255)
    attribute = models.CharField(max_length=255)
    correct = models.BooleanField(blank=True, null=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)


class Attendtion(models.Model):
    event = models.ForeignKey(
        StudyEvent, on_delete=models.SET_DEFAULT, default="unknown",)
    classroombasic_pk = models.ForeignKey(
        ClassRoomBasic, on_delete=models.CASCADE)
    group_user = models.ForeignKey(
        Group, on_delete=models.CASCADE, blank=False, null=False)
    content = models.CharField(max_length=255, null=True, blank=True)
    attendance = models.BooleanField(default=False, null=False, blank=True)

# ClassRoomBasic-score table model


class ClassRoomScore(models.Model):
    classroombasic_pk = models.ForeignKey(
        ClassRoomBasic, on_delete=models.CASCADE, blank=False, null=False)
    evaluator_pk = models.ForeignKey(ONEUser, on_delete=models.SET(
        "deleted_user"), blank=False, null=False)
    score = models.PositiveIntegerField(blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True)


class surveyEntry(models.Model):
    content = models.TextField()

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import CharField, IntegerField
#from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator

from django.dispatch import receiver
from django.db.models.signals import post_save


import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


# custom user model
class ONEUser(AbstractUser):
    profile_image = models.ImageField(
        upload_to='profile', blank=True, null=True)
    fcm_id = models.CharField(
        max_length=254, null=True, blank=True, default='EMPTY')
    group_joined = models.TextField(default=" ", blank=True)
    user_goal = models.TextField(null=True, blank=True)
    score = models.IntegerField(default=0)
    phone_number = IntegerField(blank=True, null=True)


# 계정 생성시 is_active 비활성화
@receiver(post_save, sender=ONEUser)
def user_to_inactive(sender, instance, created, update_fields, **kwargs):
    if created:
        instance.is_active = False


# money history table
class UserMoney(models.Model):
    user_pk = models.ForeignKey(
        ONEUser, on_delete=models.CASCADE, blank=False, null=False)
    date_commit = models.DateTimeField(auto_now_add=True)
    payment = models.PositiveIntegerField(blank=False, null=False)
    attribute = models.BooleanField(blank=False, null=False)
    total_money = models.PositiveIntegerField()

# key word table


class Keyword(models.Model):
    word = models.CharField(max_length=50)

# user-keyword table


class UserKeyWord(models.Model):
    user_pk = models.ForeignKey(
        ONEUser, on_delete=models.CASCADE, blank=False, null=False)
    keyword_pk = models.ForeignKey(
        Keyword, on_delete=models.CASCADE, blank=False, null=False)


# room-keyword table
class RoomKeyWord(models.Model):
    room_pk = models.ForeignKey(
        'classroom.ClassRoomBasic', on_delete=models.CASCADE, blank=False, null=False)
    keyword_pk = models.ForeignKey(
        Keyword, on_delete=models.CASCADE, blank=False, null=False)

# user-room-interesting table


class UserInterest(models.Model):
    user_pk = models.ForeignKey(
        ONEUser, on_delete=models.CASCADE, blank=False, null=False)
    room_pk = models.ForeignKey(
        'classroom.ClassRoomBasic', on_delete=models.CASCADE, blank=False, null=False)
    is_on = models.BooleanField(default=True, null=False, blank=True)
    date_set = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)


class StudyEvent(models.Model):
    user_pk = models.ForeignKey(ONEUser, on_delete=models.CASCADE)
    room_pk = models.ForeignKey(
        'classroom.ClassRoomBasic', on_delete=models.CASCADE, related_name='sub_goals')
    title = models.CharField(max_length=50, blank=False, null=False)
    explain = models.TextField()
    attribute = models.SmallIntegerField(blank=False, null=False)
    # attribute ==> sub_goal / homework /meeting / other(import day)
    #                 1           2         3         4
    date_start = models.DateTimeField(blank=True, null=True)
    date_end = models.DateTimeField(blank=True, null=True)


class UserScore(models.Model):
    rater_pk = models.ForeignKey(ONEUser, on_delete=models.SET(
        "deleted_user"), blank=False, null=False, related_name='rater_pk')
    ratee_pk = models.ForeignKey(ONEUser, on_delete=models.SET(
        "deleted_user"), blank=False, null=False, related_name='ratee_pk')
    classroom_pk = IntegerField()
    score = models.PositiveIntegerField(blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True)

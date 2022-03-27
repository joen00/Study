from classroom.models import Group, ClassRoomInfo, Attendtion
from agora.models import ONEUser
from django.utils import timezone
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


def get_user_group(guestpk):
    guest: ONEUser = ONEUser.objects.get(id=guestpk)
    # if group not exist
    if len(guest.group_joined) == 1:
        return [], None
    else:
        groups = [v.strip() for v in guest.group_joined.split(',')]
        groups = list(map(int, groups[:-1]))
        return groups, guest


def is_guest_in_classroom(guestpk, classroompk):
    groups, _ = get_user_group(guestpk)
    if classroompk in groups:
        return True
    else:
        return False


def leave_classroom(one_user: ONEUser, roompk: int, groups: list):
    try:  # 0-request   1-accepted   2-denyed  3-leave
        groups.remove(roompk)
        ret = " "
        for value in groups:
            ret += str(value)
            ret += ","
        one_user.group_joined = ret
        one_user.save()

        classinfo: ClassRoomInfo = ClassRoomInfo.objects.get(
            classroombasic_pk=roompk)
        group: Group = Group.objects.get(
            user_pk=one_user, classroombasic_pk=roompk, season=classinfo.season)
        group.state = 3
        group.date_leave = timezone.now()
        group.save()
        return True
    except:
        return False


def join_classroom(one_use: ONEUser, group: Group, roompk: int, is_allow: int, season: int):
    try:  # 0-request   1-accepted   2-denyed  3-leave
        if is_allow == 1:
            one_use.group_joined += str(roompk) + ","
            group.state = 1
            group.season = season
            group.date_join = timezone.now()
        else:
            group.state = 2

        group.save()
        one_use.save()

        return True
    except:
        return False


def attendtion_add_of_event(classroom, event_obj):
    try:
        # get latest season
        roominfo_obj: ClassRoomInfo = ClassRoomInfo.objects.get(
            classroombasic_pk=classroom)
        cur_season = roominfo_obj.season
        # 참여 인원 리스트
        users = Group.objects.filter(
            classroombasic_pk=classroom, season=cur_season, state=1)
        for user in users:
            Attendtion.objects.create(
                event=event_obj, classroombasic_pk=classroom, group_user=user)
        return True
    except Exception as e:
        return False

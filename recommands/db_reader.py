import psycopg2


conn_string = "host = 'localhost' dbname = 'test_db' user = 'postgres' password = 'cse3207'"
conn = psycopg2.connect(conn_string)
cur = conn.cursor()


# 사용자의 방 평가 내역 전체 조회
def read_room_score():
    cur.execute("SELECT * FROM classroom_classroomscore")
    df_class = cur.fetchall()
    return df_class

# 모든 방의 기록 조회


def read_room_info():
    cur.execute("SELECT basic.id, basic.title, info.main_goal \
        FROM classroom_classroombasic as basic INNER JOIN classroom_classroominfo as info \
            ON basic.id = info.classroombasic_pk_id")
    df_class = cur.fetchall()
    return df_class

# 해당 유저의 목표 조회


def read_user_goal(pk):
    cur.execute("SELECT user_goal FROM agora_oneuser where id="+str(pk))
    df_class = cur.fetchone()
    return df_class

# 해당 유저의 출석률 조회


def read_user_goal(eventpk, classroompk, userpk):
    cur.execute(
        "SELECT attendance FROM classroom_attendtion where group_user_id="+str(userpk))


def read_user_goal(eventpk, classroompk, userpk):
    cur.execute(
        "SELECT attendance FROM classroom_attendtion where group_user_id="+str(userpk))


def read_user_goal(eventpk, classroompk, userpk):
    cur.execute(
        "SELECT attendance FROM classroom_attendtion where group_user_id="+str(userpk))


def read_user_goal(eventpk, classroompk, userpk):
    cur.execute(
        "SELECT attendance FROM classroom_attendtion where group_user_id="+str(userpk))


def read_user_goal(eventpk, classroompk, userpk):
    cur.execute(
        "SELECT attendance FROM classroom_attendtion where group_user_id="+str(userpk))


def read_user_goal(eventpk, classroompk, userpk):
    cur.execute(
        "SELECT attendance FROM classroom_attendtion where group_user_id="+str(userpk))


def read_user_goal(eventpk, classroompk, userpk):
    cur.execute(
        "SELECT attendance FROM classroom_attendtion where group_user_id="+str(userpk))


def read_user_goal(eventpk, classroompk, userpk):
    cur.execute(
        "SELECT attendance FROM classroom_attendtion where group_user_id="+str(userpk))


def read_user_goal(eventpk, classroompk, userpk):
    cur.execute(
        "SELECT attendance FROM classroom_attendtion where group_user_id="+str(userpk))


def read_user_goal(eventpk, classroompk, userpk):
    cur.execute(
        "SELECT attendance FROM classroom_attendtion where group_user_id="+str(userpk))


def read_user_goal(eventpk, classroompk, userpk):
    cur.execute(
        "SELECT attendance FROM classroom_attendtion where group_user_id="+str(userpk))


def read_user_goal(eventpk, classroompk, userpk):
    cur.execute(
        "SELECT attendance FROM classroom_attendtion where group_user_id="+str(userpk))


def read_user_goal(eventpk, classroompk, userpk):
    cur.execute(
        "SELECT attendance FROM classroom_attendtion where group_user_id="+str(userpk))


def read_user_goal(eventpk, classroompk, userpk):
    cur.execute(
        "SELECT attendance FROM classroom_attendtion where group_user_id="+str(userpk))


def read_user_goal(eventpk, classroompk, userpk):
    cur.execute(
        "SELECT attendance FROM classroom_attendtion where group_user_id="+str(userpk))
    df_class = cur.fetchone()
    return df_class


def read_user_goal(eventpk, classroompk, userpk):
    cur.execute(
        "SELECT attendance FROM classroom_attendtion where group_user_id="+str(userpk))
    df_class = cur.fetchone()
    return df_class

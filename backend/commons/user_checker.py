from setting.public_set import SECRET_KEY
import jwt
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


def checkIdentity(request, pk):
    access_token = request.META['HTTP_AUTHORIZATION'].split(" ")[1]
    userInfo = jwt.decode(access_token, SECRET_KEY, algorithm='HS256')
    jwt_pk = userInfo['user_id']
    if isinstance(pk, str):
        pk = int(pk)
    if jwt_pk == pk:
        return True
    else:
        return False


def getIdentity(request):
    try:
        access_token = request.META['HTTP_AUTHORIZATION'].split(" ")[1]
        userInfo = jwt.decode(access_token, SECRET_KEY, algorithm='HS256')
        jwt_pk = userInfo['user_id']
        return jwt_pk
    except Exception as e:
        return -1

from datetime import datetime

import jwt
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication


ALGORITHM = 'HS256'


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        token = request.META.get(settings.AUTHORIZATION_HEADER)

        if token is None:
            return None
        try:
            id = jwt.decode(token, settings.SECRET_KEY_JWT, algorithms=[ALGORITHM]).get('id')
            user = User.objects.get(id=id)
            return user, None
        except:
            raise exceptions.AuthenticationFailed('Invalid token')

    def generate_token(self, user):
        payload = {'id': user.id, "nbf": datetime.utcnow()}
        return jwt.encode(payload, settings.SECRET_KEY_JWT, algorithm=ALGORITHM)

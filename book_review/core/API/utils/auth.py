import uuid
import datetime
from core.models import User
from ninja.security import HttpBearer
from config.settings import REDIS_URL, SECRET_KEY
from jose import jwt
from django.utils import timezone
from core.API.utils.tokens import token_in_redis
from django.core.cache import caches
import logging
from ninja.security import APIKeyHeader

logger = logging.getLogger("db")


def generate_tokens(user: User) -> dict:
    current_time = datetime.datetime.now(tz=datetime.timezone.utc)
    claims = {
        "sub": f"{user.id}",
        "email": f"{user.email}",
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_staff": user.is_staff,
        "is_superuser": user.is_superuser,
        "exp": current_time + timezone.timedelta(minutes=20),
        "iat": current_time,
        "type": "access",
    }
    access_token = jwt.encode(claims, SECRET_KEY)
    refresh_claims = claims.copy()
    refresh_claims.update(
        {"exp": current_time + timezone.timedelta(hours=12), "type": "refresh"}
    )
    refresh_token = jwt.encode(refresh_claims, SECRET_KEY)
    for key in ["exp", "iat", "type"]:
        claims.pop(key, None)
    return {"access": access_token, "refresh": refresh_token, "claims": claims}


class AuthBearer(HttpBearer):
    def __init__(self, *args, **kwargs) -> None:
        self._cache = caches["user"]
        super().__init__(*args, **kwargs)

    def _get_cached_user(self, user_id: uuid.UUID):
        try:
            cached_user = self._cache.get(user_id)
            if cached_user is not None and isinstance(cached_user, User):
                return cached_user
        except Exception as e:
            logger.error(f"get_cached_user: {e}")
        user = User.objects.get(id=user_id)
        self._cache.set(user_id, user)
        return user

    def authenticate(self, request, token):
        try:
            decoded_token = jwt.decode(token, SECRET_KEY)
            if decoded_token["type"] != "access":
                raise Exception("Token must be access type")
            user_id = uuid.UUID(decoded_token["sub"])
            if token_in_redis(token):
                raise Exception("Revoked Token!")
            request.user = self._get_cached_user(user_id)
            request.is_authenticated = True
            return decoded_token
        except Exception as e:
            logger.error(f"{e}")
            request.user = None
            request.is_authenticated = False
            return None

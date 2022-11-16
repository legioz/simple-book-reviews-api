from django.core.cache import cache
from config.settings import REDIS_URL, SECRET_KEY
from jose import jwt
from django.core.cache import caches
from core.models import User
from django.utils import timezone
import secrets


def generate_session_token(user: User) -> dict:
    claims = {
        "sub": f"{user.id}",
        "key": f"{secrets.token_urlsafe()}",
        "iat": timezone.now(),
    }
    session_key = jwt.encode(claims, SECRET_KEY, "HS512")
    return session_key


def revoke_token(token: str) -> None:
    try:
        token = jwt.decode(token, SECRET_KEY)
        # TODO aplicar expire time nos tokens
        if token:
            cache.set(token["sub"], token)
    except Exception as e:
        pass


def token_in_redis(token: str) -> bool:
    try:
        sub = jwt.decode(token, SECRET_KEY)["sub"]
        if cache.get(sub):
            return True
        return False
    except:
        return False

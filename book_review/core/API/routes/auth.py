from core.models import User
from ninja import Router
from core.API.schemas import auth as schemas
from config.settings import SECRET_KEY
from jose import jwt
import uuid
from core.API.utils.auth import generate_tokens
from core.API.utils.tokens import (
    revoke_token,
    token_in_redis,
)
from django.db.models import Q
import logging

logger = logging.getLogger("db")
router = Router()


@router.post(
    "token/",
    response={200: schemas.JWTPairSchema, 401: schemas.ResponseOut},
    auth=None,
)
def get_tokens_and_user_claims(request, auth: schemas.AuthSchema):
    """
    Endpoint to generate access & refresh tokens and return the current user claims.
    """
    try:
        user = User.objects.get(Q(email=auth.email))
        if not user.is_active:
            return 401, {
                "detail": "User must be activated! Check the email for the token."
            }
        if user.login_attempts > 10:
            return 401, {
                "detail": "Reached the maximum authentication attempts, reset the password"
            }
        if not user.check_password(auth.password):
            user.set_login_attempt()
            return 401, {"detail": "Invalid credentials!"}
        jwt_token_pair = generate_tokens(user)
        user.reset_login_attempts()
        return 200, jwt_token_pair
    except Exception as e:
        logger.exception(e)
        return 401, {"detail": "Invalid credentials!"}


@router.post(
    "refresh/",
    response={200: dict, 401: schemas.ResponseOut},
    auth=None,
)
def get_new_access_token(request, token: schemas.RefreshToken):
    """
    Endpoint to generate new access token sending the current active refresh token on payload
    """
    try:
        if token_in_redis(token.refresh):
            raise Exception("Token is blacklisted")
        decoded_token = jwt.decode(token.refresh, SECRET_KEY)
        if decoded_token["type"] != "refresh":
            raise Exception("Token must be refresh type")
        user = User.objects.get(id=uuid.UUID(decoded_token["sub"]))
        jwt_token_pair = generate_tokens(user)
        return 200, {"access": jwt_token_pair.get("access")}
    except Exception as e:
        logger.exception(e)
        return 401, {"detail" "Token is revoked!"}


@router.delete("revoke/", response={200: schemas.ResponseOut}, auth=None)
def revoke_tokens(request, token: schemas.AuthTokens):
    """
    Endpoint to revoke tokens
    """
    try:
        revoke_token(token.refresh)
        revoke_token(token.access)
    except Exception as e:
        pass
    finally:
        return 200, {"detail": "Token revoked!"}

from ninja import Schema
from pydantic import EmailStr


class AuthSchema(Schema):
    email: str
    password: str


class JWTPairSchema(Schema):
    refresh: str
    access: str
    claims: dict


class RefreshToken(Schema):
    refresh: str


class AuthTokens(RefreshToken):
    access: str


class ResponseOut(Schema):
    detail: str = None


class EmailSchemaMixin(Schema):
    email: EmailStr


class ErrorsOut(Schema):
    errors: dict[str, list[str]]


class ResetPasswordIn(Schema):
    password: str

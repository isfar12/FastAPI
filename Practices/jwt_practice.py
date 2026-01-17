from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import timedelta, datetime, timezone

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return password_context.hash(password)


def verify_password(password: str, has: str):
    return password_context.verify(password, hash)


def create_acess_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc)+(timedelta(minutes=30)
                                         if expires_delta is None else expires_delta)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, "secretkey", "HS256")
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token=token, key="secretkey",
                             algorithms=["HS256"])
        return payload
    except JWTError:
        return None



password = create_acess_token({"sub":"isfar"})
decoded = decode_access_token(password)
print(decoded)

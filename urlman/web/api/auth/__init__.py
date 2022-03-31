from datetime import datetime, timedelta

from jwt.api_jwt import decode, encode

from urlman.settings import settings


class JWTAuth:
    """JWT authentication class."""

    secret = settings.jwt_secret
    exp = settings.jwt_expires
    iss = settings.jwt_iss
    algorithm = settings.jwt_alg

    def encode_token(self, username: str) -> str:
        """Encode payload to JWT."""
        payload = {
            "exp": datetime.utcnow() + timedelta(self.exp),
            "iat": datetime.utcnow(),
            "iss": self.iss,
            "scope": "access_token",
            "sub": username,
        }
        return encode(
            payload=payload,
            key=self.secret,
            algorithm=self.algorithm,
        )

    def decode_token(self, token: str) -> str:
        """Decode JWT to payload."""
        payload = decode(
            jwt=token,
            key=self.secret,
            algorithms=[self.algorithm],
        )
        return payload.get("sub")


jwt_auth = JWTAuth()

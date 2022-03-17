from passlib.hash import sha256_crypt

from urlman.settings import settings


def hash_password(password: str) -> str:
    """
    Hashing password.

    @param password:
    @return: hashed password
    """
    salted_password = password + settings.hash_salt
    return sha256_crypt.hash(salted_password)


def verify_password(db_password: str, verifiable_password: str) -> bool:
    """
    Verifying entered password.

    @param db_password: user password hash
    @param verifiable_password: comparison password
    @return: password match
    """
    verifiable_password = verifiable_password + settings.hash_salt
    return sha256_crypt.verify(verifiable_password, db_password)

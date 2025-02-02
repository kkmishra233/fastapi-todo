import base64
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import requests
from models.user import User
from core.config import settings
from services.user import get_or_create_user
from services.group import get_or_create_group
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from schemas.user import UserCreate
from schemas.group import GroupCreate

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
ALGORITHMS = ["RS256"]

async def get_public_key(kid):
    JWKS_URI=f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/certs"
    response = requests.get(JWKS_URI)
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching keys from Keycloak: {response.text}"
        )
    try:
        data = response.json()
        keys = data.get("keys", [])
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Invalid JSON response from Keycloak"
        )
    for key in keys:
        if key["kid"] == kid and key["alg"] in ALGORITHMS:
            return key
    raise ValueError("Matching public key not found")


async def construct_rsa_public_key(n: str, e: str):
    """Construct an RSA public key from its modulus and exponent."""
    n_bytes = int.from_bytes(base64.urlsafe_b64decode(n + "==="), "big")
    e_bytes = int.from_bytes(base64.urlsafe_b64decode(e + "==="), "big")
    public_numbers = rsa.RSAPublicNumbers(e_bytes, n_bytes)
    public_key = public_numbers.public_key(default_backend())
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

async def get_current_user(token: str = Depends(oauth2_scheme),authorization: str | None = Header(None)) -> User:
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header"
        )
    try:
        headers = jwt.get_unverified_header(token)
        public_key_data = await get_public_key(headers["kid"])
        public_key_pem = await construct_rsa_public_key(public_key_data["n"], public_key_data["e"])
        token_info = jwt.decode(token, public_key_pem, algorithms=ALGORITHMS, audience=settings.KEYCLOAK_AUDIENCE)
        username = token_info.get("preferred_username")
        groups = token_info.get("groups", [])
        user, created = await get_or_create_user(UserCreate(username=username))

        group_objs = []
        for group_path in groups:
            group_parts = [x for x in group_path.split("/") if x != ""]
            for part in group_parts:
                group, _ = await get_or_create_group(GroupCreate(name=part))
                if group not in group_objs:
                    group_objs.append(group)

        await user.groups.add(*group_objs)
        return user
    except JWTError as ex:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(ex)
        )

def has_group(group: str):
    async def depends(user: User = Depends(get_current_user)):
        await user.fetch_related('groups')
        if not any(g.name == group for g in user.groups):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User does not have the required group"
            )
        return user
    return depends


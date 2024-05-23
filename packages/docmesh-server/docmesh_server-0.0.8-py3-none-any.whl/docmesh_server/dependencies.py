from pydantic import BaseModel

from fastapi import status, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from docmesh_core.db.auth import get_entity_from_auth
from docmesh_server.database import engine

auth_scheme = HTTPBearer()


class EntityInfo(BaseModel):
    entity_name: str


def check_access_token(
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
) -> EntityInfo:
    access_token = token.credentials

    if (entity_name := get_entity_from_auth(engine, access_token)) is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect bearer token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    entity_info = EntityInfo(entity_name=entity_name)

    return entity_info


def check_admin_access_token(
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
) -> None:
    access_token = token.credentials

    if get_entity_from_auth(engine, access_token) != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect bearer token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

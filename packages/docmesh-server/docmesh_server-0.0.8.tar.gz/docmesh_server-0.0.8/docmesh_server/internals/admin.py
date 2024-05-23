from typing import Any
from pydantic import BaseModel

from fastapi import status, APIRouter, Response, Depends

from docmesh_core.db.neo import add_entity, DuplicateEntity
from docmesh_core.db.auth import add_auth_for_entity
from docmesh_server.database import engine
from docmesh_server.dependencies import check_admin_access_token

router = APIRouter(prefix="/admin", dependencies=[Depends(check_admin_access_token)])


class EntityBody(BaseModel):
    entity_name: str


@router.post("/add_entity")
def add_entity_api(
    body: EntityBody,
    response: Response,
) -> dict[str, Any]:
    try:
        add_entity(entity_name=body.entity_name)
        access_token = add_auth_for_entity(engine, entity_name=body.entity_name)

        data = {
            "entity_name": body.entity_name,
            "access_token": access_token,
            "msg": f"Successfully add a new entity {body.entity_name}.",
        }
    except DuplicateEntity:
        response.status_code = status.HTTP_405_METHOD_NOT_ALLOWED
        data = {
            "msg": f"Failed to add a new entity, {body.entity_name} already existed.",
        }
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        data = {
            "msg": f"Failed to add a new entity {body.entity_name}, with error {e}.",
        }

    return {"data": data}

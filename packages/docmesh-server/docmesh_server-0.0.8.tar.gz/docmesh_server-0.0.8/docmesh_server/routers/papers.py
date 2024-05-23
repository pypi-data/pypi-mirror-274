from typing import Any
from pydantic import BaseModel

from fastapi import status, APIRouter, Response, Depends

from docmesh_core.utils.semantic_scholar import get_paper_id
from docmesh_core.db.neo import _add_paper, mark_paper_read
from docmesh_server.dependencies import check_access_token, EntityInfo

router = APIRouter(prefix="/papers")


class PaperBody(BaseModel):
    paper: str


@router.post("/add")
def add_paper_api(
    body: PaperBody,
    response: Response,
    entity_info: EntityInfo = Depends(check_access_token),
) -> dict[str, Any]:
    semantic_scholar_paper_id = get_paper_id(body.paper)

    if semantic_scholar_paper_id is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        data = {
            "msg": f"Failed to add a new paper {body.paper}, cannot find semantic scholar paper id.",
        }
    else:
        try:
            paper_id = _add_paper(paper_id=semantic_scholar_paper_id).paper_id
            data = {
                "msg": f"Successfully add a new paper {body.paper} with paper id {paper_id}.",
            }
        except Exception as e:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            data = {
                "msg": f"Failed to add a new paper {body.paper}, with error: {e}.",
            }

    return {"data": data}


@router.post("/add_and_mark")
def add_and_mark_paper_api(
    body: PaperBody,
    response: Response,
    entity_info: EntityInfo = Depends(check_access_token),
) -> dict[str, Any]:
    entity_name = entity_info.entity_name
    semantic_scholar_paper_id = get_paper_id(body.paper)

    if semantic_scholar_paper_id is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        data = {
            "msg": f"Failed to add and mark paper {body.paper}, cannot find semantic scholar paper id.",
        }
    else:
        try:
            paper_id = _add_paper(paper_id=semantic_scholar_paper_id).paper_id
            mark_paper_read(entity_name=entity_name, paper_id=paper_id)
            data = {
                "msg": (
                    f"Successfully add and mark paper {body.paper} read with paper id {paper_id} for {entity_name}."
                ),
            }
        except Exception as e:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            data = {
                "msg": f"Failed to add and mark paper {body.paper} read with error: {e}.",
            }

    return {"data": data}

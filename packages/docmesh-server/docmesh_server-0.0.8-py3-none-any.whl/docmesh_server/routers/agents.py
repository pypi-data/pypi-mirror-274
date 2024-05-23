from typing import Any
from pydantic import BaseModel

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from docmesh_agent.agent import execute_docmesh_agent, aexecute_docmesh_agnet
from docmesh_server.dependencies import check_access_token, EntityInfo

router = APIRouter(prefix="/agents")


class AgentBody(BaseModel):
    session_id: str
    query: str


@router.post("/execute")
def execute_docmesh_agent_api(
    body: AgentBody,
    entity_info: EntityInfo = Depends(check_access_token),
) -> dict[str, Any]:
    msg = execute_docmesh_agent(
        entity_name=entity_info.entity_name,
        query=body.query,
        session_id=body.session_id,
    )
    data = {"query": body.query, "msg": msg}
    return {"data": data}


@router.post("/aexecute")
async def aexecute_docmesh_agnet_api(
    body: AgentBody,
    entity_info: EntityInfo = Depends(check_access_token),
) -> StreamingResponse:
    return StreamingResponse(
        aexecute_docmesh_agnet(
            entity_name=entity_info.entity_name,
            query=body.query,
            session_id=body.session_id,
        )
    )

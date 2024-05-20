import os
import uuid

from typing import Any
from pydantic import BaseModel

from neomodel import config
from sqlalchemy import create_engine
from fastapi import status, Depends, HTTPException, Response, FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from docmesh_core.utils.semantic_scholar import get_paper_id
from docmesh_core.db.neo import add_entity, _add_paper, mark_paper_read, DuplicateEntity
from docmesh_core.db.neo import add_collection, add_paper_to_collection
from docmesh_core.db.auth import get_entity_from_auth, add_auth_for_entity
from docmesh_agent.agent import execute_docmesh_agent, aexecute_docmesh_agnet
from docmesh_agent.embeddings.embeddings import update_paper_embeddings

if (neo4j_url := os.getenv("NEO4J_URL")) is None:
    raise ValueError("You have not set neo4j database url using environment `NEO4J_URL`.")
else:
    config.DATABASE_URL = neo4j_url
    # HACK: server may kill idle connection, to avoid being hung for
    # a long time, we kill the connection first, the max lifetime
    # should be less then 4 mins (240 seconds)
    config.MAX_CONNECTION_LIFETIME = 200

if (mysql_url := os.getenv("MYSQL_URL")) is None:
    raise ValueError("You have to set mysql database url using environment `MYSQL_URL`.")
else:
    engine = create_engine(mysql_url)

app = FastAPI()
# cors
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# authentication
auth_scheme = HTTPBearer()


class AddEntityBody(BaseModel):
    entity_name: str


class AddCollectionBody(BaseModel):
    collection_name: str


class AddCollectionPaperBody(BaseModel):
    collection_name: str
    paper: str


class AddPaperBody(BaseModel):
    paper: str


class MarkPaperBody(BaseModel):
    paper_id: str


class AddAndMarkPaperBody(BaseModel):
    paper: str


class AgentBody(BaseModel):
    session_id: str
    query: str


def _check_access_token(access_token: str) -> str:
    if (entity_name := get_entity_from_auth(engine, access_token)) is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return entity_name


def _check_admin_access_token(access_token: str) -> None:
    if _check_access_token(access_token) != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.post("/login")
def login(
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
) -> dict[str, Any]:
    entity_name = _check_access_token(token.credentials)
    session_id = str(uuid.uuid4())
    data = {"entity_name": entity_name, "session_id": session_id}

    return {"data": data}


@app.post("/add_entity")
def add_entity_api(
    body: AddEntityBody,
    response: Response,
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
) -> dict[str, Any]:
    _check_admin_access_token(token.credentials)

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


@app.post("/add_collection")
def add_collection_api(
    body: AddCollectionBody,
    response: Response,
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
) -> dict[str, Any]:
    _check_admin_access_token(token.credentials)

    try:
        add_collection(collection_name=body.collection_name)
        data = {
            "msg": f"Successfully add a new collection {body.collection_name}.",
        }
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        data = {"msg": f"Failed to add a new collection {body.collection_name}, with error: {e}."}

    return {"data": data}


@app.post("/add_collection_paper")
def add_collection_paper_api(
    body: AddCollectionPaperBody,
    response: Response,
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
) -> dict[str, Any]:
    _check_admin_access_token(token.credentials)

    semantic_scholar_paper_id = get_paper_id(body.paper)

    if semantic_scholar_paper_id is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        data = {
            "msg": f"Failed to add {body.paper} to collection, cannot find semantic scholar paper id.",
        }
    else:
        try:
            paper_id = _add_paper(paper_id=semantic_scholar_paper_id).paper_id
            add_paper_to_collection(paper_id=paper_id, collection_name=body.collection_name)
            data = {
                "msg": f"Successfully add paper {body.paper} to collection {body.collection_name}.",
            }
        except Exception as e:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            data = {
                "msg": f"Failed to add paper {body.paper} to collection {body.collection_name} with error: {e}.",
            }

    return {"data": data}


@app.post("/update_embeddings")
def update_embeddings_api(
    response: Response,
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
) -> dict[str, Any]:
    _check_admin_access_token(token.credentials)

    try:
        update_cnt = update_paper_embeddings()
        data = {
            "msg": f"Successfully update {update_cnt} papers embeddings.",
        }
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        data = {
            "msg": f"Failed to update papers embeddings with error: {e}.",
        }

    return {"data": data}


@app.post("/add_paper")
def add_paper_api(
    body: AddPaperBody,
    response: Response,
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
) -> dict[str, Any]:
    _check_access_token(token.credentials)

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


@app.post("/mark_paper")
def mark_paper_read_api(
    body: MarkPaperBody,
    response: Response,
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
) -> dict[str, Any]:
    entity_name = _check_access_token(token.credentials)

    try:
        mark_paper_read(entity_name=entity_name, paper_id=body.paper_id)
        data = {
            "msg": f"Successfully mark paper {body.paper_id} read for {entity_name}.",
        }
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        data = {
            "msg": f"Failed to mark paper {body.paper_id} with error: {e}.",
        }

    return {"data": data}


@app.post("/add_and_mark_paper")
def add_and_mark_paper_read_api(
    body: AddAndMarkPaperBody,
    response: Response,
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
) -> dict[str, Any]:
    entity_name = _check_access_token(token.credentials)

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


@app.post("/agent")
def execute_docmesh_agent_api(
    body: AgentBody,
    response: Response,
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
) -> dict[str, Any]:
    entity_name = _check_access_token(token.credentials)
    msg = execute_docmesh_agent(
        entity_name=entity_name,
        query=body.query,
        session_id=body.session_id,
    )
    data = {"query": body.query, "msg": msg}
    return {"data": data}


@app.post("/async_agent")
async def aexecute_docmesh_agnet_api(
    body: AgentBody,
    response: Response,
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
) -> StreamingResponse:
    entity_name = _check_access_token(token.credentials)

    return StreamingResponse(
        aexecute_docmesh_agnet(
            entity_name=entity_name,
            query=body.query,
            session_id=body.session_id,
        )
    )

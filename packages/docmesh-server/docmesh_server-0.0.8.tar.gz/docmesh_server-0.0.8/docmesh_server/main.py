import uuid

from typing import Any

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from docmesh_server.routers import papers, agents
from docmesh_server.internals import admin, embeddings, collections, venues
from docmesh_server.dependencies import check_access_token, EntityInfo

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

app.include_router(papers.router)
app.include_router(agents.router)
app.include_router(admin.router)
app.include_router(embeddings.router)
app.include_router(collections.router)
app.include_router(venues.router)


@app.get("/")
def root() -> dict[str, Any]:
    data = {"msg": "Welcome to docmesh!"}
    return {"data": data}


@app.post("/login")
def login(
    entity_info: EntityInfo = Depends(check_access_token),
) -> dict[str, Any]:
    session_id = str(uuid.uuid4())
    data = {"entity_name": entity_info.entity_name, "session_id": session_id}

    return {"data": data}

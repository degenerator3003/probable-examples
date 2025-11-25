
from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from .db import Base, engine, get_db
from . import models, schemas, crud

app = FastAPI(title="FastAPI HTTP Methods Demo")


# Create tables on startup (for demo purposes; in real life use migrations)
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}


# ---------- COLLECTION ROUTES: /items ----------

@app.get("/items", response_model=list[schemas.ItemRead], tags=["items"])
def list_items(db: Session = Depends(get_db)):
    """
    GET: list all items.
    """
    items = crud.get_items(db)
    return items


@app.post(
    "/items",
    response_model=schemas.ItemRead,
    status_code=status.HTTP_201_CREATED,
    tags=["items"],
)
def create_item(item_in: schemas.ItemCreate, db: Session = Depends(get_db)):
    """
    POST: create a new item.
    """
    item = crud.create_item(db, item_in)
    return item


@app.head("/items", tags=["items"])
def head_items(db: Session = Depends(get_db)):
    """
    HEAD: return metadata about items (no body).
    Here we return total count via headers.
    """
    count = len(crud.get_items(db))
    response = Response(status_code=status.HTTP_200_OK)
    response.headers["X-Total-Count"] = str(count)
    return response


@app.options("/items", tags=["items"])
def options_items():
    """
    OPTIONS: return allowed methods for /items.
    """
    response = Response(status_code=status.HTTP_204_NO_CONTENT)
    response.headers["Allow"] = "GET,POST,HEAD,OPTIONS"
    return response


# ---------- SINGLE ITEM ROUTES: /items/{item_id} ----------

@app.get("/items/{item_id}", response_model=schemas.ItemRead, tags=["items"])
def get_item(item_id: int, db: Session = Depends(get_db)):
    """
    GET: retrieve a single item.
    """
    item = crud.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.put("/items/{item_id}", response_model=schemas.ItemRead, tags=["items"])
def put_item(item_id: int, item_in: schemas.ItemCreate, db: Session = Depends(get_db)):
    """
    PUT: full update. Caller must send all fields.
    """
    item = crud.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item = crud.update_item_full(db, item, item_in)
    return item


@app.patch("/items/{item_id}", response_model=schemas.ItemRead, tags=["items"])
def patch_item(item_id: int, item_in: schemas.ItemUpdate, db: Session = Depends(get_db)):
    """
    PATCH: partial update – only provided fields are updated.
    """
    item = crud.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item = crud.update_item_partial(db, item, item_in)
    return item


@app.delete(
    "/items/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["items"],
)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """
    DELETE: remove an item.
    """
    item = crud.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    crud.delete_item(db, item)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.options("/items/{item_id}", tags=["items"])
def options_item():
    """
    OPTIONS for single item endpoint.
    """
    response = Response(status_code=status.HTTP_204_NO_CONTENT)
    response.headers["Allow"] = "GET,PUT,PATCH,DELETE,OPTIONS"
    return response


from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas


def get_item(db: Session, item_id: int) -> Optional[models.Item]:
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def get_items(db: Session) -> List[models.Item]:
    return db.query(models.Item).order_by(models.Item.id).all()


def create_item(db: Session, item_in: schemas.ItemCreate) -> models.Item:
    item = models.Item(name=item_in.name, description=item_in.description)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_item_full(db: Session, item: models.Item, item_in: schemas.ItemCreate) -> models.Item:
    item.name = item_in.name
    item.description = item_in.description
    db.commit()
    db.refresh(item)
    return item


def update_item_partial(db: Session, item: models.Item, item_in: schemas.ItemUpdate) -> models.Item:
    if item_in.name is not None:
        item.name = item_in.name
    if item_in.description is not None:
        item.description = item_in.description
    db.commit()
    db.refresh(item)
    return item


def delete_item(db: Session, item: models.Item) -> None:
    db.delete(item)
    db.commit()

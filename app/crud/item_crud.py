from sqlalchemy.orm import Session

from app.const import TodoItemStatusCode

from ..models.item_model import ItemModel
from ..models.list_model import ListModel
from ..schemas.item_schema import NewTodoItem, UpdateTodoItem


def get_todo_items(db: Session, todo_list_id: int, page: int = 1, per_page: int = 10):
    offset = (page - 1) * per_page
    return db.query(ItemModel).filter(ItemModel.todo_list_id == todo_list_id).order_by(ItemModel.created_at.desc()).offset(offset).limit(per_page).all()


def get_todo_item(db: Session, todo_list_id: int, todo_item_id: int):
    return (
        db.query(ItemModel)
        .filter(
            ItemModel.id == todo_item_id,
            ItemModel.todo_list_id == todo_list_id,
        )
        .first()
    )


def create_todo_item(db: Session, todo_list_id: int, new_todo_item: NewTodoItem):
    # リストの存在確認
    todo_list = db.query(ListModel).filter(ListModel.id == todo_list_id).first()

    if todo_list is None:
        return None

    item = ItemModel(
        **new_todo_item.dict(),
        todo_list_id=todo_list_id,
        status_code=TodoItemStatusCode.NOT_COMPLETED.value,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_todo_item(db: Session, todo_list_id: int, todo_item_id: int, update_todo_item: UpdateTodoItem):
    todo_item = get_todo_item(db, todo_list_id, todo_item_id)

    if todo_item is None:
        return None

    update_data = update_todo_item.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(todo_item, key, value)

    if update_todo_item.complete:
        todo_item.status_code = TodoItemStatusCode.COMPLETED.value

    db.commit()
    db.refresh(todo_item)

    return todo_item


def delete_todo_item(db: Session, todo_list_id: int, todo_item_id: int):
    todo_item = get_todo_item(db, todo_list_id, todo_item_id)

    if todo_item is None:
        return False

    db.delete(todo_item)
    db.commit()
    return True

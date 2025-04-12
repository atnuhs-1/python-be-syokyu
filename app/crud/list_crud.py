from sqlalchemy.orm import Session

from app.models.list_model import ListModel
from app.schemas.list_schema import NewTodoList, UpdateTodoList


def get_todo_lists(db: Session, page: int = 1, per_page: int = 10):
    offset = (page - 1) * per_page
    return db.query(ListModel).offset(offset).limit(per_page).all()


def get_todo_list(db: Session, todo_list_id: int):
    return db.query(ListModel).filter(ListModel.id == todo_list_id).first()


def create_todo_list(db: Session, new_todo_list: NewTodoList):
    todo_list = ListModel(**new_todo_list.dict())
    db.add(todo_list)
    db.commit()
    db.refresh(todo_list)
    return todo_list


def update_todo_list(db: Session, todo_list_id: int, update_todo_list: UpdateTodoList):
    todo_list = get_todo_list(db, todo_list_id)

    if todo_list is None:
        return None

    update_data = update_todo_list.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(todo_list, key, value)

    db.commit()
    db.refresh(todo_list)

    return todo_list


def delete_todo_list(db: Session, todo_list_id: int):
    todo_list = get_todo_list(db, todo_list_id)

    if todo_list is None:
        return False

    db.delete(todo_list)
    db.commit()
    return True

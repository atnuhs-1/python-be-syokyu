from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import item_crud, list_crud
from app.dependencies import get_db
from app.schemas.item_schema import NewTodoItem, ResponseTodoItem, UpdateTodoItem

router = APIRouter(
    prefix="/lists/{todo_list_id}/items",
    tags=["Todo項目"],
)


@router.get("/", response_model=list[ResponseTodoItem])
def get_todo_items(todo_list_id: int, db: Annotated[Session, Depends(get_db)], page: int = 1, per_page: int = 10):
    # バリデーション
    page = max(page, 1)
    if per_page < 1 or per_page > 100:  # 上限を設定
        per_page = 10
    todo_items = item_crud.get_todo_items(db, todo_list_id, page, per_page)

    if todo_items is None:
        raise HTTPException(
            status_code=404,
            detail=f"Todo item in list {todo_list_id} not found",
        )

    return todo_items


@router.get("/{todo_item_id}", response_model=ResponseTodoItem)
def get_todo_item(todo_list_id: int, todo_item_id: int, db: Annotated[Session, Depends(get_db)]):
    todo_item = item_crud.get_todo_item(db, todo_list_id, todo_item_id)

    if todo_item is None:
        raise HTTPException(
            status_code=404,
            detail=f"Todo item with id {todo_item_id} in list {todo_list_id} not found",
        )

    return todo_item


@router.post("/", response_model=ResponseTodoItem)
def post_todo_item(todo_list_id: int, item_body: NewTodoItem, db: Annotated[Session, Depends(get_db)]):
    todo_list = list_crud.get_todo_list(db, todo_list_id)

    if todo_list is None:
        raise HTTPException(
            status_code=404,
            detail=f"Todo list with id {todo_list_id} not found",
        )

    todo_item = item_crud.create_todo_item(db, todo_list_id, item_body)
    return todo_item


@router.put("/{todo_item_id}", response_model=ResponseTodoItem)
def put_todo_item(todo_list_id: int, todo_item_id: int, item_body: UpdateTodoItem, db: Annotated[Session, Depends(get_db)]):
    todo_item = item_crud.update_todo_item(db, todo_list_id, todo_item_id, item_body)

    if todo_item is None:
        raise HTTPException(
            status_code=404,
            detail=f"Todo item with id {todo_item_id} in list {todo_list_id} not found",
        )

    return todo_item


@router.delete("/{todo_item_id}")
def delete_todo_item(todo_list_id: int, todo_item_id: int, db: Annotated[Session, Depends(get_db)]) -> dict:
    result = item_crud.delete_todo_item(db, todo_list_id, todo_item_id)

    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Todo item with id {todo_item_id} in list {todo_list_id} not found",
        )

    return {}

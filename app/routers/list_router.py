from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import list_crud
from app.dependencies import get_db
from app.schemas.list_schema import NewTodoList, ResponseTodoList, UpdateTodoList

router = APIRouter(
    prefix="/lists",
    tags=["Todoリスト"],
)


@router.get("/", response_model=list[ResponseTodoList])
def get_todo_lists(db: Annotated[Session, Depends(get_db)], page: int = 1, per_page: int = 10):
    # バリデーション
    page = max(page, 1)
    if per_page < 1 or per_page > 100:  # 上限を設定して大量データの取得を防止
        per_page = 10

    todo_lists = list_crud.get_todo_lists(db, page, per_page)

    if todo_lists is None:
        raise HTTPException(
            status_code=404,
            detail="Todo lists not found",
        )

    return todo_lists


@router.get("/{todo_list_id}", response_model=ResponseTodoList)
def get_todo_list(todo_list_id: int, db: Annotated[Session, Depends(get_db)]):
    todo_list = list_crud.get_todo_list(db, todo_list_id)

    if todo_list is None:
        raise HTTPException(
            status_code=404,
            detail=f"Todo list with id {todo_list_id} not found",
        )

    return todo_list


@router.post("/", response_model=ResponseTodoList)
def post_todo_list(list_body: NewTodoList, db: Annotated[Session, Depends(get_db)]):
    return list_crud.create_todo_list(db, list_body)


@router.put("/{todo_list_id}", response_model=ResponseTodoList)
def put_todo_list(todo_list_id: int, list_body: UpdateTodoList, db: Annotated[Session, Depends(get_db)]):
    todo_list = list_crud.update_todo_list(db, todo_list_id, list_body)

    if todo_list is None:
        raise HTTPException(
            status_code=404,
            detail=f"Todo list with id {todo_list_id} not found",
        )

    return todo_list


@router.delete("/{todo_list_id}")
def delete_todo_list(todo_list_id: int, db: Annotated[Session, Depends(get_db)]) -> dict:
    result = list_crud.delete_todo_list(db, todo_list_id)

    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Todo list with id {todo_list_id} not found",
        )

    return {}

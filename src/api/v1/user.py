from http.client import HTTPException

import httpx
from fastapi import APIRouter, BackgroundTasks, Depends
from starlette import status
from fastapi import HTTPException
from auth.auth import reg_user, authenticate_user, create_access_token, user_dependency
from db.db import db_dependency
from schemas.user import UserLoginSchema, UserRegisterSchema

# Создаем APIRouter с префиксом "/user" и тегом 'user' для отображения в документации
user_router = APIRouter(prefix="/user", tags=['user'])


@user_router.get("/{user_id}")
async def get_user(user_id: int):
	# Открываем асинхронное соединение с помощью httpx
	async with httpx.AsyncClient(base_url='https://jsonplaceholder.typicode.com') as client:
    	    # Отправляем GET-запрос для получения данных по конкретному пользователю
    	    response = await client.get(f'/users/{user_id}')
    	    # Возвращаем данные, полученные в формате JSON
    	    return response.json()


@user_router.post("/register")
async def register_user(user_data: UserRegisterSchema, db: db_dependency):
	try:
		return await reg_user(user_data=user_data, db=db)
	except Exception as ex:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Аn error has occurred: {ex}")


@user_router.post("/login")
async def login_for_access_token(db: db_dependency,
                                 login_data: UserLoginSchema):
    user = await authenticate_user(login_data, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": {"email": user.email}}
    )
    return {"access_token": access_token, "token_type": "bearer"}

def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


def has_role(required_role: list[str]):
    def role_checker(current_user: user_dependency):
        if current_user["role"] not in required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return current_user

    return role_checker

@user_router.post("/send-notification/{email}", dependencies=[Depends(has_role(["admin"]))])
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}
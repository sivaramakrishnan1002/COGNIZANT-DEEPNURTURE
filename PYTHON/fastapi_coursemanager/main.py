from typing import List

from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    status
)

from fastapi.middleware.cors import CORSMiddleware

from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from database import (
    Base,
    engine,
    get_db
)

import crud
import auth

from schemas import (
    UserCreate,
    Token,
    CourseCreate,
    CourseUpdate,
    CourseResponse
)


app = FastAPI(
    title="Course Management API",
    description="FastAPI Authentication using JWT",
    version="1.0"
)
app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def home():

    return {
        "message": "FastAPI Authentication Running"
    }


@app.post(
    "/api/v1/auth/register",
    status_code=201
)
async def register(

    user: UserCreate,

    db: AsyncSession = Depends(get_db)

):

    existing = await crud.get_user_by_email(
        db,
        user.email
    )

    if existing:

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    await crud.create_user(
        db,
        user
    )

    return {
        "message": "User Registered Successfully"
    }
@app.post(
    "/api/v1/auth/login",
    response_model=Token
)
async def login(

    form_data: OAuth2PasswordRequestForm = Depends(),

    db: AsyncSession = Depends(get_db)

):

    user = await crud.get_user_by_email(
        db,
        form_data.username
    )

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not auth.verify_password(
        form_data.password,
        user.hashed_password
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = auth.create_access_token(
        {
            "sub": user.email
        }
    )

    return {

        "access_token": access_token,

        "token_type": "bearer"

    }
@app.get("/api/v1/profile")
async def profile(

    current_user=Depends(
        auth.get_current_user
    )

):

    return {

        "username": current_user.username,

        "email": current_user.email

    }
@app.get(
    "/api/v1/courses",
    response_model=List[CourseResponse]
)
async def get_courses(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):

    return await crud.get_courses(db)
@app.get(
    "/api/v1/courses/{course_id}",
    response_model=CourseResponse
)
async def get_course(
    course_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):

    course = await crud.get_course(
        db,
        course_id
    )

    if not course:

        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return course
@app.post(
    "/api/v1/courses",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_course(

    course: CourseCreate,

    db: AsyncSession = Depends(get_db),

    current_user=Depends(auth.get_current_user)

):

    return await crud.create_course(
        db,
        course
    )
@app.put(
    "/api/v1/courses/{course_id}",
    response_model=CourseResponse
)
async def update_course(

    course_id: int,

    course: CourseUpdate,

    db: AsyncSession = Depends(get_db),

    current_user=Depends(auth.get_current_user)

):

    updated = await crud.update_course(
        db,
        course_id,
        course
    )

    if not updated:

        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return updated
@app.delete(
    "/api/v1/courses/{course_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_course(

    course_id: int,

    db: AsyncSession = Depends(get_db),

    current_user=Depends(auth.get_current_user)

):

    deleted = await crud.delete_course(
        db,
        course_id
    )

    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return
from fastapi.responses import JSONResponse
from fastapi import Request


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(
    request: Request,
    exc: HTTPException
):

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail
        }
    )

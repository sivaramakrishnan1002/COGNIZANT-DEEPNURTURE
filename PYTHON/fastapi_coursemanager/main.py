from typing import List

from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    BackgroundTasks,
    status
)

from sqlalchemy.ext.asyncio import AsyncSession

from database import Base, engine, get_db

from schemas import (
    CourseCreate,
    CourseUpdate,
    CourseResponse
)

import crud


app = FastAPI(
    title="Course Management API",
    description="FastAPI CRUD API",
    version="1.0.0"
)


@app.on_event("startup")
async def startup():

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def home():
    return {"message": "API Running"}


@app.get(
    "/api/courses",
    response_model=List[CourseResponse],
    tags=["Courses"]
)
async def get_all_courses(
    db: AsyncSession = Depends(get_db)
):
    return await crud.get_courses(db)


@app.get(
    "/api/courses/{course_id}",
    response_model=CourseResponse,
    tags=["Courses"]
)
async def get_single_course(
    course_id: int,
    db: AsyncSession = Depends(get_db)
):

    course = await crud.get_course(db, course_id)

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return course


@app.post(
    "/api/courses",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Courses"]
)
async def create_course(
    course: CourseCreate,
    db: AsyncSession = Depends(get_db)
):

    return await crud.create_course(db, course)


@app.put(
    "/api/courses/{course_id}",
    response_model=CourseResponse,
    tags=["Courses"]
)
async def update_course(
    course_id: int,
    course: CourseUpdate,
    db: AsyncSession = Depends(get_db)
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
    "/api/courses/{course_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Courses"]
)
async def delete_course(
    course_id: int,
    db: AsyncSession = Depends(get_db)
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


def send_email():
    print("Enrollment confirmation email sent!")


@app.post(
    "/api/enrollments",
    tags=["Enrollments"]
)
async def create_enrollment(
    background_tasks: BackgroundTasks
):

    background_tasks.add_task(send_email)

    return {
        "message": "Enrollment Created"
    }
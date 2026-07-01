from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database import Base, engine, get_db
from schemas import CourseCreate, CourseResponse
from crud import get_courses, get_course, create_course

app = FastAPI(
    title="Course Management API",
    version="1.0"
)


@app.on_event("startup")
async def startup():

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def home():

    return {
        "message": "API Running"
    }


@app.get(
    "/api/courses",
    response_model=List[CourseResponse]
)
async def all_courses(
    db: AsyncSession = Depends(get_db)
):

    return await get_courses(db)


@app.get(
    "/api/courses/{course_id}",
    response_model=CourseResponse
)
async def single_course(
    course_id: int,
    db: AsyncSession = Depends(get_db)
):

    course = await get_course(db, course_id)

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return course


@app.post(
    "/api/courses",
    response_model=CourseResponse
)
async def add_course(
    course: CourseCreate,
    db: AsyncSession = Depends(get_db)
):

    return await create_course(db, course)


@app.get("/api/courses/search/")
async def search_courses(
    skip: int = 0,
    limit: int = 2
):

    return {
        "skip": skip,
        "limit": limit
    }
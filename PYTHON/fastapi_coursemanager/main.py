from typing import List

from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    BackgroundTasks,
    Response,
    Request,
    status
)

from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from database import Base, engine, get_db
from schemas import CourseCreate, CourseUpdate, CourseResponse
import crud


app = FastAPI(
    title="Course Management API",
    description="REST API Best Practices",
    version="1.0.0",
    contact={
        "name": "Course Manager Team",
        "email": "admin@example.com"
    }
)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def home():
    return {"message": "API Running"}


# -----------------------------
# GET ALL COURSES (Pagination)
# -----------------------------
@app.get(
    "/api/v1/courses",
    response_model=List[CourseResponse],
    tags=["Courses"]
)
async def get_courses(
    page: int = 1,
    page_size: int = 2,
    db: AsyncSession = Depends(get_db)
):
    return await crud.paginated_courses(
        db,
        page,
        page_size
    )


# -----------------------------
# SEARCH
# -----------------------------
@app.get(
    "/api/v1/courses/search",
    response_model=List[CourseResponse],
    tags=["Courses"]
)
async def search_courses(
    q: str,
    db: AsyncSession = Depends(get_db)
):
    return await crud.search_courses(db, q)


# -----------------------------
# GET SINGLE COURSE
# -----------------------------
@app.get(
    "/api/v1/courses/{course_id}",
    response_model=CourseResponse,
    tags=["Courses"]
)
async def get_course(
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


# -----------------------------
# CREATE COURSE
# -----------------------------
@app.post(
    "/api/v1/courses",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Courses"]
)
async def create_course(
    course: CourseCreate,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    new_course = await crud.create_course(db, course)

    response.headers["Location"] = (
        f"/api/v1/courses/{new_course.id}"
    )

    return new_course


# -----------------------------
# UPDATE (PUT)
# -----------------------------
@app.put(
    "/api/v1/courses/{course_id}",
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


# -----------------------------
# PATCH
# -----------------------------
@app.patch(
    "/api/v1/courses/{course_id}",
    response_model=CourseResponse,
    tags=["Courses"]
)
async def patch_course(
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


# -----------------------------
# DELETE
# -----------------------------
@app.delete(
    "/api/v1/courses/{course_id}",
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

    return


# -----------------------------
# BACKGROUND TASK
# -----------------------------
def send_email():
    print("Enrollment confirmation email sent!")


@app.post(
    "/api/enrollments",
    status_code=status.HTTP_201_CREATED,
    tags=["Enrollments"]
)
async def create_enrollment(
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(send_email)

    return {
        "message": "Enrollment Created"
    }


# -----------------------------
# STANDARD ERROR FORMAT
# -----------------------------
@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.status_code,
                "message": exc.detail
            }
        }
    )
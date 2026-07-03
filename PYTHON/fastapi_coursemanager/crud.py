from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from models import Course


# -----------------------------
# Get all courses
# -----------------------------
async def get_courses(db: AsyncSession):
    result = await db.execute(select(Course))
    return result.scalars().all()


# -----------------------------
# Get one course
# -----------------------------
async def get_course(db: AsyncSession, course_id: int):
    result = await db.execute(
        select(Course).where(Course.id == course_id)
    )
    return result.scalar_one_or_none()


# -----------------------------
# Create course
# -----------------------------
async def create_course(db: AsyncSession, course):

    new_course = Course(**course.model_dump())

    db.add(new_course)

    await db.commit()

    await db.refresh(new_course)

    return new_course


# -----------------------------
# Update course (PUT/PATCH)
# -----------------------------
async def update_course(
    db: AsyncSession,
    course_id: int,
    course_data
):

    course = await get_course(db, course_id)

    if not course:
        return None

    update_data = course_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(course, key, value)

    await db.commit()

    await db.refresh(course)

    return course


# -----------------------------
# Delete course
# -----------------------------
async def delete_course(
    db: AsyncSession,
    course_id: int
):

    course = await get_course(db, course_id)

    if not course:
        return None

    await db.delete(course)

    await db.commit()

    return True


# -----------------------------
# Search courses
# -----------------------------
async def search_courses(
    db: AsyncSession,
    query: str
):

    result = await db.execute(
        select(Course).where(
            or_(
                Course.name.ilike(f"%{query}%"),
                Course.code.ilike(f"%{query}%")
            )
        )
    )

    return result.scalars().all()


# -----------------------------
# Pagination
# -----------------------------
async def paginated_courses(
    db: AsyncSession,
    page: int,
    page_size: int
):

    offset = (page - 1) * page_size

    result = await db.execute(
        select(Course)
        .offset(offset)
        .limit(page_size)
    )

    return result.scalars().all()


# -----------------------------
# Count total courses
# -----------------------------
async def count_courses(
    db: AsyncSession
):

    result = await db.execute(
        select(Course)
    )

    return len(result.scalars().all())
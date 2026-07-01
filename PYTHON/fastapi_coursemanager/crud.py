from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Course


async def get_courses(db: AsyncSession):

    result = await db.execute(select(Course))

    return result.scalars().all()


async def get_course(db: AsyncSession, course_id: int):

    result = await db.execute(
        select(Course).where(
            Course.id == course_id
        )
    )

    return result.scalar_one_or_none()


async def create_course(db: AsyncSession, course):

    new_course = Course(**course.dict())

    db.add(new_course)

    await db.commit()

    await db.refresh(new_course)

    return new_course
from __future__ import annotations

from apps.course.views import (
    CourseAccessRuleViewSet,
    CourseEnrollmentViewSet,
    CourseGroupAccessViewSet,
    CourseLessonBlockViewSet,
    CourseLessonViewSet,
    CourseMaterialLinkViewSet,
    CoursePlanImportViewSet,
    CoursePlanViewSet,
    CourseProgressViewSet,
    CourseSectionViewSet,
    CourseViewSet,
    LessonProgressViewSet,
    PublicCourseViewSet,
)
from rest_framework.routers import DefaultRouter

admin_router = DefaultRouter()
teacher_router = DefaultRouter()
learner_router = DefaultRouter()
public_router = DefaultRouter()


def register_full_course_router(router: DefaultRouter, *, prefix: str) -> None:
    """
    Регистрирует полный набор endpoints курса.
    """

    router.register(
        "courses",
        CourseViewSet,
        basename=f"{prefix}-courses",
    )
    router.register(
        "plans",
        CoursePlanViewSet,
        basename=f"{prefix}-plans",
    )
    router.register(
        "plan-imports",
        CoursePlanImportViewSet,
        basename=f"{prefix}-plan-imports",
    )
    router.register(
        "group-accesses",
        CourseGroupAccessViewSet,
        basename=f"{prefix}-group-accesses",
    )
    router.register(
        "access-rules",
        CourseAccessRuleViewSet,
        basename=f"{prefix}-access-rules",
    )
    router.register(
        "enrollments",
        CourseEnrollmentViewSet,
        basename=f"{prefix}-enrollments",
    )
    router.register(
        "sections",
        CourseSectionViewSet,
        basename=f"{prefix}-sections",
    )
    router.register(
        "lessons",
        CourseLessonViewSet,
        basename=f"{prefix}-lessons",
    )
    router.register(
        "lesson-blocks",
        CourseLessonBlockViewSet,
        basename=f"{prefix}-lesson-blocks",
    )
    router.register(
        "material-links",
        CourseMaterialLinkViewSet,
        basename=f"{prefix}-material-links",
    )
    router.register(
        "course-progress",
        CourseProgressViewSet,
        basename=f"{prefix}-course-progress",
    )
    router.register(
        "lesson-progress",
        LessonProgressViewSet,
        basename=f"{prefix}-lesson-progress",
    )


register_full_course_router(
    admin_router,
    prefix="course-admin",
)

register_full_course_router(
    teacher_router,
    prefix="course-teacher",
)

learner_router.register(
    "courses",
    CourseViewSet,
    basename="course-learner-courses",
)
learner_router.register(
    "sections",
    CourseSectionViewSet,
    basename="course-learner-sections",
)
learner_router.register(
    "lessons",
    CourseLessonViewSet,
    basename="course-learner-lessons",
)
learner_router.register(
    "lesson-blocks",
    CourseLessonBlockViewSet,
    basename="course-learner-lesson-blocks",
)
learner_router.register(
    "material-links",
    CourseMaterialLinkViewSet,
    basename="course-learner-material-links",
)
learner_router.register(
    "enrollments",
    CourseEnrollmentViewSet,
    basename="course-learner-enrollments",
)
learner_router.register(
    "course-progress",
    CourseProgressViewSet,
    basename="course-learner-course-progress",
)
learner_router.register(
    "lesson-progress",
    LessonProgressViewSet,
    basename="course-learner-lesson-progress",
)

public_router.register(
    "courses",
    PublicCourseViewSet,
    basename="course-public-courses",
)

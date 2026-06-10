from .course import CourseAdmin
from .course_access import (
    CourseAccessRuleAdmin,
    CourseEnrollmentAdmin,
    CourseGroupAccessAdmin,
)
from .course_plan import CoursePlanAdmin, CoursePlanImportAdmin
from .course_progress import CourseProgressAdmin, LessonProgressAdmin
from .course_structure import (
    CourseLessonAdmin,
    CourseLessonBlockAdmin,
    CourseMaterialLinkAdmin,
    CourseSectionAdmin,
)

__all__ = [
    "CourseAccessRuleAdmin",
    "CourseAdmin",
    "CourseEnrollmentAdmin",
    "CourseGroupAccessAdmin",
    "CourseLessonAdmin",
    "CourseLessonBlockAdmin",
    "CourseMaterialLinkAdmin",
    "CoursePlanAdmin",
    "CoursePlanImportAdmin",
    "CourseProgressAdmin",
    "CourseSectionAdmin",
    "LessonProgressAdmin",
]

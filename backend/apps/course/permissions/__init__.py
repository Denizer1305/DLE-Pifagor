from .course import (
    CourseCreateWithPlanPermission,
    CourseDuplicatePermission,
    CoursePermission,
    CourseStatusPermission,
)
from .course_access import (
    CourseAccessRulePermission,
    CourseAccessRuleStatusPermission,
    CourseEnrollmentPermission,
    CourseEnrollmentStatusPermission,
    CourseGroupAccessPermission,
    CourseGroupAccessVisibilityPermission,
)
from .course_plan import (
    CoursePlanImportPermission,
    CoursePlanImportStatusPermission,
    CoursePlanPermission,
    CoursePlanStatusPermission,
)
from .course_progress import (
    CourseProgressPermission,
    CourseProgressRecalculatePermission,
    CourseProgressTrackPermission,
    LessonProgressPermission,
    LessonProgressStatusPermission,
)
from .course_structure import (
    CourseLessonBlockPermission,
    CourseLessonBlockVisibilityPermission,
    CourseLessonPermission,
    CourseLessonStatusPermission,
    CourseMaterialLinkPermission,
    CourseMaterialLinkVisibilityPermission,
    CourseSectionPermission,
    CourseSectionStatusPermission,
)

__all__ = [
    "CourseAccessRulePermission",
    "CourseAccessRuleStatusPermission",
    "CourseCreateWithPlanPermission",
    "CourseDuplicatePermission",
    "CourseEnrollmentPermission",
    "CourseEnrollmentStatusPermission",
    "CourseGroupAccessPermission",
    "CourseGroupAccessVisibilityPermission",
    "CourseLessonBlockPermission",
    "CourseLessonBlockVisibilityPermission",
    "CourseLessonPermission",
    "CourseLessonStatusPermission",
    "CourseMaterialLinkPermission",
    "CourseMaterialLinkVisibilityPermission",
    "CoursePermission",
    "CoursePlanImportPermission",
    "CoursePlanImportStatusPermission",
    "CoursePlanPermission",
    "CoursePlanStatusPermission",
    "CourseProgressPermission",
    "CourseProgressRecalculatePermission",
    "CourseProgressTrackPermission",
    "CourseSectionPermission",
    "CourseSectionStatusPermission",
    "CourseStatusPermission",
    "LessonProgressPermission",
    "LessonProgressStatusPermission",
]

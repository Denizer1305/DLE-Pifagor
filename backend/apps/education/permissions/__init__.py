from .academic_year import AcademicYearPermission
from .curriculum import CurriculumPermission
from .curriculum_item import CurriculumItemPermission
from .education_period import EducationPeriodPermission
from .group_subject import GroupSubjectPermission
from .learner_group_enrollment import LearnerGroupEnrollmentPermission
from .teacher_group_subject import TeacherGroupSubjectPermission

__all__ = [
    "AcademicYearPermission",
    "CurriculumItemPermission",
    "CurriculumPermission",
    "EducationPeriodPermission",
    "GroupSubjectPermission",
    "LearnerGroupEnrollmentPermission",
    "TeacherGroupSubjectPermission",
]

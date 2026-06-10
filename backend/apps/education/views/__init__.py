from .academic_year import AcademicYearViewSet
from .curriculum import CurriculumViewSet
from .curriculum_item import CurriculumItemViewSet
from .education_period import EducationPeriodViewSet
from .group_subject import GroupSubjectViewSet
from .learner_group_enrollment import LearnerGroupEnrollmentViewSet
from .teacher_group_subject import TeacherGroupSubjectViewSet

__all__ = [
    "AcademicYearViewSet",
    "CurriculumItemViewSet",
    "CurriculumViewSet",
    "EducationPeriodViewSet",
    "GroupSubjectViewSet",
    "LearnerGroupEnrollmentViewSet",
    "TeacherGroupSubjectViewSet",
]

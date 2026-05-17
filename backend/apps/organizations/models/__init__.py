"""
Модели приложения organizations.
"""

from apps.organizations.models.department import Department
from apps.organizations.models.organization import Organization
from apps.organizations.models.study_group import StudyGroup

__all__ = [
    "Department",
    "Organization",
    "StudyGroup",
]

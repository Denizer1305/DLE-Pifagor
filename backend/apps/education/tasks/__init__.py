from .academic_year import deactivate_past_academic_years, refresh_current_academic_year
from .curriculum import archive_curricula_for_finished_academic_years
from .curriculum_item import deactivate_items_for_archived_curricula
from .education_period import (
    deactivate_past_education_periods,
    refresh_current_education_period,
)
from .group_subject import (
    deactivate_group_subjects_for_finished_periods,
    deactivate_group_subjects_for_inactive_periods,
    sync_group_subjects_from_curriculum,
)
from .learner_group_enrollment import (
    archive_finished_enrollments_before_date,
    assign_missing_journal_numbers,
    get_active_enrollments_without_journal_numbers_count,
    normalize_finished_enrollments_primary_flags,
)
from .teacher_group_subject import (
    deactivate_assignments_for_inactive_group_subjects,
    deactivate_expired_teacher_assignments,
)

__all__ = [
    "archive_curricula_for_finished_academic_years",
    "archive_finished_enrollments_before_date",
    "assign_missing_journal_numbers",
    "deactivate_assignments_for_inactive_group_subjects",
    "deactivate_expired_teacher_assignments",
    "deactivate_group_subjects_for_finished_periods",
    "deactivate_group_subjects_for_inactive_periods",
    "deactivate_items_for_archived_curricula",
    "deactivate_past_academic_years",
    "deactivate_past_education_periods",
    "get_active_enrollments_without_journal_numbers_count",
    "normalize_finished_enrollments_primary_flags",
    "refresh_current_academic_year",
    "refresh_current_education_period",
    "sync_group_subjects_from_curriculum",
]

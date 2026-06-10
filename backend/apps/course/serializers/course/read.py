from __future__ import annotations

from apps.course.models import Course
from apps.course.serializers.common_serializers import (
    AcademicYearShortSerializer,
    EducationPeriodShortSerializer,
    OrganizationShortSerializer,
    SubjectShortSerializer,
    UserShortSerializer,
)
from rest_framework import serializers


class CourseReadSerializer(serializers.ModelSerializer):
    """
    Read-сериализатор курса.
    """

    owner_teacher = UserShortSerializer(read_only=True)
    organization = OrganizationShortSerializer(read_only=True)
    subject = SubjectShortSerializer(read_only=True)
    academic_year = AcademicYearShortSerializer(read_only=True)
    period = EducationPeriodShortSerializer(read_only=True)

    cover_image_url = serializers.SerializerMethodField()
    sections_count = serializers.SerializerMethodField()
    lessons_count = serializers.SerializerMethodField()
    material_links_count = serializers.SerializerMethodField()
    enrollments_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            "id",
            "code",
            "slug",
            "title",
            "subtitle",
            "description",
            "course_type",
            "origin",
            "status",
            "visibility",
            "level",
            "language",
            "owner_teacher",
            "organization",
            "subject",
            "academic_year",
            "period",
            "cover_image",
            "cover_image_url",
            "is_template",
            "is_active",
            "allow_self_enrollment",
            "enrollment_code",
            "starts_at",
            "ends_at",
            "published_at",
            "archived_at",
            "sections_count",
            "lessons_count",
            "material_links_count",
            "enrollments_count",
            "created_at",
            "updated_at",
        )

    def get_cover_image_url(self, obj: Course) -> str:
        """
        Возвращает URL обложки курса.
        """

        if not obj.cover_image:
            return ""

        request = self.context.get("request")

        if request is None:
            return obj.cover_image.url

        return request.build_absolute_uri(obj.cover_image.url)

    def get_sections_count(self, obj: Course) -> int:
        """
        Возвращает количество разделов курса.
        """

        return obj.sections.count()

    def get_lessons_count(self, obj: Course) -> int:
        """
        Возвращает количество уроков курса.
        """

        return obj.lessons.count()

    def get_material_links_count(self, obj: Course) -> int:
        """
        Возвращает количество материалов курса.
        """

        return obj.material_links.count()

    def get_enrollments_count(self, obj: Course) -> int:
        """
        Возвращает количество записей на курс.
        """

        return obj.enrollments.count()

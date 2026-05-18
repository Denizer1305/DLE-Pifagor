from __future__ import annotations

from apps.organizations.models import TeacherSubject
from apps.users.models import TeacherProfile
from rest_framework import serializers


class PublicTeacherSubjectSerializer(serializers.ModelSerializer):
    """
    Предмет преподавателя.
    """

    id = serializers.IntegerField(source="subject.id")
    name = serializers.CharField(source="subject.name")
    short_name = serializers.CharField(source="subject.short_name")
    code = serializers.CharField(source="subject.code")

    class Meta:
        model = TeacherSubject
        fields = (
            "id",
            "name",
            "short_name",
            "code",
            "is_primary",
        )


class PublicTeacherSerializer(serializers.ModelSerializer):
    """
    Публичная карточка преподавателя.
    """

    id = serializers.IntegerField(source="user.id")
    full_name = serializers.SerializerMethodField()
    position = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    photo_url = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()
    subjects = serializers.SerializerMethodField()
    achievements = serializers.SerializerMethodField()
    experience_years = serializers.IntegerField(read_only=True)

    class Meta:
        model = TeacherProfile
        fields = (
            "id",
            "full_name",
            "position",
            "description",
            "photo_url",
            "department",
            "subjects",
            "achievements",
            "experience_years",
        )

    def get_full_name(self, obj: TeacherProfile) -> str:
        """
        Возвращает ФИО преподавателя.

        Args:
            obj:
                Профиль преподавателя.

        Returns:
            str: ФИО.
        """

        user = obj.user

        full_name_parts = [
            getattr(user, "last_name", ""),
            getattr(user, "first_name", ""),
            getattr(user, "middle_name", ""),
        ]
        full_name = " ".join(part for part in full_name_parts if part).strip()

        if full_name:
            return full_name

        if hasattr(user, "get_full_name"):
            full_name = user.get_full_name().strip()

            if full_name:
                return full_name

        return user.email

    def get_position(self, obj: TeacherProfile) -> str:
        """
        Возвращает публичную должность.

        Args:
            obj:
                Профиль преподавателя.

        Returns:
            str: Должность.
        """

        return obj.public_title or obj.position or "Преподаватель"

    def get_description(self, obj: TeacherProfile) -> str:
        """
        Возвращает краткое описание.

        Args:
            obj:
                Профиль преподавателя.

        Returns:
            str: Описание.
        """

        return obj.short_bio or obj.bio or ""

    def get_photo_url(self, obj: TeacherProfile) -> str:
        """
        Возвращает URL фото преподавателя.

        Args:
            obj:
                Профиль преподавателя.

        Returns:
            str: URL изображения.
        """

        image = None

        if obj.cover_image:
            image = obj.cover_image
        elif hasattr(obj.user, "profile") and obj.user.profile.avatar:
            image = obj.user.profile.avatar

        if not image:
            return ""

        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(image.url)

        return image.url

    def get_department(self, obj: TeacherProfile) -> dict[str, str] | None:
        """
        Возвращает отделение преподавателя.

        Args:
            obj:
                Профиль преподавателя.

        Returns:
            dict[str, str] | None: Отделение.
        """

        if not obj.department:
            return None

        return {
            "id": obj.department.id,
            "name": obj.department.name,
            "short_name": obj.department.short_name,
            "code": obj.department.code,
        }

    def get_subjects(self, obj: TeacherProfile) -> list[dict[str, object]]:
        """
        Возвращает предметы преподавателя.

        Args:
            obj:
                Профиль преподавателя.

        Returns:
            list[dict[str, object]]: Предметы.
        """

        subject_links = [
            link
            for link in obj.user.teacher_subjects.all()
            if link.is_active and link.subject and link.subject.is_active
        ]

        serializer = PublicTeacherSubjectSerializer(
            subject_links,
            many=True,
            context=self.context,
        )

        return serializer.data

    def get_achievements(self, obj: TeacherProfile) -> list[str]:
        """
        Возвращает достижения преподавателя, максимум 5 пунктов.

        Args:
            obj:
                Профиль преподавателя.

        Returns:
            list[str]: Список достижений.
        """

        if not obj.achievements:
            return []

        achievements = [
            line.strip(" -•\t")
            for line in obj.achievements.splitlines()
            if line.strip(" -•\t")
        ]

        return achievements[:5]

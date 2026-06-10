from __future__ import annotations

from apps.course.models import CoursePlan, CoursePlanImport
from apps.course.serializers.common_serializers import UserShortSerializer
from apps.course.serializers.course_plan.read import CoursePlanReadSerializer
from apps.course.services import create_course_plan_import, update_course_plan_import
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class CoursePlanImportReadSerializer(serializers.ModelSerializer):
    """
    Read-сериализатор импорта КТП.
    """

    course_plan = CoursePlanReadSerializer(read_only=True)
    imported_by = UserShortSerializer(read_only=True)
    source_file_url = serializers.SerializerMethodField()

    class Meta:
        model = CoursePlanImport
        fields = (
            "id",
            "course_plan",
            "source_file",
            "source_file_url",
            "original_filename",
            "file_hash",
            "status",
            "parser_version",
            "parsed_payload",
            "errors",
            "imported_by",
            "imported_at",
            "applied_at",
        )

    def get_source_file_url(self, obj: CoursePlanImport) -> str:
        """
        Возвращает URL файла импорта.
        """

        if not obj.source_file:
            return ""

        request = self.context.get("request")

        if request is None:
            return obj.source_file.url

        return request.build_absolute_uri(obj.source_file.url)


class CoursePlanImportWriteSerializer(serializers.ModelSerializer):
    """
    Write-сериализатор импорта КТП.
    """

    course_plan_id = serializers.IntegerField()
    imported_by_id = serializers.IntegerField(
        required=False,
        allow_null=True,
    )

    class Meta:
        model = CoursePlanImport
        fields = (
            "course_plan_id",
            "source_file",
            "original_filename",
            "file_hash",
            "status",
            "parser_version",
            "parsed_payload",
            "errors",
            "imported_by_id",
            "applied_at",
        )
        extra_kwargs = {
            "source_file": {
                "required": False,
                "allow_null": True,
            },
            "original_filename": {
                "required": False,
                "allow_blank": True,
            },
            "file_hash": {
                "required": False,
                "allow_blank": True,
            },
            "parser_version": {
                "required": False,
                "allow_blank": True,
            },
            "parsed_payload": {
                "required": False,
            },
            "errors": {
                "required": False,
            },
            "applied_at": {
                "required": False,
                "allow_null": True,
            },
        }

    def validate_course_plan_id(
        self,
        value: int,
    ) -> int:
        """
        Проверяет существование КТП.
        """

        if not CoursePlan.objects.filter(id=value).exists():
            raise serializers.ValidationError("КТП не найден.")

        return value

    def validate_imported_by_id(
        self,
        value: int | None,
    ) -> int | None:
        """
        Проверяет существование пользователя, выполнившего импорт.
        """

        if value is None:
            return value

        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("Пользователь не найден.")

        return value

    def validate(self, attrs: dict) -> dict:
        """
        Дополняет imported_by текущим пользователем.
        """

        request = self.context.get("request")

        if (
            request is not None
            and request.user.is_authenticated
            and not attrs.get("imported_by_id")
        ):
            attrs["imported_by_id"] = request.user.id

        return attrs

    def create(self, validated_data: dict) -> CoursePlanImport:
        """
        Создаёт импорт КТП через сервисный слой.
        """

        return create_course_plan_import(data=validated_data)

    def update(
        self,
        instance: CoursePlanImport,
        validated_data: dict,
    ) -> CoursePlanImport:
        """
        Обновляет импорт КТП через сервисный слой.
        """

        return update_course_plan_import(
            plan_import=instance,
            data=validated_data,
        )


class CoursePlanImportStatusActionSerializer(serializers.Serializer):
    """
    Action-сериализатор изменения статуса импорта КТП.
    """

    parsed_payload = serializers.DictField(
        required=False,
        default=dict,
    )
    parser_version = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=64,
    )
    errors = serializers.ListField(
        required=False,
        default=list,
    )

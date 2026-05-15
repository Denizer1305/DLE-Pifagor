from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthenticatedAndActive(BasePermission):
    """
    Разрешает доступ только авторизованному и активному пользователю.

    Проверяет:
        - пользователь прошёл аутентификацию;
        - пользователь не является AnonymousUser;
        - пользователь активен.

    Используется как базовая permission для защищённых endpoints.
    """

    message = "Для доступа необходимо войти в активный аккаунт."

    def has_permission(self, request, view) -> bool:
        """
        Проверяет доступ на уровне запроса.

        Args:
            request:
                DRF request.
            view:
                DRF view.

        Returns:
            bool: True, если пользователь авторизован и активен.
        """

        user = request.user

        return bool(
            user and user.is_authenticated and getattr(user, "is_active", False)
        )


class IsReadOnly(BasePermission):
    """
    Разрешает только безопасные методы чтения.

    Безопасные методы:
        - GET;
        - HEAD;
        - OPTIONS.
    """

    message = "Разрешён только просмотр данных."

    def has_permission(self, request, view) -> bool:
        """
        Проверяет, является ли HTTP-метод безопасным.

        Args:
            request:
                DRF request.
            view:
                DRF view.

        Returns:
            bool: True, если метод безопасный.
        """

        return request.method in SAFE_METHODS


class IsOwner(BasePermission):
    """
    Разрешает доступ владельцу объекта.

    Ожидает, что у объекта есть поле `user` или `owner`.
    Подходит для простых объектов, принадлежащих пользователю.

    Для сложных доменных правил лучше писать отдельные permissions
    внутри конкретного приложения.
    """

    message = "Вы можете работать только со своими объектами."

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет, является ли пользователь владельцем объекта.

        Args:
            request:
                DRF request.
            view:
                DRF view.
            obj:
                Проверяемый объект.

        Returns:
            bool: True, если пользователь является владельцем.
        """

        user = request.user

        if not user or not user.is_authenticated:
            return False

        object_user = getattr(obj, "user", None)
        object_owner = getattr(obj, "owner", None)

        return object_user == user or object_owner == user


class IsOwnerOrReadOnly(BasePermission):
    """
    Разрешает чтение всем, а изменение только владельцу.

    Ожидает, что объект имеет поле `user` или `owner`.
    """

    message = "Изменять объект может только владелец."

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет доступ к объекту.

        Args:
            request:
                DRF request.
            view:
                DRF view.
            obj:
                Проверяемый объект.

        Returns:
            bool: True, если доступ разрешён.
        """

        if request.method in SAFE_METHODS:
            return True

        user = request.user

        if not user or not user.is_authenticated:
            return False

        object_user = getattr(obj, "user", None)
        object_owner = getattr(obj, "owner", None)

        return object_user == user or object_owner == user


class IsSuperUser(BasePermission):
    """
    Разрешает доступ только Django superuser.

    Это техническая permission для системных действий.
    Бизнес-роль `superadmin` в users должна проверяться отдельно.
    """

    message = "Доступ разрешён только системному администратору."

    def has_permission(self, request, view) -> bool:
        """
        Проверяет, является ли пользователь superuser.

        Args:
            request:
                DRF request.
            view:
                DRF view.

        Returns:
            bool: True, если пользователь является superuser.
        """

        user = request.user

        return bool(
            user and user.is_authenticated and getattr(user, "is_superuser", False)
        )

from __future__ import annotations

from apps.core.permissions import IsAuthenticatedAndActive


class CanAccessNotifications(IsAuthenticatedAndActive):
    """Restricts the notifications feed to an active authenticated user."""
